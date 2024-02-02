import argparse
import sys

from racetrack_client.log.logs import configure_logs, get_logger

from proxy_wrapper.api import serve_proxy

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser('run', help='run wrapped entrypoint in a server')
    subparser.add_argument('--port', type=int, default=None, nargs='?', help='HTTP port to run the server on')
    subparser.set_defaults(func=run_entrypoint)

    if len(sys.argv) > 1:
        args: argparse.Namespace = parser.parse_args()
        args.func(args)
    else:
        parser.print_help(sys.stderr)


def run_entrypoint(args: argparse.Namespace):
    """Load entrypoint class and run it embedded in a HTTP server"""
    configure_logs(log_level='debug')

    http_port = args.port or 7000
    serve_proxy(http_port)


if __name__ == '__main__':
    main()
