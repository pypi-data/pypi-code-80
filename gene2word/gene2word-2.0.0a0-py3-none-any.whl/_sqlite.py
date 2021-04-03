import peewee
import playhouse.sqlite_ext as sqlite
import numpy as np
import functools
from ._source import DataSource

db_proxy = peewee.DatabaseProxy()


class BaseModel(peewee.Model):
    class Meta:
        database = db_proxy


class Gene(BaseModel):
    gene = peewee.CharField(index=True, constraints=[peewee.SQL('COLLATE NOCASE')])
    vector = sqlite.JSONField()


class Word(BaseModel):
    word = sqlite.CharField(index=True, constraints=[peewee.SQL('COLLATE NOCASE')])
    vector = sqlite.JSONField()


class SqliteSource(DataSource):
    def __init__(self, file):
        self._db = sqlite.SqliteExtDatabase(file)
        db_proxy.initialize(self._db)
        self._db.create_tables([Gene, Word])

    def _fill_matrix(self, results):
        count = results.count()
        results = results.tuples().iterator()
        matrix = np.empty((count, self.vector_size))
        for i, (_, _, vector) in enumerate(results):
            matrix[i] = vector
        return matrix

    def get_gene_matrix(self, gene_set):
        results = Gene.select().where(Gene.gene << gene_set)
        return self._fill_matrix(results)

    def get_word_matrix(self, words=None):
        results = Word.select()
        if words is not  None:
            results = results.where(Word.word << words)
        elif hasattr(self, "_wm_cache"):
            return self._wm_cache
        matrix = self._fill_matrix(results)
        if words is None:
            self._wm_cache = matrix
        return matrix


    @functools.cached_property
    def vector_size(self):
        return len(Gene.select().first().vector)

    def import_genes(self, genes, vectors):
        Gene.insert_many(
            [{"gene": gene, "vector": vector} for gene, vector in zip(genes, vectors)]
        ).execute()

    def import_words(self, words, vectors):
        Word.insert_many(
            [{"word": word, "vector": vector} for word, vector in zip(words, vectors)]
        ).execute()
