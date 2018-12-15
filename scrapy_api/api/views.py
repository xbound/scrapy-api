from flask import Blueprint
from flask_restplus import Api

from scrapy_api.api.resources import ping_namespace, document_namespace, image_namespace

blueprint = Blueprint('api', __name__, url_prefix='/api/')

api = Api(
    blueprint,
    title='Scrapy API',
    version='1.0-dev',
    description='REST API for parsing data information from websites.')

api.add_namespace(ping_namespace, path='ping')
api.add_namespace(document_namespace, path='document')
api.add_namespace(image_namespace, path='image')