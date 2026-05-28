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
    assert "senha" not in dados_resposta


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
        "senha": "senha_errada_456"
    }
    response_senha_errada = client.post("/login", json=dados_senha_errada)
    assert response_senha_errada.status_code == 401

    # CENÁRIO C: Usuário Inexistente -> Deve retornar 404
    dados_usuario_fantasma = {
        "email": "nao.existe@ufpa.br",
        "senha": "senha_qualquer"
    }
    response_fantasma = client.post("/login", json=dados_usuario_fantasma)
    assert response_fantasma.status_code == 404


def test_cadastro_produto_com_sucesso(client, override_get_session):
    """
    Testa o cadastro de um produto vinculado a um usuário que já existe.
    Usa o e-mail fixo definido no cenário de testes como chave de vínculo.
    """
    # Passo 1: Cria o usuário dono do produto via API
    email_teste = "pedro.teste@ufpa.br"
    payload_usuario = {
        "nome_completo": "Pedro Lucas Leão",
        "email": email_teste,
        "senha": "senha_secreta_123",
        "numero_telefone": "91988888888",
        "cep": "68450000",
        "estado": "PA",
        "cidade": "Baião",
        "bairro": "Centro",
        "logradouro": "Rua Principal, 123"
    }
    resposta_usuario = client.post("/cadastro_usuario", json=payload_usuario)
    assert resposta_usuario.status_code in [200, 201]

    # Passo 2: Cadastra o produto utilizando o mesmo e-mail do Passo 1
    payload_produto = {
        "nome_do_produto": "Açaí da Roça",
        "proprietario_usuario": email_teste,
        "unidade_de_medida": "Litro",
        "quantidade_em_estoque": 50,
        "categoria_do_produto": "Alimentos",
        "valor_de_custo": 10.00,
        "valor_final": 15.00,
        "descricao_do_produto": "Açaí puro tirado direto do palmeiro"
    }
    
    response = client.post("/cadastro_produtos", json=payload_produto)

    assert response.status_code in [200, 201]
    dados_resposta = response.json()
    assert "com sucesso" in dados_resposta["mensagem"]


def test_cadastro_produto_usuario_inexistente(client, override_get_session):
    """
    Testa que não é possível cadastrar um produto para um usuário que não existe.
    A API deve barrar e retornar HTTP 404.
    """
    email_fantasma = "usuario.inexistente@naoexiste.com"

    payload_produto = {
        "nome_do_produto": "Produto Fantasma",
        "proprietario_usuario": email_fantasma,
        "unidade_de_medida": "Unidade",
        "quantidade_em_estoque": 10,
        "categoria_do_produto": "Outros",
        "valor_de_custo": 5.00,
        "valor_final": 10.00,
        "descricao_do_produto": "Esse produto não deveria ser criado"
    }
    
    response = client.post("/cadastro_produtos", json=payload_produto)

    assert response.status_code == 404

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
    assert "senha" not in dados_resposta


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
        "senha": "senha_errada_456"
    }
    response_senha_errada = client.post("/login", json=dados_senha_errada)
    assert response_senha_errada.status_code == 401

    # CENÁRIO C: Usuário Inexistente -> Deve retornar 404
    dados_usuario_fantasma = {
        "email": "nao.existe@ufpa.br",
        "senha": "senha_qualquer"
    }
    response_fantasma = client.post("/login", json=dados_usuario_fantasma)
    assert response_fantasma.status_code == 404


def test_cadastro_produto_com_sucesso(client, override_get_session):
    """
    Testa o cadastro de um produto vinculado a um usuário que já existe.
    Usa o e-mail fixo definido no cenário de testes como chave de vínculo.
    """
    # Passo 1: Cria o usuário dono do produto via API
    email_teste = "pedro.teste@ufpa.br"
    payload_usuario = {
        "nome_completo": "Pedro Lucas Leão",
        "email": email_teste,
        "senha": "senha_secreta_123",
        "numero_telefone": "91988888888",
        "cep": "68450000",
        "estado": "PA",
        "cidade": "Baião",
        "bairro": "Centro",
        "logradouro": "Rua Principal, 123"
    }
    resposta_usuario = client.post("/cadastro_usuario", json=payload_usuario)
    assert resposta_usuario.status_code in [200, 201]

    # Passo 2: Cadastra o produto utilizando o mesmo e-mail do Passo 1
    payload_produto = {
        "nome_do_produto": "Açaí da Roça",
        "proprietario_usuario": email_teste,
        "unidade_de_medida": "Litro",
        "quantidade_em_estoque": 50,
        "categoria_do_produto": "Alimentos",
        "valor_de_custo": 10.00,
        "valor_final": 15.00,
        "descricao_do_produto": "Açaí puro tirado direto do palmeiro"
    }
    
    response = client.post("/cadastro_produtos", json=payload_produto)

    assert response.status_code in [200, 201]
    dados_resposta = response.json()
    assert "com sucesso" in dados_resposta["mensagem"]


def test_cadastro_produto_usuario_inexistente(client, override_get_session):
    """
    Testa que não é possível cadastrar um produto para um usuário que não existe.
    A API deve barrar e retornar HTTP 404.
    """
    email_fantasma = "usuario.inexistente@naoexiste.com"

    payload_produto = {
        "nome_do_produto": "Produto Fantasma",
        "proprietario_usuario": email_fantasma,
        "unidade_de_medida": "Unidade",
        "quantidade_em_estoque": 10,
        "categoria_do_produto": "Outros",
        "valor_de_custo": 5.00,
        "valor_final": 10.00,
        "descricao_do_produto": "Esse produto não deveria ser criado"
    }
    
    response = client.post("/cadastro_produtos", json=payload_produto)

    assert response.status_code == 404

def test_get_produtos_usuario(client, override_get_session):
    """
    Testa que GET /get_produtos_usuario retorna a lista paginada
    de produtos do usuário com os headers de paginação corretos.
    """
    email_teste = "pedro.teste@ufpa.br"

    # Cria usuário
    client.post("/cadastro_usuario", json={
        "nome_completo": "Pedro Lucas Leão",
        "email": email_teste,
        "senha": "senha_secreta_123",
        "numero_telefone": "91988888888",
        "cep": "68450000",
        "estado": "PA",
        "cidade": "Baião",
        "bairro": "Centro",
        "logradouro": "Rua Principal, 123"
    })

    # Cria um produto
    client.post("/cadastro_produtos", json={
        "nome_do_produto": "Açaí da Roça",
        "proprietario_usuario": email_teste,
        "unidade_de_medida": "Litro",
        "quantidade_em_estoque": 50,
        "categoria_do_produto": "Alimentos",
        "valor_de_custo": 10.00,
        "valor_final": 15.00,
        "descricao_do_produto": "Açaí puro tirado direto do palmeiro"
    })

    response = client.get(f"/get_produtos_usuario/{email_teste}")

    assert response.status_code == 200
    dados = response.json()
    assert isinstance(dados, list)
    assert len(dados) >= 1
    assert dados[0]["nome_do_produto"] == "Açaí da Roça"
    assert "X-Total-Items" in response.headers
    assert "X-Total-Pages" in response.headers


def test_delete_produto(client, override_get_session):
    """
    Testa que DELETE /delete_produto marca o produto como indisponível
    e que ele some da listagem após a exclusão.
    """
    email_teste = "pedro.teste@ufpa.br"

    # Cria usuário e produto
    client.post("/cadastro_usuario", json={
        "nome_completo": "Pedro Lucas Leão",
        "email": email_teste,
        "senha": "senha_secreta_123",
        "numero_telefone": "91988888888",
        "cep": "68450000",
        "estado": "PA",
        "cidade": "Baião",
        "bairro": "Centro",
        "logradouro": "Rua Principal, 123"
    })
    client.post("/cadastro_produtos", json={
        "nome_do_produto": "Açaí da Roça",
        "proprietario_usuario": email_teste,
        "unidade_de_medida": "Litro",
        "quantidade_em_estoque": 50,
        "categoria_do_produto": "Alimentos",
        "valor_de_custo": 10.00,
        "valor_final": 15.00,
        "descricao_do_produto": "Açaí puro tirado direto do palmeiro"
    })

    # Deleta o produto
    response = client.delete(f"/delete_produto/{email_teste}/Açaí da Roça")
    assert response.status_code == 200
    assert "deletado" in response.json()["mensagem"]

    # Confirma que sumiu da listagem
    response_lista = client.get(f"/get_produtos_usuario/{email_teste}")
    assert response_lista.status_code == 200
    assert len(response_lista.json()) == 0


def test_update_produto_com_sucesso(client, override_get_session):
    """
    Testa que PATCH /update_produto atualiza os dados do produto corretamente.
    """
    email_teste = "pedro.teste@ufpa.br"

    client.post("/cadastro_usuario", json={
        "nome_completo": "Pedro Lucas Leão",
        "email": email_teste,
        "senha": "senha_secreta_123",
        "numero_telefone": "91988888888",
        "cep": "68450000",
        "estado": "PA",
        "cidade": "Baião",
        "bairro": "Centro",
        "logradouro": "Rua Principal, 123"
    })
    client.post("/cadastro_produtos", json={
        "nome_do_produto": "Açaí da Roça",
        "proprietario_usuario": email_teste,
        "unidade_de_medida": "Litro",
        "quantidade_em_estoque": 50,
        "categoria_do_produto": "Alimentos",
        "valor_de_custo": 10.00,
        "valor_final": 15.00,
        "descricao_do_produto": "Açaí puro tirado direto do palmeiro"
    })

    response = client.patch(
        f"/update_produto/{email_teste}/Açaí da Roça",
        json={"valor_final": 20.00, "quantidade_em_estoque": 30}
    )

    assert response.status_code == 200
    assert "atualizado" in response.json()["mensagem"]


def test_update_produto_payload_vazio(client, override_get_session):
    """
    Testa que PATCH /update_produto com payload vazio retorna HTTP 400.
    """
    email_teste = "pedro.teste@ufpa.br"

    client.post("/cadastro_usuario", json={
        "nome_completo": "Pedro Lucas Leão",
        "email": email_teste,
        "senha": "senha_secreta_123",
        "numero_telefone": "91988888888",
        "cep": "68450000",
        "estado": "PA",
        "cidade": "Baião",
        "bairro": "Centro",
        "logradouro": "Rua Principal, 123"
    })
    client.post("/cadastro_produtos", json={
        "nome_do_produto": "Açaí da Roça",
        "proprietario_usuario": email_teste,
        "unidade_de_medida": "Litro",
        "quantidade_em_estoque": 50,
        "categoria_do_produto": "Alimentos",
        "valor_de_custo": 10.00,
        "valor_final": 15.00,
        "descricao_do_produto": "Açaí puro tirado direto do palmeiro"
    })

    response = client.patch(
        f"/update_produto/{email_teste}/Açaí da Roça",
        json={}
    )

    assert response.status_code == 400

def test_cadastro_usuario_email_duplicado(client, override_get_session):
    """Testa que cadastrar o mesmo email duas vezes retorna 409."""
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

    client.post("/cadastro_usuario", json=payload)
    response = client.post("/cadastro_usuario", json=payload)

    assert response.status_code == 409

def test_cadastro_produto_duplicado(client, override_get_session):
    """Testa que cadastrar o mesmo produto duas vezes para o mesmo usuário retorna 409."""
    email_teste = "pedro.teste@ufpa.br"

    client.post("/cadastro_usuario", json={
        "nome_completo": "Pedro Lucas Leão",
        "email": email_teste,
        "senha": "senha_secreta_123",
        "numero_telefone": "91988888888",
        "cep": "68450000",
        "estado": "PA",
        "cidade": "Baião",
        "bairro": "Centro",
        "logradouro": "Rua Principal, 123"
    })

    payload_produto = {
        "nome_do_produto": "Açaí da Roça",
        "proprietario_usuario": email_teste,
        "unidade_de_medida": "Litro",
        "quantidade_em_estoque": 50,
        "categoria_do_produto": "Alimentos",
        "valor_de_custo": 10.00,
        "valor_final": 15.00,
        "descricao_do_produto": "Açaí puro tirado direto do palmeiro"
    }

    client.post("/cadastro_produtos", json=payload_produto)
    response = client.post("/cadastro_produtos", json=payload_produto)

    assert response.status_code == 409

def test_update_produto_inexistente(client, override_get_session):
    """Testa que tentar atualizar um produto que não existe retorna 404."""
    email_teste = "pedro.teste@ufpa.br"

    client.post("/cadastro_usuario", json={
        "nome_completo": "Pedro Lucas Leão",
        "email": email_teste,
        "senha": "senha_secreta_123",
        "numero_telefone": "91988888888",
        "cep": "68450000",
        "estado": "PA",
        "cidade": "Baião",
        "bairro": "Centro",
        "logradouro": "Rua Principal, 123"
    })

    response = client.patch(
        f"/update_produto/{email_teste}/ProdutoQueNaoExiste",
        json={"valor_final": 20.00}
    )

    assert response.status_code == 404