from typing import Dict
import re


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

    elif 'text/css' in headers['content-type']:
        content = rewrite_css_proxy_paths(content, base_path)
        headers['content-length'] = str(len(content))

    return content


def rewrite_html_proxy_paths(content: bytes, base_path: str) -> bytes:
    content_str = content.decode()

    content_str = content_str.replace("URL=/", f"URL={base_path}/")
    content_str = content_str.replace('"baseUrl":"\\/', f'"baseUrl":"\\{base_path}/')
    content_str = content_str.replace('"basePath":"\\/', f'"basePath":"\\{base_path}/')
    content_str = content_str.replace('href=\\u0022\\/', f'href=\\u0022\\{base_path}/')
    content_str = content_str.replace('"uri":"\\/', f'"uri":"\\{base_path}/')
    content_str = content_str.replace('href="/', f'href="{base_path}/')
    content_str = content_str.replace('http://localhost/', f'{base_path}/')
    content_str = content_str.replace('http://localhost:7000/', f'{base_path}/')
    content_str = content_str.replace('http://localhost:7200/', f'{base_path}/')

    for _ in range(2):

        for html_attr in ['href', 'src', 'action']:

            def _replace_url_attr(match):
                subpath = '/' + match.group(1)
                if subpath.startswith(base_path):
                    return f'{html_attr}="{subpath}"'
                else:
                    return f'{html_attr}="{base_path}{subpath}"'

            content_str = re.sub(f"{html_attr}=['\"]http://(?:localhost|127\.0\.0\.1|0.0.0.0)(?:\:\d+)?/(.*)['\"]", _replace_url_attr, content_str)
            content_str = re.sub(f"{html_attr}=['\"]http://(?:localhost|127\.0\.0\.1|0.0.0.0)(?:\:\d+)?['\"]", f'{html_attr}="{base_path}"', content_str)
            content_str = re.sub(f"{html_attr}=['\"]/(.*)['\"]", _replace_url_attr, content_str)

    return content_str.encode()


def rewrite_css_proxy_paths(content: bytes, base_path: str) -> bytes:
    content_str = content.decode()
    content_str = content_str.replace("url(/", f"url({base_path}/")
    return content_str.encode()
