# -*- coding: utf=8 -*-
import ast
from datetime import datetime, timedelta
import requests


class Autenticacao:
    instances = []

    def __init__(self):
        self.token = None
        self.data_hora_limite = None

    def set_token(self, result):
        self.token = result
        data_hora = datetime.now()
        self.data_hora_limite = data_hora + timedelta(minutes=100)
        self.instances.append(self)

    def get_token(self):
        """verifica se tem token e se ele está denro do prazo estipulado"""
        data_hora = datetime.now()
        if self.data_hora_limite > data_hora:
            return self.token
        return False

    def autentica(self, url, cert, client_id, client_secret):
        """Autenticacao de homologacao"""
        url +="/oauth/token?grant_type=client_credentials"

        payload = 'client_id={}&client_secret={}'.format(client_id, client_secret)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload, cert=cert)

        return response


def get_autenticacao_token(url, cert, client_id, client_secret):
    """Realiza a autenticação através da classe Autenticacao """
    autenticacoes = Autenticacao.instances
    """verifica se existe token válido em memória"""
    if autenticacoes and autenticacoes[0].get_token():
        '''o token sempre estará na posição zero'''
        result = autenticacoes[0].get_token()
        result = ast.literal_eval(result.text)
        return result
    else:
        """Cria um token válido no santander"""
        autenticacao_obj = Autenticacao()
        autenticacao = autenticacao_obj.autentica(url, cert, client_id, client_secret)

        if autenticacao.status_code == 200:
            result = ast.literal_eval(autenticacao.text)
            if 'access_token' in result:
                if autenticacoes:
                    '''atualiza o primeiro registro com um token válido'''
                    autenticacoes[0].set_token(autenticacao)
                else:
                    autenticacao_obj.set_token(autenticacao)
                return result
        """pode retornar erro interno devido a instabilidades do santander"""
        return {"status_code": 500, "mensagem": "Erro interno"}

