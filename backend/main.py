from backend.models import backup_base_dados as backup
from contextlib import asynccontextmanager
from backend.models import banco_dados_inicia
from backend.API import rotas
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    banco_dados_inicia.criar_banco_de_dados()
    task = asyncio.create_task(backup.backup())
    yield
    task.cancel()

app = FastAPI(title="API_Sistema_de_contas", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Items", "X-Total-Pages"],
)

app.include_router(rotas.router)