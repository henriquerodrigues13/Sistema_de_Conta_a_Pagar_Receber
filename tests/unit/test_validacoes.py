import pytest
import requests
from unittest.mock import patch, MagicMock
from pydantic import ValidationError

import backend.API.validações as validacoes_modulo
from backend.API.validações import validacao_email, validacao_cnpj, normalizada_cnpj
from backend.models.engine import cadastro_usuario

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


def test_normalizar_cnpj():
    """
    Testa se a função remove pontuação do CNPJ corretamente.
    CNPJ formatado (com pontos, barra e traço) deve virar só números.
    """
    # CNPJ com a formatação padrão brasileira
    cnpj_formatado = "12.345.678/0001-99"

    resultado = normalizada_cnpj(cnpj_formatado)

    # Só deve sobrar os dígitos, sem nenhum caractere especial
    assert resultado == "12345678000199"


def test_validacao_cnpj_sucesso():
    """
    Testa que a função retorna o dicionário com dados quando o CNPJ é válido.
    Adaptado para o comportamento real do back-end (que retorna um dict, não True).
    """
    patch.stopall()
    with patch.object(validacoes_modulo, "requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "valid"}
        mock_requests.get.return_value = mock_response

        resultado = validacao_cnpj("12345678000199")

        # Como o back-end retorna o dicionário bruto da API, testamos isso:
        assert isinstance(resultado, dict)
        assert resultado.get("status") == "valid"


def test_validacao_cnpj_falha():
    """
    Testa que a função retorna False quando o serviço externo lança HTTPError.
    """
    patch.stopall()
    with patch.object(validacoes_modulo, "requests") as mock_requests:
        mock_response = MagicMock()
        # Força o raise_for_status a lançar o erro esperado pelo try/except do back-end
        mock_response.raise_for_status.side_effect = requests.HTTPError("CNPJ inválido")
        mock_requests.get.return_value = mock_response

        resultado = validacao_cnpj("00000000000000")
        assert resultado is False


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