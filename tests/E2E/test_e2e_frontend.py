import pytest
from playwright.sync_api import sync_playwright

def test_login_sucesso():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Abrir frontend
        page.goto("http://127.0.0.1:3000/index.html")

        # Garantir que estamos na tela de login
        page.wait_for_selector("#btn-logar")

        # Preencher login
        page.fill("#email", "admin")
        page.fill("#senha", "admin")
        page.click("#btn-logar")

        # Capturar alerta
        def handle_dialog(dialog):
            assert "Bem-vindo" in dialog.message or "usuarioLayout" in page.content()
            dialog.dismiss()
        page.on("dialog", handle_dialog)

        browser.close()


def test_login_incorreto():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("http://localhost:8000/frontend/index.html")
        page.wait_for_selector("#btn-logar")

        page.fill("#email", "teste@example.com")
        page.fill("#senha", "senhaErrada")
        page.click("#btn-logar")

        def handle_dialog(dialog):
            assert "senha incorreta" in dialog.message.lower()
            dialog.dismiss()
        page.on("dialog", handle_dialog)

        browser.close()


def test_cadastro_usuario():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("http://localhost:8000/frontend/index.html")

        # Renderizar tela de cadastro
        page.click("#cadastrar button")  # botão "Cadastre-se"
        page.wait_for_selector("#btn-cadastrarUsuario")

        # Preencher cadastro
        page.fill("#nome-completo", "Pedro Teste")
        page.fill("#bairro", "Centro")
        page.fill("#email", "pedro@example.com")
        page.fill("#estado", "PA")
        page.fill("#telefone", "91999999999")
        page.fill("#cidade", "Cametá")
        page.fill("#cep", "68400000")
        page.fill("#logradouro", "Rua Principal")
        page.fill("#senha", "senhaSegura123")
        page.fill("#conf-senha", "senhaSegura123")
        page.click("#btn-cadastrarUsuario")

        def handle_dialog(dialog):
            assert "Usuario cadastrado com sucesso" in dialog.message
            dialog.dismiss()
        page.on("dialog", handle_dialog)

        browser.close()
