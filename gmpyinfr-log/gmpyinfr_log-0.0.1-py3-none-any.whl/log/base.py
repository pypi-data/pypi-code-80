"""
Implementação básica do log.
"""

import logging
from warnings import warn

from gmpyinfr_log.utils import read_conf_file
from gmpyinfr_log.dsgpttn.singleton import SingletonMeta

class BaseLogger(metaclass=SingletonMeta):
    """
    Implementa um logger que serve de base para os demais.

    Se aproveita do logging implementado para o python e é um singleton,
    permitindo que o desenvolvedor utilize várias vezes o mesmo objeto sem
    a necessidade de transportar a referência através do código.
    """

    def __init__(self, filepath=None, **kwargs):
        """
        Construtor.

        Params:
            - filepath : str indicando o local do arquivo de configuração
            - Recebe os parâmetros de um logging.basicConfig. Confira mais detalhes
            em https://docs.python.org/3/library/logging.html#logging.basicConfig.
        """

        self.conf = read_conf_file(filepath)

        # se não for manualmente especificado, passa o filename do arquivo de
        # configuração
        f = 'filename'
        if f not in kwargs or kwargs[f] is None:
            try:
                kwargs[f] = self.conf['file']
            except KeyError:  # não foi especificado arquivo
                kwargs[f] = None

        if not kwargs[f]:
            warn("Não foi informado arquivo de log. É recomendado que um arquivo"
                 " de log seja utilizado")

        # se não for manualmente especificado, passa o format padrão
        f = 'format'
        if f not in kwargs or kwargs[f] is None:
            kwargs[f] = ('%(asctime)s [%(levelname)s] - %(message)s')

        logging.basicConfig(**kwargs)
        self.logger = logging.getLogger("base")

        # redireciona os métodos do log
        self.harmless_levels = ['debug', 'info', 'warning']
        self.error_levels = ['error', 'critical', 'exception']
        self.__levels = self.harmless_levels + self.error_levels
        for level in self.__levels:
            self.__create_log_method_for_level(level)

    def log(self, **kwargs):
        """
        Método log que deve ser implementado pelas Child Classes para ser invocado
        após da utilização do logging python.
        """

        pass

    def __create_log_method_for_level(self, level):
        """Faz a criação dos métodos de log para esta classe."""

        def logml(msg, *args, **kwargs):
            func = getattr(self.logger, level)
            rtn = func(msg, *args, **kwargs)
            self.log(msg=msg, level=level.upper(), **kwargs)
            return rtn

        setattr(self, level, logml)
