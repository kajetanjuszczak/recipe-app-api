FROM python:3.7-alpine
MAINTAINER Kajetan

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requrements.txt
RUN pip install -r /requrements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
