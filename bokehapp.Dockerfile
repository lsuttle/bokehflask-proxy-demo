FROM continuumio/miniconda

MAINTAINER Garrett McGrath <gmcgrath815 at gmail.com>

<<<<<<< HEAD
#RUN apt-get build-dep python-psycopg2
RUN conda install -y bokeh numpy pandas psycopg2 sqlalchemy scikit-learn
=======

RUN conda install -y bokeh numpy pandas sqlalchemy
>>>>>>> 39405f464a21d68b13d140c765496fe9c817b55f

## Scripts are in here.
VOLUME ['/app']
VOLUME ['/data']

EXPOSE 5006

ENTRYPOINT ["bokeh","serve","/app/bokeh-sliders.py","--host=*","--allow-websocket-origin=*","--prefix=bokehapp","--address=0.0.0.0"]
