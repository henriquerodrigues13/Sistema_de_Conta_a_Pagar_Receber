import asyncio
import sqlite3
from datetime import datetime
from pathlib import Path

def backup_sqlite():
    caminho_db = Path(__file__).parent.parent.parent / 'cpr.sqlite'

    backup_db = Path().home() / 'Documents' / 'backup'
    Path(backup_db).mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_db / f"backup_{timestamp}.sqlite"

    source = sqlite3.connect(caminho_db)
    with sqlite3.connect(str(backup_path)) as dest:
        source.backup(dest)
    source.close()

    manter = 3
    backups = sorted(backup_db.glob("backup_*.sqlite"))

    if len(backups) > manter:
        for antigo in backups[:-manter]:
            antigo.unlink()

async def agenda_backup():
    while True:
        await asyncio.sleep(30)
        backup_sqlite()
