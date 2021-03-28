from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from ctlml_commons.util.date_utils import convert_dates


@dataclass(frozen=True)
class News:
    api_source: str
    author: str
    num_clicks: int
    preview_image_url: str
    published_at: datetime
    relay_url: str
    source: str
    summary: str
    title: str
    updated_at: datetime
    url: str
    uuid: str
    related_instruments: List[str]
    preview_text: str
    currency_id: str

    @classmethod
    def deserialize(cls, input_data: Dict[str, Any]) -> News:
        return News(**cls.clean(input_data=input_data))

    @classmethod
    def clean(cls, input_data: Dict[str, Any]) -> Dict[str, Any]:
        data = deepcopy(input_data)

        data = convert_dates(data, "published_at")

        return data
