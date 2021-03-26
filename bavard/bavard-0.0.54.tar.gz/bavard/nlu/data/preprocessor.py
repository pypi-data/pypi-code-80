import typing as t

from bavard_ml_common.types.nlu import NLUExampleDataset
from pydantic import BaseModel
from sklearn.preprocessing import LabelEncoder
from transformers import AutoTokenizer, BatchEncoding
import numpy as np
from bavard_ml_common.ml.utils import onehot

from bavard.nlu.pydantics import TagPrediction


class NLUDataPreprocessor:
    """
    Data preprocessing model that fits label encoders to the targets of an agent's
    NLU data and processes the raw NLU data into a tensorflow.data.Dataset instance
    ready for training.
    """

    def __init__(self, *, lm_name: str, max_seq_len: int) -> None:
        """
        Parameters
        ----------
        lm_name : str
            The name of the HuggingFace model the tokenizer will be loaded for.
        max_seq_len : int
            Each encoded utterance will be padded or truncated to this l
        """
        self._fitted = False
        self.lm_name = lm_name
        self.max_seq_len = max_seq_len
        self.intents = None
        self.tag_types = None
        self.intents_encoder = LabelEncoder()
        self.tag_encoder = LabelEncoder()
        self.n_tags = None
        self.n_intents = None
        self.tokenizer = AutoTokenizer.from_pretrained(self.lm_name)
        self.tag_reducer = IOBTagReducer()

    def fit(self, nlu_data: NLUExampleDataset) -> None:
        self.intents = nlu_data.unique_labels()
        self.tag_types = nlu_data.unique_tag_types()

        # intents encoder
        self.intents_encoder.fit(sorted(self.intents))

        # tags encoder
        tag_set = {"O"}
        for tag_type in sorted(self.tag_types):
            tag_set.add(f"B-{tag_type}")
            tag_set.add(f"I-{tag_type}")
        self.tag_encoder.fit(list(tag_set))

        # tag and intent sizes
        self.n_tags = len(tag_set)
        self.n_intents = len(self.intents)

        self._fitted = True

    def transform_utterances(self, utterances: t.List[str]) -> BatchEncoding:
        """Transform a batch of utterances with no labels.

        Returns
        encoding : BatchEncoding
            a `BatchEncoding` object having an `input_ids` attribute and an
            `attention_mask` attribute, each a numpy ndarray of shape
            `(len(utterances), self.max_seq_len)`.
        """
        assert self._fitted
        return self.tokenizer(
            utterances,
            add_special_tokens=True,
            padding="max_length",
            truncation=True,
            max_length=self.max_seq_len,
            return_tensors="np"
        )

    def transform(self, nlu_data: NLUExampleDataset) -> t.Tuple[t.Dict[str, np.ndarray], ...]:
        """Transform a whole training dataset of utterances and labels.
        """
        assert self._fitted

        encoding = self.transform_utterances([ex.text for ex in nlu_data])
        n = len(nlu_data)

        # Encode each token's tag.
        tag_labels = np.full((n, self.max_seq_len), self.tag_encoder.transform(["O"])[0])
        for ex_i, ex in enumerate(nlu_data):
            for tag in ex.tags:
                beginning_tag, inside_tag = self.tag_encoder.transform([f"B-{tag.tagType}", f"I-{tag.tagType}"])
                tag_start_token_i = encoding.char_to_token(ex_i, tag.start)
                # `tag.end` is the exclusive end of the tag. We want the inclusive end,
                # so we subtract 1.
                tag_end_token_i = encoding.char_to_token(ex_i, tag.end - 1)
                # Add the B-<tagtype> and I-<tagtype> tags to the appropriate token indices for this tag.
                tag_labels[ex_i, tag_start_token_i] = beginning_tag
                for token_i in range(tag_start_token_i + 1, tag_end_token_i + 1):
                    tag_labels[ex_i, token_i] = inside_tag

        # Encode the intents.
        intent_labels = self.intents_encoder.transform(nlu_data.labels())

        X = {
            "input_ids": encoding.input_ids,
            "input_mask": encoding.attention_mask
        }
        y = {
            "intent": onehot(intent_labels),
            "tags": onehot(tag_labels)
        }
        return X, y

    def decode_tags(
        self, raw_tag_predictions: np.ndarray, original_encoding: BatchEncoding, original_utterances: t.Sequence[str]
    ) -> t.List[t.List[TagPrediction]]:
        """
        Parameters
        ----------
        raw_tag_predictions : np.ndarray
            softmaxed ndarray of shape `(batch_size, self.max_seq_len, self.n_tags)`.
        original_encoding : BatchEncoding
            The original `BatchEncoding` object that was used as inputs to whatever model to create
            the raw tag predictions.
        original_utterances : sequence of str
            The original utterances that were passed to the encoder to create `original_encoding`.
            Should be a sequence of length `batch_size`.
        """
        tags = []
        tag_labels = np.argmax(raw_tag_predictions, axis=-1)
        for utterance_i, (utterance_tag_labels, utterance) in enumerate(zip(tag_labels, original_utterances)):

            # Filter out special tokens like padding tokens: we don't classify those.
            in_utterance_token_indices = np.argwhere(
                np.array(original_encoding.word_ids(utterance_i)) != None
            ).flatten()
            utterance_tag_labels = utterance_tag_labels[in_utterance_token_indices]

            # Group all adjacent token tags of the same type into entities.
            utterance_tags = []
            utterance_tag_tokens = self.tag_reducer.reduce_sequence(
                in_utterance_token_indices, self.tag_encoder.inverse_transform(utterance_tag_labels)
            )

            # Recover the text of each entity from the original utterance.
            for tag_tokens in utterance_tag_tokens:
                start_token = tag_tokens.token_indices[0]
                end_token = tag_tokens.token_indices[-1]
                tag_start = original_encoding.token_to_chars(utterance_i, start_token).start
                tag_end = original_encoding.token_to_chars(utterance_i, end_token).end
                utterance_tags.append(
                    TagPrediction(
                        tagType=tag_tokens.tag_type,
                        value=utterance[tag_start:tag_end],
                        start=tag_start,
                        end=tag_end
                    )
                )
            tags.append(utterance_tags)
        return tags


class TagTokens(BaseModel):
    tag_type: str
    token_indices: t.List[int]


class IOBTagReducer:
    """Processes a sequence of token tags into the NER entities found in the sequence.
    """

    def __init__(self):
        self._current_tag_tokens = []
        self._current_tag_type = None

    def reduce_sequence(self, token_indices: t.Sequence[int], tag_names: t.Sequence[str]) -> t.List[TagTokens]:
        """Given a sequence of IOB token tags and the NER entities found therein, group the tokens by entity.

        Parameters
        ----------
        token_indices : sequence of int
            The indexes of the tokens in the sequence. Each result entity will be associated with the indices
            of the tokens that make up that entity.
        tag_names : sequence of str
            The IOB tag name of each token identified in `token_indices`.
        """
        assert len(token_indices) == len(tag_names)
        processed_tags = []
        for token_i, tag_name in zip(token_indices, tag_names):
            finalized = self._ingest(token_i, tag_name)
            if finalized is not None:
                processed_tags.append(finalized)

        # Handle the case where there could be a tag at the very end of a sequence.
        finalized = self._finalize()
        if finalized is not None:
            processed_tags.append(finalized)

        return processed_tags

    def _ingest(self, token_i: int, tag_name: str) -> t.Optional[TagTokens]:
        if tag_name == "O":
            # This tag is "outside" our defined tag types.
            return self._finalize()

        if tag_name.startswith("B-"):
            # We've come to a whole new token, so the one we've been working on
            # has come to an end, so we'll return it.
            finalized_tag = self._finalize()
            self._handle_tag(token_i, tag_name)
            return finalized_tag

        if tag_name.startswith("I-"):
            self._handle_tag(token_i, tag_name)
            return None

        raise ValueError(f"tag name {tag_name} is not in IOB format")

    def _finalize(self) -> t.Optional[TagTokens]:
        if self._current_tag_type is None:
            # No token has been captured.
            return None
        # Capture the finished token.
        finalized_tag_tokens = self._current_tag_tokens
        finalized_tag_type = self._current_tag_type
        # Reset.
        self._current_tag_tokens = []
        self._current_tag_type = None
        return TagTokens(tag_type=finalized_tag_type, token_indices=finalized_tag_tokens)

    def _handle_tag(self, token_i: int, tag_name: str):
        # This token has a beginning or inside tag, so let's add it to the current tag.
        self._current_tag_tokens.append(token_i)
        self._current_tag_type = tag_name[2:]
