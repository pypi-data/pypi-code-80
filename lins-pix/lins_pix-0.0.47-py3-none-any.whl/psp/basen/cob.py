# python3 setup.py sdist upload -r testpypi
# pip install -i https://test.pypi.org/simple/ lins_pix==0.0.14


'''
Reúne endpoints destinados a lidar com gerenciamento de cobranças imediatas
'''


class Cob:
    def __init__(self):
        self.x = 1

    def criar_cobranca_put(self, txid, body):
        '''
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

        if txid == 201:
            code = 201
            result = {
                "calendario": {
                    "criacao": "2020-09-09T20:15:00.358Z",
                    "expiracao": 3600
                },
                "txid": "7978c0c97ea847e78e8849634473c1f1",
                "revisao": 0,
                "loc": {
                    "id": 789,
                    "location": "pix.example.com/qr/v2/9d36b84fc70b478fb95c12729b90ca25",
                    "tipoCob": "cob"
                },
                "location": "pix.example.com/qr/v2/9d36b84fc70b478fb95c12729b90ca25",
                "status": "ATIVA",
                "devedor": {
                    "cnpj": "12345678000195",
                    "nome": "Empresa de Serviços SA"
                },
                "valor": {
                    "original": "567.89"
                },
                "chave": "a1f4102e-a446-4a57-bcce-6fa48899c1d1",
                "solicitacaoPagador": "Informar cartão fidelidade"
            }

        elif txid == 400:
            code = 400
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/CobOperacaoInvalida",
                "title": "Cobrança inválida.",
                "status": 400,
                "detail": "A requisição que busca alterar ou criar uma cobrança para pagamento imediato não respeita o schema ou está semanticamente errada.",
                "violacoes": [
                    {
                        "razao": "O campo cob.valor.original não respeita o schema.",
                        "propriedade": "cob.valor.original"
                    }
                ]
            }

        elif txid == 403:
            code = 403
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/AcessoNegado",
                "title": "Acesso Negado",
                "status": 403,
                "detail": "Requisição de participante autenticado que viola alguma regra de autorização."
            }

        elif txid == 404:
            code = 404
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/NaoEncontrado",
                "title": "Não Encontrado",
                "status": 404,
                "detail": "Entidade não encontrada."
            }

        elif txid == 503:
            code = 503
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/ServicoIndisponivel",
                "title": "Serviço Indisponível",
                "status": 503,
                "detail": "Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento."
            }

        return result, code

    def revisar_cobranca_patch(self, txid, body):
        '''
        Revisar cobrança imediata.
        PATCH - /cob/{txid}

        Status code tratados:
        200 (sucesso) - Cobrança imediata revisada. A revisão deve ser incrementada em 1.
        400 (erro) - Requisição com formato inválido.
        403 (erro) - Requisição de participante autenticado que viola alguma regra de autorização.
        404 (erro) - Recurso solicitado não foi encontrado.
        503 (erro) - Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento.
        '''

        if txid == 200:
            code = 200
            result = {
                "calendario": {
                    "criacao": "2020-09-09T20:15:00.358Z",
                    "expiracao": 3600
                },
                "txid": "7978c0c97ea847e78e8849634473c1f1",
                "revisao": 1,
                "loc": {
                    "id": 789,
                    "location": "pix.example.com/qr/v2/9d36b84fc70b478fb95c12729b90ca25",
                    "tipoCob": "cob"
                },
                "location": "pix.example.com/qr/v2/9d36b84fc70b478fb95c12729b90ca25",
                "status": "ATIVA",
                "devedor": {
                    "cnpj": "12345678000195",
                    "nome": "Empresa de Serviços SA"
                },
                "valor": {
                    "original": "567.89"
                },
                "chave": "a1f4102e-a446-4a57-bcce-6fa48899c1d1",
                "solicitacaoPagador": "Informar cartão fidelidade"
            }

        elif txid == 400:
            code = 400
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/CobOperacaoInvalida",
                "title": "Operação inválida.",
                "status": 400,
                "detail": "A requisição que busca alterar ou criar uma cobrança para pagamento imediato não respeita o schema ou está semanticamente errada."
            }

        elif txid == 403:
            code = 403
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/AcessoNegado",
                "title": "Acesso Negado",
                "status": 403,
                "detail": "Requisição de participante autenticado que viola alguma regra de autorização."
            }

        elif txid == 404:
            code = 404
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/NaoEncontrado",
                "title": "Não Encontrado",
                "status": 404,
                "detail": "Entidade não encontrada."
            }

        elif txid == 503:
            code = 503
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/ServicoIndisponivel",
                "title": "Serviço Indisponível",
                "status": 503,
                "detail": "Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento."
            }

        return result, code

    def consultar_cobranca_get(self, txid, revisao=None):
        '''
        Consultar cobrança imediata.
        Endpoint para consultar uma cobrança através de um determinado txid.
        GET - /cob/{txid}

        Status code tratados:
        200 (sucesso) - Dados da cobrança imediata.
        403 (erro) - Requisição de participante autenticado que viola alguma regra de autorização.
        404 (erro) - Recurso solicitado não foi encontrado.
        503 (erro) - Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento.
        '''

        if txid == 200:
            code = 200
            result = {
                "calendario": {
                    "criacao": "2020-09-09T20:15:00.358Z",
                    "expiracao": 3600
                },
                "txid": "7978c0c97ea847e78e8849634473c1f1",
                "revisao": 0,
                "loc": {
                    "id": 789,
                    "location": "pix.example.com/qr/v2/9d36b84fc70b478fb95c12729b90ca25",
                    "tipoCob": "cob"
                },
                "location": "pix.example.com/qr/v2/9d36b84fc70b478fb95c12729b90ca25",
                "status": "ATIVA",
                "devedor": {
                    "cnpj": "12345678000195",
                    "nome": "Empresa de Serviços SA"
                },
                "valor": {
                    "original": "567.89"
                },
                "chave": "a1f4102e-a446-4a57-bcce-6fa48899c1d1",
                "solicitacaoPagador": "Informar cartão fidelidade"
            }

        elif txid == 403:
            code = 403
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/AcessoNegado",
                "title": "Acesso Negado",
                "status": 403,
                "detail": "Requisição de participante autenticado que viola alguma regra de autorização."
            }

        elif txid == 404:
            code = 404
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/NaoEncontrado",
                "title": "Não Encontrado",
                "status": 404,
                "detail": "Entidade não encontrada."
            }

        elif txid == 503:
            code = 503
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/ServicoIndisponivel",
                "title": "Serviço Indisponível",
                "status": 503,
                "detail": "Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento."
            }

        return result, code

    def criar_cobranca_post(self, txid):
        '''
        TODO: remover parametro de entrada txid

        Criar cobrança imediata.
        Endpoint para criar uma cobrança imediata, neste caso, o txid deve ser definido pelo PSP.

        POST - /cob
        '''

        if txid == 200:
            code = 200
            result = {
                "calendario": {
                    "criacao": "2020-09-09T20:15:00.358Z",
                    "expiracao": 3600
                },
                "txid": "7978c0c97ea847e78e8849634473c1f1",
                "revisao": 0,
                "loc": {
                    "id": 789,
                    "location": "pix.example.com/qr/v2/9d36b84fc70b478fb95c12729b90ca25",
                    "tipoCob": "cob"
                },
                "location": "pix.example.com/qr/v2/9d36b84fc70b478fb95c12729b90ca25",
                "status": "ATIVA",
                "devedor": {
                    "cnpj": "12345678000195",
                    "nome": "Empresa de Serviços SA"
                },
                "valor": {
                    "original": "567.89"
                },
                "chave": "a1f4102e-a446-4a57-bcce-6fa48899c1d1",
                "solicitacaoPagador": "Informar cartão fidelidade"
            }

        elif txid == 403:
            code = 403
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/AcessoNegado",
                "title": "Acesso Negado",
                "status": 403,
                "detail": "Requisição de participante autenticado que viola alguma regra de autorização."
            }

        elif txid == 404:
            code = 404
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/NaoEncontrado",
                "title": "Não Encontrado",
                "status": 404,
                "detail": "Entidade não encontrada."
            }

        elif txid == 503:
            code = 503
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/ServicoIndisponivel",
                "title": "Serviço Indisponível",
                "status": 503,
                "detail": "Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento."
            }

        return result, code

    def consultar_lista_cobranca_get(self, txid, inicio, fim, cpf, cnpj, locationPresente, status, paginaAtual=0, itensPorPagina=100):
        '''
        TODO: remover parametro de entrada txid

        Consultar lista de cobranças imediatas.
        Endpoint para consultar cobranças imediatas através de parâmetros como início, fim, cpf, cnpj e status.
        GET - /cob

        Status code tratados:
        200 (sucesso) - Lista de cobranças imediatas.
        403 (erro) - Requisição de participante autenticado que viola alguma regra de autorização.
        503 (erro) - Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento.
        '''

        if txid == 200:
            code = 200
            result = {
                "parametros": {
                    "inicio": "2020-04-01T00:00:00Z",
                    "fim": "2020-04-02T10:00:00Z",
                    "paginacao": {
                        "paginaAtual": 0,
                        "itensPorPagina": 100,
                        "quantidadeDePaginas": 1,
                        "quantidadeTotalDeItens": 2
                    }
                },
                "cobs": [
                    {
                        "$ref": "openapi.yaml#/components/examples/cobResponse1/value"
                    },
                    {
                        "$ref": "openapi.yaml#/components/examples/cobResponse2/value"
                    }
                ]
            }

        elif txid == 403:
            code = 403
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/AcessoNegado",
                "title": "Acesso Negado",
                "status": 403,
                "detail": "Requisição de participante autenticado que viola alguma regra de autorização."
            }

        elif txid == 503:
            code = 503
            result = {
                "type": "https://pix.bcb.gov.br/api/v2/error/ServicoIndisponivel",
                "title": "Serviço Indisponível",
                "status": 503,
                "detail": "Serviço não está disponível no momento. Serviço solicitado pode estar em manutenção ou fora da janela de funcionamento."
            }

        return result, code
