# This file is just a stub, it is overwritten by fatman-template.Dockerfile
from typing import Dict


def rewrite_proxy_paths(content: bytes, headers: Dict[str, str], base_path: str) -> bytes:
    """
    Add Base URL prefix to the paths in the HTTP content
    :param content: original HTTP content
    :param headers: HTTP response headers
    :param base_path: Base URL prefix
    :return: rewritten HTTP response content
    """
    if 'text/html' in headers['content-type']:
        content = rewrite_html_proxy_paths(content, base_path)
        headers['content-length'] = str(len(content))

    return content


def rewrite_html_proxy_paths(content: bytes, base_path: str) -> bytes:
    return content
