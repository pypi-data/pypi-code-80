import typing as t

import numpy as np
from bavard_ml_common.types.conversations.actions import Actor, AgentAction
from bavard_ml_common.types.conversations.conversation import Conversation
from bavard_ml_common.types.conversations.dialogue_turns import DialogueTurn, UserDialogueTurn, AgentDialogueTurn

from bavard.dialogue_policy.constants import MAX_UTTERANCE_LEN
from bavard.dialogue_policy.data.encode.actions import AgentActionEncoder
from bavard.dialogue_policy.data.encode.dialogue_turns import UserDialogueTurnEncoder, AgentDialogueTurnEncoder
from bavard.dialogue_policy.data.utils import EncodingContext, TypeEncoder
from bavard.dialogue_policy.data.utils import concat_ndarray_dicts


class ConversationEncoder(TypeEncoder[Conversation]):

    @staticmethod
    def num_agent_turns(conv: Conversation) -> int:
        return sum(1 for turn in conv.turns if turn.actor == Actor.AGENT)

    @staticmethod
    def is_last_turn_user(conv: Conversation) -> bool:
        return False if len(conv.turns) == 0 else conv.turns[-1].actor == Actor.USER

    @staticmethod
    def encode(conv: Conversation, enc_context: EncodingContext) -> t.Union[np.ndarray, t.Dict[str, np.ndarray]]:
        """
        Encodes the conversation into a 2D matrix, wich includes binarized encodings
        of the user and agent actions taken at each turn. Axis 0 is the time dimension;
        one row for each agent action taken. Also encodes a Y matrix; a one hot representation
        of the agent action taken at each timestep. The whole matrix can be treated as a training
        example for a sequence-based neural network, with each row being a time step in the
        sequence. Segments of the conversation that were with a human agent are excluded.
        """

        last_user_turn: t.Optional[UserDialogueTurn] = None
        last_agent_turn: t.Optional[AgentDialogueTurn] = None

        def encode_last_user_turn() -> t.Dict[str, np.ndarray]:
            if last_user_turn is not None:
                return UserDialogueTurnEncoder.encode(last_user_turn, enc_context)
            else:
                return UserDialogueTurnEncoder.encode_null(enc_context)

        def encode_last_agent_turn() -> np.ndarray:
            if last_agent_turn:
                return AgentDialogueTurnEncoder.encode(last_agent_turn, enc_context)
            else:
                return AgentDialogueTurnEncoder.encode_null(enc_context)

        def encode_agent_output_action(action: AgentAction) -> int:
            return AgentActionEncoder.encode_index(action, enc_context)

        encoded_turns: t.List[t.Dict[str, np.ndarray]] = []

        def get_encoded_turn(next_turn: t.Optional[DialogueTurn]):
            user_turn_features = encode_last_user_turn()
            agent_feature_vec = encode_last_agent_turn()

            feature_vec = np.concatenate([
                user_turn_features['feature_vec'],
                agent_feature_vec
            ], axis=-1)

            action = None
            if next_turn and next_turn.actor == Actor.AGENT:
                # next action
                action = np.expand_dims(encode_agent_output_action(next_turn.agentAction), axis=-1)

            return {
                'feature_vec': feature_vec,
                'utterance_ids': user_turn_features['utterance_ids'],
                'utterance_mask': user_turn_features['utterance_mask'],
                'action': action
            }

        for i, turn in enumerate(conv.turns):
            if turn.actor == Actor.USER:
                last_user_turn = turn

                # If conversation ends with a user turn.
                if i == len(conv.turns) - 1:
                    encoded_turns.append(get_encoded_turn(turn))
            elif turn.actor == Actor.AGENT:
                if turn.agentAction.name not in enc_context.classes_("action"):
                    # The action encoder has not seen this turn's action before, so filter this turn out,
                    # because the action encoder won't know how to encode it, and the model won't know
                    # how to predict it.
                    continue
                encoded_turns.append(get_encoded_turn(turn))
                last_agent_turn = turn

        if len(encoded_turns) > 0:
            return concat_ndarray_dicts(encoded_turns)
        else:
            result = get_encoded_turn(None)
            result['action'] = np.zeros(0)
            return result

    @staticmethod
    def get_encoding_shape(enc_context: EncodingContext) -> t.Union[t.Sequence[int], t.Dict[str, t.Sequence[int]]]:
        """Returns the encoding dimensionality of one row of `X`.
        """
        n_features = (
            AgentDialogueTurnEncoder.get_encoding_shape(enc_context)[1]
            + UserDialogueTurnEncoder.get_encoding_shape(enc_context)['feature_vec'][1]
        )
        return {
            'feature_vec': (1, n_features),
            'utterance_ids': (1, MAX_UTTERANCE_LEN),
            'utterance_mask': (1, MAX_UTTERANCE_LEN),
            'action': (1, enc_context.get_size('action'))
        }
