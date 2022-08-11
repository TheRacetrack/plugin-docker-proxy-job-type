from typing import Callable
import importlib
import os
from urllib.parse import urlsplit

import uvicorn
from uvicorn.config import LOGGING_CONFIG
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from starlette.background import BackgroundTask
from starlette.datastructures import MutableHeaders
import httpx

from proxy_wrapper.exception import log_exception
from proxy_wrapper.logs import get_logger

logger = get_logger(__name__)

FATMAN_NAME = os.environ.get('FATMAN_NAME', 'fatman_name')
FATMAN_VERSION = os.environ.get('FATMAN_VERSION', 'fatman_version')
BASE_URL = f'/pub/fatman/{FATMAN_NAME}/{FATMAN_VERSION}'

REWRITE_PROXY_PATHS_FUNCTION = 'rewrite_proxy_paths'


def serve_proxy():
    fastapi_app = create_fastapi_app()

    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "\033[2m[%(asctime)s]\033[0m %(levelname)s %(message)s"
    LOGGING_CONFIG["formatters"]["default"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    LOGGING_CONFIG["formatters"]["default"]["()"] = "proxy_wrapper.logs.ColoredDefaultFormatter"

    LOGGING_CONFIG["formatters"]["access"]["fmt"] = "\033[2m[%(asctime)s]\033[0m %(levelname)s %(request_line)s %(status_code)s"
    LOGGING_CONFIG["formatters"]["access"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
    LOGGING_CONFIG["formatters"]["access"]["()"] = "proxy_wrapper.logs.ColoredAccessFormatter"

    LOGGING_CONFIG["handlers"]["default"]["stream"] = 'ext://sys.stdout'
    LOGGING_CONFIG["handlers"]["access"]["stream"] = 'ext://sys.stdout'

    LOGGING_CONFIG["loggers"]["uvicorn"]["propagate"] = False

    http_port = int(os.environ.get('HTTP_PORT', 7000))
    uvicorn.run(app=fastapi_app, host="0.0.0.0", port=http_port, log_level="debug")


def create_fastapi_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    subapi = FastAPI()

    setup_endpoints(subapi)
    app.mount(BASE_URL, subapi)

    @app.get("/")
    @app.get(BASE_URL)
    async def home():
        return RedirectResponse(f"{BASE_URL}/")

    @app.get("/fatman/status")
    async def _status():
        return {'status': 'ok'}

    @app.get("/live")
    async def _live():
        deployment_timestamp = int(os.environ.get('FATMAN_DEPLOYMENT_TIMESTAMP', '0'))
        return {
            'live': True,
            'deployment_timestamp': deployment_timestamp,
        }

    @app.get("/ready")
    async def _ready():
        return {'ready': True}

    @app.exception_handler(Exception)
    async def _error_handler(request: Request, exc: Exception):
        log_exception(exc)
        return JSONResponse(
            status_code=500,
            content={'error': str(exc)},
        )

    @subapi.exception_handler(Exception)
    async def _subapi_error_handler(request: Request, exc: Exception):
        log_exception(exc)
        return JSONResponse(
            status_code=500,
            content={'error': str(exc)},
        )

    async def catch_exceptions_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            log_exception(exc)
            return JSONResponse(
                status_code=500,
                content={'error': str(exc)},
            )

    app.middleware('http')(catch_exceptions_middleware)
    subapi.middleware('http')(catch_exceptions_middleware)

    return app


def setup_endpoints(app: FastAPI):
    user_module_hostname = os.environ['FATMAN_ENTRYPOINT_HOSTNAME']
    user_module_port = int(os.environ.get('FATMAN_ENTRYPOINT_PORT', 80))
    logger.info(f'Proxying requests to "{user_module_hostname}:{user_module_port}" at base path "{BASE_URL}"')

    rewrite_proxy_paths = load_proxy_rewriter()

    async def _proxy_endpoint(request: Request):

        subpath = f'/{request.path_params["path"]}'
        logger.info(f'Forwarding {request.url.path}{request.url.query} to: {subpath}')

        client = httpx.AsyncClient(base_url=f"http://{user_module_hostname}:{user_module_port}/")

        url = httpx.URL(path=subpath, query=request.url.query.encode("utf-8"))

        request_headers = MutableHeaders(request.headers)
        request_headers['referer'] = request.url.path

        rp_req = client.build_request(request.method, url,
                                      headers=request_headers.raw,
                                      content=await request.body())
        response = await client.send(rp_req, stream=True)
        content: bytes = await response.aread()
        headers = response.headers

        location_header = headers.get('location')
        if location_header:
            logger.debug(f'Transforming Location header into relative one: {location_header}')

            if location_header.startswith('://'):
                location_header = location_header[3:]

            split = urlsplit(location_header)
            if split.scheme or split.netloc:
                location_header = split._replace(scheme='', netloc='').geturl()
            else:
                location_header = '/' + location_header.split('/', 1)[-1]

            if location_header.startswith('/') and not location_header.startswith(BASE_URL):
                headers['location'] = BASE_URL + location_header
            else:
                headers['location'] = location_header

        if 'content-encoding' in headers:
            del headers['content-encoding']
            headers['content-length'] = str(len(content))

        if 'content-length' not in headers and 'transfer-encoding' not in headers and len(content) > 0:
            headers['content-length'] = str(len(content))
        
        if 'content-length' in headers and 'transfer-encoding' in headers:
            del headers['transfer-encoding']
            headers['content-length'] = str(len(content))

        content = rewrite_proxy_paths(content, headers, BASE_URL)

        return Response(
            content=content,
            status_code=response.status_code,
            headers=headers,
            background=BackgroundTask(response.aclose),
        )

    app.add_route("/{path:path}", _proxy_endpoint, ["GET", "POST"])


def load_proxy_rewriter() -> Callable:
    proxy_module_name = os.environ.get('PROXY_MODULE')
    if not proxy_module_name:
        from proxy_wrapper.proxy import rewrite_proxy_paths
        return rewrite_proxy_paths

    spec = importlib.util.spec_from_file_location("ext.proxy_module", proxy_module_name)
    ext_module = importlib.util.module_from_spec(spec)
    loader = spec.loader
    assert loader is not None, 'no module loader'
    loader.exec_module(ext_module)

    assert hasattr(ext_module, REWRITE_PROXY_PATHS_FUNCTION), f'function {REWRITE_PROXY_PATHS_FUNCTION} was not found'
    proxy_function = getattr(ext_module, REWRITE_PROXY_PATHS_FUNCTION)
    logger.info(f'Proxy rewriter function loaded from {proxy_module_name} module')
    return proxy_function
