from pprint import pprint
import requests
import re

def validacao_cpf(cpf: str) -> bool:
    api_key = '3d45d9df5d6151e9532292e11cf726b9f3f7db2a76209bcf290ad8117a15d546'

    try:
        response = requests.get(
            f'https://api.cpfhub.io/cpf/{cpf}',
            headers={'x-api-key': api_key},
            timeout=5
        )
        response.raise_for_status()

    except Exception:
        return False
    else:
        return True

def validacao_email(email) -> dict | bool:
    api_key = '3f1c2d022729488da21f370e1a81ccf9'
    url = "https://api.zerobounce.net/v2/validate"

    params = {
        "api_key": api_key,
        "email": email
    }

    try:
        response = requests.post(url, params, timeout=5)
        response.raise_for_status()
    except Exception:
        return False
    else:
        dados = response.json()

        if dados['status'] == 'valid':
            return True
        return False

def normalizada(dado: str) -> str:
    return re.sub(r"\D", "", dado)

if __name__ == '__main__':
    resultado = validacao_cpf('')
    pprint(resultado)