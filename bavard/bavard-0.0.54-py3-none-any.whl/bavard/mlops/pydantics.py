import typing as t

from bavard_ml_common.types.conversations.conversation import Conversation
from bavard_ml_common.types.ml import StrPredWithConf
from pydantic import BaseModel

from bavard.nlu.pydantics import NLUPrediction


class ChatbotPipelinePrediction(BaseModel):
    nlu: t.Optional[NLUPrediction]
    dp: t.Optional[t.List[StrPredWithConf]]


class ChatbotPipelinePredictions(BaseModel):
    predictions: t.List[ChatbotPipelinePrediction]


class ChatbotPipelineInputs(BaseModel):
    instances: t.List[Conversation]
