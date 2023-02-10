FROM drupal:9.4.4

RUN chmod -R 777 /var/www/html && chmod -R 777 /var/www/html/sites

RUN mkdir /var/www/html/sites/default/files &&\
    chmod a+w /var/www/html/sites/default/files &&\
    chmod a+w /var/www/html/sites/default &&\
    cp /var/www/html/sites/default/default.settings.php /var/www/html/sites/default/settings.php &&\
    chmod a+w /var/www/html/sites/default/settings.php

COPY apache-ports.conf /etc/apache2/ports.conf

EXPOSE 8000
LABEL racetrack-component="job"
