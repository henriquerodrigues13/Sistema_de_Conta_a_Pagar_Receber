from pprint import pprint
import requests
import re


def validacao_email(email):
    api_key = '3f1c2d022729488da21f370e1a81ccf9'
    url = "https://api.zerobounce.net/v2/validate"

    params = {
        "api_key": api_key,
        "email": email
    }

    response = requests.post(url, params)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f'Erro no request: {e}')
    else:
        dados = response.json()

        if dados['status'] == 'valid':
            return True
        return False

def normalizada_cnpj(cnpj: str) -> str:
    return re.sub(r"\D", "", cnpj)

if __name__ == '__main__':
    resultado = normalizada_cnpj('00.00.000/00001-91')
    pprint(resultado)