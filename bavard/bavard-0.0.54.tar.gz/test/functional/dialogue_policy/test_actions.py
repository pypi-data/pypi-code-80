from unittest import TestCase

from bavard_ml_common.types.conversations.actions import UserAction, AgentAction, TagValue

from bavard.dialogue_policy.data.encode.actions import UserActionEncoder, AgentActionEncoder
from test.functional.dialogue_policy.utils import DummyContext, check_agent_action_feature_vec


class TestActions(TestCase):

    def setUp(self):
        self.ctx = DummyContext()

    def test_user_action_encoding(self):
        user_action = UserAction(
            intent="intent1",
            utterance="I am uttering.",
            tags=[TagValue(tagType="tagtype1", value="tagvalue"), TagValue(tagType="tagtype3", value="othervalue")],
            type="UTTERANCE_ACTION"
        )
        encoding = UserActionEncoder.encode(user_action, self.ctx.enc_context)
        # Shape should be correct
        self.assertEqual(encoding['feature_vec'].shape,
                         (1, len(self.ctx.intents)
                          + len(self.ctx.tag_types)))
        # Content should be correct
        enc_intent = encoding["feature_vec"][:, :len(self.ctx.intents)]
        self.assertEqual(self.ctx.enc_context.inverse_transform("intent", enc_intent)[0], "intent1")
        tags_enc = encoding["feature_vec"][:, -len(self.ctx.tag_types):]
        self.assertEqual(self.ctx.enc_context.inverse_transform("tags", tags_enc)[0], ("tagtype1", "tagtype3"))

    def test_agent_action_encoding(self):
        agent_action = AgentAction(name="action2", utterance="I am uttering also.", type="UTTERANCE_ACTION")
        encoding = AgentActionEncoder.encode(agent_action, self.ctx.enc_context)
        check_agent_action_feature_vec(encoding, self.ctx, action="action2")
