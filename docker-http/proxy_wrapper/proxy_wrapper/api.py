import os
import time
from urllib.parse import urlsplit

from fastapi import FastAPI, Request, Response, Body
from starlette.background import BackgroundTask
from starlette.datastructures import MutableHeaders
import httpx

from racetrack_client.log.logs import get_logger
from racetrack_commons.api.asgi.asgi_server import serve_asgi_app
from racetrack_commons.api.asgi.fastapi import create_fastapi
from racetrack_commons.api.asgi.proxy import mount_at_base_path
from racetrack_commons.api.metrics import setup_metrics_endpoint
from racetrack_commons.auth.methods import get_racetrack_authorizations_methods
from racetrack_commons.telemetry.otlp import setup_opentelemetry
from proxy_wrapper.config import Config
from proxy_wrapper.metrics import (
    metric_request_duration,
    metric_request_internal_errors,
    metric_requests_started,
    metric_endpoint_requests_started,
    metric_requests_done,
    metric_last_call_timestamp,
)

logger = get_logger(__name__)


def serve_proxy(config: Config):
    fastapi_app = create_fastapi_app()
    serve_asgi_app(
        fastapi_app, http_addr=config.http_addr, http_port=config.http_port,
    )


def create_fastapi_app() -> FastAPI:
    fatman_name = os.environ.get('FATMAN_NAME', 'fatman_name')
    fatman_version = os.environ.get('FATMAN_VERSION', '0.0.0')
    base_url = f'/pub/fatman/{fatman_name}/{fatman_version}'

    fastapi_app = create_fastapi(
        title=f'Fatman - {fatman_name}',
        description='Fatman Proxy forwarding requests to a User Module',
        base_url=base_url,
        version=fatman_version,
        authorizations=get_racetrack_authorizations_methods(),
        request_access_log=True,
        response_access_log=True,
    )

    _setup_health_endpoints(fastapi_app)
    setup_metrics_endpoint(fastapi_app)

    setup_proxy_endpoints(fastapi_app, base_url)

    if os.environ.get('OPENTELEMETRY_ENDPOINT'):
        setup_opentelemetry(fastapi_app, os.environ.get('OPENTELEMETRY_ENDPOINT'), 'fatman', {
            'fatman_name': fatman_name,
            'fatman_version': fatman_version,
        })

    return mount_at_base_path(fastapi_app, '/pub/fatman/{fatman_name}/{version}')


def _setup_health_endpoints(app: FastAPI):
    @app.get("/live", tags=['root'])
    async def _live():
        deployment_timestamp = int(os.environ.get('FATMAN_DEPLOYMENT_TIMESTAMP', '0'))
        return {
            'live': True,
            'deployment_timestamp': deployment_timestamp,
        }

    @app.get("/ready", tags=['root'])
    async def _ready():
        return {'ready': True}


def setup_proxy_endpoints(app: FastAPI, base_url: str):
    user_module_hostname = os.environ['FATMAN_ENTRYPOINT_HOSTNAME']
    user_module_port = int(os.environ.get('FATMAN_ENTRYPOINT_PORT', 7004))
    logger.info(f'Proxying requests to "{user_module_hostname}:{user_module_port}" at base path "{base_url}"')

    async def _proxy_endpoint(request: Request, path: str, payload = Body(default={})):
        """Forward request to a user module"""
        subpath = f'/{request.path_params["path"]}'
        logger.info(f'Forwarding {request.url} to http://{user_module_hostname}:{user_module_port}{subpath}')

        metric_requests_started.inc()
        metric_endpoint_requests_started.labels(endpoint=subpath).inc()
        start_time = time.time()

        try:
            client = httpx.AsyncClient(base_url=f"http://{user_module_hostname}:{user_module_port}/")

            url = httpx.URL(path=subpath, query=request.url.query.encode("utf-8"))
            request_headers = MutableHeaders(request.headers)
            request_headers['referer'] = request.url.path

            rp_req = client.build_request(request.method, url,
                                          headers=request_headers.raw,
                                          content=await request.body())
            httpx_response = await client.send(rp_req, stream=True)

            return await _build_proxy_response(httpx_response, base_url)

        except BaseException as e:
            metric_request_internal_errors.labels(endpoint=subpath).inc()
            raise e
        finally:
            metric_request_duration.labels(endpoint=subpath).observe(time.time() - start_time)
            metric_requests_done.inc()
            metric_last_call_timestamp.set(time.time())

    app.router.add_api_route("/api/v1/{path:path}", _proxy_endpoint,
                             methods=["GET", "POST", "PUT", "DELETE"], tags=['API'])


async def _build_proxy_response(httpx_response, base_url: str) -> Response:
    content: bytes = await httpx_response.aread()
    headers = httpx_response.headers

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

        if location_header.startswith('/') and not location_header.startswith(base_url):
            headers['location'] = base_url + location_header
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

    return Response(
        content=content,
        status_code=httpx_response.status_code,
        headers=headers,
        background=BackgroundTask(httpx_response.aclose),
    )
