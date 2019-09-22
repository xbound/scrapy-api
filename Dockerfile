FROM python:3.6-stretch

ENV FLASK_ENV staging

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements.txt

EXPOSE 8000
