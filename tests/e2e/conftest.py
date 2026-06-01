import pytest
import subprocess
import time
import requests


# Reinicia o backend antes dos testes E2E para evitar conexões travadas
@pytest.fixture(scope="session", autouse=True)
def reiniciar_backend():
    """
    Mata qualquer processo uvicorn rodando na porta 8000 e sobe um novo.
    Isso garante que o backend esteja fresco e sem conexões travadas.
    """
    print("\n🔄 Reiniciando backend para testes E2E...")

    # Mata processos uvicorn na porta 8000
    subprocess.run(
        ["taskkill", "/F", "/IM", "python.exe", "/FI", "WINDOWTITLE eq*uvicorn*"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1)

    # Sobe novo backend em background
    backend_process = subprocess.Popen(
        ["python", "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Aguarda backend ficar pronto
    max_tentativas = 30
    for tentativa in range(max_tentativas):
        try:
            requests.get("http://127.0.0.1:8000/docs", timeout=2)
            print("✅ Backend reiniciado com sucesso!")
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)

    yield

    # Cleanup: mata o backend ao final
    backend_process.terminate()


# Desabilita o bloqueio de "Private Network Access" do Chromium.
# Sem isso, requests de localhost:3000 → localhost:8000 falham com "Failed to fetch"
# porque o Chrome bloqueia chamadas entre origens privadas que não retornam o header
# Access-Control-Allow-Private-Network: true (que o backend não envia).
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": [
            "--disable-features=BlockInsecurePrivateNetworkRequests",
            "--disable-web-security",
        ],
    }
