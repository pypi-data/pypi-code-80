import typing as t

from bavard_ml_common.types.ml import StrPredWithConf
from pydantic import BaseModel


class TagPrediction(BaseModel):
    """Represents a named entity's type, value, and position in an utterance.
    """
    tagType: str
    value: str
    start: int
    end: int


class NLUPrediction(BaseModel):
    intent: StrPredWithConf
    tags: t.List[TagPrediction]


class NLUPredictions(BaseModel):
    predictions: t.List[NLUPrediction]
