import os
import shutil
from unittest import TestCase
from pathlib import Path

from bavard_ml_common.types.agent import AgentExport

from bavard.nlu.model import NLUModel
from bavard.nlu.pydantics import NLUPredictions


class TestModel(TestCase):
    def setUp(self):
        super().setUp()
        self.model_save_dir = "test-model"
        self.max_model_size_in_gigabytes = 2
        # Translations of the same utterance
        self.prediction_inputs = {
            "eng": "how much is a flight from washington to boston",
            "chi": "从华盛顿飞往波士顿多少钱",
            "rus": "сколько стоит перелет из вашингтона в бостон",
            "spa": "¿Cuánto cuesta un vuelo de Washington a Boston?",
            "fre": "Combien est un vol de Washington à Boston",
        }
        self.nlu_dataset = AgentExport.parse_file("test/data/agents/test-agent.json").config.to_nlu_dataset()
        self.bavard_nlu_dataset = AgentExport.parse_file("test/data/agents/bavard.json").config.to_nlu_dataset()

    def tearDown(self) -> None:
        if os.path.exists(self.model_save_dir):
            shutil.rmtree(self.model_save_dir)

    def test_train_and_predict(self):
        # Check that model can build and train without failing.
        model = NLUModel(save_model_dir=self.model_save_dir)
        model.set_params(batch_size=1, epochs=1)
        model.train(self.nlu_dataset)

        # Check that the saved model is small enough
        saved_model_size = self._get_dir_size(self.model_save_dir, "GB")
        self.assertLessEqual(saved_model_size, self.max_model_size_in_gigabytes)

        # Check that model can handle multiple languages without breaking.
        self._assert_model_can_predict(model)

        # Check that the model can be successfully loaded
        loaded_model = NLUModel.from_dir(self.model_save_dir, delete=True)
        self._assert_model_can_predict(loaded_model)

    def test_evaluate(self):
        # Check that model can evaluate without failing.
        model = NLUModel()
        model.set_params(batch_size=4, epochs=1)
        model.evaluate(self.bavard_nlu_dataset, test_ratio=0.2)

    def _assert_model_can_predict(self, model: NLUModel) -> None:
        predictions = model.predict(list(self.prediction_inputs.values()))
        self._assert_predictions_are_valid(predictions)

    def _assert_predictions_are_valid(self, predictions: NLUPredictions) -> None:
        valid_intents = set(self.nlu_dataset.labels())
        valid_tag_types = set(tag.tagType for ex in self.nlu_dataset for tag in ex.tags)
        for prediction in predictions.predictions:
            self.assertIn(prediction.intent.value, valid_intents)
            for tag in prediction.tags:
                self.assertIn(tag.tagType, valid_tag_types)

    @staticmethod
    def _get_dir_size(path: str, units: str = "GB") -> int:
        """
        Gets the size of the directory at `path`.
        Source: https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
        """
        units_map = {"KB": 1e-3, "MB": 1e-6, "GB": 1e-9}
        path_obj = Path(path)
        total_bytes = sum(f.stat().st_size for f in path_obj.glob("**/*") if f.is_file())
        return int(total_bytes * units_map[units])
