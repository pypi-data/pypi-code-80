import typing as t

import numpy as np
from bavard_ml_common.types.conversations.dialogue_turns import DialogueState, UserDialogueTurn, AgentDialogueTurn

from bavard.dialogue_policy.constants import MAX_UTTERANCE_LEN
from bavard.dialogue_policy.data.encode.actions import UserActionEncoder, AgentActionEncoder
from bavard.dialogue_policy.data.utils import EncodingContext, TypeEncoder


class DialogueStateEncoder(TypeEncoder[DialogueState]):

    @staticmethod
    def encode(state: DialogueState, enc_context: EncodingContext) -> t.Union[np.ndarray, t.Dict[str, np.ndarray]]:
        # Encodes the names of the slots that are filled.
        encoded_slots = enc_context.transform(
            "slots", [[sv.name for sv in state.slotValues if sv.name in enc_context.classes_("slots")]]
        )
        return encoded_slots

    @staticmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Union[t.Sequence[int], t.Dict[str, t.Sequence[int]]]:
        return 1, enc_context.get_size("slots")


class UserDialogueTurnEncoder(TypeEncoder[UserDialogueTurn]):

    @staticmethod
    def encode(turn: UserDialogueTurn, enc_context: EncodingContext) -> t.Union[np.ndarray, t.Dict[str, np.ndarray]]:
        if turn.state is not None:
            encoded_state = DialogueStateEncoder.encode(turn.state, enc_context)
        else:
            encoded_state = DialogueStateEncoder.encode_null(enc_context)
        encoded_action = UserActionEncoder.encode(turn.userAction, enc_context)
        feature_vec = np.concatenate([encoded_state, encoded_action['feature_vec']], axis=-1)
        return {
            'feature_vec': feature_vec,
            'utterance_ids': encoded_action['utterance_ids'],
            'utterance_mask': encoded_action['utterance_mask'],
        }

    @staticmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Union[t.Sequence[int], t.Dict[str, t.Sequence[int]]]:
        feature_vec_shape = (
            1, DialogueStateEncoder.get_encoding_shape(enc_context)[1]
            + UserActionEncoder.get_encoding_shape(enc_context)['feature_vec'][1]
        )
        return {
            'feature_vec': feature_vec_shape,
            'utterance_ids': (1, MAX_UTTERANCE_LEN),
            'utterance_mask': (1, MAX_UTTERANCE_LEN),
        }


class AgentDialogueTurnEncoder(TypeEncoder[AgentDialogueTurn]):

    @staticmethod
    def encode(turn: AgentDialogueTurn, enc_context: EncodingContext) -> t.Union[np.ndarray, t.Dict[str, np.ndarray]]:
        return AgentActionEncoder.encode(turn.agentAction, enc_context)

    @staticmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Union[t.Sequence[int], t.Dict[str, t.Sequence[int]]]:
        return 1, AgentActionEncoder.get_encoding_shape(enc_context)[1]
