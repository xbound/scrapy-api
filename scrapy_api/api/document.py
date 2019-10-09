from flask import request, abort
from flask_restplus import Namespace, Resource, reqparse

from scrapy_api.models import DocumentTask
from scrapy_api import errors

__all__ = ['document_namespace']

document_namespace = Namespace('document', description='Documents endpoint')

put_arguments = reqparse.RequestParser()
put_arguments.add_argument('url', type=str, help='URL of web page.')

post_arguments = reqparse.RequestParser()
post_arguments.add_argument('task_id', type=str, help='Task id.')



@document_namespace.errorhandler(DocumentTask.DoesNotExist)
def doccument_task_does_not_exist(error):
    return errors.make_error_response(errors.TaskDoesNotExist)


@document_namespace.route('/')
class DocumentAPI(Resource):
    '''
    Documents endpoint
    '''

    @document_namespace.expect(put_arguments)
    def put(self):
        '''
        Submit task to get text from page by url.
        '''
        args = put_arguments.parse_args()
        document = DocumentPUTInput.load(args).data
        document.save()
        return DocumentPUTOutput.dump(document)

    @document_namespace.expect(post_arguments)
    def post(self):
        '''
        Get status of submitted task.
        '''
        args = post_arguments.parse_args()
        document: DocumentTask = DocumentTask.objects.get(task_id=args['task_id'])
        document.refresh_task_state()
        return DocumentPOSTOutput.dump(document)

    @document_namespace.expect(post_arguments)
    def get(self):
        '''
        Get task result.
        '''
        task_id = request.args.get('task_id')
        if not task_id:
            abort(400)
        document = DocumentTask.objects.get(task_id=task_id)
        return DocumentSchema().dump(document)
