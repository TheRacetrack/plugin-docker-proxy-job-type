FROM sphinxdoc/sphinx:5.0.2

WORKDIR /docs
RUN sphinx-quickstart -q --project sphinx --author sphinx

COPY ./docs /docs/

RUN pip install \
    furo==2022.6.21 \
    sphinx-copybutton==0.5.0
RUN make html


FROM nginx:1.23.1

RUN mkdir -p /tmp/nginx && chmod -R 777 /var/cache/nginx /tmp/nginx
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

COPY --from=0 /docs/_build/html /usr/share/nginx/html

EXPOSE 8000
LABEL racetrack-component="fatman"
