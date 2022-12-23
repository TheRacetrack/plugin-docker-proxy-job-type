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
