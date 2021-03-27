from typing import ClassVar, Tuple

from pyworks_generator.imports import Import
from pyworks_generator.model import DataModel
from pyworks_generator.model.pydantic.imports import IMPORT_DATACLASS


class DataClass(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = 'pydantic/dataclass.jinja2'
    DEFAULT_IMPORTS: ClassVar[Tuple[Import, ...]] = (IMPORT_DATACLASS,)
