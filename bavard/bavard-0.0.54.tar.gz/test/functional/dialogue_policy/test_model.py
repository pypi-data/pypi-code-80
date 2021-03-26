from unittest import TestCase
import typing as t

from bavard_ml_common.types.agent import AgentExport
from bavard_ml_common.types.conversations.conversation import Conversation

from bavard.dialogue_policy.models import Classifier


class TestModel(TestCase):

    def setUp(self) -> None:
        self.convs = AgentExport.parse_file("test/data/agents/bavard.json").config.to_conversation_dataset()

    def test_can_fit_and_predict(self) -> None:
        convs, _ = self.convs.make_validation_pairs()

        # Should be able to fit
        model = Classifier(epochs=1)
        model.fit(self.convs)
        # Predicted actions should be valid actions
        self._assert_can_predict(model, convs)

        # Model should be able to be serialized and deserialized and still work.
        model.to_dir("temp-model")
        loaded_model = Classifier.from_dir("temp-model", True)
        self._assert_can_predict(loaded_model, convs)

        # Model should be able to predict on a conversation of length 0.
        self._assert_can_predict(loaded_model, [Conversation(turns=[])])

    def _assert_can_predict(self, model: Classifier, convs: t.List[Conversation]):
        preds = model.predict(convs)
        self.assertEqual(len(preds), len(convs))
        for conv_preds in preds:
            # One prediction for each action.
            self.assertEqual(len(conv_preds), model._preprocessor.enc_context.get_size("action_index"))
            # Predicted actions should be valid actions
            for pred in conv_preds:
                self.assertIn(pred.value, model._preprocessor.enc_context.classes_("action_index"))
