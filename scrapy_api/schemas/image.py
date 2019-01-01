'''
Schemas for image related models.
'''
from marshmallow_mongoengine import ModelSchema
from scrapy_api.models import ImageTask, Image

class ImageSchema(ModelSchema):
    '''
    Embedded image schema for Image model.
    '''

    class Meta:
        model = Image
        exclude = ('img', )


class ImageTaskSchema(ModelSchema):
    '''
    ImageTaskSchema schema for generating JSON response
    based on ImageTask model.
    '''

    images = ImageSchema(many=True)

    class Meta:
        model = ImageTask


# PUT /images endpoint request and response schemas
ImagePUTInput = ImageTaskSchema(only=('url', ))
ImagePUTOutput = ImageTaskSchema(only=(
    'task_id',
    'task_status',
))

# POST /images endpoint request and response schemas
ImagePOSTInput = ImageTaskSchema(only=('task_id', ))
ImagePOSTOutput = ImageTaskSchema(only=('task_id', 'task_status', 'images.id'))
