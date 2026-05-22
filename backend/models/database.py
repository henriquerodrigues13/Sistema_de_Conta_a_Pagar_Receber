from sqlalchemy_utils import create_database, database_exists
from backend.models.engine import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

DATABASE_URL = os.getenv(
    "URL_DB",
    "postgresql+psycopg2://postgres:13092004He!@localhost:5432/meu_banco"
)
engine = create_engine(DATABASE_URL)

def init_db():
    if not database_exists(DATABASE_URL):
        create_database(DATABASE_URL)

    Base.metadata.create_all(bind=engine)

def get_session():
    with Session(bind=engine) as session:
        yield session
