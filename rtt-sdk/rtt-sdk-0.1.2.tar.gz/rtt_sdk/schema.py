import datetime
from typing import TYPE_CHECKING

import fastapi.openapi.models
from pydantic import BaseConfig, BaseModel, validator
from pydantic.main import Extra

if TYPE_CHECKING:
    from dataclasses import dataclass
else:

    def dataclass(model):
        return model


autocomplete = dataclass

# Allow custom field additions in schema objects (x-thing)
fastapi.openapi.models.SchemaBase.__config__.extra = Extra.allow


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(word if index == 0 else word.capitalize() for index, word in enumerate(string.split("_")))


class Schema(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {datetime.datetime: convert_datetime_to_realworld}
        alias_generator = convert_field_to_camel_case

    @validator("*", pre=True)
    def not_none(cls, v, field):
        if field.default and v is None:
            return field.default
        else:
            return v
