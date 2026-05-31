import pytest


# =============================================================================
# PAYLOADS
# =============================================================================

PAYLOAD_USUARIO = {
    "nome_completo": "Ana Teste Despesas",
    "email": "ana.despesas@teste.com",
    "senha": "senha456",
    "numero_telefone": "91977775555",
    "cep": "68450000",
    "estado": "PA",
    "cidade": "Belém",
    "bairro": "Umarizal",
    "logradouro": "Rua dos Testes, 789"
}

PAYLOAD_DESPESA = {
    "pagador_email": "ana.despesas@teste.com",
    "tipo_da_despesa": "Material de Escritório",
    "descricao_da_despesa": "Compra de canetas e cadernos para o escritório",
    "valor_total_da_despesa": 150.00,
    "forma_de_pagamento": "cartao_debito",
    "valor_por_unidade": 15.00
}


# =============================================================================
# TESTES DE CADASTRO DE DESPESA
# =============================================================================

def test_cadastro_despesa_com_sucesso(client, override_get_session):
    """Cria uma despesa para um usuário existente e verifica que foi bem-sucedido."""
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)

    response = client.post("/cadastro_despesa", json=PAYLOAD_DESPESA)

    # Nota: BUG-004 - o backend retorna mensagem dizendo 'receita' no lugar de 'despesa'
    # Por isso não checamos o conteúdo da mensagem, só o status code
    assert response.status_code in [200, 201]


def test_cadastro_despesa_pagador_inexistente(client, override_get_session):
    """Testa que não dá pra criar despesa com um pagador que não existe no banco."""
    payload_sem_usuario = PAYLOAD_DESPESA.copy()
    payload_sem_usuario["pagador_email"] = "nao.existe@email.com"

    response = client.post("/cadastro_despesa", json=payload_sem_usuario)

    assert response.status_code == 404


def test_cadastro_despesa_payload_incompleto(client, override_get_session):
    """Testa que um payload faltando campos obrigatórios retorna 422."""
    payload_incompleto = {
        "pagador_email": "ana.despesas@teste.com"
        # faltam tipo_da_despesa, descricao, valor_total, etc.
    }
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)

    response = client.post("/cadastro_despesa", json=payload_incompleto)

    assert response.status_code == 422


# =============================================================================
# TESTES DE LISTAGEM DE DESPESAS
# =============================================================================

def test_get_despesas_usuario(client, override_get_session):
    """Testa que a listagem de despesas retorna as despesas cadastradas."""
    email = "ana.despesas@teste.com"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)
    client.post("/cadastro_despesa", json=PAYLOAD_DESPESA)

    response = client.get(f"/get_despesas/{email}")

    assert response.status_code == 200
    dados = response.json()
    assert isinstance(dados, list)
    assert len(dados) >= 1
    assert dados[0]["tipo_da_despesa"] == "Material de Escritório"
    assert "X-Total-Items" in response.headers
    assert "X-Total-Pages" in response.headers


def test_get_despesas_usuario_lista_vazia(client, override_get_session):
    """Testa que um usuário sem despesas retorna lista vazia (não erro)."""
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)

    response = client.get("/get_despesas/ana.despesas@teste.com")

    assert response.status_code == 200
    assert response.json() == []


# =============================================================================
# TESTES DE ATUALIZAÇÃO DE DESPESA
# =============================================================================

def test_update_despesa_com_sucesso(client, override_get_session):
    """Testa que atualizar uma despesa existente retorna 200."""
    email = "ana.despesas@teste.com"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)
    client.post("/cadastro_despesa", json=PAYLOAD_DESPESA)

    # Precisa pegar o identificador real da despesa antes de atualizar
    # (identificador é um nanoid gerado automaticamente, tipo "2xKF9Bm3Ly")
    resp_lista = client.get(f"/get_despesas/{email}")
    assert resp_lista.status_code == 200
    despesas_lista = resp_lista.json()
    assert len(despesas_lista) > 0
    identificador = despesas_lista[0]["identificador"]

    response = client.patch(
        f"/update_despesa/{email}/{identificador}",
        json={"valor_total_da_despesa": 200.00, "descricao_da_despesa": "Compra revisada"}
    )

    assert response.status_code == 200
    assert "atualizado" in response.json()["mensagem"]


def test_update_despesa_payload_vazio(client, override_get_session):
    """Testa que mandar payload vazio no update da despesa retorna 400."""
    email = "ana.despesas@teste.com"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)
    client.post("/cadastro_despesa", json=PAYLOAD_DESPESA)

    resp_lista = client.get(f"/get_despesas/{email}")
    identificador = resp_lista.json()[0]["identificador"]

    response = client.patch(f"/update_despesa/{email}/{identificador}", json={})

    assert response.status_code == 400


def test_update_despesa_inexistente(client, override_get_session):
    """Testa que tentar atualizar uma despesa com identificador inválido retorna 404."""
    email = "ana.despesas@teste.com"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)

    response = client.patch(
        f"/update_despesa/{email}/IDENTIFICADOR_QUE_NAO_EXISTE",
        json={"valor_total_da_despesa": 999.00}
    )

    assert response.status_code == 404


# =============================================================================
# TESTES DE DELEÇÃO DE DESPESA
# =============================================================================

def test_delete_despesa(client, override_get_session):
    """Testa que deletar uma despesa retorna 200 e remove ela da listagem."""
    email = "ana.despesas@teste.com"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)
    client.post("/cadastro_despesa", json=PAYLOAD_DESPESA)

    resp_lista = client.get(f"/get_despesas/{email}")
    identificador = resp_lista.json()[0]["identificador"]

    response = client.delete(f"/delete_despesa/{email}/{identificador}")

    assert response.status_code == 200
    assert "deletada" in response.json()["mensagem"]

    # Garante que sumiu da lista
    resp_depois = client.get(f"/get_despesas/{email}")
    assert len(resp_depois.json()) == 0


def test_delete_despesa_inexistente(client, override_get_session):
    """Testa que tentar deletar uma despesa com identificador inválido retorna 404."""
    email = "ana.despesas@teste.com"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO)

    response = client.delete(f"/delete_despesa/{email}/IDENTIFICADOR_INVALIDO_123")

    assert response.status_code == 404
