import pytest
import requests
from unittest.mock import patch, MagicMock
from pydantic import ValidationError

import backend.API.validações as validacoes_modulo
from backend.API.validações import validacao_email
from backend.models.tabelas import cadastro_usuario

def test_validacao_email_com_resposta_valid():
    """Testa que se o serviço externo responder 'valid', a função retorna True."""
    patch.stopall()
    with patch.object(validacoes_modulo, "requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "valid"}
        mock_requests.post.return_value = mock_response
        mock_requests.get.return_value = mock_response

        resultado = validacao_email("pedro.teste@ufpa.br")
        assert resultado is True

def test_validacao_email_com_resposta_invalid():
    """Testa que se o serviço externo responder 'invalid', a função retorna False."""
    patch.stopall()
    with patch.object(validacoes_modulo, "requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "invalid"}
        mock_requests.post.return_value = mock_response
        mock_requests.get.return_value = mock_response

        resultado = validacao_email("email_falso_estragado@provedor.com")
        assert resultado is False

def test_pydantic_rejeita_campos_obrigatorios_ausentes():
    """Valida que o schema 'cadastro_usuario' do Pydantic lança erro se faltarem campos."""
    payload_incompleto = {
        "nome_completo": "Pedro Lucas Leão"
    }
    with pytest.raises(ValidationError):
        cadastro_usuario.model_validate(payload_incompleto)

def test_api_rejeita_payload_invalido_com_http_422(client):
    """Testa via TestClient se a rota intercepta o erro do Pydantic e retorna HTTP 422."""
    payload_com_erro = {
        "nome_completo": "Pedro Lucas Leão",
        "email": "email_invalido"
    }
    response = client.post("/cadastro_usuario", json=payload_com_erro)
    assert response.status_code == 422

def test_validacao_email_erro_http():
    """
    Testa que quando há erro de conexão, a função retorna False
    em vez de deixar a exceção explodir (graceful degradation).
    """
    patch.stopall()
    with patch.object(validacoes_modulo, "requests") as mock_requests:
        mock_requests.post.side_effect = Exception("Timeout na conexão")

        resultado = validacao_email("pedro.teste@ufpa.br")
        
        # O código trata a exceção e retorna False
        assert resultado is False