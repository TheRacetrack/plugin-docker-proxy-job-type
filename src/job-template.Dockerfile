FROM python:3.9-slim-bullseye

WORKDIR /src/proxy_wrapper

COPY --from=jobtype proxy_wrapper/racetrack_client/requirements.txt /src/proxy_wrapper/racetrack_client/
COPY --from=jobtype proxy_wrapper/racetrack_commons/requirements.txt /src/proxy_wrapper/racetrack_commons/
COPY --from=jobtype proxy_wrapper/requirements.txt /src/proxy_wrapper/
RUN pip install -r /src/proxy_wrapper/racetrack_client/requirements.txt \
  -r /src/proxy_wrapper/racetrack_commons/requirements.txt \
  -r /src/proxy_wrapper/requirements.txt

COPY --from=jobtype proxy_wrapper/racetrack_client/. /src/proxy_wrapper/racetrack_client/
COPY --from=jobtype proxy_wrapper/racetrack_commons/. /src/proxy_wrapper/racetrack_commons/
COPY --from=jobtype proxy_wrapper/proxy_wrapper/. /src/proxy_wrapper/proxy_wrapper/

ENV PYTHONPATH "/src/proxy_wrapper"
CMD python -u -m proxy_wrapper.main run
LABEL racetrack-component="job"


{% if manifest.jobtype_extra and manifest.jobtype_extra['proxy_mode'] == 'rewrite' %}
COPY proxy_settings.py /src/proxy_wrapper/proxy_wrapper/proxy_settings.py
ENV PROXY_MODE "rewrite"
{% endif %}

{% if manifest.jobtype_extra and manifest.jobtype_extra['user_module_port'] %}
ENV JOB_USER_MODULE_PORT "{{ manifest.jobtype_extra['user_module_port'] }}"
{% endif %}

ENV JOB_NAME "{{ manifest.name }}"
ENV JOB_VERSION "{{ manifest.version }}"
ENV GIT_VERSION "{{ git_version }}"
ENV DEPLOYED_BY_RACETRACK_VERSION "{{ deployed_by_racetrack_version }}"
