FROM httpd:2.4

MAINTAINER Garrett McGrath <gmcgrath815 at gmail.com>


COPY ./httpd/vhost.conf /usr/local/apache2/conf/httpd.conf

VOLUME ['/static']

EXPOSE 80
