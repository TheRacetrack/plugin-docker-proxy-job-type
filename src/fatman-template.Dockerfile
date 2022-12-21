FROM {{ base_image }}

COPY proxy.py /src/proxy_wrapper/proxy_wrapper/proxy.py

{% if manifest.wrapper_properties and manifest.wrapper_properties['user_module_port'] %}
ENV FATMAN_USER_MODULE_PORT "{{ manifest.wrapper_properties['user_module_port'] }}"
{% endif %}
ENV FATMAN_NAME "{{ manifest.name }}"
ENV FATMAN_VERSION "{{ manifest.version }}"
ENV GIT_VERSION "{{ git_version }}"
ENV DEPLOYED_BY_RACETRACK_VERSION "{{ deployed_by_racetrack_version }}"
