import os
import pytest
import httpx
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import backend.main as backend_main
import backend.models.database as database_module
from backend.models.engine import Base, usuario

@pytest.fixture(scope="session")
def app():
    return backend_main.app

@pytest.fixture()
def client(app, override_get_session):
    with TestClient(app) as c:
        yield c

@pytest.fixture()
async def async_client(app, override_get_session):
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ.setdefault("TESTING", "1")
    os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
    yield

@pytest.fixture(autouse=True)
def mock_validacao_email():
    with patch("backend.API.routes.validacao_email") as mock:
        mock.return_value = True  
        yield mock

@pytest.fixture()
def override_get_session(app):
    engine = create_engine(
        "sqlite:///:memory:", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Cria apenas a tabela de usuário isolando seu teste dos erros do backend
    usuario.metadata.create_all(bind=engine, tables=[usuario.__table__])

    def _get_test_session():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[database_module.get_session] = _get_test_session
    yield
    app.dependency_overrides.clear()
    engine.dispose()