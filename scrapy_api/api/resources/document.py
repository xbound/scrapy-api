from flask import request, abort
from flask_restplus import Namespace, Resource
from celery.result import AsyncResult

from scrapy_api.models import DocumentTask
from scrapy_api.schemas.document import (
    DocumentSchema,
    DocumentPOSTOutput,
    DocumentPUTInput,
    DocumentPUTOutput,
)

api = Namespace('documents', description='Documents endpoint')


@api.route('/')
class DocumentAPI(Resource):
    '''
    Documents endpoint
    '''

    def get_document(self, task_id):
        try:
            return DocumentTask.objects.get(task_id=task_id)
        except DocumentTask.DoesNotExist:
            return None

    def put(self):
        '''
        Submit task to get text from page by url.
        '''
        json_data = api.payload
        document = DocumentPUTInput.load(json_data).data
        document.save()
        return DocumentPUTOutput.dump(document)

    def post(self):
        '''
        Get status of submitted task.
        '''
        json_data = api.payload
        task_id = json_data['task_id']
        document = self.get_document(task_id)
        if not document:
            abort(404, 'Task does not exist.')
        celery_task = AsyncResult(document.task_id)
        document.task_status = celery_task.state
        document.save()
        return DocumentPOSTOutput.dump(document)

    def get(self):
        '''
        Get task result.
        '''
        task_id = request.args.get('task_id')
        if not task_id:
            abort(400)
        document = self.get_document(task_id)
        if not document:
            abort(404, 'Task does not exist.')
        return DocumentSchema().dump(document)
