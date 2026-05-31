# =============================================================================
# ARQUIVO: tests/e2e/test_fluxo_usuario.py
#
# O QUE SÃO TESTES E2E? Testes "End-to-End" (de ponta a ponta) simulam
# um usuário de verdade usando o navegador. O robô (Playwright) abre o
# Chrome, clica nos botões, preenche formulários e verifica resultados,
# igualzinho um humano faria manualmente.
#
# PRÉ-REQUISITOS PARA RODAR ESTES TESTES:
#   1. O servidor backend deve estar rodando em http://127.0.0.1:8000
#      Comando para subir o backend:  uvicorn backend.main:app --reload
#
#   2. O servidor frontend será iniciado AUTOMATICAMENTE por uma fixture
#      deste arquivo (na porta 3000). Nenhuma ação manual é necessária.
#
#   3. O Playwright e o navegador Chromium devem estar instalados:
#      pip install pytest-playwright
#      playwright install chromium
#
# COMO RODAR ESTE ARQUIVO:
#   pytest tests/e2e/test_fluxo_usuario.py -v
#
# PARA VER O NAVEGADOR ABRINDO (modo visível, não headless):
#   pytest tests/e2e/test_fluxo_usuario.py -v --headed
#
# =============================================================================

import os
import time
import subprocess
from pathlib import Path

import pytest
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.API.criptografia import senha_hash


# =============================================================================
# CONFIGURAÇÕES
# Mude estas constantes se precisar usar portas diferentes
# =============================================================================

# URL do servidor backend FastAPI
URL_BACKEND = "http://127.0.0.1:8000"

# Porta em que vamos subir o servidor do frontend para os testes
PORTA_FRONTEND = 3000

# URL completa do frontend (montada com a porta acima)
URL_FRONTEND = f"http://127.0.0.1:{PORTA_FRONTEND}"

# Caminho para a pasta 'frontend' do projeto.
# __file__ é este arquivo Python. Subimos 2 níveis para chegar na raiz do projeto.
CAMINHO_FRONTEND = os.path.join(
    os.path.dirname(__file__),   # pasta: tests/e2e/
    "..",                         # sobe para: tests/
    "..",                         # sobe para: raiz do projeto
    "frontend"                    # entra em: frontend/
)

# =============================================================================
# DADOS DO USUÁRIO DE TESTE
# Este usuário será criado no backend via API antes dos testes que precisam dele.
# =============================================================================
EMAIL_USUARIO_TESTE    = "teste.e2e.sistema@gmail.com"
SENHA_USUARIO_TESTE    = "senha_do_robo_123"
NOME_USUARIO_TESTE     = "Robozinho de Teste"
TIPO_DESPESA_CADASTRO  = "Conta de Luz E2E"    # texto que verificaremos na tabela

# Sufixo único por execução para evitar conflitos 409 (item duplicado no backend real)
# Sufixo único removido — receita, produto e serviço não têm testes E2E
# (já cobertos completamente em testes de integração)


# =============================================================================
# FIXTURE: servidor_frontend
#
# O que é uma fixture no pytest? É uma função especial que roda ANTES dos testes
# para preparar o ambiente. O decorator @pytest.fixture avisa o pytest disso.
#
# scope="module" significa que este servidor sobe UMA VEZ para todos os testes
# deste arquivo, em vez de subir e descer para cada teste (mais eficiente).
#
# autouse=True significa que esta fixture roda automaticamente, sem precisar
# ser declarada como parâmetro em cada função de teste.
# =============================================================================
@pytest.fixture(scope="module", autouse=True)
def servidor_frontend():
    """
    Sobe um servidor HTTP simples para servir os arquivos da pasta 'frontend'.
    Python já vem com um servidor HTTP embutido: 'python -m http.server'.
    Usamos subprocess.Popen para rodá-lo em segundo plano (não bloqueia o pytest).
    """

    # Caminho absoluto da pasta frontend (resolve os ".." do CAMINHO_FRONTEND)
    caminho_absoluto = os.path.abspath(CAMINHO_FRONTEND)

    print(f"\n▶ Iniciando servidor do frontend em: {URL_FRONTEND}")
    print(f"  Servindo arquivos de: {caminho_absoluto}")

    # Inicia o processo do servidor HTTP em segundo plano
    # stdout/stderr=subprocess.DEVNULL silencia as mensagens do servidor
    processo_servidor = subprocess.Popen(
        ["python", "-m", "http.server", str(PORTA_FRONTEND)],  # comando a executar
        cwd=caminho_absoluto,                                   # pasta de trabalho
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Aguarda 1 segundo para o servidor subir completamente antes de começar os testes
    time.sleep(1)

    # 'yield' pausa a fixture aqui e entrega o controle para os testes.
    # Tudo abaixo do yield roda DEPOIS que todos os testes terminam (limpeza).
    yield

    # ---- LIMPEZA: Encerra o servidor ao fim de todos os testes ----
    print("\n■ Encerrando servidor do frontend...")
    processo_servidor.terminate()


# =============================================================================
# FUNÇÃO AUXILIAR: inserção direta no banco (bypass do ZeroBounce)
# Usada quando a API /cadastro_usuario retorna erro por causa da validação
# de email externa. Conecta direto no cpr.sqlite e cria o usuário lá.
# =============================================================================
def _criar_usuario_direto_no_banco():
    """
    Cria o usuário de teste diretamente no arquivo SQLite, sem passar pela API.
    Isso contorna o ZeroBounce quando a cota está esgotada ou a API está fora do ar.
    """
    # O banco fica na raiz do projeto (2 níveis acima de tests/e2e/)
    raiz_projeto = Path(__file__).parent.parent.parent
    caminho_banco = raiz_projeto / "cpr.sqlite"

    engine = create_engine(
        f"sqlite:///{caminho_banco}",
        connect_args={"check_same_thread": False},
    )

    Session = sessionmaker(bind=engine)

    with Session() as session:
        # Garante que o esquema está atualizado — o cpr.sqlite pode ter sido
        # criado com uma versão mais antiga do modelo (sem token_reset_senha e
        # expiracao_do_token). Se essas colunas não existirem, o backend vai
        # quebrar em qualquer query de login. O ALTER TABLE falha silenciosamente
        # se a coluna já existir — esse é o comportamento correto.
        for migrar in [
            "ALTER TABLE usuarios ADD COLUMN token_reset_senha VARCHAR(100)",
            "ALTER TABLE usuarios ADD COLUMN expiracao_do_token DATETIME",
        ]:
            try:
                session.execute(text(migrar))
                session.commit()
            except Exception:
                pass  # coluna já existe, ignora

        # Usa SQL puro pra não depender do ORM na busca de existência
        ja_existe = session.execute(
            text("SELECT id FROM usuarios WHERE email = :email"),
            {"email": EMAIL_USUARIO_TESTE}
        ).scalar_one_or_none()

        if not ja_existe:
            session.execute(
                text("""
                    INSERT INTO usuarios
                        (nome_completo, email, senha, numero_telefone, cep, estado, cidade, bairro, logradouro)
                    VALUES
                        (:nome, :email, :senha, :tel, :cep, :estado, :cidade, :bairro, :logradouro)
                """),
                {
                    "nome":      NOME_USUARIO_TESTE,
                    "email":     EMAIL_USUARIO_TESTE,
                    "senha":     senha_hash(SENHA_USUARIO_TESTE),
                    "tel":       "91988889999",
                    "cep":       "68450000",
                    "estado":    "PA",
                    "cidade":    "Belém",
                    "bairro":    "Centro",
                    "logradouro": "Rua dos Testes Automatizados, 1",
                }
            )
            session.commit()

    # Libera TODAS as conexões do pool imediatamente.
    # Se o engine ficar com conexão aberta pro cpr.sqlite, o backend uvicorn
    # pode travar em writes seguintes (SQLite exclusive lock).
    engine.dispose()


# =============================================================================
# FUNÇÃO AUXILIAR (não é um teste, não é uma fixture — é uma função normal)
# Cria o usuário de teste diretamente na API para podermos fazer login real.
# =============================================================================
def criar_usuario_no_backend():
    """
    Tenta criar o usuário de teste no backend.

    Cenários tratados:
    - 200/201 → criado agora, continua
    - 409     → já existia de rodada anterior, continua
    - qualquer outro erro (401, 500, etc.) → tenta login; se funcionar, continua;
                                             se não, pula o teste com mensagem clara
    - ConnectionError → backend fora do ar, pula o teste

    Obs: erros 401/500 geralmente indicam que a validação de email do backend
    (ZeroBounce) está com problema — seja email de domínio inválido, cota
    esgotada ou a API externa retornando formato inesperado.
    Solução: crie o usuário manualmente uma vez com o backend rodando e a
    validação funcionando. Nas próximas execuções, o 409 vai garantir que
    o teste continue normalmente.
    """

    payload_usuario = {
        "nome_completo":   NOME_USUARIO_TESTE,
        "email":           EMAIL_USUARIO_TESTE,
        "senha":           SENHA_USUARIO_TESTE,
        "numero_telefone": "91988889999",
        "cep":             "68450000",
        "estado":          "PA",
        "cidade":          "Belém",
        "bairro":          "Centro",
        "logradouro":      "Rua dos Testes Automatizados, 1"
    }

    try:
        resposta = requests.post(
            f"{URL_BACKEND}/cadastro_usuario",
            json=payload_usuario,
            timeout=5
        )

        if resposta.status_code in [200, 201, 409]:
            return  # tudo certo — criado agora ou já existia

        # Qualquer erro (401 = email inválido, 500 = ZeroBounce quebrou, etc.)
        # Antes de desistir, tenta fazer login — o usuário pode ter sido criado
        # numa execução anterior quando a validação ainda estava funcionando.
        print(f"\n⚠️  Cadastro retornou {resposta.status_code}. "
              "Tentando login pra ver se o usuário já existe de rodada anterior...")
        try:
            resp_login = requests.post(
                f"{URL_BACKEND}/login",
                json={"email": EMAIL_USUARIO_TESTE, "senha": SENHA_USUARIO_TESTE},
                timeout=5
            )
            if resp_login.status_code == 200:
                print("✔ Login funcionou — usuário existe. Continuando.")
                return
        except requests.exceptions.ConnectionError:
            pass

        # API não funciona e usuário não existe — cria direto no banco SQLite
        print("API bloqueada pelo ZeroBounce. Criando usuário direto no banco SQLite...")
        _criar_usuario_direto_no_banco()
        print("✔ Usuário criado direto no banco. Continuando.")

    except requests.exceptions.ConnectionError:
        pytest.skip(
            f"Backend não está acessível em {URL_BACKEND}. "
            "Suba o servidor com: uvicorn backend.main:app --reload"
        )


# =============================================================================
# TESTE E2E 1: FLUXO DE LOGIN
#
# Objetivo: Verificar que o robô consegue abrir o sistema, navegar até o
#           formulário de login, preencher as credenciais e acessar a
#           área principal (layout do usuário).
#
# Estratégia: usamos o login especial 'admin/admin' que existe no código
#             do frontend (login.js) para evitar dependência do backend.
#             Isso torna o teste mais simples e rápido.
# =============================================================================
def test_fluxo_login_admin_com_sucesso(page):
    """
    Simula um usuário abrindo o sistema, clicando em 'Acessar',
    preenchendo 'admin' no email e senha, e verificando que o
    layout principal (com o menu lateral) foi carregado.

    O parâmetro 'page' é fornecido automaticamente pelo pytest-playwright.
    Ele representa uma aba do navegador controlada pelo robô.
    """

    # ------------------------------------------------------------------
    # PASSO 1: O robô abre a página inicial do sistema no navegador
    # ------------------------------------------------------------------
    page.goto(f"{URL_FRONTEND}/index.html")

    # Aguarda o elemento da página inicial aparecer antes de continuar
    # '#container-paginaInicial' é o ID do div renderizado por paginaInicial.js
    page.wait_for_selector("#container-paginaInicial", timeout=5000)

    print("✔ Página inicial carregada.")

    # ------------------------------------------------------------------
    # PASSO 2: O robô clica no botão "Acessar" para ir para a tela de login
    # O seletor '.btn-login' é a classe CSS do botão definida em paginaInicial.js
    # ------------------------------------------------------------------
    page.click(".btn-login")

    # Aguarda o formulário de login aparecer na tela
    # '#container-login' é o ID do div renderizado por login.js
    page.wait_for_selector("#container-login", timeout=5000)

    print("✔ Tela de login carregada.")

    # ------------------------------------------------------------------
    # PASSO 3: O robô preenche o campo de e-mail com 'admin'
    # '#email' é o ID do input definido em login.js
    # ------------------------------------------------------------------
    page.fill("#email", "admin")  # Digita 'admin' no campo de e-mail

    # ------------------------------------------------------------------
    # PASSO 4: O robô preenche o campo de senha com 'admin'
    # '#senha' é o ID do input de senha definido em login.js
    # ------------------------------------------------------------------
    page.fill("#senha", "admin")  # Digita 'admin' no campo de senha

    # ------------------------------------------------------------------
    # PASSO 5: O robô clica no botão "Entrar"
    # '#btn-logar' é o ID do botão definido em login.js
    # Ao clicar, a função fazerLogin() é chamada. Como email='admin' e
    # senha='admin', o código entra no atalho especial que bypassa a API
    # e chama renderizarPagina('usuarioLayout') diretamente.
    # ------------------------------------------------------------------
    page.click("#btn-logar")

    # ------------------------------------------------------------------
    # PASSO 6: Verificar que o layout principal foi carregado com sucesso
    # '#usuarioLayout' é o ID do div renderizado por usuarioLayout.js
    # Como é uma SPA (Single Page Application), a URL não muda —
    # apenas o conteúdo da página é trocado dinamicamente.
    # Por isso verificamos o conteúdo, não a URL.
    # ------------------------------------------------------------------
    page.wait_for_selector("#usuarioLayout", timeout=5000)

    print("✔ Layout do usuário carregado — login realizado com sucesso!")

    # Verifica que o layout está visível na tela
    layout_esta_visivel = page.is_visible("#usuarioLayout")
    assert layout_esta_visivel, (
        "O layout do usuário (#usuarioLayout) não está visível após o login. "
        "Algo deu errado no fluxo de login com admin/admin."
    )

    # Confirma que o botão de 'Contas a Pagar' do menu lateral existe
    # (é um indicador extra de que estamos na área logada do sistema)
    botao_despesas_existe = page.is_visible("#btn-sectionDespesa")
    assert botao_despesas_existe, (
        "O botão 'Contas a Pagar' (#btn-sectionDespesa) não foi encontrado no menu. "
        "O layout pode não ter sido renderizado corretamente."
    )


# =============================================================================
# TESTE E2E 2: FLUXO DE CADASTRO DE DESPESA
#
# Objetivo: Verificar que o robô consegue preencher o formulário de despesa,
#           salvar com sucesso e depois confirmar que o registro aparece
#           na tabela de listagem de despesas.
#
# Estratégia: criamos um usuário real via API, fazemos login real com esse
#             usuário e interagimos com o formulário de despesa. Assim,
#             a chamada à API de cadastro de despesa tem um usuário válido.
# =============================================================================
def test_fluxo_cadastro_de_despesa_aparece_na_tabela(page):
    """
    Simula um usuário logado que:
    1. Navega para a tela de nova despesa
    2. Preenche os campos obrigatórios
    3. Clica em salvar
    4. Confirma o alerta de sucesso
    5. Navega para a lista de despesas
    6. Verifica que a despesa cadastrada aparece na tabela
    """

    # ------------------------------------------------------------------
    # PRÉ-REQUISITO: Garantir que o usuário de teste existe no backend
    # Esta função chama a API para criar o usuário (ou confirma que já existe)
    # Se o backend não estiver rodando, o teste é pulado automaticamente.
    # ------------------------------------------------------------------
    criar_usuario_no_backend()

    # ------------------------------------------------------------------
    # PASSO 1: O robô abre a página inicial do sistema
    # ------------------------------------------------------------------
    page.goto(f"{URL_FRONTEND}/index.html")
    page.wait_for_selector("#container-paginaInicial", timeout=5000)

    # ------------------------------------------------------------------
    # PASSO 2: O robô clica em "Acessar" e vai para a tela de login
    # ------------------------------------------------------------------
    page.click(".btn-login")
    page.wait_for_selector("#container-login", timeout=5000)

    # ------------------------------------------------------------------
    # PASSO 3: O robô preenche o login com as credenciais do usuário de teste
    # Usamos o e-mail e senha reais (não o atalho admin/admin),
    # pois precisamos que o e-mail fique salvo no localStorage para a
    # chamada de API ao cadastrar a despesa funcionar corretamente.
    # ------------------------------------------------------------------
    page.fill("#email", EMAIL_USUARIO_TESTE)
    page.fill("#senha", SENHA_USUARIO_TESTE)

    # ------------------------------------------------------------------
    # PASSO 4: O robô clica em "Entrar" para fazer o login real via API
    # ------------------------------------------------------------------
    page.click("#btn-logar")

    # Aguarda o layout do usuário aparecer (confirma que o login funcionou)
    page.wait_for_selector("#usuarioLayout", timeout=8000)
    print(f"✔ Login realizado como: {EMAIL_USUARIO_TESTE}")

    # ------------------------------------------------------------------
    # PASSO 5: O robô clica no botão "Contas a Pagar" no menu lateral
    # para ir à seção de despesas onde fica o botão de cadastro.
    # '#btn-sectionDespesa' está definido em usuarioLayout.js
    # ------------------------------------------------------------------
    page.click("#btn-sectionDespesa")

    # Aguarda o botão de adicionar despesa aparecer na tela
    # '#btn-adicionarDespesa' está definido em despesaPage.js
    page.wait_for_selector("#btn-adicionarDespesa", timeout=5000)
    print("✔ Seção de despesas carregada.")

    # ------------------------------------------------------------------
    # PASSO 6: O robô clica em "+ Cadastrar Despesa" para abrir o formulário
    # ------------------------------------------------------------------
    page.click("#btn-adicionarDespesa")

    # Aguarda o formulário de cadastro de despesa aparecer
    # '#container-cadastroDespesa' está definido em cadastroDespesaPage.js
    page.wait_for_selector("#container-cadastroDespesa", timeout=5000)
    print("✔ Formulário de cadastro de despesa aberto.")

    # ------------------------------------------------------------------
    # PASSO 7: O robô preenche os campos do formulário de despesa
    # Os IDs dos campos estão definidos em cadastroDespesaPage.js
    # ------------------------------------------------------------------

    # Campo: Tipo ou nome da Despesa
    page.fill("#input-tipoDespesa", TIPO_DESPESA_CADASTRO)

    # Campo: Descrição
    page.fill("#input-descricaoDespesa", "Despesa criada pelo robô de teste automatizado")

    # Campo: Valor Total (precisa ser maior que 0 — validado no frontend)
    page.fill("#input-valorTotalDespesa", "350.00")

    # Campo: Forma de Pagamento (select/dropdown)
    # O select tem id='opcoes-pagamentosDespesa' e precisamos selecionar pelo value
    page.select_option("#opcoes-pagamentosDespesa", value="Pix")

    # Campo: Valor pago por unidade
    page.fill("#input-valorUnidadeDespesa", "350.00")

    print(f"✔ Formulário preenchido. Tipo da despesa: '{TIPO_DESPESA_CADASTRO}'")

    # ------------------------------------------------------------------
    # PASSO 8: Configurar o robô para aceitar o alerta (alert) automaticamente
    # Quando clicamos em salvar, o JavaScript chama alert('Despesa cadastrada com sucesso!')
    # O Playwright precisa estar "ouvindo" o alerta ANTES de ele aparecer.
    # page.once("dialog", ...) registra um ouvinte para o próximo dialog.
    # ------------------------------------------------------------------
    page.once("dialog", lambda dialog: dialog.accept())
    # ↑ Isso diz: "quando aparecer um alert/confirm/prompt, aceita automaticamente"

    # ------------------------------------------------------------------
    # PASSO 9: O robô clica no botão "Cadastrar" para salvar a despesa
    # '#cadastrarDespesa' está definido em cadastroDespesaPage.js
    # O click dispara a função cadastrarDespesa() que chama a API
    # ------------------------------------------------------------------
    page.click("#cadastrarDespesa")
    print("✔ Botão 'Cadastrar' clicado. Aguardando resposta da API...")

    # Aguarda o layout do usuário renderizar novamente.
    # Após o sucesso, o código JS chama renderizarPagina('usuarioLayout')
    # que substitui o formulário pelo layout com menu lateral.
    page.wait_for_selector("#usuarioLayout", timeout=8000)
    print("✔ Despesa cadastrada! Redirecionado para o layout principal.")

    # ------------------------------------------------------------------
    # PASSO 10: O robô navega para a seção de despesas para ver a tabela
    # ------------------------------------------------------------------
    page.click("#btn-sectionDespesa")

    # Aguarda a tabela de despesas aparecer na tela
    # '#tabela-despesa' está definido em despesaPage.js
    page.wait_for_selector("#tabela-despesa", timeout=5000)

    # A função carregarDespesas() é chamada com setTimeout de 1000ms,
    # então aguardamos um pouco mais para garantir que a tabela foi preenchida
    page.wait_for_timeout(2000)  # espera 2 segundos (2000 milissegundos)

    print("✔ Tabela de despesas carregada. Verificando se a despesa aparece...")

    # ------------------------------------------------------------------
    # PASSO 11: Verificar que o texto da despesa está na tabela
    # Usamos page.locator para buscar qualquer elemento dentro da tabela
    # que contenha o texto que digitamos.
    # ------------------------------------------------------------------
    # Busca dentro do tbody da tabela por uma célula com o texto da despesa
    celula_com_despesa = page.locator(
        f"#tabela-despesa tbody td:has-text('{TIPO_DESPESA_CADASTRO}')"
    )

    # Verifica se pelo menos um elemento foi encontrado
    quantidade_encontrada = celula_com_despesa.count()

    assert quantidade_encontrada >= 1, (
        f"A despesa '{TIPO_DESPESA_CADASTRO}' deveria aparecer na tabela, "
        f"mas não foi encontrada. "
        f"Verifique se o backend está rodando e se o usuário '{EMAIL_USUARIO_TESTE}' "
        f"foi criado corretamente."
    )

    print(f"✔ Despesa '{TIPO_DESPESA_CADASTRO}' encontrada na tabela! Teste concluído com sucesso.")





# =============================================================================
# TESTE E2E 4: FLUXO DE LISTAGEM DE RECEITAS
#
# Objetivo: Verificar que o menu de receitas carrega e exibe a tabela corretamente.
# =============================================================================
@pytest.mark.e2e
def test_fluxo_navegacao_receitas(page):
    """
    Simula um usuário logado navegando para a seção de receitas
    e verificando que a tabela de receitas foi carregada.
    """
    criar_usuario_no_backend()

    # Login
    page.goto(f"{URL_FRONTEND}/index.html")
    page.wait_for_selector("#container-paginaInicial", timeout=5000)
    page.click(".btn-login")
    page.wait_for_selector("#container-login", timeout=5000)
    page.fill("#email", EMAIL_USUARIO_TESTE)
    page.fill("#senha", SENHA_USUARIO_TESTE)
    page.click("#btn-logar")
    page.wait_for_selector("#usuarioLayout", timeout=8000)
    print(f"✔ Login realizado como: {EMAIL_USUARIO_TESTE}")

    # Navega para receitas
    page.click("#btn-sectionReceita")
    page.wait_for_selector("#container-receita", timeout=5000)
    print("✔ Seção de receitas carregada.")

    # Verifica que a tabela de receitas existe
    tabela_existe = page.is_visible("#tabela-receita")
    assert tabela_existe, "Tabela de receitas não foi encontrada na página"
    print("✔ Tabela de receitas carregada com sucesso!")


# =============================================================================
# TESTE E2E 5: FLUXO DE LISTAGEM DE SERVIÇOS
#
# Objetivo: Verificar que o menu de serviços carrega e exibe a tabela corretamente.
# =============================================================================
@pytest.mark.e2e
def test_fluxo_navegacao_servicos(page):
    """
    Simula um usuário logado navegando para a seção de serviços
    e verificando que a tabela de serviços foi carregada.
    """
    criar_usuario_no_backend()

    # Login
    page.goto(f"{URL_FRONTEND}/index.html")
    page.wait_for_selector("#container-paginaInicial", timeout=5000)
    page.click(".btn-login")
    page.wait_for_selector("#container-login", timeout=5000)
    page.fill("#email", EMAIL_USUARIO_TESTE)
    page.fill("#senha", SENHA_USUARIO_TESTE)
    page.click("#btn-logar")
    page.wait_for_selector("#usuarioLayout", timeout=8000)
    print(f"✔ Login realizado como: {EMAIL_USUARIO_TESTE}")

    # Navega para serviços (já está na seção de produtos/serviços)
    # Clica na aba "Serviço" para mostrar a tabela de serviços
    page.click("#btn-sectionProdutosServicos")
    page.wait_for_selector("#container-produtoServico", timeout=5000)
    # Clica no botão da aba Serviço
    page.locator("#opcoes-tabelas button:has-text('Serviço')").click()
    page.wait_for_selector("#tabela-servicos", timeout=5000)
    print("✔ Aba de serviços carregada.")

    # Verifica que a tabela de serviços existe
    tabela_existe = page.is_visible("#tabela-servicos")
    assert tabela_existe, "Tabela de serviços não foi encontrada na página"
    print("✔ Tabela de serviços carregada com sucesso!")
