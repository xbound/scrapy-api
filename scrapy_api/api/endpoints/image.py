import io
from flask import request, abort, send_file
from flask_restplus import Namespace, Resource, reqparse
from celery.result import AsyncResult

from scrapy_api.models import ImageTask, Image
from scrapy_api.schemas.image import (ImagePOSTOutput, ImagePUTInput,
                                      ImagePUTOutput)

__all__ = ['image_namespace']

image_namespace = Namespace('/image/', description='Images endpoint')

put_arguments = reqparse.RequestParser()
put_arguments.add_argument('url', type=str, help='URL of web page.')

post_arguments = reqparse.RequestParser()
post_arguments.add_argument('task_id', type=str, help='Task id.')

get_arguments = reqparse.RequestParser()
get_arguments.add_argument('task_id', type=str, help='Task id.')
get_arguments.add_argument('img_id', type=int, help='Image id.')

@image_namespace.route('/')
class ImageAPI(Resource):
    '''
    Images endpoint
    '''

    def get_image(self, task_id, id):
        task = ImageTask.objects(task_id=task_id, images__id=id).first()
        image = next((img for img in task.images if img.id == id), None)
        return image

    @image_namespace.expect(put_arguments)
    def put(self):
        '''
        Submit task to get images from page by url.
        '''
        json_data = image_namespace.payload
        image = ImagePUTInput.load(json_data).data
        image.save()
        return ImagePUTOutput.dump(image)

    @image_namespace.expect(post_arguments)
    def post(self):
        '''
        Get status of submitted task.
        '''
        json_data = image_namespace.payload
        task_id = json_data['task_id']
        image = ImageTask.objects.get(task_id=task_id)
        celery_task = AsyncResult(image.task_id)
        image.task_status = celery_task.state
        image.save()
        return ImagePOSTOutput.dump(image)

    @image_namespace.expect(get_arguments)
    @image_namespace.produces(['image/jpeg'])
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
