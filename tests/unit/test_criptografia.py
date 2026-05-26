import sys
import os
import pytest

# Garantindo que a pasta 'backend' seja encontrada não importa de onde o teste seja executado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importando as funções de criptografia do backend
from backend.API.criptografia import senha_hash, verificar_senha

def test_criptografia_da_senha():
    senha_original = "123456"
    
    # 1. Executa a função para gerar o hash
    hash_gerado = senha_hash(senha_original)
    
    # VALIDAÇÃO 1: O hash gerado não pode ser igual à senha pura (Criptografia funcionando)
    assert hash_gerado != senha_original
    
    # VALIDAÇÃO 2: Se colocar a senha certa, o sistema precisa retornar True
    assert verificar_senha(senha_original, hash_gerado) is True
    
    # VALIDAÇÃO 3: Se colocar uma senha errada, o sistema precisa retornar False
    assert verificar_senha("senha_errada", hash_gerado) is False