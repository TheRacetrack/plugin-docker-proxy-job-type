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

bundle:
	cd docker-proxy-job &&\
	racetrack plugin bundle --out=..
