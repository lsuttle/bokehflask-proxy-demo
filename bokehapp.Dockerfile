FROM continuumio/miniconda

MAINTAINER Garrett McGrath <gmcgrath815 at gmail.com>


RUN conda install -y bokeh numpy pandas

## Scripts are in here.
VOLUME ['/app']
VOLUME ['/data']

EXPOSE 5006

ENTRYPOINT ["bokeh","serve","/app/bokeh-sliders.py","--host=*","--allow-websocket-origin=*","--prefix=bokehapp","--address=0.0.0.0"]
