'''
Extensions module.
'''
from celery import Celery
from flask_mongoengine import MongoEngine

celery = Celery()
mongo = MongoEngine()
