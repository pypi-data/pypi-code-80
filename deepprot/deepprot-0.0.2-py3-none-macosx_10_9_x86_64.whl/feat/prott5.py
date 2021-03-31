"""
ProtT5
~~~

References
----

prottrans
https://arxiv.org/abs/2007.06225
t5
https://arxiv.org/abs/1910.10683
"""

from transformers import T5Tokenizer, AutoModel, pipeline

from deepprot.feat.featurizer import EmbeddingFeaturizer


class ProtT5(EmbeddingFeaturizer):

    """
    References
    ----

    """

    def __init__(self, pretrain_data: str = "uniref"):
        super().__init__()

        data_map = {
            "uniref": "Rostlab/prot_t5_xl_uniref50",
            "bfd": "Rostlab/prot_t5_xl_bfd",
        }

        T5Tokenizer.from_pretrained(data_map[pretrain_data], do_lower_case=False)

        self._model = AutoModel.from_pretrained(data_map[pretrain_data])
        self._extraction_pipeline = pipeline(
            "feature-extraction", model=self._model, tokenizer=self._tokenizer
        )
