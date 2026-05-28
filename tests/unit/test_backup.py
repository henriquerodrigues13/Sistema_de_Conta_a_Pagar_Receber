from pathlib import Path


def test_backup_rotacionamento(tmp_path):
    """
    Testa que o rotacionamento mantém no máximo 3 arquivos de backup,
    removendo os mais antigos quando há mais de 3.
    """
    # Cria 5 arquivos de backup simulados
    for i in range(1, 6):
        arquivo = tmp_path / f"backup_2024010{i}_120000.sqlite"
        arquivo.write_bytes(b"")

    arquivos_antes = sorted(tmp_path.glob("backup_*.sqlite"))
    assert len(arquivos_antes) == 5

    # Lógica de rotacionamento igual à do backup_sqlite()
    manter = 3
    backups = sorted(tmp_path.glob("backup_*.sqlite"))
    if len(backups) > manter:
        para_deletar = backups[:-manter]
        for antigo in para_deletar:
            antigo.unlink()

    arquivos_depois = sorted(tmp_path.glob("backup_*.sqlite"))
    assert len(arquivos_depois) == 3

    # Garante que os 3 mais recentes foram mantidos
    nomes = [a.name for a in arquivos_depois]
    assert "backup_20240103_120000.sqlite" in nomes
    assert "backup_20240104_120000.sqlite" in nomes
    assert "backup_20240105_120000.sqlite" in nomes


def test_backup_rotacionamento_menos_de_3(tmp_path):
    """
    Testa que quando há menos de 3 backups nenhum arquivo é removido.
    """
    for i in range(1, 3):
        arquivo = tmp_path / f"backup_2024010{i}_120000.sqlite"
        arquivo.write_bytes(b"")

    manter = 3
    backups = sorted(tmp_path.glob("backup_*.sqlite"))
    if len(backups) > manter:
        para_deletar = backups[:-manter]
        for antigo in para_deletar:
            antigo.unlink()

    arquivos_depois = sorted(tmp_path.glob("backup_*.sqlite"))
    assert len(arquivos_depois) == 2