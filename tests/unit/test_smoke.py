import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
import backend.main as main_modulo

def test_docs_available(client):
    """Smoke test: a documentação Swagger deve estar disponível em /docs."""
    resp = client.get("/docs")
    assert resp.status_code == 200


def test_docs_with_db_fixture(client, override_get_session):
    """Smoke test que usa o override_get_session para garantir que o fixture não quebre."""
    resp = client.get("/docs")
    assert resp.status_code == 200

def test_api_subida_e_chamada_init_db_no_lifespan():
    """
    Smoke Test: Garante que a API sobe (HTTP 200 no /docs) e que o
    criar_banco_de_dados() é chamado corretamente durante o lifespan.

    CORRIGIDO: o patch apontava para 'backend.main.database.init_db' que não existe.
    O módulo correto é 'backend.main.banco_dados_inicia' e a função é 'criar_banco_de_dados'.
    """
    # 1. Interceptamos a função de inicialização do banco antes de carregar o cliente
    with patch("backend.main.banco_dados_inicia.criar_banco_de_dados") as mock_init_db:
        
        # 2. O TestClient ativa o evento de 'lifespan' (startup) ao entrar no contexto 'with'
        with TestClient(main_modulo.app) as client:
            # Faz uma requisição simples para garantir que está de pé
            response = client.get("/docs")
            
            assert response.status_code == 200
            
            # 3. VALIDAÇÃO DO CHECKLIST: O init_db foi chamado no startup?
            assert mock_init_db.called is True, "O database.init_db() não foi chamado no lifespan!"