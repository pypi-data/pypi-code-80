import numpy as np
import pandas as pd

informacoes_classe = {'Classe': ('C20', 'C30', 'C40', 'C60'),
                      'Fc0k': (20, 30, 40, 60),
                      'Ec0m': (9500, 14500, 19500, 24500)}
tabela_classe = pd.DataFrame(informacoes_classe, index=(1, 2, 3, 4))

informacoes_kmod1 = {'Permanente': 0.6,
                     'Longa Duração': 0.7,
                     'Média Duração': 0.8,
                     'Curta Duração': 0.9,
                     'Instantânea': 1.1}

duracoes = ('Permanente', 'Longa Duração', 'Média Duração', 'Curta Duração', 'Instantânea')

informacoes_kmod2 = 1

informacoes_kmod3 = {'1ª Categoria': 1, '2ª Categoria': 0.8}

categorias = ('1ª Categoria', '2ª Categoria')


class Pegador:

    @staticmethod
    def escolhe():

        mensagem = f'''A viga é retangular ou circular?

                (1) Circular
                (2) Retangular

            '''

        circulo_ou_retangulo = input(mensagem)
        if circulo_ou_retangulo in ('1', '2'):
            return circulo_ou_retangulo
        else:
            raise ValueError('Digite um valor válido. ')

    @staticmethod
    def pega_dimensoes(viga):
        if viga.circulo_ou_retangulo == '1':
            diametro = float(input('Informe o diâmetro em centímetro da peça. '))
            return diametro / 100
        else:
            base = float(input('Informe a medida da base em centímetro da peça. '))
            altura = float(input('Informe a medida da altura em centímetro da peça. '))
            return base / 100, altura / 100

    @staticmethod
    def pega_comprimento():
        comprimento = float(input('Informe o comprimento em metro da viga. '))
        return comprimento

    @staticmethod
    def pega_cargas():
        peso_proprio = float(input('Informe o peso próprio da viga. '))
        carga_acidental = float(input('Informe a carga acidental da viga. '))

        return peso_proprio, carga_acidental

    @staticmethod
    def pega_classe_categoria_e_duracao():
        mensagem_classe = '''Informe a classe da madeira. 

                (1) C20
                (2) C30
                (3) C40
                (4) C60

                '''

        mensagem_categoria = '''Informe a categoria da madeira.

                (1) 1ª categoria
                (2) 2ª categoria

                '''

        mensagem_duracao = '''Informe a duração do carregamento.

                (1) Permanente
                (2) Longa Duração
                (3) Média Duração
                (4) Curta Duração
                (5) Instantânea
                
                '''

        classe = int(input(mensagem_classe))
        if classe not in (1, 2, 3, 4):
            raise ValueError('Digite um valor válido para classe. ')

        categoria = int(input(mensagem_categoria))
        if categoria not in (1, 2):
            raise ValueError('Digite um valor válido para categoria. ')

        duracao = int(input(mensagem_duracao))
        if duracao not in (1, 2, 3, 4, 5):
            raise ValueError('Digite um valor válido para duração. ')

        return classe, categoria, duracao

    @staticmethod
    def pega_Fc0k(viga):
        fc0k = tabela_classe.loc[viga.classe, 'Fc0k']
        return fc0k

    @staticmethod
    def pega_kmod(viga):
        duracao = duracoes[viga.duracao - 1]
        kmod1 = informacoes_kmod1[duracao]

        kmod2 = informacoes_kmod2

        categoria = categorias[viga.categoria - 1]
        kmod3 = informacoes_kmod3[categoria]

        kmod = kmod1 * kmod2 * kmod3

        return round(kmod, 3), (kmod1, kmod2, kmod3)

    @staticmethod
    def pega_Ec0m(viga):
        Ec0m = tabela_classe.loc[viga.classe, 'Ec0m']
        return Ec0m


class Calculador:

    @staticmethod
    def calcula_area(viga):
        if viga.circulo_ou_retangulo == '1':
            area = (np.pi * viga.dimensoes ** 2) / 4
            return area
        else:
            area = viga.dimensoes[0] * viga.dimensoes[1]
            return round(area, 6)

    @staticmethod
    def calcula_inercia(viga):
        if viga.circulo_ou_retangulo == '1':
            inercia = (np.pi * (viga.dimensoes ** 4)) / 64
        else:
            inercia = (viga.dimensoes[0] * viga.dimensoes[1] ** 3) / 12

        return round(inercia, 8)

    @staticmethod
    def calcula_resistencia(viga):
        if viga.circulo_ou_retangulo == '1':
            W = (np.pi * (viga.dimensoes ** 3)) / 32
        else:
            W = (viga.dimensoes[0] * (viga.dimensoes[1] ** 2)) / 6

        return W

    @staticmethod
    def calcula_carga_permanente(viga):
        carga_permanente = viga.area * 10 + viga.peso_proprio
        return carga_permanente

    @staticmethod
    def calcula_momento_fletor(viga):
        momento_fletor = (1.4 * (viga.carga_permanente + viga.carga_acidental) * viga.comprimento ** 2) / 8
        return momento_fletor

    @staticmethod
    def calcula_tensao_normal(viga):
        tensao_normal = (viga.momento_fletor / viga.modulo_resistencia) / 1000
        return round(tensao_normal, 3)

    @staticmethod
    def calcula_fc0d(viga):
        fc0d = (viga.kmod * viga.Fc0k) / 1.4
        return round(fc0d, 2)

    @staticmethod
    def calcula_flecha_maxima(viga):
        flecha_maxima = (viga.comprimento / 200) * 1000
        return flecha_maxima

    @staticmethod
    def calcula_modulo_elasticidade(viga):
        Eef = (viga.Ec0m * viga.kmod) * 1000
        return round(Eef, 2)

    @staticmethod
    def calcula_flecha_efetiva(viga):
        Vef = ((5 * (viga.carga_permanente + 0.2 * viga.carga_acidental) * viga.comprimento ** 4) / (
                384 * viga.modulo_elasticidade * viga.inercia)) * 1000
        return round(Vef, 3)


class VigaDeMadeira:

    def __init__(self):

    	print('\n\nBem vindo ao Calculador de Vigas do 4º TE. A seguir, um pequeno tutorial de uso.\n\n')
        print('Não é necessário digitar as unidades dos valores, apenas o número é necessário.')
        print('Caso a unidade seja digitada, erros ocorrerão.')
        print('Quando aparecer um seletor, por exemplo: \n (1) Opção 1 \n (2) Opção 2')
        print('Digite somente o número que está dentro dos parênteses. Por exemplo, se sua a opção desejada for a 2,')
        print('digite apenas "2" (sem as aspas).\n\n')

        self.circulo_ou_retangulo = Pegador.escolhe()
        self.dimensoes = Pegador.pega_dimensoes(self)
        self.comprimento = Pegador.pega_comprimento()
        self.peso_proprio, self.carga_acidental = Pegador.pega_cargas()
        self.classe, self.categoria, self.duracao = Pegador.pega_classe_categoria_e_duracao()
        self.Fc0k = Pegador.pega_Fc0k(self)
        self.kmod, self.kmods = Pegador.pega_kmod(self)
        self.Ec0m = Pegador.pega_Ec0m(self)

        self.area = Calculador.calcula_area(self)
        self.inercia = Calculador.calcula_inercia(self)
        self.modulo_resistencia = Calculador.calcula_resistencia(self)
        self.carga_permanente = Calculador.calcula_carga_permanente(self)
        self.momento_fletor = Calculador.calcula_momento_fletor(self)
        self.tensao_normal = Calculador.calcula_tensao_normal(self)
        self.fc0d = Calculador.calcula_fc0d(self)
        self.flecha_maxima = Calculador.calcula_flecha_maxima(self)
        self.modulo_elasticidade = Calculador.calcula_modulo_elasticidade(self)
        self.flecha_efetiva = Calculador.calcula_flecha_efetiva(self)

        print(self)

    def compara_estado_limite_ultimo(self):
        if self.tensao_normal <= self.fc0d:
            return 'Passou!'
        else:
            return 'Não passou!'

    def compara_flecha(self):
        if self.flecha_efetiva <= self.flecha_maxima:
            return 'Passou!'
        else:
            return 'Não passou!'

    def __str__(self):
        return f'''
        
Área (A): {self.area:.8f} m²
Momento de Inércia (Iz): {self.inercia:.8f} m⁴
Módulo de Resistência (W): {self.modulo_resistencia:.8f} m³
Carga Permanente (gk): {self.carga_permanente:.8f} kN/m
Momento Fletor Máximo (Mzd): {self.momento_fletor:.8f} kNm
Tensão Máxima (σMzd): {self.tensao_normal:.3f} MPa
Resistência a Compressão (Fc0k): {self.Fc0k} MPa
Kmod1, Kmod2, Kmod3: {self.kmods}
Kmod: {self.kmod}
Resistência da Madeira (Fc0d): {self.fc0d} MPa

Verificação Parte 3: {self.tensao_normal} <= {self.fc0d}
        {self.compara_estado_limite_ultimo()}

Flecha Limite (Vlim): {self.flecha_maxima} mm
Ec0m: {self.Ec0m} MPa
Modulo de Elasticidade Efetivo (Eef): {self.modulo_elasticidade} kN/m²
Flecha Efetiva (Vef): {self.flecha_efetiva} mm

Verificação Parte 4: {self.flecha_efetiva} <= {self.flecha_maxima}
        {self.compara_flecha()}


'''


if __name__ == '__main__':
    VigaDeMadeira()
