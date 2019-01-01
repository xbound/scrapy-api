from flask import Blueprint
from flask import current_app, jsonify
from flask_restplus import Api
from mongoengine.errors import DoesNotExist

from scrapy_api.api.endpoints import *
from scrapy_api.commons.constants import MESSAGE, ENVIRONMENT
from scrapy_api.models import DocumentTask, ImageTask

__all__ = [
    'blueprint',
    'api',
]

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(
    blueprint,
    title='Scrapy API',
    version='1.0-dev',
    description='REST API for parsing data information from websites.')

# Error handlers
@blueprint.app_errorhandler(404)
def path_not_found(error):
    return jsonify({'message': MESSAGE.ERROR_404.value}), 404


@api.errorhandler
def default_error_handler(error):
    message = MESSAGE.ERROR_500.value
    if current_app.config.ENV == ENVIRONMENT.PRODUCTION.value:
        return {'message': message}, 500


@api.errorhandler(DocumentTask.DoesNotExist)
def doccument_task_does_not_exist(error):
    return {'message': MESSAGE.DOCUMENT_TASK_404.value}, 404


@api.errorhandler(ImageTask.DoesNotExist)
def image_task_does_not_exist(error):
    return {'message': MESSAGE.IMAGE_TASK_404.value}, 404

# Adding namespaces
api.add_namespace(ping_namespace, '/ping')
api.add_namespace(document_namespace, '/document')
api.add_namespace(image_namespace, '/image')