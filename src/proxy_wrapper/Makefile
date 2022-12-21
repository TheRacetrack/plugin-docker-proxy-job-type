.PHONY: setup test run

setup:
	pip install -r requirements.txt

run:
	FATMAN_NAME=proxy FATMAN_VERSION=0.0.1 FATMAN_USER_MODULE_HOSTNAME=localhost \
	python -m proxy_wrapper.main run --port=7200
