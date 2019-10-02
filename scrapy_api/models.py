'''
Database models
'''
from celery.result import AsyncResult
from flask_mongoengine import Document
from mongoengine import (BinaryField, EmbeddedDocument, EmbeddedDocumentField,
                         IntField, ListField, StringField, signals)

from scrapy_api.tasks import get_images, get_text


class Task(Document):
    meta = {'abstract': True}
    url = StringField(max_length=100)
    task_id = StringField(max_length=50)
    task_status = StringField(max_length=10)

    task_function = None

    @classmethod
    def pre_save(cls, sender, task, **kwargs):
        '''
        Hook function which is executes celery task
        before model object is saved.
        '''
        if not task.task_id:
            celery_task = cls.task_function.apply_async((task.url, ))
            task.task_id = celery_task.id
            task.task_status = celery_task.state

    def refresh_task_state(self):
        '''
        Function which fetches task state from Celery
        and saves it.
        '''
        celery_task = AsyncResult(self.task_id)
        self.task_status = celery_task.state
        self.save()


class DocumentTask(Task):
    text = StringField()
    status_code = IntField()

    task_function = get_text


signals.pre_save.connect(DocumentTask.pre_save, sender=DocumentTask)


class Image(EmbeddedDocument):
    id = IntField()
    img = BinaryField()


class ImageTask(Task):
    images = ListField(EmbeddedDocumentField(Image))

    task_function = get_images


signals.pre_save.connect(ImageTask.pre_save, sender=ImageTask)