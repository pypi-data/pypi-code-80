import json
import logging
from typing import Any, Dict

from ._base import Base

sqspy_logger = logging.getLogger("sqspy")


class Producer(Base):
    """
    Message producer.

    :param str queue_name: Optional queue name.
    :param str queue_url: Optional queue url, according to AWS
        guidelines.
    :param SQS.Queue queue: Optional queue resource.
    :param str visibility_timeout: Message visibility timeout in
        seconds, but as a string value.  Defaults to
        :const:`~sqspy._base.Base.QUEUE_VISIBILITY_TIMEOUT`
    :param bool create_queue: Set to `False` if the queue should not
        be created in case it does not exist.  Default value is
        `True`.

    :raises ValueError: At least one of `queue`, `queue_url` or
        `queue_name` has to be provided.
    """

    def __init__(self, queue_name: str = None, queue_url: str = None, **kwargs):
        queue = kwargs.get("queue")
        if not any([queue, queue_name, queue_url]):
            raise ValueError(
                "One of `queue`, `queue_name` or `queue_url` should be provided"
            )
        super().__init__(**kwargs)
        queue_data: Dict[str, str] = {
            "name": queue_name,
            "url": queue_url,
            "visibility_timeout": kwargs.get("visibility_timeout"),
        }
        create_queue: bool = bool(kwargs.get("create_queue", True))
        self._queue = queue or self.get_or_create_queue(
            queue_data,
            create_queue=create_queue,
        )
        if self.queue is None:
            raise ValueError(
                "No queue found with name or URL provided, or "
                "application did not have permission to create one."
            )
        self._queue_name = self.queue.url.split("/")[-1]

    @property
    def queue(self):
        """See :attr:`~sqspy.consumer.Consumer.queue`"""
        return self._queue

    @property
    def queue_name(self) -> str:
        """See :attr:`~sqspy.consumer.Consumer.queue_name`"""
        return self._queue_name

    def publish(self, message: Any, **kwargs):
        """
        Method to publish message to queue.

        The message should be json serializable.  The other arguments
        can be sent as named parameters.  More information is
        available at :meth:`SQS.Queue.send_message`.

        :param Any message: The message body.

        :returns: Dictionary of attributes as per AWS guidelines.
                  Check: :meth:`~SQS.Queue.send_message`.

        :rtype: dict
        """
        sqspy_logger.info(f"Sending message to queue {self.queue_name}.")
        return self._queue.send_message(MessageBody=json.dumps(message), **kwargs)
