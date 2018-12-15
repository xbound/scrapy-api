from .app import create_app
from celery import Celery

app = create_app()