import re
import unicodedata
import requests
from pprint import pprint
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

token = os.getenv('CHAVE_API_CPF')

def validacao_cpf(cpf, nome_completo, data_nascimento):
    url_base = f'https://api.cpfhub.io/cpf/{cpf}'

    headers = {
        'x-api-key': token,
        'Accept': 'application/json'
    }

    response = requests.get(
    url=url_base, 
    headers=headers,
    verify=False
)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        return response.status_code
    else:
        resultado = response.json()
        resultado_data_nascimento = datetime.strptime(resultado['data']['birthDate'], '%d/%m/%Y')
        data_nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d')
        resultado_nome = ''.join(resultado['data']['nameUpper'].replace(' ', ''))
        if resultado_nome == ''.join(nome_completo.replace(' ', '')).upper() and data_nascimento == resultado_data_nascimento:
            return 200
        return 400


def validacao_cnpj(cnpj,nome_oficial_empresa ):
    url_base = f'https://brasilapi.com.br/api/cnpj/v1/{cnpj}'

    response = requests.get(url=url_base)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        return response.status_code
    else:
        resultado = response.json()
        nome_oficial_empresa = ''.join(re.sub(r'\W', '', nome_oficial_empresa)).upper()
        nome_oficial_empresa = remover_acentos(nome_oficial_empresa)
        print(nome_oficial_empresa, resultado['razao_social'])
        if nome_oficial_empresa == ''.join(re.sub(r'\W', '', resultado['razao_social']).upper()):
            return {'cnpj' : resultado['cnpj'],
                    'nome_oficial_empresa': resultado['razao_social'],
                    'nome_cormecial_empresa': resultado['nome_fantasia'],
                    'situacao_cadastral':resultado['situacao_cadastral'],
                    'data_abertura':resultado['data_inicio_atividade'],
                    'natureza_juridica':resultado['natureza_juridica'],
                    'cnae':resultado['cnae_fiscal'],
                    'capital_social':resultado['capital_social'],
                    'porte_empresa':resultado['porte'],
                    'uf': resultado['uf'],
                    'cep': resultado['cep'],
                    'cidade': resultado['municipio'],
                    'bairro': resultado['bairro'],
                    'logradouro': resultado['logradouro'],}
        return 400

def remover_acentos(texto):
    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')

def normalizadacao_cpf_cnpj(cpf_cnpj) -> str:
    return ''.join(re.sub(r'\W', '', cpf_cnpj))


if __name__ == '__main__':
    resposta = validacao_cnpj('34.028.316/0001-03', 'Empresa Brasileira de Correios e Telégrafos ')
    #resposta = validacao_cpf('06331229205', '  henrique costa rodrigues   ', '2004-09-13')
    print(resposta)