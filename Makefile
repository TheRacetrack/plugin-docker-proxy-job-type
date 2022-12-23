.PHONY: setup test

setup:
	python3 -m venv venv &&\
	. venv/bin/activate &&\
	pip install --upgrade pip setuptools &&\
	(cd src/proxy_wrapper && make setup)
	@echo Activate your venv:
	@echo . venv/bin/activate

test-build:
	cd src &&\
	DOCKER_BUILDKIT=1 docker build \
		-t racetrack/fatman-base/docker-proxy:latest \
		-f base.Dockerfile .

bundle:
	cd src &&\
	racetrack plugin bundle --out=..

run:
	cd src/proxy_wrapper &&\
	FATMAN_NAME=drupal FATMAN_VERSION=0.0.1 \
	FATMAN_USER_MODULE_HOSTNAME=127.0.0.1 \
	FATMAN_USER_MODULE_PORT=80 \
	PROXY_MODULE=../../sample/drupal/proxy_settings.py \
	python -m proxy_wrapper.main run
