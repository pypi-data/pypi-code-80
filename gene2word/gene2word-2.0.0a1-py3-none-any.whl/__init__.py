__version__ = "2.0.0a1"

import os, sys, appdirs
import abc, functools, numpy as np
from ._source import DataSource
from ._sqlite import SqliteSource
from .exceptions import *


_dirs = appdirs.AppDirs("gene2word", "ReceptorBiologyLab")


class Translation(dict):
    def __init__(self, genes, words, cosines):
        super().__init__(zip(words, cosines))
        self._genes = genes.copy()
        self._words = words
        self._cos = cosines

    def __str__(self):
        cname = self.__class__.__name__
        return f"<{cname} ({len(self._genes)} genes) at {hex(id(self))}>"

    def take(self, n):
        return self.__class__(self._genes, self._words[:n], self._cos[:n])

    def take_similar(self, similarity):
        mask = self._cos >= similarity
        return self.__class__(self._genes, self._words[mask], self._cos[mask])

    def p_values(self):
        import scipy.stats

        return scipy.stats.norm.sf(np.abs(self.z_values())) * 2

    def z_values(self):
        import scipy.stats

        return scipy.stats.zscore(self._cos)


class Translator(abc.ABC):
    def __init__(self, data_source):
        self.data_source = data_source

    def translate(self, gene_set):
        from sklearn.metrics.pairwise import cosine_similarity
        V = self.data_source.get_gene_matrix(gene_set).sum(axis=0)
        U = self.data_source.get_word_matrix()
        cos = cosine_similarity(V.reshape(1, -1), U)[0]
        similars = np.argsort(-cos)
        cos = cos[similars]
        words = self.data_source.get_all_words()[similars]
        return Translation(gene_set, words, cos)


@functools.cache
def get_translator(db=None):
    if db is None:
        db = os.path.join(_dirs.user_cache_dir, "g2w.db")
        if not os.path.exists(db):
            _unpack_data(db)
    if not os.path.exists(db):
        raise MissingSourceError("Could not open source file '%source%'.", db)
    source = SqliteSource(db)
    return Translator(source)


def translate(gene_set):
    return get_translator().translate(gene_set)


def _unpack_data(path):
    import warnings, py7zr

    data_archive = os.path.join(os.path.dirname(__file__), "data.7z")
    if not os.path.exists(data_archive):
        raise IOError(f"Package data missing! Could not find '{data_archive}'")

    warnings.warn("First time use: unpacking database, this can take a while...", DeploymentWarning)
    sys.stderr.flush()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with py7zr.SevenZipFile(data_archive, 'r') as archive:
        archive.extractall(path=os.path.dirname(path))
