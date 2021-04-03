import abc


class DataSource(abc.ABC):
    @abc.abstractmethod
    def get_gene_matrix(self, gene_set):
        pass

    @abc.abstractmethod
    def get_word_matrix(self, words=None):
        pass
