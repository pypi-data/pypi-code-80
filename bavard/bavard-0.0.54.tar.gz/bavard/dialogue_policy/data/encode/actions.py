import typing as t

import numpy as np
from bavard_ml_common.types.conversations.actions import UserAction, AgentAction

from bavard.dialogue_policy.constants import MAX_UTTERANCE_LEN
from bavard.dialogue_policy.data.utils import EncodingContext, TypeEncoder


class UserActionEncoder(TypeEncoder[UserAction]):

    @staticmethod
    def encode(action: UserAction, enc_context: EncodingContext) -> t.Dict[str, np.ndarray]:
        intent = action.intent if action.intent in enc_context.classes_("intent") else None
        # feature vec
        encoded_intent = enc_context.transform("intent", [intent])
        encoded_tags = enc_context.transform(
            "tags",
            [[]] if action.tags is None else [
                [tag.tagType for tag in action.tags if tag.tagType in enc_context.classes_("tags")]
            ]
        )
        feature_vec = np.concatenate([encoded_intent, encoded_tags], axis=1)

        utterance = action.translatedUtterance if action.translatedUtterance else action.utterance
        utterance_encoding = enc_context.transform("utterance", utterance)

        return {
            "feature_vec": feature_vec,
            "utterance_ids": utterance_encoding["input_ids"],
            "utterance_mask": utterance_encoding["input_mask"],
        }

    @staticmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Union[t.Sequence[int], t.Dict[str, t.Sequence[int]]]:
        return {
            "feature_vec": (1, enc_context.get_size("intent") + enc_context.get_size("tags")),
            "utterance_ids": (1, MAX_UTTERANCE_LEN),
            "utterance_mask": (1, MAX_UTTERANCE_LEN),
        }


class AgentActionEncoder(TypeEncoder[AgentAction]):

    @staticmethod
    def encode(action: AgentAction, enc_context: EncodingContext) -> t.Union[np.ndarray, t.Dict[str, np.ndarray]]:
        # TODO: include utterance encoding
        return enc_context.transform("action", [action.name])

    @staticmethod
    def encode_index(action: AgentAction, enc_context: EncodingContext) -> int:
        return enc_context.transform("action_index", [action.name])[0]

    @staticmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Union[t.Sequence[int], t.Dict[str, t.Sequence[int]]]:
        return 1, enc_context.get_size("action")
