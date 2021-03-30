import json
import logging
import os
from datetime import datetime

import fastjsonschema

from metaphor.common.metadata_change_event import (
    MetadataChangeEvent,
    Dataset,
    EventHeader,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class EventUtil:
    """Event utilities"""

    kinesis_tenant = os.environ.get("KINESIS_TENANT", "default")

    with open("metadata_change_event.json", "r") as f:
        validate = fastjsonschema.compile(json.load(f))

    @staticmethod
    def build_event(entity: Dataset) -> MetadataChangeEvent:
        """Build MCE given entity"""
        event = MetadataChangeEvent()
        event.eventHeader = EventHeader()
        event.eventHeader.time = datetime.now().isoformat()
        event.tenant = EventUtil.kinesis_tenant
        event.snapshot = entity
        return event

    @staticmethod
    def validate_message(message: dict) -> bool:
        """Validate message against json schema"""
        try:
            EventUtil.validate(message)
        except fastjsonschema.JsonSchemaException as e:
            logger.error("MCE validation error: {}. Message: {}".format(e, message))
            return False
        return True

    @staticmethod
    def clean_nones(value):
        """
        Recursively remove all None values from dictionaries and lists, and returns
        the result as a new dictionary or list.
        """
        if isinstance(value, list):
            return [EventUtil.clean_nones(x) for x in value if x is not None]
        elif isinstance(value, dict):
            return {
                key: EventUtil.clean_nones(val)
                for key, val in value.items()
                if val is not None
            }
        else:
            return value

    @staticmethod
    def trim_event(event: MetadataChangeEvent) -> dict:
        """Cast event to dict and remove all None values"""
        return EventUtil.clean_nones(event.to_dict())

    @staticmethod
    def serialize_event(event: MetadataChangeEvent) -> str:
        """Serialize event to json string"""
        return json.dumps(EventUtil.trim_event(event))
