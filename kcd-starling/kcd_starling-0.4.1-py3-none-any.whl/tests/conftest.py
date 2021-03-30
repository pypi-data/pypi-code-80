from datetime import datetime, timedelta

import pytest

from starling.types import MessageData


@pytest.fixture()
def message_data():
    return MessageData(
        message={'contents': 'test'},
    )
