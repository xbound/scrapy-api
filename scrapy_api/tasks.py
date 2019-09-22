'''
Celery tasks module.
'''
from celery.signals import task_success, task_postrun
from celery.utils.log import get_logger

from requests_html import HTMLSession
from requests import get
from requests.exceptions import MissingSchema, ConnectionError

from scrapy_api.extensions import celery
from scrapy_api import models

logger = get_logger(__name__)


@celery.task(bind=True)
def get_text(self, page_url):
    ''' Taks to get all text from page.

    :param page_url: url of page
    :return: result dictionary
    '''
    r = HTMLSession().get(page_url)
    result = {
        'url': page_url,
        'status_code': r.status_code,
    }
    if r.status_code == 200:
        page_links = r.html.absolute_links
        full_text = r.html.text
        result['text'] = full_text or ''
    return result


@celery.task(bind=True)
def get_images(self, page_url):
    ''' Taks to get all images from page.

    :param page_url: url of page
    :return: result dictionary
    '''
    r = HTMLSession().get(page_url)
    images = r.html.find('img')
    result = []
    for idx, img in enumerate(images):
        img_url = img.attrs.get('src')
        if img_url:
            response = get(img_url)
            result.append({'id': idx, 'img': response.content})
    return result


@task_postrun.connect
def on_get_text_task_end(task_id, task, *args, **kwargs):
    ''' Trigger to register pending task in the system.

    :param task_id: id of pending task.
    :param task: instance if pending task.
    :param args: positional parametres.
    :param kwargs: key-value parametres.
    '''
    if task.name == 'scrapy_api.commons.tasks.get_text':
        try:
            document_task = models.DocumentTask.objects.get(task_id=task_id)
            task_status = kwargs['state']
            result = kwargs['retval']
            document_task.status_code = result.get('status_code')
            document_task.text = result.get('text')
            document_task.task_status = task_status
            document_task.save()
        except models.DocumentTask.DoesNotExist as exc:
            logger.error(exc)
    else:
        try:
            image_task = models.ImageTask.objects.get(task_id=task_id)
            task_status = kwargs['state']
            image_results = [
                models.Image(
                    id=image_result.get('id'), img=image_result.get('img'))
                for image_result in kwargs['retval']
            ]
            image_task.task_status = task_status
            image_task.images = image_results
            image_task.save()
        except models.ImageTask.DoesNotExist as exc:
            logger.error(exc)
