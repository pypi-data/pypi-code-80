import logging

from kitchensink.utils.aws import publish_to_aws
from celery import shared_task

logger = logging.getLogger('tasks')


@shared_task(acks_late=True)
def task_publish_to_aws(
    filepath,
    data,
    mode='preview',
    contentType='application/json'
):
    publish_to_aws(filepath, data, mode, contentType)
    logger.info('AWS Published: %s: %s.' % (mode, filepath))
