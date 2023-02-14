FROM python:3.9-slim-bullseye

WORKDIR /src/proxy_wrapper

COPY proxy_wrapper/racetrack_client/requirements.txt /src/proxy_wrapper/racetrack_client/
COPY proxy_wrapper/racetrack_commons/requirements.txt /src/proxy_wrapper/racetrack_commons/
COPY proxy_wrapper/requirements.txt /src/proxy_wrapper/
RUN pip install -r /src/proxy_wrapper/racetrack_client/requirements.txt \
  -r /src/proxy_wrapper/racetrack_commons/requirements.txt \
  -r /src/proxy_wrapper/requirements.txt

COPY proxy_wrapper/racetrack_client/. /src/proxy_wrapper/racetrack_client/
COPY proxy_wrapper/racetrack_commons/. /src/proxy_wrapper/racetrack_commons/
COPY proxy_wrapper/proxy_wrapper/. /src/proxy_wrapper/proxy_wrapper/

ENV PYTHONPATH "/src/proxy_wrapper"
CMD python -u -m proxy_wrapper.main run
LABEL racetrack-component="job"
