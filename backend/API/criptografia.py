from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from base64 import b64encode, b64decode
from dotenv import load_dotenv
import hashlib
import secrets
import bcrypt
import hmac
import os

load_dotenv()

HASH_SALT = os.getenv("HASH_SALT").encode()

def email_hash(cpf_cnpj:str) -> str:
    return hmac.new(HASH_SALT, cpf_cnpj.encode(), hashlib.sha256).hexdigest()

def senha_hash(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt(rounds=10)).decode()

def verificar_senha(senha: str, hash_salvo: str) -> bool:
    return bcrypt.checkpw(senha.encode(), hash_salvo.encode())
