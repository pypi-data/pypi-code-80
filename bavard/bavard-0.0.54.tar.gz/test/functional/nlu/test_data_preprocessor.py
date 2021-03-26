from unittest import TestCase

import numpy as np
from bavard_ml_common.types.agent import AgentExport

from bavard.nlu.data.preprocessor import NLUDataPreprocessor


class TestDataPreprocessor(TestCase):
    def setUp(self):
        super().setUp()
        self.max_seq_len = 120
        self.nlu_dataset = AgentExport.parse_file("test/data/agents/test-agent.json").config.to_nlu_dataset()
        self.lm_name = "distilbert-base-multilingual-cased"
        self.preprocessor = NLUDataPreprocessor(max_seq_len=self.max_seq_len, lm_name=self.lm_name)
        self.preprocessor.fit(self.nlu_dataset)
        self.n_examples = len(self.nlu_dataset)
        self.X, self.y = self.preprocessor.transform(self.nlu_dataset)

    def test_tag_encoding(self) -> None:
        encoded_example_tag_one_hots = self.y["tags"][1]
        encoded_example_tags = self.preprocessor.tag_encoder.inverse_transform(
            np.argmax(encoded_example_tag_one_hots, axis=-1)
        )

        example_tokens = self.preprocessor.tokenizer.tokenize(self.nlu_dataset[1].text, add_special_tokens=True)
        padding = encoded_example_tags[len(example_tokens):]

        # Padding should be all "O" tokens.
        self.assertTrue(np.all(padding == "O"))

        encoded_example_tags = encoded_example_tags[:len(example_tokens)]

        # Check that the tags were identified and aligned correctly.
        self.assertTrue(
            np.all(
                encoded_example_tags == [
                    'O', 'O', 'O', 'O',
                    'B-flight_stop', 'I-flight_stop',
                    'O', 'O',
                    'B-fromloc.city_name', 'I-fromloc.city_name', 'I-fromloc.city_name',
                    'O',
                    'B-toloc.city_name', 'I-toloc.city_name', 'I-toloc.city_name', 'I-toloc.city_name',
                    'O'
                ]
            )
        )

    def test_tag_decoding(self):
        utterances = [ex.text for ex in self.nlu_dataset]
        encoding = self.preprocessor.transform_utterances(utterances)
        # Pretend the ground truth labels are predictions.
        raw_tag_predictions = self.y["tags"]
        # Say the starting [CLS] token is associated with a tag, to ensure the model can successfully filter
        # out special token tags.
        city_name_label_i = self.preprocessor.tag_encoder.transform(["B-fromloc.city_name"])[0]
        raw_tag_predictions[:, 0, city_name_label_i] = 1
        tags = self.preprocessor.decode_tags(raw_tag_predictions, encoding, utterances)

        # Since we used the ground truth labels as the predictions, the decoded predicted tags should
        # be the exact same as the tags in our NLU training data.
        for utterance_tags, example in zip(tags, self.nlu_dataset):
            decoded_tag_set = {f"{tag.tagType}_{tag.start}_{tag.end}" for tag in utterance_tags}
            example_tag_set = {f"{tag.tagType}_{tag.start}_{tag.end}" for tag in example.tags}
            self.assertSetEqual(decoded_tag_set, example_tag_set)

        # NLU data doesn't have the actual tag values (just the spans). Check one to make sure its correct.
        self.assertSetEqual({tag.value for tag in tags[1]}, {"nonstop", "kansas city", "st. paul"})

    def test_transform(self) -> None:
        # Check that the examples were encoded into ndarrays of the correct shape.
        expected_x_shape = {
            "input_ids": (self.n_examples, self.max_seq_len,),
            "input_mask": (self.n_examples, self.max_seq_len,)
        }
        expected_y_shape = {
            "intent": (self.n_examples, len(self.preprocessor.intents_encoder.classes_),),
            "tags": (self.n_examples, self.max_seq_len, len(self.preprocessor.tag_encoder.classes_)),
        }
        for key, shape in expected_x_shape.items():
            self.assertEqual(self.X[key].shape, shape)
        for key, shape in expected_y_shape.items():
            self.assertEqual(self.y[key].shape, shape)
