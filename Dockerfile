FROM python:3.6-stretch

ENV C_FORCE_ROOT true

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["./run.sh"]