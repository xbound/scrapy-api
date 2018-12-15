import io
from flask import request, abort, send_file
from flask_restplus import Namespace, Resource
from celery.result import AsyncResult

from scrapy_api.models import ImageTask, Image
from scrapy_api.schemas.image import (ImagePOSTOutput, ImagePUTInput,
                                      ImagePUTOutput)

api = Namespace('images', description='Images endpoint')


@api.route('/')
class ImageAPI(Resource):
    '''
    Images endpoint
    '''

    def get_image(self, task_id, id):
        try:
            task = ImageTask.objects(task_id=task_id, images__id=id).first()
            image = next((img for img in task.images if img.id == id), None)
            return image
        except ImageTask.DoesNotExist:
            return None

    def get_image_task(self, task_id):
        try:
            return ImageTask.objects.get(task_id=task_id)
        except ImageTask.DoesNotExist:
            return None

    def put(self):
        '''
        Submit task to get images from page by url.
        '''
        json_data = api.payload
        image = ImagePUTInput.load(json_data).data
        image.save()
        return ImagePUTOutput.dump(image)

    def post(self):
        '''
        Get status of submitted task.
        '''
        json_data = api.payload
        task_id = json_data['task_id']
        image = self.get_image_task(task_id)
        if not image:
            abort(404, 'Task does not exist.')
        celery_task = AsyncResult(image.task_id)
        image.task_status = celery_task.state
        image.save()
        return ImagePOSTOutput.dump(image)

    @api.produces(['image/jpeg'])
    def get(self):
        '''
        Get image from task result.
        '''
        task_id = request.args.get('task_id')
        img_id = int(request.args.get('img_id'))
        image = self.get_image(task_id, img_id)
        if not image:
            abort(404)
        return send_file(
            io.BytesIO(image.img),
            mimetype='image/jpeg',
            as_attachment=True,
            attachment_filename='{}-{}-{}.jpg'.format('Image', task_id, id))
