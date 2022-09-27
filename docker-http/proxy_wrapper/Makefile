.PHONY: setup test run

setup:
	pip install -r requirements.txt -r requirements-dev.txt
	python setup.py develop

run:
	FATMAN_NAME=proxy FATMAN_VERSION=0.0.1 FATMAN_ENTRYPOINT_HOSTNAME=localhost \
	proxy_wrapper run --port=7200
