'''
Schemas for document related models.
'''
from marshmallow_mongoengine import ModelSchema
from scrapy_api.models import DocumentTask


class DocumentSchema(ModelSchema):
    '''
    Document schema for generating JSON response
    based on DocumentTask model.
    '''

    class Meta:
        model = DocumentTask


# PUT /documents endpoint request and response schemas
DocumentPUTInput = DocumentSchema(only=('url', ))
DocumentPUTOutput = DocumentSchema(only=(
    'task_id',
    'task_status',
))

# POST /documents endpoint request and response schemas
DocumentPOSTOutput = DocumentPUTOutput