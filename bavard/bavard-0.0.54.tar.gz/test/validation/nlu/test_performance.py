from unittest import TestCase

from bavard_ml_common.types.agent import AgentExport

from bavard.nlu.model import NLUModel


class TestPerformance(TestCase):
    def setUp(self):
        self.nlu_dataset = AgentExport.parse_file("test/data/agents/bavard.json").config.to_nlu_dataset()

    def test_model_performance(self):
        # A model fully trained on a dataset representative of what
        # we might see in production should give good generalizeable
        # predictive performance.
        model = NLUModel(auto=True)
        train_performance, test_performance = model.evaluate(self.nlu_dataset, nfolds=3)
        print("train_performance:", train_performance)
        print("test_performance:", test_performance)
        self.assertGreaterEqual(train_performance["intent_acc"], .9)
        self.assertGreaterEqual(test_performance["intent_acc"], .60)
