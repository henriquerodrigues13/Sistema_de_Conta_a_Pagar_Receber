import pytest
from unittest.mock import patch, AsyncMock
from datetime import datetime


# =============================================================================
# PAYLOADS GLOBAIS DE TESTE
# =============================================================================

PAYLOAD_USUARIO_PADRAO = {
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

# CORRIGIDO: antes tinhas campos errados ("descricao", "valor", "email_usuario")
# O modelo request_receita espera recebedor_email, tipo_da_receita, etc.
PAYLOAD_RECEITA_VALIDO = {
    "recebedor_email": "maria.teste@email.com",
    "tipo_da_receita": "Consultoria de TI",
    "data_da_receita": "2024-12-15T00:00:00",
    "valor_da_receita": 4500.00,
    "forma_de_pagamento": "PIX",
    "observacao": "Venda de Consultoria de TI"
}

# Payload inválido pra testar validação: email sem @ e data com formato errado
PAYLOAD_RECEITA_INVALIDO = {
    "recebedor_email": "isso_nao_e_um_email",
    "tipo_da_receita": "Teste",
    "data_da_receita": "data-invalida",
    "valor_da_receita": 100.00,
    "forma_de_pagamento": "PIX",
    "observacao": "teste invalido"
}


# =============================================================================
# TESTES DO FLUXO DE USUÁRIOS E LOGIN
# =============================================================================

def test_cadastro_usuario_com_sucesso(client, override_get_session):
    """Testa o fluxo de cadastro com sucesso usando o banco isolado em memória."""
    response = client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)

    assert response.status_code in [200, 201]
    dados_resposta = response.json()
    assert dados_resposta["nome_completo"] == "Pedro Lucas Leão"
    assert "senha" not in dados_resposta


def test_cadastro_usuario_email_duplicado(client, override_get_session):
    """Testa que cadastrar o mesmo email duas vezes retorna 409."""
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)
    response = client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)
    assert response.status_code == 409


def test_fluxo_login_comportamento_real(client, override_get_session):
    """Testa os cenários do checklist de login: Sucesso (200), 401 e 404."""
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)

    # CENÁRIO A: Credenciais Corretas
    dados_login_correto = {"email": "pedro.teste@ufpa.br", "senha": "senha_secreta_123"}
    response_sucesso = client.post("/login", json=dados_login_correto)
    assert response_sucesso.status_code == 200

    # CENÁRIO B: Senha Incorreta
    dados_senha_errada = {"email": "pedro.teste@ufpa.br", "senha": "senha_errada_456"}
    response_senha_errada = client.post("/login", json=dados_senha_errada)
    assert response_senha_errada.status_code == 401

    # CENÁRIO C: Usuário Inexistente
    dados_usuario_fantasma = {"email": "nao.existe@ufpa.br", "senha": "senha_qualquer"}
    response_fantasma = client.post("/login", json=dados_usuario_fantasma)
    assert response_fantasma.status_code == 404


# =============================================================================
# TESTES DE RECUPERAÇÃO E RESET DE SENHA
# =============================================================================

def test_recuperacao_senha_usuario_existente(client, override_get_session):
    """
    Testa que pedir recuperação de senha para um usuário que existe retorna 201.
    Precisamos mockar o envio de email pra não tentar conectar no servidor SMTP de verdade.
    """
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)

    with patch("backend.API.rotas.fast_mail.send_message", new_callable=AsyncMock):
        response = client.post("/recuperacao_senha", json={"email": "pedro.teste@ufpa.br"})

    assert response.status_code == 201


def test_recuperacao_senha_usuario_inexistente(client, override_get_session):
    """Testa que pedir recuperação de senha para email que não existe retorna 404."""
    response = client.post("/recuperacao_senha", json={"email": "fantasma@naoexiste.com"})
    assert response.status_code == 404


def test_reset_senha_com_token_valido(client, override_get_session):
    """
    Testa o fluxo completo: solicita recuperação e depois reseta a senha com o token.

    Precisamos mockar o token pra saber o valor exato que foi salvo no banco,
    e mockar a data de expiração pra colocar bem no futuro (ano 2099).
    """
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)

    TOKEN_FIXO = "token_de_teste_que_nao_expira_nunca"
    # Coloca a expiração bem no futuro pra não ter problema de timing
    expiracao_futura = datetime(2099, 12, 31, 23, 59, 59)

    with patch("backend.API.rotas.gerador_de_token", return_value=TOKEN_FIXO):
        with patch("backend.API.rotas.limite_de_expiracao_token", return_value=expiracao_futura):
            with patch("backend.API.rotas.fast_mail.send_message", new_callable=AsyncMock):
                resp_recuperacao = client.post(
                    "/recuperacao_senha", json={"email": "pedro.teste@ufpa.br"}
                )
    assert resp_recuperacao.status_code == 201

    # Agora tenta redefinir com o token que foi salvo
    response = client.post("/reset_senha", json={"token": TOKEN_FIXO, "senha": "senha_nova_789"})
    assert response.status_code == 200


def test_reset_senha_token_invalido(client, override_get_session):
    """Testa que tentar resetar a senha com token que não existe retorna 404."""
    response = client.post(
        "/reset_senha",
        json={"token": "TOKEN_INEXISTENTE_QUE_NAO_EXISTE", "senha": "qualquer"}
    )
    assert response.status_code == 404


def test_reset_senha_token_expirado(client, override_get_session):
    """
    Testa que usar um token que já passou da data de expiração retorna 400.
    Mockamos a expiração pra ano 2000 pra garantir que já expirou.
    """
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)

    TOKEN_EXPIRADO = "token_que_ja_expirou_ha_muito_tempo"
    expiracao_passada = datetime(2000, 1, 1, 0, 0, 0)  # lá em 2000, claramente expirado

    with patch("backend.API.rotas.gerador_de_token", return_value=TOKEN_EXPIRADO):
        with patch("backend.API.rotas.limite_de_expiracao_token", return_value=expiracao_passada):
            with patch("backend.API.rotas.fast_mail.send_message", new_callable=AsyncMock):
                client.post("/recuperacao_senha", json={"email": "pedro.teste@ufpa.br"})

    response = client.post("/reset_senha", json={"token": TOKEN_EXPIRADO, "senha": "nova_senha"})
    assert response.status_code == 400


# =============================================================================
# TESTES DO FLUXO DE PRODUTOS
# =============================================================================

def test_cadastro_produto_com_sucesso(client, override_get_session):
    """Testa o cadastro de um produto vinculado a um usuário existente."""
    email_teste = "pedro.teste@ufpa.br"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)

    payload_produto = {
        "nome_do_produto": "Açaí da Roça",
        "proprietario_usuario": email_teste,
        "unidade_de_medida": "Litro",
        "quantidade_em_estoque": 50,
        "categoria_do_produto": "Alimentos",
        "valor_de_custo": 10.00,
        "valor_final": 15.00,
        "descricao_do_produto": "Açaí puro tirado direto da palmeira"
    }
    response = client.post("/cadastro_produtos", json=payload_produto)

    assert response.status_code in [200, 201]
    assert "com sucesso" in response.json()["mensagem"]


def test_cadastro_produto_usuario_inexistente(client, override_get_session):
    """Garante que a API barra produtos vinculados a e-mails inexistentes."""
    payload_produto = {
        "nome_do_produto": "Produto Fantasma",
        "proprietario_usuario": "usuario.inexistente@naoexiste.com",
        "unidade_de_medida": "Unidade",
        "quantidade_em_estoque": 10,
        "categoria_do_produto": "Outros",
        "valor_de_custo": 5.00,
        "valor_final": 10.00,
        "descricao_do_produto": "Esse produto não deveria ser criado"
    }
    response = client.post("/cadastro_produtos", json=payload_produto)
    assert response.status_code == 404


def test_cadastro_produto_duplicado(client, override_get_session):
    """Testa que cadastrar o mesmo produto duas vezes para o mesmo usuário retorna 409."""
    email_teste = "pedro.teste@ufpa.br"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)

    payload_produto = {
        "nome_do_produto": "Açaí da Roça",
        "proprietario_usuario": email_teste,
        "unidade_de_medida": "Litro",
        "quantidade_em_estoque": 50,
        "categoria_do_produto": "Alimentos",
        "valor_de_custo": 10.00,
        "valor_final": 15.00,
        "descricao_do_produto": "Açaí puro tirado direto da palmeira"
    }
    client.post("/cadastro_produtos", json=payload_produto)
    response = client.post("/cadastro_produtos", json=payload_produto)
    assert response.status_code == 409


def test_get_produtos_usuario(client, override_get_session):
    """Testa o GET de listagem de produtos com validação de headers de paginação."""
    email_teste = "pedro.teste@ufpa.br"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)

    client.post("/cadastro_produtos", json={
        "nome_do_produto": "Açaí da Roça",
        "proprietario_usuario": email_teste,
        "unidade_de_medida": "Litro",
        "quantidade_em_estoque": 50,
        "categoria_do_produto": "Alimentos",
        "valor_de_custo": 10.00,
        "valor_final": 15.00,
        "descricao_do_produto": "Açaí puro tirado direto da palmeira"
    })

    response = client.get(f"/get_produtos_usuario/{email_teste}")
    assert response.status_code == 200
    dados = response.json()
    assert isinstance(dados, list)
    assert len(dados) >= 1
    assert dados[0]["nome_do_produto"] == "Açaí da Roça"
    assert "X-Total-Items" in response.headers
    assert "X-Total-Pages" in response.headers


def test_update_produto_com_sucesso(client, override_get_session):
    """Testa que PATCH /update_produto altera os dados do produto com sucesso."""
    email_teste = "pedro.teste@ufpa.br"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)

    client.post("/cadastro_produtos", json={
        "nome_do_produto": "Açaí da Roça",
        "proprietario_usuario": email_teste,
        "unidade_de_medida": "Litro",
        "quantidade_em_estoque": 50,
        "categoria_do_produto": "Alimentos",
        "valor_de_custo": 10.00,
        "valor_final": 15.00,
        "descricao_do_produto": "Açaí puro tirado direto da palmeira"
    })

    response = client.patch(
        f"/update_produto/{email_teste}/Açaí da Roça",
        json={"valor_final": 20.00, "quantidade_em_estoque": 30}
    )
    assert response.status_code == 200
    assert "atualizado" in response.json()["mensagem"]


def test_update_produto_payload_vazio(client, override_get_session):
    """Testa que enviar corpo vazio no update de produtos retorna 400."""
    email_teste = "pedro.teste@ufpa.br"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)

    client.post("/cadastro_produtos", json={
        "nome_do_produto": "Açaí da Roça",
        "proprietario_usuario": email_teste,
        "unidade_de_medida": "Litro",
        "quantidade_em_estoque": 50,
        "categoria_do_produto": "Alimentos",
        "valor_de_custo": 10.00,
        "valor_final": 15.00,
        "descricao_do_produto": "Açaí puro tirado direto da palmeira"
    })

    response = client.patch(f"/update_produto/{email_teste}/Açaí da Roça", json={})
    assert response.status_code == 400


def test_update_produto_inexistente(client, override_get_session):
    """Testa que tentar atualizar um produto que não existe retorna 404."""
    email_teste = "pedro.teste@ufpa.br"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)

    response = client.patch(
        f"/update_produto/{email_teste}/ProdutoQueNaoExiste",
        json={"valor_final": 20.00}
    )
    assert response.status_code == 404


def test_delete_produto(client, override_get_session):
    """Testa a remoção de um produto e se ele deixa de ser listado."""
    email_teste = "pedro.teste@ufpa.br"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)

    client.post("/cadastro_produtos", json={
        "nome_do_produto": "Açaí da Roça",
        "proprietario_usuario": email_teste,
        "unidade_de_medida": "Litro",
        "quantidade_em_estoque": 50,
        "categoria_do_produto": "Alimentos",
        "valor_de_custo": 10.00,
        "valor_final": 15.00,
        "descricao_do_produto": "Açaí puro tirado direto da palmeira"
    })

    response = client.delete(f"/delete_produto/{email_teste}/Açaí da Roça")
    assert response.status_code == 200
    assert "deletado" in response.json()["mensagem"]

    response_lista = client.get(f"/get_produtos_usuario/{email_teste}")
    assert response_lista.status_code == 200
    assert len(response_lista.json()) == 0


# =============================================================================
# TESTES DE FORNECEDORES
# =============================================================================

def test_get_fornecedor_lista_vazia(client, override_get_session):
    """
    Testa que GET /get_fornecedor retorna 200.
    No banco de teste não tem fornecedores (nenhum CSV é carregado), então a lista vem vazia.
    """
    response = client.get("/get_fornecedor")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# =============================================================================
# TESTES DO FLUXO DE VENDAS
# =============================================================================

def _criar_usuario_produto_padrao(client):
    """
    Função auxiliar pra criar usuário e produto de uma vez.
    Evita repetir o mesmo código em cada teste de venda.
    """
    email = "pedro.teste@ufpa.br"
    client.post("/cadastro_usuario", json=PAYLOAD_USUARIO_PADRAO)
    client.post("/cadastro_produtos", json={
        "nome_do_produto": "Produto de Venda",
        "proprietario_usuario": email,
        "unidade_de_medida": "Unidade",
        "quantidade_em_estoque": 100,
        "categoria_do_produto": "Geral",
        "valor_de_custo": 10.00,
        "valor_final": 20.00,
        "descricao_do_produto": "Produto criado pra testes de venda"
    })
    return email


def test_get_vendas_usuario(client, override_get_session):
    """Testa que GET /get_vendas retorna as vendas criadas para o usuário."""
    email = _criar_usuario_produto_padrao(client)

    client.post("/cadastro_venda_produto", json={
        "nome_do_produto": "Produto de Venda",
        "vendedor_email": email,
        "descricao_da_venda": "Venda de teste de listagem",
        "quantidade": 2,
        "valor_da_venda": 40.00,
        "forma_de_pagamento": "PIX",
        "porcentagem_do_desconto": 0.0,
        "valor_final": 40.00
    })

    response = client.get(f"/get_vendas/{email}")
    assert response.status_code == 200
    dados = response.json()
    assert isinstance(dados, list)
    assert len(dados) >= 1
    assert "X-Total-Items" in response.headers


def test_update_venda(client, override_get_session):
    """
    Testa que atualizar uma venda existente retorna HTTP 200.

    BUG CORRIGIDO: o teste antigo passava o nome do produto ('Açaí da Roça') como
    identificador da venda, mas o identificador é um nanoid gerado automaticamente.
    Agora o teste busca o identificador real via GET /get_vendas antes de atualizar.
    """
    email = _criar_usuario_produto_padrao(client)

    client.post("/cadastro_venda_produto", json={
        "nome_do_produto": "Produto de Venda",
        "vendedor_email": email,
        "descricao_da_venda": "Venda que vai ser atualizada",
        "quantidade": 2,
        "valor_da_venda": 40.00,
        "forma_de_pagamento": "PIX",
        "porcentagem_do_desconto": 0.0,
        "valor_final": 40.00
    })

    # Busca o identificador REAL da venda (é um nanoid, não o nome do produto)
    resp_get = client.get(f"/get_vendas/{email}")
    assert resp_get.status_code == 200
    vendas_lista = resp_get.json()
    assert len(vendas_lista) > 0
    identificador_real = vendas_lista[0]["identificador"]

    response = client.patch(
        f"/update_venda/{email}/{identificador_real}",
        json={"valor_final": 25.00}
    )
    assert response.status_code == 200
    assert "atualizado" in response.json()["mensagem"]


def test_delete_venda(client, override_get_session):
    """Testa que deletar uma venda retorna 200 e remove ela da listagem."""
    email = _criar_usuario_produto_padrao(client)

    client.post("/cadastro_venda_produto", json={
        "nome_do_produto": "Produto de Venda",
        "vendedor_email": email,
        "descricao_da_venda": "Venda que vai ser deletada",
        "quantidade": 1,
        "valor_da_venda": 20.00,
        "forma_de_pagamento": "Dinheiro",
        "porcentagem_do_desconto": 0.0,
        "valor_final": 20.00
    })

    # Pega o identificador real
    resp_get = client.get(f"/get_vendas/{email}")
    assert resp_get.status_code == 200
    identificador = resp_get.json()[0]["identificador"]

    response = client.delete(f"/delete_venda/{email}/{identificador}")
    assert response.status_code == 200

    # Verifica que a lista ficou vazia
    resp_depois = client.get(f"/get_vendas/{email}")
    assert len(resp_depois.json()) == 0


# =============================================================================
# TESTES DO FLUXO DE RECEITAS
# =============================================================================

def test_cadastro_receita_sucesso(client, override_get_session):
    """Garante que uma receita válida é cadastrada com sucesso após o usuário existir."""
    # Cria o usuário com o email que vai ser o recebedor da receita
    payload_usuario = PAYLOAD_USUARIO_PADRAO.copy()
    payload_usuario["email"] = PAYLOAD_RECEITA_VALIDO["recebedor_email"]

    client.post("/cadastro_usuario", json=payload_usuario)

    resposta = client.post("/cadastro_receita", json=PAYLOAD_RECEITA_VALIDO)
    assert resposta.status_code in [200, 201]
    assert "sucesso" in resposta.json()["mensagem"]


def test_cadastro_receita_erro_validacao(client, override_get_session):
    """Valida se o sistema recusa email inválido e data mal formatada com 422."""
    resposta = client.post("/cadastro_receita", json=PAYLOAD_RECEITA_INVALIDO)
    assert resposta.status_code in [400, 422]


def test_listar_receitas_sucesso(client, override_get_session):
    """
    Garante que a rota de listagem retorna as receitas cadastradas.

    BUG CORRIGIDO: o teste antigo chamava client.get('/get_receitas') sem passar o email,
    mas o endpoint correto é GET /get_receitas/{usuario_email}.
    """
    payload_usuario = PAYLOAD_USUARIO_PADRAO.copy()
    payload_usuario["email"] = PAYLOAD_RECEITA_VALIDO["recebedor_email"]

    client.post("/cadastro_usuario", json=payload_usuario)
    client.post("/cadastro_receita", json=PAYLOAD_RECEITA_VALIDO)

    email_recebedor = PAYLOAD_RECEITA_VALIDO["recebedor_email"]
    resposta = client.get(f"/get_receitas/{email_recebedor}")

    assert resposta.status_code == 200
    dados = resposta.json()
    assert isinstance(dados, list)
    assert len(dados) > 0


def test_update_receita(client, override_get_session):
    """Testa que atualizar uma receita existente retorna 200."""
    payload_usuario = PAYLOAD_USUARIO_PADRAO.copy()
    payload_usuario["email"] = PAYLOAD_RECEITA_VALIDO["recebedor_email"]

    client.post("/cadastro_usuario", json=payload_usuario)
    client.post("/cadastro_receita", json=PAYLOAD_RECEITA_VALIDO)

    email = PAYLOAD_RECEITA_VALIDO["recebedor_email"]

    # Precisa pegar o identificador antes de tentar atualizar
    resp_lista = client.get(f"/get_receitas/{email}")
    assert resp_lista.status_code == 200
    receitas_lista = resp_lista.json()
    assert len(receitas_lista) > 0
    identificador = receitas_lista[0]["identificador"]

    response = client.patch(
        f"/update_receita/{email}/{identificador}",
        json={"valor_da_receita": 5000.00, "observacao": "Valor revisado após reunião"}
    )
    assert response.status_code == 200
    assert "atualizado" in response.json()["mensagem"]


def test_delete_receita(client, override_get_session):
    """Testa que deletar uma receita retorna 200 e remove ela da listagem."""
    payload_usuario = PAYLOAD_USUARIO_PADRAO.copy()
    payload_usuario["email"] = PAYLOAD_RECEITA_VALIDO["recebedor_email"]

    client.post("/cadastro_usuario", json=payload_usuario)
    client.post("/cadastro_receita", json=PAYLOAD_RECEITA_VALIDO)

    email = PAYLOAD_RECEITA_VALIDO["recebedor_email"]

    resp_lista = client.get(f"/get_receitas/{email}")
    identificador = resp_lista.json()[0]["identificador"]

    response = client.delete(f"/delete_receita/{email}/{identificador}")
    assert response.status_code == 200

    # Lista deve estar vazia depois
    resp_depois = client.get(f"/get_receitas/{email}")
    assert len(resp_depois.json()) == 0


# =============================================================================
# TESTES DO FLUXO DE VENDA DE SERVIÇO
# =============================================================================

_USUARIO_VENDA_SERVICO = {
    "nome_completo": "Carlos Vendedor de Serviços",
    "email": "carlos.venda.servico@teste.com",
    "senha": "senha_carlos_123",
    "numero_telefone": "91988880000",
    "cep": "68450000",
    "estado": "PA",
    "cidade": "Belém",
    "bairro": "Marco",
    "logradouro": "Trav. Mauriti, 100"
}

_SERVICO_PARA_VENDER = {
    "nome_do_servico": "Manutenção de Computador",
    "prestador_do_servico_usuario": "carlos.venda.servico@teste.com",
    "descricao_do_servico": "Limpeza e formatação de computador",
    "valor_do_servico": 300.00,
    "categoria_do_servico": "Tecnologia"
}


def _criar_usuario_e_servico(client):
    """Auxiliar: cria usuário e serviço pra reutilizar nos testes de venda de serviço."""
    client.post("/cadastro_usuario", json=_USUARIO_VENDA_SERVICO)
    client.post("/cadastro_servico", json=_SERVICO_PARA_VENDER)


def test_cadastro_venda_servico_com_sucesso(client, override_get_session):
    """Testa o cadastro de venda de serviço com vendedor e serviço existentes."""
    _criar_usuario_e_servico(client)

    response = client.post("/cadastro_venda_servico", json={
        "nome_do_servico": "Manutenção de Computador",
        "vendedor_email": "carlos.venda.servico@teste.com",
        "descricao_da_venda": "Formatação do notebook do cliente",
        "valor_da_venda": 300.00,
        "forma_de_pagamento": "PIX",
        "porcentagem_do_desconto": 0.0,
        "valor_final": 300.00
    })

    assert response.status_code in [200, 201]


def test_cadastro_venda_servico_vendedor_inexistente(client, override_get_session):
    """Testa que não dá pra registrar venda de serviço com vendedor que não existe."""
    response = client.post("/cadastro_venda_servico", json={
        "nome_do_servico": "Qualquer Serviço",
        "vendedor_email": "vendedor.fantasma@naoexiste.com",
        "descricao_da_venda": "Venda que não deveria ser criada",
        "valor_da_venda": 100.00,
        "forma_de_pagamento": "PIX",
        "porcentagem_do_desconto": 0.0,
        "valor_final": 100.00
    })

    assert response.status_code == 404


def test_cadastro_venda_servico_servico_inexistente(client, override_get_session):
    """Testa que não dá pra registrar venda de um serviço que não existe pro vendedor."""
    client.post("/cadastro_usuario", json=_USUARIO_VENDA_SERVICO)

    response = client.post("/cadastro_venda_servico", json={
        "nome_do_servico": "Serviço Que Não Existe",
        "vendedor_email": "carlos.venda.servico@teste.com",
        "descricao_da_venda": "Tentativa de venda de serviço inexistente",
        "valor_da_venda": 100.00,
        "forma_de_pagamento": "PIX",
        "porcentagem_do_desconto": 0.0,
        "valor_final": 100.00
    })

    assert response.status_code == 404


def test_venda_servico_aparece_na_listagem(client, override_get_session):
    """Testa que a venda de serviço aparece no GET /get_vendas após ser criada."""
    email = "carlos.venda.servico@teste.com"
    _criar_usuario_e_servico(client)

    client.post("/cadastro_venda_servico", json={
        "nome_do_servico": "Manutenção de Computador",
        "vendedor_email": email,
        "descricao_da_venda": "Venda que vai aparecer na listagem",
        "valor_da_venda": 300.00,
        "forma_de_pagamento": "Dinheiro",
        "porcentagem_do_desconto": 0.0,
        "valor_final": 300.00
    })

    response = client.get(f"/get_vendas/{email}")
    assert response.status_code == 200
    vendas = response.json()
    assert len(vendas) >= 1
