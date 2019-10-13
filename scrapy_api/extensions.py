'''
Extensions module. Here are all extensions are instantiated.
'''
from celery import Celery
from flask_mongoengine import MongoEngine

celery = Celery()
mongo = MongoEngine()
