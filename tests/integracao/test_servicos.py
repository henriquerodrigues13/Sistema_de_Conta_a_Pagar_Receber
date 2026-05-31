import pytest


# =============================================================================
# PAYLOADS
# =============================================================================

PAYLOAD_USUARIO = {
    "nome_completo": "Lucas Teste Serviços",
    "email": "lucas.servicos@teste.com",
    "senha": "senha123",
    "numero_telefone": "91988887777",
    "cep": "68450000",
    "estado": "PA",
    "cidade": "Belém",
    "bairro": "Nazaré",
    "logradouro": "Av. Nazaré, 456"
}

PAYLOAD_SERVICO = {
    "nome_do_servico": "Consultoria em TI",
    "prestador_do_servico_usuario": "lucas.servicos@teste.com",
    "descricao_do_servico": "Consultoria em sistemas de informação",
    "valor_do_servico": 500.00,
    "categoria_do_servico": "Tecnologia"
}


# =============================================================================
# TESTES DE CADASTRO DE SERVIÇO
# =============================================================================

def test_cadastro_servico_com_sucesso(client, override_get_session):
    """Cria um serviço vinculado a um usuário existente e espera sucesso."""
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)

    response = client.post("/cadastro_servico", json=PAYLOAD_SERVICO)

    assert response.status_code in [200, 201]
    assert "sucesso" in response.json()["mensagem"]


def test_cadastro_servico_usuario_inexistente(client, override_get_session):
    """Testa que não dá pra cadastrar serviço para um usuário que não existe no banco."""
    payload_sem_usuario = PAYLOAD_SERVICO.copy()
    payload_sem_usuario["prestador_do_servico_usuario"] = "nao.existe@email.com"

    response = client.post("/cadastro_servico", json=payload_sem_usuario)

    assert response.status_code == 404


def test_cadastro_servico_duplicado(client, override_get_session):
    """Testa que cadastrar o mesmo serviço duas vezes pro mesmo usuário retorna 409."""
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)
    client.post("/cadastro_servico", json=PAYLOAD_SERVICO)

    response = client.post("/cadastro_servico", json=PAYLOAD_SERVICO)

    assert response.status_code == 409


# =============================================================================
# TESTES DE LISTAGEM DE SERVIÇOS
# =============================================================================

def test_get_servico_usuario(client, override_get_session):
    """Testa que a listagem de serviços retorna o serviço que foi cadastrado."""
    email = "lucas.servicos@teste.com"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)
    client.post("/cadastro_servico", json=PAYLOAD_SERVICO)

    response = client.get(f"/get_servico_usuario/{email}")

    assert response.status_code == 200
    dados = response.json()
    assert isinstance(dados, list)
    assert len(dados) >= 1
    assert dados[0]["nome_do_servico"] == "Consultoria em TI"
    assert "X-Total-Items" in response.headers
    assert "X-Total-Pages" in response.headers


def test_get_servico_usuario_lista_vazia(client, override_get_session):
    """Testa que um usuário sem serviços retorna lista vazia (não erro)."""
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)

    response = client.get("/get_servico_usuario/lucas.servicos@teste.com")

    assert response.status_code == 200
    assert response.json() == []


# =============================================================================
# TESTES DE ATUALIZAÇÃO DE SERVIÇO
# =============================================================================

def test_update_servico_com_sucesso(client, override_get_session):
    """Testa que atualizar um serviço existente retorna 200 com mensagem de sucesso."""
    email = "lucas.servicos@teste.com"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)
    client.post("/cadastro_servico", json=PAYLOAD_SERVICO)

    response = client.patch(
        f"/update_servico/{email}/Consultoria em TI",
        json={"valor_do_servico": 750.00}
    )

    assert response.status_code == 200
    assert "atualizado" in response.json()["mensagem"]


def test_update_servico_payload_vazio(client, override_get_session):
    """Testa que mandar payload vazio no update retorna 400."""
    email = "lucas.servicos@teste.com"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)
    client.post("/cadastro_servico", json=PAYLOAD_SERVICO)

    response = client.patch(f"/update_servico/{email}/Consultoria em TI", json={})

    assert response.status_code == 400


def test_update_servico_inexistente(client, override_get_session):
    """Testa que tentar atualizar um serviço que não existe retorna 404."""
    email = "lucas.servicos@teste.com"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)

    response = client.patch(
        f"/update_servico/{email}/ServicoQueNaoExiste",
        json={"valor_do_servico": 100.00}
    )

    assert response.status_code == 404


# =============================================================================
# TESTES DE DELEÇÃO DE SERVIÇO
# =============================================================================

def test_delete_servico(client, override_get_session):
    """Testa que deletar um serviço retorna 200 e remove ele da listagem."""
    email = "lucas.servicos@teste.com"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)
    client.post("/cadastro_servico", json=PAYLOAD_SERVICO)

    response = client.delete(f"/delete_servico/{email}/Consultoria em TI")

    assert response.status_code == 200
    assert "deletado" in response.json()["mensagem"]

    # Garante que sumiu da lista
    response_lista = client.get(f"/get_servico_usuario/{email}")
    assert response_lista.status_code == 200
    assert len(response_lista.json()) == 0


def test_delete_servico_inexistente(client, override_get_session):
    """Testa que tentar deletar um serviço que não existe retorna 404."""
    email = "lucas.servicos@teste.com"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)

    response = client.delete(f"/delete_servico/{email}/ServicoQueNaoExiste")

    assert response.status_code == 404
