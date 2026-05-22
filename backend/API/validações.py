import requests
from pprint import pprint


def validacao_email(email):
    api_key = '3f1c2d022729488da21f370e1a81ccf9'
    url = "https://api.zerobounce.net/v2/validate"

    params = {
        "api_key": api_key,
        "email": email
    }

    resposta = requests.get(url, params=params)
    dados = resposta.json()

    pprint(dados)
    if dados['status'] == 'valid':
        return True
    return False

if __name__ == '__main__':
    resultado = validacao_email(email="henriquefnaf2680@gmail.com")
    print(resultado)