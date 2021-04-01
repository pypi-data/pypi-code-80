"""
Kibana Logger.
"""

import json
import socket
import logging
from io import StringIO
from warnings import warn
from traceback import extract_stack

from gmpyinfr_log.log.base import BaseLogger

class KibanaLogger(BaseLogger):
    """
    Implementa um logger baseado no Kibana.
    """

    def __init__(self, filepath, process_name, **kwargs):
        """
        Construtor.

        Params:
            - filepath : str indicando o local do arquivo de configuração
            - process_name : str exibe a informação do nome do processo
            - Recebe os parâmetros de um logging.basicConfig. Confira mais detalhes
            em https://docs.python.org/3/library/logging.html#logging.basicConfig.
        """

        if not filepath:
            raise ValueError("Um arquivo de configuração válido deve ser especificado "
                             "para um logger do tipo Kibana")

        super().__init__(filepath, **kwargs)
        try:
            self.server = self.conf['server']
            self.port = self.conf['port']
        except KeyError:
            raise ValueError("Aparentemente seu arquivo de configuração não contém os "
                             "campos 'server' e 'port' necessários para o funcionamento "
                             "desta classe")

        self.process_name = process_name

        self.stream = StringIO()
        self.bytes_read = 0  # bytes lidos (controle do seek)
        self.hs = logging.StreamHandler(self.stream)

        self.logger.addHandler(self.hs)
        self.logger.setLevel(logging.DEBUG)

        # mensagens que não foram enviadas para o servidor do kibana
        self.unsent_msgs = []

    def __read_last_message(self):
        """
        Faz a leitura da stream e trunca após.
        Ao final, retorna o lido.
        """

        self.stream.seek(self.bytes_read)  # aponta para o último ponto da leitura
        _str = self.stream.read(-1)  # lê até o final da stream
        self.bytes_read = self.stream.tell()  # atualiza o último ponto de leitura
        return _str

    def __deal_with_failed_sock(self, msg, level):
        """
        Executa trecho de código para informação no logger de que o socket falhou.
        """

        # bypass no logger para informar que a conexão socket falhou
        strace = '\n'.join(extract_stack().format())
        self.logger.warning(
            "Não foi possível enviar mensagem ao logstash: '{}'".format(strace))
        # pula o warning acima, mas mantém no buffer
        _msg = self.__read_last_message()
        # armazena mensagem e nível
        self.unsent_msgs.append((msg, level))

    def log(self, **kwargs):
        """
        Envia mensagem de log ao logstash.

        Lê o stream, 
        """

        msg = self.__read_last_message()
        level = kwargs['level'] if 'level' in kwargs else 'INFO'
        
        if not msg:  # não há mensagem a ser enviada
            return True  # informa que o método executou como esperado neste caso

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.server, self.port))
        except:
            self.__deal_with_failed_sock(msg, level)
            sock.close()  # só pra ter certeza...
            return False  # indica que o método não executou como esperado

        body = {
            'serviceName': self.process_name,
            'message': msg,
            'level': level,
            'type': 'ERROR' if level.lower() in self.error_levels else 'SUCCESS'
        }

        try:
            sock.send(str(json.dumps(body)).enconde('utf-8'))
        except:
            self.__deal_with_failed_sock(msg, level)
            return False
        finally:
            sock.close()

        return True
