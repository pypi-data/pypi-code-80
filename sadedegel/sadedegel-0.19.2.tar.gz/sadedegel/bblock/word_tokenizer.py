import sys
import warnings
from abc import ABC, abstractmethod
from typing import List

from cached_property import cached_property
from rich.console import Console

from .util import normalize_tokenizer_name
from .vocabulary import Vocabulary
from .word_tokenizer_helper import word_tokenize, ICUTokenizerHelper
from ..about import __version__

console = Console()


class WordTokenizer(ABC):
    __instances = {}

    def __init__(self):
        self._vocabulary = None

    @abstractmethod
    def _tokenize(self, text: str) -> List[str]:
        pass

    @abstractmethod
    def convert_tokens_to_ids(self, tokens: List[str]) -> List[int]:
        pass

    def __call__(self, sentence: str) -> List[str]:
        return self._tokenize(str(sentence))

    @staticmethod
    def factory(tokenizer_name: str):
        normalized_name = normalize_tokenizer_name(tokenizer_name)
        if normalized_name not in WordTokenizer.__instances:
            if normalized_name == "bert":
                WordTokenizer.__instances[normalized_name] = BertTokenizer()
            elif normalized_name == "simple":
                warnings.warn(
                    ("Note that SimpleTokenizer is pretty new in sadedeGel. "
                     "If you experience any problems, open up a issue "
                     "(https://github.com/GlobalMaksimum/sadedegel/issues/new)"))
                WordTokenizer.__instances[normalized_name] = SimpleTokenizer()
            elif normalized_name == "icu":
                WordTokenizer.__instances[normalized_name] = ICUTokenizer()
            else:
                raise Exception(
                    (f"No word tokenizer type match with name {tokenizer_name}."
                     " Use one of 'bert-tokenizer', 'SimpleTokenizer', etc."))

        return WordTokenizer.__instances[normalized_name]


class BertTokenizer(WordTokenizer):
    __name__ = "BertTokenizer"

    def convert_tokens_to_ids(self, tokens: List[str]) -> List[int]:
        return self.tokenizer.convert_tokens_to_ids(tokens)

    def __init__(self):
        super(BertTokenizer, self).__init__()

        self.tokenizer = None

    def _tokenize(self, text: str) -> List[str]:
        if self.tokenizer is None:
            try:
                import torch
                from transformers import AutoTokenizer
            except ImportError:
                console.print(
                    ("Error in importing transformers module. "
                     "Ensure that you run 'pip install sadedegel[bert]' to use BERT features."))
                sys.exit(1)
            self.tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased")

        return self.tokenizer.tokenize(text)

    @cached_property
    def vocabulary(self):
        try:
            return Vocabulary("bert")
        except FileNotFoundError:
            console.print("[red]bert[/red] vocabulary file not found.")

            return None


class SimpleTokenizer(WordTokenizer):
    __name__ = "SimpleTokenizer"

    def __init__(self):
        super(SimpleTokenizer, self).__init__()
        self.tokenizer = word_tokenize

    def _tokenize(self, text: str) -> List[str]:
        return self.tokenizer(text)

    def convert_tokens_to_ids(self, ids: List[str]) -> List[int]:
        raise NotImplementedError("convert_tokens_to_ids is not implemented for SimpleTokenizer yet. Use BERTTokenizer")

    @cached_property
    def vocabulary(self):
        try:
            return Vocabulary("simple")
        except FileNotFoundError:
            console.print("[red]simple[/red] vocabulary file not found.")

            return None


class ICUTokenizer(WordTokenizer):
    __name__ = "ICUTokenizer"

    def __init__(self):
        super(ICUTokenizer, self).__init__()
        self.tokenizer = ICUTokenizerHelper()

    def _tokenize(self, text: str) -> List[str]:
        return self.tokenizer(text)

    def convert_tokens_to_ids(self, ids: List[str]) -> List[int]:
        raise NotImplementedError("convert_tokens_to_ids is not implemented for SimpleTokenizer yet. Use BERTTokenizer")

    @cached_property
    def vocabulary(self):
        try:
            return Vocabulary("icu")
        except FileNotFoundError:
            console.print("[red]icu[/red] vocabulary file not found.")

            return None


def get_default_word_tokenizer() -> WordTokenizer:
    if tuple(map(int, __version__.split('.'))) < (0, 17):
        warnings.warn(
            ("get_default_word_tokenizer is deprecated and will be removed by 0.17. "
             "Use `sadedegel config` to get default configuration. "
             "Use ~/.sadedegel/user.ini to update default tokenizer."),
            DeprecationWarning,
            stacklevel=2)
    else:
        raise Exception("Remove get_default_word_tokenizer before release.")

    return WordTokenizer.factory(BertTokenizer.__name__)
