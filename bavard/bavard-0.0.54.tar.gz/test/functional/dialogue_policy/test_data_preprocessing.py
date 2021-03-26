from unittest import TestCase

import numpy as np
from bavard_ml_common.types.agent import AgentExport
from bavard_ml_common.types.conversations.conversation import Conversation

from bavard.dialogue_policy.data.encode.conversation import ConversationEncoder
from bavard.dialogue_policy.data.preprocessed_data import PreprocessedTrainingData
from test.utils import load_json_file


class TestDataPreprocessing(TestCase):
    def setUp(self) -> None:
        self.convs = AgentExport.parse_file(
            "test/data/agents/mwoz2_2_hotel_dialogs.json"
        ).config.to_conversation_dataset()
        self.bavard_convs = AgentExport.parse_file("test/data/agents/bavard.json").config.to_conversation_dataset()
        self.conv_last_turn_user = load_json_file("test/data/conversations/last-turn-user.json")
        self.conv_single_turn = load_json_file("test/data/conversations/length-one.json")
        self.conv_missing_fields = load_json_file("test/data/conversations/missing-fields.json")

    def test_preprocessor(self) -> None:
        preprocessor = PreprocessedTrainingData(self.convs)

        # Should encode actions (y) correctly.
        actions = np.array([conv.turns[-1].agentAction.name for conv in preprocessor.conversations])
        encoded_actions = preprocessor.encoded_convs["action"]
        decoded_actions = preprocessor.enc_context.inverse_transform("action_index", encoded_actions)
        self.assertTrue((actions == decoded_actions).all())

        # Should encode X properly.
        for i, conv in enumerate(preprocessor.conversations):
            X = preprocessor.encoded_convs['feature_vec'][i][-conv.num_agent_turns:]  # account for padding
            # X should have one row for every agent turn.
            self.assertEqual(X.shape[0], conv.num_agent_turns)
            # X should have correct number of columns
            self.assertEqual(
                X.shape[1], ConversationEncoder.get_encoding_shape(preprocessor.enc_context)['feature_vec'][1]
            )

    def test_preprocessor_inference_time(self) -> None:
        # Should be an extra row during inference time when a user action was last.
        # (The extra row is for that last user action.)
        preprocessor = PreprocessedTrainingData(self.convs)

        encoded_conv = preprocessor.encode_conversations([Conversation.parse_obj(self.conv_last_turn_user)])
        self.assertEqual(
            encoded_conv['feature_vec'].shape[-1],
            ConversationEncoder.get_encoding_shape(preprocessor.enc_context)['feature_vec'][-1]
        )

        # Should be able to handle single turn conversations.
        X = preprocessor.encode_conversations([Conversation.parse_obj(self.conv_single_turn)])
        self.assertEqual(X['feature_vec'].shape[0], 1)

        # Should be able to handle zero length conversations.
        X = preprocessor.encode_conversations([Conversation(turns=[])])
        self.assertEqual(X['feature_vec'].shape[0], 1)
        self.assertEqual(np.count_nonzero(X['feature_vec']), 0)

        # Should be able to handle conversations longer than any seen in the training data.
        conv = Conversation.parse_obj(self.conv_last_turn_user)
        while len(conv.turns) < preprocessor.max_len + 10:
            conv.turns.append(conv.turns[0])
        X = preprocessor.encode_conversations([conv])
        self.assertEqual(X['feature_vec'].shape[1], preprocessor.max_len)

    def test_can_handle_optional_fields(self) -> None:
        preprocessor = PreprocessedTrainingData(self.convs)
        # Should be able to encode optional fields like intents and utterances without choking.
        preprocessor.encode_conversations([Conversation.parse_obj(self.conv_missing_fields)])
