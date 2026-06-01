"""
TESTES DE ENDPOINTS COM BUGS CONHECIDOS
========================================

Esses testes documentam o comportamento ESPERADO de endpoints que têm bugs
no código de produção. Todos estão marcados com @pytest.mark.xfail, o que
significa que a falha é esperada — não é um problema da suite de testes.

Quando os devs corrigirem os bugs, esses testes vão passar automaticamente
e o pytest vai mostrar XPASS (unexpected pass), o que serve como aviso de
"ei, o bug foi corrigido, pode remover o xfail".

Ver BUG_REPORT.md para detalhes de cada bug.
"""

import pytest

PAYLOAD_USUARIO_BUG = {
    "nome_completo": "Usuário Teste Bug",
    "email": "teste.bug@teste.com",
    "senha": "senha_bug_123",
    "numero_telefone": "91900000000",
    "cep": "68450000",
    "estado": "PA",
    "cidade": "Belém",
    "bairro": "Reduto",
    "logradouro": "Rua dos Bugs, 404"
}

# Payload completo da nota fiscal (todos os campos são obrigatórios pelo modelo)
PAYLOAD_NOTA_FISCAL = {
    "usuario_email": "teste.bug@teste.com",
    "emitente_razao_social": "Empresa Teste LTDA",
    "emitente_cnpj": "12345678000190",
    "emitente_inscricao_estadual": "123456789",
    "emitente_inscricao_municipal": "987654",
    "emitente_codigo_municipal": "1501402",
    "emitente_cep": "68450000",
    "emitente_uf": "PA",
    "emitente_logradouro": "Rua Principal, 123",
    "emitente_bairro": "Centro",
    "emitente_municipio": "Belém",
    "emitente_pais": "Brasil",
    "emitente_regime_tributario": "1",
    "cliente_nome_razao_social": "Cliente Teste da Silva",
    "cliente_cpf_cnj": "12345678901",
    "cliente_indicador_ie": "9",
    "cliente_codigo_municipal": "1501402",
    "cliente_cep": "68450000",
    "cliente_uf": "PA",
    "cliente_logradouro": "Av. Cliente, 456",
    "cliente_bairro": "Nazaré",
    "cliente_municipio": "Belém",
    "cliente_pais": "Brasil",
    "produto_codigo": "001",
    "produto_valor_unidade": "15.00",
    "produto_quantidade": "2",
    "nota_informacoes": "Nota emitida pelo sistema de testes",
    "nota_forma_de_pagamento": "01",
    "nota_modalidade_do_frete": "0"
}


# =============================================================================
# BUG-001: Lógica invertida em POST /cadastro_nota_fiscal
# =============================================================================

@pytest.mark.xfail(
    reason="BUG-001: a condição 'if not usuario_existe' está invertida — "
           "cria nota quando o usuário NÃO existe e retorna 404 quando EXISTE. "
           "Ver BUG_REPORT.md para detalhes."
)
def test_cadastro_nota_fiscal_usuario_existente_deve_retornar_sucesso(client, override_get_session):
    """
    Comportamento ESPERADO: criar nota fiscal para usuário existente → 200/201.
    Comportamento ATUAL (bug): retorna 404 mesmo com usuário existente.
    """
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_BUG)

    response = client.post("/cadastro_nota_fiscal", json=PAYLOAD_NOTA_FISCAL)

    # Isso deveria funcionar, mas falha por causa do BUG-001
    assert response.status_code in [200, 201]


@pytest.mark.xfail(
    reason="BUG-001: com a lógica atual invertida, usuário INEXISTENTE recebe 200 "
           "em vez de 404. O correto seria 404."
)
def test_cadastro_nota_fiscal_usuario_inexistente_deve_retornar_404(client, override_get_session):
    """
    Comportamento ESPERADO: usuário inexistente → 404.
    Comportamento ATUAL (bug): usuário inexistente → 200 (cria a nota mesmo sem usuário).
    """
    payload_sem_usuario = PAYLOAD_NOTA_FISCAL.copy()
    payload_sem_usuario["usuario_email"] = "nao.existe.mesmo@fantasma.com"

    response = client.post("/cadastro_nota_fiscal", json=payload_sem_usuario)

    # Com a lógica correta deveria dar 404, mas atualmente dá 200
    assert response.status_code == 404


# =============================================================================
# BUG-002: Parâmetro de path errado em GET /get_produtos_fornecedor/{cnpj}
# =============================================================================

@pytest.mark.xfail(
    reason="BUG-002: o endpoint tem '{cnpj}' na URL mas o parâmetro da função "
           "se chama 'fornecedor_cnpj'. O FastAPI trata 'fornecedor_cnpj' como "
           "query param obrigatório, então a chamada sem ele retorna 422. "
           "Ver BUG_REPORT.md para detalhes."
)
def test_get_produtos_fornecedor_retorna_lista_por_cnpj(client, override_get_session):
    """
    Comportamento ESPERADO: GET /get_produtos_fornecedor/12345 → 200 com lista vazia.
    Comportamento ATUAL (bug): retorna 422 porque 'fornecedor_cnpj' é query param obrigatório.
    """
    # CNPJ fictício — no banco de teste não tem fornecedores mesmo,
    # mas o endpoint deveria retornar 200 com lista vazia
    cnpj_ficticio = "12345678000190"

    response = client.get(f"/get_produtos_fornecedor/{cnpj_ficticio}")

    # Isso deveria ser 200, mas por causa do bug é 422
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# =============================================================================
# BUG-003: Parâmetro de path errado em GET /get_servicos_fornecedor/{cnpj}
# =============================================================================

@pytest.mark.xfail(
    reason="BUG-003: mesmo problema do BUG-002, mas no endpoint de serviços do fornecedor. "
           "O parâmetro 'fornecedor_cnpj' não casa com '{cnpj}' da URL, "
           "causando 422 ao invés de 200. Ver BUG_REPORT.md."
)
def test_get_servicos_fornecedor_retorna_lista_por_cnpj(client, override_get_session):
    """
    Comportamento ESPERADO: GET /get_servicos_fornecedor/12345 → 200 com lista vazia.
    Comportamento ATUAL (bug): retorna 422 porque 'fornecedor_cnpj' é query param obrigatório.
    """
    cnpj_ficticio = "12345678000190"

    response = client.get(f"/get_servicos_fornecedor/{cnpj_ficticio}")

    # Isso deveria ser 200, mas por causa do bug é 422
    assert response.status_code == 200
    assert isinstance(response.json(), list)
