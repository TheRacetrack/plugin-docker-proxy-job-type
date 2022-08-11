import argparse
import sys

from proxy_wrapper.logs import configure_logs
from proxy_wrapper.api import serve_proxy


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser('run', help='run wrapped entrypoint in a server')
    subparser.set_defaults(func=_run_proxy)

    if len(sys.argv) > 1:
        args: argparse.Namespace = parser.parse_args()
        args.func(args)
    else:
        parser.print_help(sys.stderr)


def _run_proxy(args: argparse.Namespace):
    configure_logs(log_level='debug')
    serve_proxy()
