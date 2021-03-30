import json
import logging
from typing import List

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from metaphor.common.event_util import EventUtil
from metaphor.common.metadata_change_event import Dataset

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Kinesis:
    """Kinesis client functions"""

    _stream_name = "mce"
    _partition_key = "123"

    _client = boto3.client(
        "kinesis",
        config=Config(
            region_name="us-west-2",
            signature_version="v4",
            retries={"max_attempts": 3, "mode": "standard"},
        ),
    )

    @staticmethod
    def send_messages(entities: List[Dataset]) -> None:
        """Send MCE message to Kinesis Stream"""
        events = [EventUtil.build_event(entity) for entity in entities]
        records = [EventUtil.trim_event(e) for e in events]
        valid_records = [r for r in records if EventUtil.validate_message(r)]
        logger.debug("Records: {}".format(json.dumps(valid_records)))
        if valid_records:
            Kinesis.__send_records(valid_records)

    @staticmethod
    def __send_records(messages: List) -> None:
        """Send records to Kinesis Stream"""
        records = [
            {
                "Data": json.dumps(msg),
                "PartitionKey": Kinesis._partition_key,
            }
            for msg in messages
        ]

        try:
            response = Kinesis._client.put_records(
                StreamName=Kinesis._stream_name, Records=records
            )
            logger.info(
                "Sent {} records. Response {}".format(len(messages), str(response))
            )
        except ClientError:
            logger.error("Error putting Kinesis records.")
            raise
        else:
            # TODO: error handling of some records failure within batch
            return response
