import pytest

def test_cadastro_usuario_com_sucesso(client, override_get_session):
    """
    Testa o fluxo de cadastro com sucesso usando o client síncrono da conftest
    e o banco de dados isolado em memória.
    """
    payload = {
        "nome_completo": "Pedro Lucas Leão",
        "email": "pedro.teste@ufpa.br",
        "senha": "senha_secreta_123",
        "numero_telefone": "91988888888",
        "cep": "68450000",
        "estado": "PA",
        "cidade": "Baião",
        "bairro": "Centro",
        "logradouro": "Rua Principal, 123"
    }
    
    response = client.post("/cadastro_usuario", json=payload)
    
    assert response.status_code in [200, 201]
    
    dados_resposta = response.json()
    assert dados_resposta["nome_completo"] == "Pedro Lucas Leão"
    assert dados_resposta.get("senha") != "senha_secreta_123"


def test_fluxo_login_comportamento_real(client, override_get_session):
    """
    Testa os três cenários obrigatórios do checklist para o /login:
    Sucesso (200), Senha Incorreta (401) e Usuário Inexistente (404).
    """
    
    # 1. Cadastra o usuário primeiro no banco em memória que inicia limpo
    payload_cadastro = {
        "nome_completo": "Pedro Lucas Leão",
        "email": "pedro.teste@ufpa.br",
        "senha": "senha_secreta_123",
        "numero_telefone": "91988888888",
        "cep": "68450000",
        "estado": "PA",
        "cidade": "Baião",
        "bairro": "Centro",
        "logradouro": "Rua Principal, 123"
    }
    client.post("/cadastro_usuario", json=payload_cadastro)

    # CENÁRIO A: Credenciais Corretas -> Deve retornar 200
    dados_login_correto = {
        "email": "pedro.teste@ufpa.br",
        "senha": "senha_secreta_123"
    }
    response_sucesso = client.post("/login", json=dados_login_correto)
    assert response_sucesso.status_code == 200

    # CENÁRIO B: Senha Incorreta -> Deve retornar 401
    dados_senha_errada = {
        "email": "pedro.teste@ufpa.br",
        "senha": "senha_errada_qualquer"
    }
    response_401 = client.post("/login", json=dados_senha_errada)
    assert response_401.status_code == 401

    # CENÁRIO C: Usuário Inexistente -> Deve retornar 404
    dados_usuario_fantasma = {
        "email": "nao_existe_no_sistema@ufpa.br",
        "senha": "qualquer_senha"
    }
    response_404 = client.post("/login", json=dados_usuario_fantasma)
    assert response_404.status_code == 404