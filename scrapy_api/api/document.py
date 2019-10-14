from flask import request, abort
from flask_restplus import Namespace, Resource, fields

from scrapy_api.models import DocumentTask
from scrapy_api import errors

__all__ = ['document_namespace']

document_namespace = Namespace('document', description='Documents endpoint')

put_input = document_namespace.model(
    'Document task PUT request', {
        'url': fields.Url(description='URL of website', required=True),
    })

put_output = document_namespace.model(
    'Document task PUT response', {
        'task_id':
        fields.String(description='Task unique identifier.',
                      example='440df-edf-4e'),
        'task_status':
        fields.String(description='Task status', example='SUBMITTED'),
    })

post_input = document_namespace.model(
    'Document task status request', {
        'task_id':
        fields.String(description='Task unique identifier', required=True),
    })

get_output = document_namespace.inherit(
    'Document task GET response', put_output, {
        'text': fields.String(description='Extracted text'),
        'status_code': fields.Integer(description='Fetch HTTP code result'),
    })

task_not_found = errors.error_to_swagger(document_namespace,
                                         errors.TaskDoesNotExist)
task_not_provided = errors.error_to_swagger(document_namespace,
                                            errors.TaskNotProvided)


@document_namespace.errorhandler(DocumentTask.DoesNotExist)
def document_task_does_not_exist(error):
    return errors.make_error_response(errors.TaskDoesNotExist)


@document_namespace.route('/')
class DocumentAPI(Resource):
    '''
    Documents endpoint
    '''
    @document_namespace.expect(put_input, validate=True)
    @document_namespace.response(400, 'Bad request')
    @document_namespace.marshal_with(put_output,
                                     code=201,
                                     description='New task submitted')
    def put(self):
        '''
        Submit task to get text from page by url.
        '''
        input_args: dict = document_namespace.payload
        document = DocumentTask(**input_args)
        document.save()
        return document, 201

    @document_namespace.expect(post_input, validate=True)
    @document_namespace.marshal_with(put_output,
                                     code=200,
                                     description='Task status')
    @document_namespace.marshal_with(task_not_found,
                                     code=404,
                                     description='Task not found')
    def post(self):
        '''
        Get status of submitted task using task_id.
        '''
        input_args: dict = document_namespace.payload
        document: DocumentTask = DocumentTask.objects.get(
            task_id=input_args['task_id'])
        document.refresh_task_state()
        return document, 200


@document_namespace.route('/<task_id>')
@document_namespace.param('task_id', 'Task unique identifier.')
class DocumentAPIGet(Resource):
    @document_namespace.marshal_with(get_output, code=200)
    @document_namespace.marshal_with(task_not_provided,
                                     code=400,
                                     description='Task not provided')
    @document_namespace.marshal_with(task_not_found,
                                     code=404,
                                     description='Task not found')
    def get(self):
        '''
        Get task result using task_id.
        '''
        task_id = request.args.get('task_id')
        if not task_id:
            abort(400)
        document: DocumentTask = DocumentTask.objects.get(task_id=task_id)
        return document, 200
