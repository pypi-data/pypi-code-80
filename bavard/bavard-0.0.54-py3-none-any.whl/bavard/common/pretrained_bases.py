from abc import ABC, abstractmethod
import typing as t

from transformers import TFDistilBertModel, TFBertModel, TFXLMRobertaModel
import tensorflow as tf


class TFPreTrainedTokenLM(ABC):
    """
    Provides a common interface for using a few Tensorflow HuggingFace language models, since the way
    they are called can differ from model to model.
    """

    def __init__(self, trainable: bool):
        """
        Parameters
        ----------
        trainable : bool
            Should be used to set whether the base model should be fine-tuned.
        """
        self.trainable = trainable

    @abstractmethod
    def __call__(self, input_ids: tf.Tensor, attention_mask: tf.Tensor) -> t.Tuple[tf.Tensor, tf.Tensor]:
        """Should return a tuple of two tensors: the sequence level embedding then the per-token embeddings.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """The name that can be used to load the model in the HuggingFace library.
        """
        pass


class TFDistilMBert(TFPreTrainedTokenLM):
    name = "distilbert-base-multilingual-cased"

    def __init__(self, trainable: bool):
        super().__init__(trainable)
        self._distilbert = TFDistilBertModel.from_pretrained(self.name).distilbert
        self._distilbert.trainable = trainable

    def __call__(self, input_ids: tf.Tensor, attention_mask: tf.Tensor) -> t.Tuple[tf.Tensor, tf.Tensor]:
        token_embeddings = self._distilbert(input_ids, attention_mask)[0]
        pooled_embedding = token_embeddings[:, 0]  # the embedding for the [CLS] token
        return pooled_embedding, token_embeddings


class TFMBert(TFPreTrainedTokenLM):
    name = "bert-base-multilingual-cased"

    def __init__(self, trainable: bool):
        super().__init__(trainable)
        self._bert = TFBertModel.from_pretrained(self.name).bert
        self._bert.trainable = self.trainable

    def __call__(self, input_ids: tf.Tensor, attention_mask: tf.Tensor) -> t.Tuple[tf.Tensor, tf.Tensor]:
        token_embeddings = self._bert(input_ids, attention_mask)[0]
        pooled_embedding = token_embeddings[:, 0]  # the embedding for the [CLS] token
        return pooled_embedding, token_embeddings


class TFXLMRoberta(TFPreTrainedTokenLM):
    name = "jplu/tf-xlm-roberta-base"

    def __init__(self, trainable: bool):
        super().__init__(trainable)
        self._roberta = TFXLMRobertaModel.from_pretrained(self.name)
        self._roberta.trainable = self.trainable

    def __call__(self, input_ids: tf.Tensor, attention_mask: tf.Tensor) -> t.Tuple[tf.Tensor, tf.Tensor]:
        token_embeddings = self._roberta(input_ids, attention_mask)[0]
        pooled_embedding = token_embeddings[:, 0]  # the embedding for the [CLS] token
        return pooled_embedding, token_embeddings


pretrained_bases: t.Dict[str, t.Type[TFPreTrainedTokenLM]] = {
    cls.name: cls for cls in [TFDistilMBert, TFMBert, TFXLMRoberta]
}
