'''
Database models. In this module all ORM related stuff are declared.
'''
from celery.result import AsyncResult
from flask_mongoengine import Document
from mongoengine import (BinaryField, EmbeddedDocument, EmbeddedDocumentField,
                         IntField, ListField, StringField, signals, errors)

from scrapy_api.tasks import get_images, get_text


class Task(Document):
    '''
    Task base model.
    '''
    meta = {'abstract': True}
    url = StringField(max_length=100, required=True)
    task_id = StringField(max_length=50)
    task_status = StringField(max_length=10)

    # needs to be overwritten in child's class
    task_function = None

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        '''
        Hook function which is executes celery task
        before model object is saved.
        '''
        if not document.task_id:
            celery_task = cls.task_function.apply_async((document.url, ))
            document.task_id = celery_task.id
            document.task_status = celery_task.state

    @classmethod
    def get_task(cls, task_id):
        '''
        Returns Task like object using task's id.
        '''
        task = cls.objects.get_or_404(task_id=task_id)
        return task

    def refresh_task_state(self):
        '''
        Function which fetches task state from Celery
        and saves it.
        '''
        celery_task = AsyncResult(self.task_id)
        self.task_status = celery_task.state
        self.save()

    def to_json(self) -> dict:
        return {
            'task_id': self.task_id,
            'task_status': self.task_status,
            'url': self.url,
        }


class DocumentTask(Task):
    '''
    Document model class.
    '''
    text = StringField()
    status_code = IntField()

    task_function = get_text

    def to_json(self):
        json_dict = super().to_json()
        json_dict.update({
            'text': self.text,
            'status_code': self.status_code,
        })
        return json_dict


signals.pre_save.connect(DocumentTask.pre_save, sender=DocumentTask)


class Image(EmbeddedDocument):
    '''
    Image model class.
    '''
    img = BinaryField()

    @classmethod
    def get_image(cls, img_id):
        image = cls.objects.get(id=img_id)
        if not image:
            raise errors.DoesNotExist()
        return image

    def to_json(self):
        return {'img_id': self.pk, 'img': self.img}


class ImageTask(Task):
    '''
    Image task model class.
    '''
    images = ListField(EmbeddedDocumentField(Image))

    task_function = get_images

    def to_json(self):
        json_dict = super().to_json()
        json_dict.update({'images': [img.to_json() for img in self.images]})
        return json_dict


signals.pre_save.connect(ImageTask.pre_save, sender=ImageTask)
