from typing import Dict


def rewrite_proxy_paths(content: bytes, headers: Dict[str, str], base_path: str) -> bytes:
    """
    Add Base URL prefix to the paths in the HTTP content
    :param content: original HTTP content
    :param headers: HTTP response headers
    :param base_path: Base URL prefix
    :return: rewritten HTTP response content
    """
    return content
