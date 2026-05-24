from backend.models.engine import Base, fornecedores
from sqlalchemy import create_engine, select
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from backend.logs import setup_logger
from pathlib import Path
import csv

logger = setup_logger('DATABASE INIT')

DATABASE_URL = "sqlite:///./cpr.sqlite"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    logger.debug('Iniciando DB')
    Base.metadata.create_all(bind=engine)
    populate_db()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def populate_db():
    CSV_PATH = Path(__file__).parent.parent.parent / 'fornecedores.csv'

    with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        linhas = list(reader)

    with Session(engine) as session:
        for linha in linhas:
            ja_existe = session.scalar(
                select(fornecedores).where(fornecedores.cnpj == linha["cnpj"])
            )

            if ja_existe:
                continue

            novo = fornecedores(
                cnpj=linha.get("cnpj"),
                nome_oficial_empresa=linha.get("nome_oficial_empresa"),
                nome_cormecial_empresa=linha.get("nome_cormecial_empresa"),
                situacao_cadastral=linha.get("situacao_cadastral"),
                data_abertura=linha.get("data_abertura"),
                natureza_juridica=linha.get("natureza_juridica"),
                cnae=linha.get("cnae"),
                capital_social=linha.get("capital_social"),
                porte_empresa=linha.get("porte_empresa"),
                cep=linha.get("cep"),
                uf=linha.get("uf"),
                cidade=linha.get("cidade"),
                bairro=linha.get("bairro"),
                logradouro=linha.get("logradouro"),
            )
            session.add(novo)

        session.commit()