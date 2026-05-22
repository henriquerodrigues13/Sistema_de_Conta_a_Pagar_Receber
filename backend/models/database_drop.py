import os
from sqlalchemy import create_engine, text
from backend.models.engine import Base
from dotenv import load_dotenv

load_dotenv()
engine = create_engine('postgresql+psycopg2://postgres:13092004He!@localhost:5432/meu_banco')

with engine.connect() as conn:
    conn.execute(text("DROP SCHEMA public CASCADE"))
    conn.execute(text("CREATE SCHEMA public"))
    conn.commit()