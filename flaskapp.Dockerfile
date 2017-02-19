FROM continuumio/miniconda

MAINTAINER Garrett McGrath <gmcgrath815 at gmail.com>

RUN conda install -y flask bokeh

## Scripts are in here.
VOLUME ['/app']
VOLUME ['/data']

EXPOSE 5000

WORKDIR /app

ENTRYPOINT ["python","/app/hello.py"]
