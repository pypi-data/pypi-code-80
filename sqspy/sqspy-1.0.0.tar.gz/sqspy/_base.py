import logging
from typing import Any, Dict

import boto3
import boto3.session

sqspy_logger = logging.getLogger("sqspy")


class Base:
    """Base class initialisation to setup aws credentials.

    To make use of instance roles when deploying to AWS
    infrastructure, leave the `aws_*` keys blank (``None``).

    :param str aws_access_key_id: AWS access key credential.

    :param str aws_secret_access_key: AWS access key credential.

    :param str profile_name: Local AWS credential profile name.

    :param str region_name: AWS region for resources.

    :param str endpoint_url: Custom endpoint URL for usage.
    """

    #: Message's visibility timeout in seconds. See `Visibility Timeout
    #: <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html>`_
    #: in *Amazon Simple Queue Service Developer Guide* for more information.
    QUEUE_VISIBILITY_TIMEOUT: str = "600"

    def __init__(self, **kwargs):
        aws_access_key_id = kwargs.get("aws_access_key_id")
        aws_secret_access_key = kwargs.get("aws_secret_access_key")
        profile_name = kwargs.get("profile_name")
        endpoint_url = kwargs.get("endpoint_url")
        region_name = kwargs.get("region_name")
        self._session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            profile_name=profile_name,
            region_name=region_name,
        )
        self._sqs = self._session.resource(
            "sqs",
            region_name=region_name,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        sqspy_logger.debug("Initialised SQS resource")

    def get_or_create_queue(
        self,
        queue_data: Dict[str, str],
        create_queue: bool = True,
    ):
        """Fetch or create the sqs Queue resource from boto3.

        Also tries to create the queue resource with the configured
        credentials as dictated by the `create_queue` parameter if the
        resource was not located.

        :param dict[str,str] queue_data: Dictionary referencing
            parameters for the queue to be retrieved or created.

            The keys for the data are: `name`, `url` and
            `visibility_timeout`.  The visibility_timeout defaults to
            :const:`QUEUE_VISIBILITY_TIMEOUT`.

        :param bool create_queue: Force creation of queue resource on
            AWS.  Default is `True`

        :returns: An `Queue` resource on success, `None` otherwise.

        :rtype: SQS.Queue or None
        """
        queue_name = queue_data.get("name", "")
        queue_visibility: str = (
            queue_data.get("visibility_timeout") or self.QUEUE_VISIBILITY_TIMEOUT
        )
        queue = self.get_queue(queue_data)
        if queue is not None:
            return queue
        if create_queue is False:
            sqspy_logger.warning("Denied creation of queue.")
            return None
        sqspy_logger.debug(f"Creating the queue: {queue_name}")
        queue_attributes = {
            "VisibilityTimeout": queue_visibility,
        }
        if queue_name.endswith(".fifo"):
            queue_attributes["FifoQueue"] = "true"
        return self.create_queue(queue_name, queue_attributes)

    def get_queue(self, queue_data: Dict[str, str]):
        """Retrieve the Queue resource based on provided parameters.

        :param dict[str,str] queue_data: Same as used for
            :meth:`get_or_create_queue`

        :returns:
        """
        queue_url = queue_data.get("url")
        queue_name = queue_data.get("name")
        if queue_url:
            return self._sqs.Queue(queue_url)
        for q in self._sqs.queues.filter(QueueNamePrefix=queue_name):
            name = q.url.split("/")[-1]
            if name == queue_name:
                return q
        sqspy_logger.warning("Queue not found.")
        return None

    def create_queue(self, name: str, attributes: Dict[str, Any]):
        """Create a Queue resource.

        For more information, check
        :meth:`SQS.ServiceResource.create_queue`

        :param str name: Sent as the `QueueName` to the boto3 method.

        :param dict[str,str] attributes: Same as parameter
            `Attributes` to :meth:`~SQS.ServiceResource.create_queue`

        :returns: A Queue resource

        :rtype: SQS.Queue
        """
        return self._sqs.create_queue(QueueName=name, Attributes=attributes)
