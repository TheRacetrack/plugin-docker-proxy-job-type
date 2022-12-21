.PHONY: setup test run

setup:
	pip install -r requirements.txt

run:
	FATMAN_NAME=proxy FATMAN_VERSION=0.0.1 \
	python -m proxy_wrapper.main run

run-proxy:
	FATMAN_NAME=drupal FATMAN_VERSION=0.0.1 FATMAN_USER_MODULE_HOSTNAME=10.10.3.10 FATMAN_USER_MODULE_PORT=80 HTTP_PORT=7200 \
	python -m proxy_wrapper.main run
