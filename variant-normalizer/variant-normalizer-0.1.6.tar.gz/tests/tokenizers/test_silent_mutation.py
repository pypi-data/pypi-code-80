"""A module for testing Silent Mutation tokenization."""
import unittest
from variant.tokenizers import SilentMutation
from .tokenizer_base import TokenizerBase
from variant.tokenizers.caches import AminoAcidCache


class TestSilentMutationTokenizer(TokenizerBase, unittest.TestCase):
    """A class for testing Silent Mutation Tokenization."""

    def tokenizer_instance(self):
        """Return Silent Mutation instance."""
        return SilentMutation(AminoAcidCache())

    def token_type(self):
        """Return Silent Mutation token type."""
        return 'SilentMutation'

    def fixture_name(self):
        """Return the fixture name for Silent Mutation."""
        return 'silent_mutation'
