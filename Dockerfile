FROM python:2

RUN apt-get update
RUN apt-get install git --yes

RUN mkdir /build
WORKDIR /build
