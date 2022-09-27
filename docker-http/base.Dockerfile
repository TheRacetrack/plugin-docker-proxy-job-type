FROM python:3.9-slim-bullseye

WORKDIR /src/fatman

COPY racetrack/racetrack_client/setup.py racetrack/racetrack_client/requirements.txt racetrack/racetrack_client/README.md /src/racetrack_client/
COPY racetrack/racetrack_commons/setup.py racetrack/racetrack_commons/requirements.txt /src/racetrack_commons/
COPY proxy_wrapper/setup.py proxy_wrapper/requirements.txt /src/proxy_wrapper/
RUN pip install -r /src/racetrack_client/requirements.txt \
  -r /src/racetrack_commons/requirements.txt \
  -r /src/proxy_wrapper/requirements.txt

COPY racetrack/racetrack_client/racetrack_client/. /src/racetrack_client/racetrack_client/
COPY racetrack/racetrack_commons/racetrack_commons/. /src/racetrack_commons/racetrack_commons/
COPY proxy_wrapper/proxy_wrapper/. /src/proxy_wrapper/proxy_wrapper/
RUN cd /src/racetrack_client && python setup.py develop &&\
  cd /src/racetrack_commons && python setup.py develop &&\
  cd /src/proxy_wrapper && python setup.py develop

ENV PYTHONPATH "/src/fatman/"
CMD python -u -m proxy_wrapper run
LABEL racetrack-component="fatman"
