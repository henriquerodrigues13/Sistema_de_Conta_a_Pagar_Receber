import requests
from pprint import pprint


def validacao_email(email):
    api_key = "haI23M8iNJUOIRXpP6uYIvgJYC7JSpds"
    url = "https://emailverifier.reoon.com/api/v1/verify"

    params = {
        "email": email,
        "key": api_key,
        "mode": "power"  # modo mais preciso
    }

    resposta = requests.get(url, params=params)
    dados = resposta.json()

    if dados['status'] == 'safe' or dados['status'] == 'catch_all':
        return True
    return False

if __name__ == '__main__':
    resultado = validacao_email(email="henrique.rodrigues@cameta.ufpa.br")
    pprint(resultado)