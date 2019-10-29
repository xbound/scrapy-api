import io
from flask import request, abort, send_file
from flask_restplus import Namespace, Resource, fields
from celery.result import AsyncResult

from scrapy_api.models import ImageTask, Image
from scrapy_api import errors

__all__ = ['image_namespace']

image_namespace = Namespace('images', description='Images endpoint')

put_input = image_namespace.model(
    'Image task PUT request', {
        'url': fields.Url(description='URL of website', required=True),
    })

task_output = image_namespace.model(
    'Image task PUT response', {
        'task_id':
        fields.String(description='Task unique identifier.',
                      example='440df-edf-4e'),
        'task_status':
        fields.String(description='Task status', example='SUBMITTED'),
    })

post_input = image_namespace.model(
    'Image task status request', {
        'task_id':
        fields.String(description='Task unique identifier', required=True),
    })


@image_namespace.errorhandler(ImageTask.DoesNotExist)
def image_task_does_not_exist(error):
    return errors.make_error_response(errors.TaskDoesNotExist())


@image_namespace.route('/')
class ImageAPI(Resource):
    '''
    Images endpoint
    '''
    @image_namespace.expect(put_input)
    @image_namespace.marshal_with(task_output)
    def put(self):
        '''
        Submit task to get images from page by url.
        '''
        json_data: dict = image_namespace.payload
        image = ImagePUTInput.load(json_data).data
        image.save()
        return ImagePUTOutput.dump(image)

    @image_namespace.expect(put_input)
    @image_namespace.expect(task_output)
    def post(self):
        '''
        Get status of submitted task.
        '''
        json_data: dict = image_namespace.payload
        task_id = json_data['task_id']
        image: ImageTask = ImageTask.objects.get(task_id=task_id)
        image.refresh_task_state()
        return image


@image_namespace.route('/<string:image_id>')
@image_namespace.param('image_id', 'Image unique identifier.')
class ImageAPIDownload(Resource):
    @image_namespace.produces(['image/jpeg'])
    def get(self, image_id):
        '''
        Get image from task result.
        '''
        task_id = request.args.get('task_id')
        img_id = int(request.args.get('img_id'))
        image = self.get_image(task_id, img_id)
        if not image:
            abort(404)
        return send_file(io.BytesIO(image.img),
                         mimetype='image/jpeg',
                         as_attachment=True,
                         attachment_filename='{}-{}-{}.jpg'.format(
                             'Image', task_id, id))
