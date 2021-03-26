from unittest import TestCase

from bavard_ml_common.types.conversations.dialogue_turns import UserDialogueTurn, AgentDialogueTurn

from bavard.dialogue_policy.data.encode.dialogue_turns import UserDialogueTurnEncoder, AgentDialogueTurnEncoder
from test.functional.dialogue_policy.utils import (
    DummyContext, check_user_dialogue_turn_feature_vec, check_agent_action_feature_vec
)


class TestDialogueTurns(TestCase):

    def setUp(self):
        self.ctx = DummyContext()

    def test_user_dialogue_turn_encoding(self):
        turn = UserDialogueTurn.parse_obj({
            "actor": "USER",
            "userAction": {
                "intent": "intent2",
                "utterance": "This too is an utterance.",
                "tags": [{"tagType": "tagtype1", "value": "value1"}],
                "type": "UTTERANCE_ACTION"
            },
            "state": {
                "slotValues": [
                    {"name": "slot3", "value": "foo"},
                    {"name": "slot1", "value": "bar"}
                ]
            }
        })
        encoding = UserDialogueTurnEncoder.encode(turn, self.ctx.enc_context)

        check_user_dialogue_turn_feature_vec(
            encoding["feature_vec"], self.ctx, slots=("slot1", "slot3"), intent="intent2", tag_types=("tagtype1",)
        )

    def test_agent_dialogue_turn_encoding(self):
        turn = AgentDialogueTurn.parse_obj({
            "actor": "AGENT",
            "agentAction": {
                "name": "action3",
                "utterance": "This too is an utterance.",
                "type": "UTTERANCE_ACTION"
            },
            "state": {
                "slotValues": [
                    {"name": "slot2", "value": "foo"},
                    {"name": "slot3", "value": "bar"}
                ]
            }
        })
        encoding = AgentDialogueTurnEncoder.encode(turn, self.ctx.enc_context)
        check_agent_action_feature_vec(encoding, self.ctx, action="action3")

    def test_can_handle_no_state(self):
        user_turn = UserDialogueTurn.parse_obj(
            {
                "userAction": {
                    "type": "UTTERANCE_ACTION",
                    "utterance": "Ok thank you, that's great to know. What are your prices like? Are they competitive?",
                    "intent": "ask_pricing",
                    "tags": []
                },
                "actor": "USER"
            }
        )
        self.assertEqual(user_turn.state, None)

    def test_can_handle_no_intent(self):
        user_turn = UserDialogueTurn.parse_obj({
            "actor": "USER",
            "userAction": {
                "type": "UTTERANCE_ACTION",
                "utterance": "What are your prices like?",
                "tags": []
            },
            "timestamp": 1607471164994
        })
        self.assertEqual(user_turn.userAction.intent, None)

    def test_doesnt_error_on_unseen_fields(self):
        turn = UserDialogueTurn.parse_obj({
            "actor": "USER",
            "userAction": {
                "intent": "unseen_intent",
                "utterance": "This is an utterance.",
                "tags": [
                    {"tagType": "unseen_tag", "value": "value1"},
                    {"tagType": "tagtype1", "value": "value1"}
                ],
                "type": "UTTERANCE_ACTION"
            },
            "state": {
                "slotValues": [
                    {"name": "unseen_slot", "value": "foo"},
                    {"name": "slot1", "value": "bar"}
                ]
            }
        })
        encoding = UserDialogueTurnEncoder.encode(turn, self.ctx.enc_context)

        check_user_dialogue_turn_feature_vec(
            encoding["feature_vec"], self.ctx, slots=("slot1",), intent=None, tag_types=("tagtype1",)
        )
