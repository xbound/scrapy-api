from flask import Blueprint
from flask_restplus import Api

from scrapy_api import errors

from scrapy_api.api.endpoints import document
from scrapy_api.api.endpoints import image
from scrapy_api.api.endpoints import ping

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

rest_api = Api(api_blueprint)

# Adding namespaces
rest_api.add_namespace(ping.ping_namespace)
rest_api.add_namespace(document.document_namespace)
rest_api.add_namespace(image.image_namespace)

# Error handlers
@api_blueprint.app_errorhandler(404)
def path_not_found(error):
    return errors.make_error_response(errors.Error404())

@rest_api.errorhandler
def default_error_handler(error):
    return errors.make_error_response(error)