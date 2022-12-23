import os

from fastapi import FastAPI

from racetrack_client.log.logs import get_logger
from racetrack_commons.api.asgi.asgi_server import serve_asgi_app
from proxy_wrapper.forward import create_forwarder_app
from proxy_wrapper.rewrite import create_rewrite_proxy_app

logger = get_logger(__name__)


def serve_proxy(http_port: int):
    fastapi_app = create_app()
    serve_asgi_app(
        fastapi_app, http_addr='0.0.0.0', http_port=http_port,
    )


def create_app() -> FastAPI:
    if os.environ.get('PROXY_MODE') == 'rewrite':
        # Mode 'rewrite', Trim prefixes from paths, proxy all requests (including root)
        return create_rewrite_proxy_app()
    # Mode 'forward': Keep original paths, forward requests only to /api/v1/*
    return create_forwarder_app()
