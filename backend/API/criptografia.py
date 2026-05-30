from datetime import datetime, timedelta, timezone
import secrets
import bcrypt


BRASILIA = timezone(timedelta(hours=-3))

def senha_hash(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt(rounds=10)).decode()

def verificar_senha(senha: str, hash_salvo: str) -> bool:
    return bcrypt.checkpw(senha.encode(), hash_salvo.encode())

def gerador_de_token() -> str:
    return secrets.token_urlsafe(32)

def limite_de_expiracao_token() -> datetime:
    return datetime.now(BRASILIA) + timedelta(hours=1)