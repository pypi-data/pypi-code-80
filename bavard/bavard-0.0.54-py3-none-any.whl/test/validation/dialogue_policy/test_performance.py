from unittest import TestCase

from bavard_ml_common.types.agent import AgentExport

from bavard.dialogue_policy.models import Classifier


class TestPerformance(TestCase):
    def setUp(self):
        self.data = AgentExport.parse_file("test/data/agents/bavard.json").config.to_conversation_dataset()

    def test_model_performance(self):
        # The DP model should be able to at *least* memorize and recreate a small
        # set of training conversations when in predict/inference mode.
        model = Classifier()  # default hyperparams, which is what our docker containers use
        model.fit(self.data)
        train_performance = model.score(self.data)
        print("train_performance:", train_performance)
        self.assertGreaterEqual(train_performance["f1_macro"], .95)
