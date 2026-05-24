from backend.models.engine import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.logs import setup_logger

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

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()