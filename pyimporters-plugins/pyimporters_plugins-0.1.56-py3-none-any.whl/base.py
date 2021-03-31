import abc
from contextlib import contextmanager
from gzip import GzipFile
from typing import Optional, List, Dict, Any, Type, Generator, Union
from pathlib import Path
from zipfile import ZipFile

from fastapi import Query
from progress.bar import Bar
from pydantic import BaseModel, Field, validator, Extra
from pydantic.dataclasses import dataclass
from pydantic.fields import FieldInfo


class Term(BaseModel):
    identifier: str = Field(..., description="Unique identifier of the term", example="http://www.example.com/rocks")
    prefLabel: str = Field(..., description="The preferred label of the term", example="rocks")
    altLabel: Optional[List[str]] = Field(None, description="The alternative labels of the term", example=["basalt", "granite", "slate"])
    properties: Optional[Dict[str,Any]] = Field(None, description="Additional properties of the term", example={"wikidataId" : "Q8063"})

@dataclass
class KnowledgeParserOptions:
    project: str = Query(None, description="Name of the project", extra="internal")
    lexicon: str = Query(None, description="Lexicon to inject the terms", extra="internal")
    lang: str = Query('en', description="Language of the project", extra="internal")
    limit: int = Query(0, description="Number of terms to import. O means all", extra="advanced", ge=0)

KnowledgeParserModel = KnowledgeParserOptions.__pydantic_model__

class KnowledgeParserBase(metaclass=abc.ABCMeta):
    """Base class for example plugin used in the tutorial.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse(self, source : Path, options: Union[BaseModel, Dict[str, Any]], bar : Bar) -> Generator[Term, None, None]:
        """Parse the input source file and return a stream of concepts.

        :param source: A file object containing the knowledge.
        :param options: options of the parser.
        :returns: Iterable producing the concepts.
        """

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return KnowledgeParserOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return KnowledgeParserModel

@contextmanager
def maybe_archive(source : Path):
    try:
        archive = None
        file = None
        if source.suffix == ".gz":
            file = GzipFile(str(source))
        elif source.suffix == ".zip":
            archive = ZipFile(str(source))
            file = archive.open(archive.filelist[0])
        else:
            file = source.open("r", encoding="utf-8")
        yield file
    finally:
        if file:
            file.close()
        if archive:
            archive.close()
