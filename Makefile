TAG ?= 2.3.0

-include .env

setup:
	python3 -m venv venv &&\
	. venv/bin/activate &&\
	pip install --upgrade pip setuptools &&\
	cd docker-http &&\
	( cd proxy_wrapper && make setup ) &&\
	( cd racetrack/racetrack_client && make setup ) &&\
	( cd racetrack/racetrack_commons && make setup )
	@echo Activate your venv:
	@echo . venv/bin/activate

build:
	cd docker-http &&\
	DOCKER_BUILDKIT=1 docker build \
		-t racetrack/fatman-base/docker-http:latest \
		-f base.Dockerfile .

push-local: build
	docker tag racetrack/fatman-base/docker-http:latest localhost:5000/racetrack/fatman-base/docker-http:$(TAG)
	docker push localhost:5000/racetrack/fatman-base/docker-http:$(TAG)

push-private: build
	docker login ${REGISTRY}
	docker tag racetrack/fatman-base/docker-http:latest ${REGISTRY}/fatman-base/docker-http:$(TAG)
	docker push ${REGISTRY}/fatman-base/docker-http:$(TAG)

push-public: build
	docker login ghcr.io
	docker tag racetrack/fatman-base/docker-http:latest ghcr.io/theracetrack/racetrack/fatman-base/docker-http:$(TAG)
	docker push ghcr.io/theracetrack/racetrack/fatman-base/docker-http:$(TAG)

# Use it if you want to change the default settings
env-template:
	cp -n .env.dist .env
	@echo "Now fill in the .env file with your settings"

bundle:
	cd docker-http &&\
	racetrack-plugin-bundler bundle --plugin-version=${TAG} --out=..

release: push-local push-private push-public bundle
