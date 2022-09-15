TAG ?= 1.1.0

-include .env

setup:
	cd docker-proxy-job &&\
	pip install -r proxy_wrapper/requirements.txt
	cd docker-proxy-job/proxy_wrapper && python setup.py develop

run:
	cd docker-proxy-job &&\
	FATMAN_NAME=drupal FATMAN_VERSION=0.0.1 \
	FATMAN_ENTRYPOINT_HOSTNAME=127.0.0.1 \
	FATMAN_ENTRYPOINT_PORT=80 \
	PROXY_MODULE=../sample-drupal/proxy.py \
	python -u -m proxy_wrapper run

build:
	cd docker-proxy-job &&\
	DOCKER_BUILDKIT=1 docker build \
		-t ghcr.io/theracetrack/racetrack/fatman-base/docker-proxy:latest \
		-f base.Dockerfile .

push: build
	docker login ghcr.io
	docker tag ghcr.io/theracetrack/racetrack/fatman-base/docker-proxy:latest ghcr.io/theracetrack/racetrack/fatman-base/docker-proxy:$(TAG)
	docker push ghcr.io/theracetrack/racetrack/fatman-base/docker-proxy:$(TAG)

push-local: build
	docker tag ghcr.io/theracetrack/racetrack/fatman-base/docker-proxy:latest localhost:5000/racetrack/fatman-base/docker-proxy:$(TAG)
	docker push localhost:5000/racetrack/fatman-base/docker-proxy:$(TAG)

push-private-registry: build
	dcoker login ${REGISTRY}
	docker tag ghcr.io/theracetrack/racetrack/fatman-base/docker-proxy:latest ${REGISTRY}/fatman-base/docker-proxy:$(TAG)
	docker push ${REGISTRY}/fatman-base/docker-proxy:$(TAG)

push-all: push push-local push-private-registry

env-template:
	cp -n .env.dist .env
	@echo "Now fill in the .env file with your settings"

bundle:
	cd docker-proxy-job &&\
	racetrack-plugin-bundler bundle
