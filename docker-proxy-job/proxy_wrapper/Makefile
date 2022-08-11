.PHONY: setup test run

SHELL=/bin/bash

setup:
	pip install -r requirements.txt
	python setup.py develop

run:
	FATMAN_NAME=proxy FATMAN_VERSION=0.0.1 \
	proxy_wrapper run

run-proxy:
	FATMAN_NAME=drupal FATMAN_VERSION=0.0.1 FATMAN_ENTRYPOINT_HOSTNAME=10.10.3.10 FATMAN_ENTRYPOINT_PORT=80 HTTP_PORT=7200 \
	proxy_wrapper run
