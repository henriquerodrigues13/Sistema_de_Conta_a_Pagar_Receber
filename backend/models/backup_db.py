from email.message import EmailMessage
from backend.logs import setup_logger
from datetime import datetime
from pathlib import Path
import asyncio
import sqlite3
import smtplib

logger = setup_logger('backup_db')

EMAIL_REMETENTE = "henriquefnaf2680@gmail.com"
EMAIL_SENHA = "vrsn ptmn nhni aena"
EMAIL_DESTINO = "darlancota8@gmail.com"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def backup_sqlite():
    caminho_db = Path(__file__).parent.parent.parent / 'cpr.sqlite'

    backup_db = Path(__file__).parent.parent / 'Backup'
    Path(backup_db).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_db / f"backup_{timestamp}.sqlite"

    source = sqlite3.connect(caminho_db)
    dest = sqlite3.connect(str(backup_path))
    source.backup(dest)
    dest.close()
    source.close()

    manter = 3
    backups = sorted(backup_db.glob("backup_*.sqlite"))

    if len(backups) > manter:
        para_deletar = backups[:-manter]
        for antigo in para_deletar:
            antigo.unlink()
            logger.info(f"Arquivo {antigo.name} removido")
    logger.debug('backup concluido')

def enviar_backup():
    backup_dir = Path(__file__).parent.parent / 'Backup'
    arquivos = list(Path(backup_dir).glob("*.sqlite"))

    arquivo_mais_recente = max(arquivos, key=lambda x: x.stat().st_mtime)

    msg = EmailMessage()
    msg["Subject"] = f"Backup do banco — {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    msg["From"]    = EMAIL_REMETENTE
    msg["To"]      = EMAIL_DESTINO
    msg.set_content(
        f"Backup gerado em {datetime.now().strftime('%d/%m/%Y_%H:%M:%S')}.\n"
        f"Arquivo: {arquivo_mais_recente.name}\n"
        f"Tamanho: {arquivo_mais_recente.stat().st_size / 1024:.1f} KB"
    )

    with open(arquivo_mais_recente, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename=arquivo_mais_recente.name
        )

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(EMAIL_REMETENTE, EMAIL_SENHA)
        smtp.send_message(msg)
    logger.info(f' backup do banco de dados enviado para {EMAIL_DESTINO} as {datetime.now().strftime('%d/%m/%Y %H:%M')}')


async def backup():
    while True:
        await asyncio.sleep(10)
        backup_sqlite()
        #enviar_backup()
