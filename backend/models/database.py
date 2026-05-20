from sqlalchemy_utils import create_database, database_exists
from backend.models.engine import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os


env = os.getenv("ENV", "development")

if env == "production":
    load_dotenv(".env.production")
else:
    load_dotenv(".env.development")

db_url = os.getenv("URL_DB")
engine = create_engine(db_url)

def init_db():
    if not database_exists(db_url):
        create_database(db_url)

    Base.metadata.create_all(bind=engine)

def get_session():
    with Session(bind=engine) as session:
        yield session
