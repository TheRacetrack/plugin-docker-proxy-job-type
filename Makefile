.PHONY: setup test

setup:
	python3 -m venv venv &&\
	. venv/bin/activate &&\
	pip install --upgrade pip setuptools &&\
	(cd src/proxy_wrapper && make setup)
	@echo Activate your venv:
	@echo . venv/bin/activate

bundle:
	cd src &&\
	racetrack plugin bundle --out=.. &&\
	racetrack plugin bundle --out=.. --out-filename=latest.zip

install:
	racetrack plugin install --replace latest.zip

run:
	cd src/proxy_wrapper &&\
	JOB_NAME=drupal JOB_VERSION=0.0.1 \
	JOB_USER_MODULE_HOSTNAME=127.0.0.1 \
	JOB_USER_MODULE_PORT=80 \
	PROXY_MODULE=../../sample/drupal/proxy_settings.py \
	python -m proxy_wrapper.main run
