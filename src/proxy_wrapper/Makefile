.PHONY: setup test run

setup:
	pip install \
		-r requirements.txt \
		-r racetrack_client/requirements.txt \
		-r racetrack_commons/requirements.txt

run:
	JOB_NAME=proxy JOB_VERSION=0.0.1 JOB_USER_MODULE_HOSTNAME=localhost \
	python -m proxy_wrapper.main run --port=7200
