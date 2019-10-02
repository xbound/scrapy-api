FROM python:3.6-stretch

ENV FLASK_ENV testing

RUN pip3 install pipenv

WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pipenv install --system --deploy --ignore-pipfile

RUN useradd -m scrapy
USER scrapy

EXPOSE 8000
