FROM python:3.6-stretch

ENV C_FORCE_ROOT true
ENV FLASK_ENV staging

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements.txt
RUN pip install pytest
RUN pip install pdbpp

EXPOSE 8000
