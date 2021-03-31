"""
ProtAlbert
~~~

"""

from transformers import AlbertTokenizer, AutoModel, pipeline

from deepprot.feat.featurizer import EmbeddingFeaturizer


class ProtAlbert(EmbeddingFeaturizer):

    """
    References
    ----

    """

    def __init__(self, pretrain_data: str = "uniref"):
        super().__init__()

        data_map = {"uniref": "Rostlab/prot_albert"}

        self._tokenizer = AlbertTokenizer.from_pretrained(
            data_map[pretrain_data], do_lower_case=False
        )
        self._model = AutoModel.from_pretrained(data_map[pretrain_data])
        self._extraction_pipeline = pipeline(
            "feature-extraction", model=self._model, tokenizer=self._tokenizer
        )
