"""
Utils
"""

import re

def read_conf_file(filepath):
    """
    Faz a leitura do arquivo de configuração.

    Arquivo deve ter a seguinte configuração:
        file=<path do arquivo de log>
        server=<endereço do servidor do logstash/kibana>
        port=<ids a receber mensagens de warn, separados por vírgula>

    Por favor, mantenha esta configuração. Separe as linhas apenas por quebras.
    Linhas em branco serão ignoradas. Linhas iniciadas por # também são ignoradas.
    As configurações dispostas aqui são opcionais. Em geral, se nenhuma configuração
    for informada, valores padrão serão utilizados.

    Params:
        - filepath : str path do arquivo de configuração do bot

    Returns:
        tuple contendo as configurações do bot
    """

    special_parse = ['port']
    parse = lambda x: int(x)

    filepath = '' if not filepath else filepath
    try:
        with open(filepath, 'r') as _f:
            confs = map(lambda x: x.strip(), _f.read().split('\n'))
    except FileNotFoundError:
        return {'file': None}

    confs = [x for x in confs if x and not x.startswith('#')]
    if not confs:
        raise ValueError("Arquivo de configuração deve conter configurações.")

    regex = re.compile(r'^(\w+)\s*=\s*(.+)$')
    confs = {k.lower(): v for k, v in [regex.findall(c)[0] for c in confs]}

    for c in special_parse:
        if c in confs:
            confs[c] = parse(confs[c])

    return confs
