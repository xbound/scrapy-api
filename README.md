# Scrapy API

REST API for fetching text and images from webpage using asynchronous Celery tasks and storing results in MongoDB.

## Setting up 

For development project uses [pipenv](https://github.com/pypa/pipenv) tool. 
To setup local development environment run:

```shell
$ pipenv install --dev
```

## Running project 

Command to run project:
```shell
$ docker-compose up --build
```
TO run tests:
```shell
$ docker-compose exec app py.test
```

You can also only run local development server (only server without celery):
```shell
$ pipenv run dev
```

After laucnch API will be available at http://localhost:8000/api/.
