FROM continuumio/miniconda

MAINTAINER Garrett McGrath <gmcgrath815 at gmail.com>

#RUN apt-get build-dep python-psycopg2
RUN conda install -y bokeh numpy pandas psycopg2 sqlalchemy scikit-learn

## Scripts are in here.
VOLUME ['/app']
VOLUME ['/data']

EXPOSE 5006

ENTRYPOINT ["bokeh","serve","/app/bokeh-sliders.py","--host=*","--allow-websocket-origin=*","--prefix=bokehapp","--address=0.0.0.0"]
