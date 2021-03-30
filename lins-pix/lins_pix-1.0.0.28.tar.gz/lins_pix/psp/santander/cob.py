# python3 setup.py sdist upload -r testpypi
# pip install -i https://test.pypi.org/simple/ lins_pix==0.0.14
# requests~=2.25.1
# urllib3~=1.26.4
# PyJWT~=1.7.1
# websocket-client~=0.53.0


'''
Reúne endpoints destinados a lidar com gerenciamento de cobranças imediatas
'''
import requests

from ..santander.autenticacao import get_autenticacao_token


def checa_validade_dados(body):
    '''
        Verifica validade dos dados e caso positivo retorna os dados em um dicionario
    '''
    try:
        valor = body['valor']["original"]
        try:
            tipo_pessoa = "cnpj"
            doc_pessoa = body['devedor']["cnpj"]
        except:
            doc_pessoa = body['devedor']["cpf"]
            tipo_pessoa = "cpf"

        nome = body['devedor']["nome"]
        expiracao = body['calendario']['expiracao']
        info_adicionais = body['infoAdicionais']
        chave = body['chave']
        solicitacao_pagador = body['solicitacaoPagador']

        data = {
            "calendario": {
                "expiracao": expiracao
            },
            "devedor": {
                tipo_pessoa: doc_pessoa,
                "nome": nome
            },
            "valor": {
                "original": valor
            },
            "chave": chave,
            "solicitacaoPagador": solicitacao_pagador,
            "infoAdicionais": info_adicionais,
        }
        data = str(data).replace("'", '"')
        return data
    except:

        return False


class Cob:
    def __init__(self):
        self.x = 1

    def criar_cobranca_put(self, txid, body, url, cert, client_id, client_secret):

        '''
        TXID entre 27 e 35 caracteres
        Criar cobrança imediata.
        Endpoint para criar uma cobrança imediata.
        PUT - /cob/{txid}

        Status code tratados:
        201 (sucesso) - Cobrança imediata criada.
        400 (erro) - Requisição com formato inválido.
        403 (erro) - Requisição de participante autenticado que viola alguma regra de autorização.
        404 (erro) - Recurso solicitado não foi encontrado.
        503 (erro) - Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento.
        '''
        data = checa_validade_dados(body)
        if not data or len(txid) < 27:
            result = {
                "title": "Cobrança inválida.",
                "status": 400,
                "detail": "A requisição que busca alterar ou criar uma cobrança para pagamento imediato não respeita o "
                          "schema ou está semanticamente errada."
            }
            return result, 400

        autenticacao = get_autenticacao_token(url, cert, client_id, client_secret)
        if not 'access_token' in autenticacao:
            result = {
                "title": "Erro ao autenticar",
                "status": 400,
                "detail:": "Erro na autenticação na api do Santader."
            }
            return result, 400
        access_token = autenticacao['access_token']

        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json'
        }
        url += "/api/v1/cob/{}".format(str(txid))
        result = requests.request("PUT", url, headers=headers, data=data, cert=cert)

        return result.text, result.status_code

    def consultar_cobranca_get(self, txid, url, cert, client_id, client_secret):
        '''
        Consultar cobrança imediata.
        Endpoint para consultar uma cobrança através de um determinado txid.
        GET - /cob/{txid}

        Status code tratados:
        200 (sucesso) - Dados da cobrança imediata.
        400 (erro) - Erro na autenticação na api do Santader
        403 (erro) - Requisição de participante autenticado que viola alguma regra de autorização.
        404 (erro) - Recurso solicitado não foi encontrado.
        503 (erro) - Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou
         fora da janela de funcionamento.
        '''
        if len(txid) < 27:
            result = {
                "title": "Cobrança inválida.",
                "status": 400,
                "detail": "Quantidade de caracteres do TXID inválido."
            }
            return result, 400
        autenticacao = get_autenticacao_token(url, cert, client_id, client_secret)
        if not 'access_token' in autenticacao:
            result = {
                "title": "Erro ao autenticar",
                "status": 400,
                "detail:": "Erro na autenticação na api do Santader."
            }
            return result, 400
        access_token = autenticacao['access_token']

        url += "/api/v1/cob/{}".format(str(txid))
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json'
        }
        result = requests.request("GET", url, headers=headers, data=None, cert=cert)

        return result.text, result.status_code

    def consultar_lista_cobranca_get(self, inicio, fim, body, url, cert, client_id, client_secret):

        """Não definido pela área de negócio"""
        '''
        Todas as entradas são no formato de string e tem como campo obrigatório inicio e fim.
        O Body deve trazer um dicionario com as seguintes opções:
        cpf ou cnpj, locationPresent, status, paginaAtual, itensPorPagina

        Consultar lista de cobranças imediatas.
        Endpoint para consultar cobranças imediatas através de parâmetros como início, fim, cpf, cnpj e status.
        GET - /cob

        Status code tratados:
        200 (sucesso) - Lista de cobranças imediatas.
        403 (erro) - Requisição de participante autenticado que viola alguma regra de autorização.
        503 (erro) - Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da 
        janela de funcionamento.
        '''
        autenticacao = get_autenticacao_token(url, cert, client_id, client_secret)
        if not 'access_token' in autenticacao:
            result = {
                "title": "Erro ao autenticar",
                "status": 400,
                "detail:": "Erro na autenticação na api do Santader."
            }
            return result, 400
        access_token = autenticacao['access_token']
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'Content-Type': 'application/json'
        }

        url += "/api/v1/pix/" + '?inicio=' + inicio + '&fim=' + fim

        if body:
            for item in body:
                url += '&{}={}'.format(item, body[item])

        result = requests.request("GET", url, headers=headers, data=None, cert=cert)

        return result.text, result.status_code

