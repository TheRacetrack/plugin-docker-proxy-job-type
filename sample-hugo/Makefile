run-local:
	cd hugo_site &&\
	hugo server -D --bind 0.0.0.0 --port 8000

test-build:
	DOCKER_BUILDKIT=1 docker build \
		-t sample-hugo:latest \
		-f Dockerfile .
