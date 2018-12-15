'''
Database models
'''
from flask_mongoengine import Document
from mongoengine import (
    EmbeddedDocument,
    StringField,
    IntField,
    BinaryField,
    EmbeddedDocumentField,
    ListField,
)
from mongoengine import signals

from scrapy_api.commons.tasks import get_text, get_images


class Task(Document):
    meta = {'abstract': True}
    url = StringField(max_length=100)
    task_id = StringField(max_length=50)
    task_status = StringField(max_length=10)


class DocumentTask(Task):
    text = StringField()
    status_code = IntField()

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if not document.task_id:
            celery_task = get_text.apply_async((document.url, ))
            document.task_id = celery_task.id
            document.task_status = celery_task.state


signals.pre_save.connect(DocumentTask.pre_save, sender=DocumentTask)


class Image(EmbeddedDocument):
    id = IntField()
    img = BinaryField()


class ImageTask(Task):
    images = ListField(EmbeddedDocumentField(Image))

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        if not document.task_id:
            celery_task = get_images.apply_async((document.url, ))
            document.task_id = celery_task.id
            document.task_status = celery_task.state



signals.pre_save.connect(ImageTask.pre_save, sender=ImageTask)
