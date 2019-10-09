from celery import Celery
from dynaconf import FlaskDynaconf
from flask import Flask, Blueprint
from flask_restplus import Api, Resource
from werkzeug.debug import DebuggedApplication

from scrapy_api import extensions
from scrapy_api import errors

from scrapy_api.api.ping import ping_namespace
from scrapy_api.api.image import image_namespace
from scrapy_api.api.document import document_namespace


def configure_app(app):
    '''
    Configure app settings.
    '''
    FlaskDynaconf(app)


def init_celery(app=None):
    '''
    Initialize Celery instance
    '''
    app = app or create_app()
    extensions.celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    extensions.celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    extensions.celery.conf.update(app.config)

    class ContextTask(extensions.celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    extensions.celery.Task = ContextTask
    extensions.celery.conf.imports = extensions.celery.conf.imports + (
        'scrapy_api.tasks', )
    extensions.celery.conf.task_serializer = 'json'
    extensions.celery.conf.result_serializer = 'pickle'
    extensions.celery.conf.accept_content = ['json', 'pickle']
    extensions.celery.finalize()
    return extensions.celery


def init_extensions(app):
    '''
    Initialize Flask extensions.
    '''
    extensions.mongo.init_app(app)


def register_blueprints(app):
    '''
    Register blueprints for app.
    '''
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api = Api(blueprint,
              title=app.config.app_name,
              version=app.config.app_version,
              description=app.config.app_descr)

    # Error handlers
    @blueprint.app_errorhandler(404)
    def path_not_found(error):
        return errors.make_error_response(errors.Error404())

    @api.errorhandler
    def default_error_handler(error):
        return errors.make_error_response(error)

    # Adding namespaces
    api.add_namespace(ping_namespace)
    api.add_namespace(document_namespace)
    api.add_namespace(image_namespace)

    app.register_blueprint(blueprint)


def create_app():
    ''' 
    Create new Flask app instance.
    '''
    app = Flask(__name__)
    configure_app(app)
    init_extensions(app)
    register_blueprints(app)
    init_celery(app)
    return app
