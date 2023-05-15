FROM {{ base_image }}

{% if manifest.wrapper_properties %}
{% if manifest.wrapper_properties and manifest.wrapper_properties['proxy_mode'] == 'rewrite' %}
COPY proxy_settings.py /src/proxy_wrapper/proxy_wrapper/proxy_settings.py
ENV PROXY_MODE "rewrite"
{% endif %}

{% if manifest.wrapper_properties and manifest.wrapper_properties['user_module_port'] %}
ENV JOB_USER_MODULE_PORT "{{ manifest.wrapper_properties['user_module_port'] }}"
{% endif %}
{% endif %}

{% if manifest.jobtype_extra %}
{% if manifest.jobtype_extra and manifest.jobtype_extra['proxy_mode'] == 'rewrite' %}
COPY proxy_settings.py /src/proxy_wrapper/proxy_wrapper/proxy_settings.py
ENV PROXY_MODE "rewrite"
{% endif %}

{% if manifest.jobtype_extra and manifest.jobtype_extra['user_module_port'] %}
ENV JOB_USER_MODULE_PORT "{{ manifest.jobtype_extra['user_module_port'] }}"
{% endif %}
{% endif %}

ENV JOB_NAME "{{ manifest.name }}"
ENV JOB_VERSION "{{ manifest.version }}"
ENV GIT_VERSION "{{ git_version }}"
ENV DEPLOYED_BY_RACETRACK_VERSION "{{ deployed_by_racetrack_version }}"
