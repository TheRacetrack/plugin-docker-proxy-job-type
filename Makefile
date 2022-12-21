setup:
	cd src &&\
	pip install -r proxy_wrapper/requirements.txt

run:
	cd src/proxy_wrapper &&\
	FATMAN_NAME=drupal FATMAN_VERSION=0.0.1 \
	FATMAN_USER_MODULE_HOSTNAME=127.0.0.1 \
	FATMAN_USER_MODULE_PORT=80 \
	PROXY_MODULE=../../sample/drupal/proxy.py \
	python -m proxy_wrapper.main run

test-build:
	cd src &&\
	DOCKER_BUILDKIT=1 docker build \
		-t ghcr.io/theracetrack/racetrack/fatman-base/docker-proxy:latest \
		-f base.Dockerfile .

bundle:
	cd src &&\
	racetrack plugin bundle --out=..
