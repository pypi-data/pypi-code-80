import json
import logging
import sys
from abc import ABCMeta, abstractmethod
from time import sleep
from typing import Dict, List

from ._base import Base
from .producer import Producer

sqspy_logger = logging.getLogger("sqspy")


class Consumer(Base):
    """
    Message consumer/worker.

    :param str queue_name: Optional queue name.
    :param str queue_url: Optional queue url, according to AWS
        guidelines.
    :param SQS.Queue queue: Optional queue resource.
    :param str visibility_timeout: Message visibility timeout in
        seconds, but as a string value.  Defaults to
        :const:`~sqspy._base.Base.QUEUE_VISIBILITY_TIMEOUT`
    :param str error_queue: Name for error queue, when messages were
        not consumed successfully.
    :param str error_queue_url: Queue url as per AWS guidelines, for
        the error queue.
    :param str error_visibility_timeout: Same as `visibility_timeout`
        but for error queue.
    :param bool create_queue: Set to `False` if the queue should not
        be created in case it does not exist.  The default is `True`.
    :param bool create_error_queue: Same as `create_queue` but for
        error queue.  The default is `True`.
    :param int poll_interval: Polling interval between messages.
        Defaults to :attr:`poll_interval`.
    :param list[str] message_attribute_names: List of attributes for
        message to fetch.  See :attr:`SQS.Message.message_attributes`.
    :param int wait_time: Time to wait (in seconds) when fetching
        messages.  Defaults to :attr:`wait_time`.
    :param bool force_delete: Whether to delete the message from queue
        before handling or not.  Defaults to False.
    :param int max_messages_count: Maximum message count when fetching
        from the queue.  Defaults to :attr:`max_messages_count`.
    :param list[str] attribute_names: Attributes to be retrieved along
        with message when fetching.  See more at:
        :meth:`SQS.Queue.receive_messages`

    :raises ValueError: At least one of `queue`, `queue_url` or
        `queue_name` has to be provided.
    """

    __metaclass__ = ABCMeta

    #: Wait time when fetching message from queue (in seconds).
    wait_time: int = 0

    #: Time between continuous fetch from queue (in seconds).
    poll_interval: int = 60

    #: Upper limit of message count when fetching from queue.
    max_messages_count: int = 1

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
        error_queue_data: Dict[str, str] = {
            "name": kwargs.get("error_queue"),
            "url": kwargs.get("error_queue_url"),
            "visibility_timeout": kwargs.get("error_visibility_timeout"),
        }
        create_queue: bool = kwargs.get("create_queue", True)
        create_error_queue: bool = kwargs.get("create_error_queue", True)
        self.poll_interval: int = int(kwargs.get("interval", self.poll_interval))
        self._message_attribute_names: List = kwargs.get("message_attribute_names", [])
        self._attribute_names: List = kwargs.get("attribute_names", [])
        self.wait_time: int = int(kwargs.get("wait_time", self.wait_time))
        self.max_messages_count: int = int(
            kwargs.get("max_messages_count", self.max_messages_count)
        )
        self._force_delete: bool = kwargs.get("force_delete", False)
        self._queue = queue or self.get_or_create_queue(
            queue_data,
            create_queue=create_queue,
        )
        if self.queue is None:
            raise ValueError(
                "No queue found with name or URL provided, or "
                "application did not have permission to create one."
            )
        self._queue_name = self._queue.url.split("/")[-1]
        self._error_queue = None
        if error_queue_data.get("name") or error_queue_data.get("url"):
            self._error_queue = Producer(
                queue_name=error_queue_data.get("name"),
                queue_url=error_queue_data.get("url"),
                queue=self.get_or_create_queue(
                    error_queue_data,
                    create_queue=create_error_queue,
                ),
            )
            self._error_queue_name = self.error_queue.queue.url.split("/")[-1]

    @property
    def queue(self):
        """
        The connected Queue resource.

        :rtype: SQS.Queue
        """
        return self._queue

    @property
    def queue_name(self) -> str:
        """
        Base name of the connected Queue resource.

        :rtype: str
        """
        return self._queue_name

    @property
    def error_queue(self):
        """
        The Queue resource for when messages were not processed
        correctly.

        :rtype: SQS.Queue
        """
        return self._error_queue

    def poll_messages(self):
        """
        Poll the queue for new messages.

        The polling happens as per the `poll_interval` specified, and
        the message fetch timeout is set as per the value in
        `wait_time`.

        :returns: A list of message resources.

        :rtype: list[SQS.Message]
        """
        while True:
            messages = self._queue.receive_messages(
                AttributeNames=self._attribute_names,
                MessageAttributeNames=self._message_attribute_names,
                WaitTimeSeconds=self.wait_time,
                MaxNumberOfMessages=self.max_messages_count,
            )
            if not messages:
                sqspy_logger.debug(
                    f"No messages were fetched for {self.queue_name}. "
                    f"Sleeping for {self.poll_interval} seconds."
                )
                sleep(self.poll_interval)
                continue
            sqspy_logger.info(
                f"{len(messages)} messages received for {self.queue_name}"
            )
            break
        return messages

    def _start_listening(self):
        while True:
            messages = self.poll_messages()
            for message in messages:
                m_body = message.body
                message_attribs = message.message_attributes
                attribs: Dict = message.attributes
                # catch problems with malformed JSON, usually a result
                # of someone writing poor JSON directly in the AWS
                # console
                try:
                    body = json.loads(m_body)
                except:
                    sqspy_logger.warning(
                        f"Unable to parse message - JSON is not formatted properly. "
                        f"Received message: {m_body}"
                    )
                    continue
                try:
                    if self._force_delete:
                        message.delete()
                        self.handle_message(body, message_attribs, attribs)
                    else:
                        self.handle_message(body, message_attribs, attribs)
                        message.delete()
                except Exception as ex:
                    # need exception logtype to log stack trace
                    sqspy_logger.exception(ex)
                    if self._error_queue:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        sqspy_logger.info("Pushing exception to error queue")
                        self._error_queue.publish(
                            {
                                "exception_type": str(exc_type),
                                "error_message": str(ex.args),
                            }
                        )

    def listen(self):
        """
        Method that triggers listening for messages, and forwards to
        :meth:`handle_message`.

        This is a blocking call.
        """
        sqspy_logger.info(f"Listening to queue {self.queue_name}")
        if self.error_queue:
            sqspy_logger.info(f"Using error queue {self._error_queue_name}")
        self._start_listening()

    @abstractmethod
    def handle_message(self, body, attributes, messages_attributes):
        """
        Method representing the handling of messages retrieved from
        queue.

        :param Any body: The body retrieved from the queue after
            passing through a json deserialiser.
        :param dict attributes: A map of the attributes requested from
            queue when fetching messages.

            See more at: :attr:`SQS.Message.attributes`

        :param dict messages_attributes: Strucutred metadata as
            retrieved from the queue.

            See more at: :attr:`SQS.Message.message_attributes`

        :rtype: None

        :raises NotImplementedError: If not overridden in a subclass.
        """
        raise NotImplementedError("Implement this function in subclass.")
