"""
ProtBert
~~~

"""

from deepprot.feat.featurizer import EmbeddingFeaturizer


class ProtBert(EmbeddingFeaturizer):

    """
    References
    ----

    """

    def __init__(self, pretrain_data: str = "uniref"):
        super().__init__()

        id_map = {"uniref": "Rostlab/prot_bert", "bfd": "Rostlab/prot_bert_bfd"}

        (
            self._tokenizer,
            self._model,
            self._extraction_pipeline,
        ) = self._init_extraction_pipeline(id_map[pretrain_data])
