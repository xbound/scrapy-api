'''
Extensions module. Here are all extensions are instantiated.
'''
from celery import Celery
from flask_mongoengine import MongoEngine
from flask_restplus import Api

celery = Celery()
mongo = MongoEngine()
