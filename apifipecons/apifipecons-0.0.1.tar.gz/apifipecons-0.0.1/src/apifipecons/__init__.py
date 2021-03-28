import requests
from dateutil.relativedelta import relativedelta
from datetime import date, datetime

class apiFIPE():

    def getCodigoMarca(self, anoModelo, modeloCodigoExterno):

        response = requests.post(
            'https://veiculos.fipe.org.br/api/veiculos//ConsultarValorComTodosParametros',
            json={'codigoTabelaReferencia': self.codigoTabelaReferencia(),
                    'codigoMarca': '',
                    'codigoModelo': '',
                    'codigoTipoVeiculo': 1,
                    'anoModelo': anoModelo,
                    'codigoTipoCombustivel': 1,
                    'tipoVeiculo': 'carro',
                    'modeloCodigoExterno': modeloCodigoExterno,
                    'tipoConsulta': 'codigo'
                    },
            headers={
                'Host': 'veiculos.fipe.org.br',
                'Referer': 'http://veiculos.fipe.org.br/'
            }
        )

        return response.json()


    def codigoTabelaReferencia(self, *args):
        fipe_first_table = date(1999,1,1)
        if not args:
            data_ref = date.today()
        else:
            data_ref = [0]
        relativedelta_obj = relativedelta(data_ref, fipe_first_table)
        codTabela = relativedelta_obj.months + (12*relativedelta_obj.years)
        return codTabela

if __name__ == '__main__':
    #apiFIPE = apiFIPE()
    result = apiFIPE().getCodigoMarca(2018,'001461-3')
    print(result)
