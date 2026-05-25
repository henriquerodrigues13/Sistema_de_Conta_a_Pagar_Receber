Markdown
# DOCUMENTAÇÃO OFICIAL DA SUÍTE DE TESTES

## SUMÁRIO

- [1. Introdução](#1-introdução)
- [2. Arquitetura dos Testes](#2-arquitetura-dos-testes)
- [3. Arquivos de Teste](#3-arquivos-de-teste)
    - [3.1 conftest.py - Configuração Global](#31-conftestpy---configuração-global)
    - [3.2 test_criptografia.py - Testes Unitários](#32-test_criptografiapy---testes-unitários)
    - [3.3 test_smoke.py - Testes de Saúde](#33-test_smokepy---testes-de-saúde)
    - [3.4 test_validacoes.py - Testes de Validação](#34-test_validacoespy---testes-de-validação)
    - [3.5 test_api.py - Testes de Integração](#35-test_apipy---testes-de-integração)
- [4. Como Executar os Testes](#4-como-executar-os-testes)
- [5. Estrutura e Padrões](#5-estrutura-e-padrões)
- [6. Problemas Comuns e Soluções](#6-problemas-comuns-e-soluções)
- [7. Próximas Etapas](#7-próximas-etapas)
- [8. Referência Rápida](#8-referência-rápida)
- [Apêndice: Arquivos Relacionados](#apêndice-arquivos-relacionados)


**Sistema de Contas a Pagar e Receber** **Disciplina:** Teoria de Sistemas Aplicada a Informática  
**Curso:** Sistemas de Informação - UFPA  
**Data:** Maio de 2026  
**Status:** 📝 Em Construção

---

## 1. INTRODUÇÃO

Esta documentação descreve a suíte de testes do sistema de contas a pagar e receber. Os testes foram organizados para validar diferentes camadas da aplicação: desde funções unitárias até fluxos completos de integração.

### 1.1 Objetivo

Os testes têm como objetivos:
- ✅ Validar a corretude do código
- ✅ Garantir que dados são armazenados corretamente
- ✅ Verificar segurança (hash de senhas, validações)
- ✅ Testar fluxos completos de usuário
- ✅ Detectar regressões em novas versões


### 1.2 Status Atual

- Testes básicos de criptografia ✅
- Testes de integração de API ✅
- Testes de validação de dados ✅
- Testes smoke (saúde da aplicação) ✅


---

## 2. ARQUITETURA DOS TESTES

### 2.1 Estrutura de Diretórios

Sistema_de_Conta_a_Pagar_Receber/
├── backend/
│   ├── API/
│   └── models/
├── tests/
│   ├── unit/
│   │   ├── test_criptografia.py
│   │   └── test_smoke.py
│   └── integracao/
│       ├── test_api.py
│       └── test_validacoes.py
├── conftest.py
├── requirements.txt
└── ...


### 2.2 Fluxo de Execução dos Testes

pytest (comando)
↓
conftest.py (preparação)
├─ Cria banco de dados SQLite em memória RAM
├─ Cria automaticamnete TODAS as tabelas do ecossistema (Base.metadata)
├─ Configura mock de email (API externa isolada)
└─ Substitui dependência get_session globalmente
↓
test_*.py (testes)
├─ test_unitário (rápido, isolado)
├─ test_integração (completo, focado em endpoints)
└─ test_smoke (saúde geral da API)
↓
Resultado (✅ ou ❌)


---

## 3. ARQUIVOS DE TESTE

### 3.1 `conftest.py` - Configuração Global

**Propósito:** Definir fixtures compartilhadas entre todos os testes e isolar o ambiente real de desenvolvimento do ambiente de testes.

**Principais Componentes:**

#### 3.1.1 Fixture `app`

```python
@pytest.fixture(scope="session")
def app():
    return backend_main.app
O que faz: Retorna a instância da aplicação FastAPI.

Escopo: session (criada uma única vez por sessão de testes).

Usada por: Outras fixtures do sistema.

3.1.2 Fixture client
Python
@pytest.fixture()
def client(app, override_get_session):
    with TestClient(app) as c:
        yield c
O que faz: Cria um cliente síncrono HTTP nativo para disparar requisições aos endpoints da API.

Escopo: function (um cliente novo e zerado para cada função de teste).

Como usar no teste:

Python
def test_algo(client):
    response = client.post("/cadastro_usuario", json=dados)
3.1.3 Fixture override_get_session
Python
@pytest.fixture()
def override_get_session(app):
    engine = create_engine(
        "sqlite:///:memory:", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Cria a estrutura completa de tabelas mapeadas no ecossistema
    Base.metadata.create_all(bind=engine)
    
    def _get_test_session():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[database_module.get_session] = _get_test_session
    yield
    
    app.dependency_overrides.clear()
    engine.dispose()
O que faz:

Instancia um mecanismo de banco de dados SQLite volátil em memória RAM dedicado.

Executa a criação de todas as tabelas do projeto (Usuários, Contas, Fornecedores, etc.) mapeadas sob a classe declarativa Base.

Substitui de forma transparente a dependência get_session injetada nas rotas do FastAPI pela sessão de testes.

Limpa as sobreposições de dependência (clear()) e descarta a conexão do banco de dados ao final do ciclo de execução.

Por que é importante:

Isolamento Total: Evita o acoplamento de estados. Cada teste roda em um ambiente limpo, impedindo que dados cadastrados em um teste quebrem outro.

Proteção contra Erros de Relacionamento: Ao gerar a árvore de tabelas unificada via Base.metadata.create_all, elimina falhas de restrições de chaves estrangeiras (Foreign Key) ou tabelas inexistentes ao testar fluxos integrados.

StaticPool?

Mantém a mesma conexão ativa em memória compartilhada pelas threads do teste. Sem isso, cada requisição HTTP disparada pelo TestClient destruiria e recriaria um banco zerado, estourando erros operacionais.

3.1.4 Fixture mock_validacao_email
Python
@pytest.fixture(autouse=True)
def mock_validacao_email():
    with patch("backend.API.routes.validacao_email") as mock:
        mock.return_value = True  
        yield mock
O que faz: Intercepta e simula com sucesso chamadas para serviços externos de e-mail ou microsserviços de validação.

Por que é importante: Garante autonomia e velocidade na execução local dos testes, eliminando dependência de rede ou cota de requisições de APIs externas.

autouse=True: Ativada silenciosamente em todos os contextos de testes.

3.1.5 Fixture set_env
Python
@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ.setdefault("TESTING", "1")
    os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
    yield
O que faz: Força as configurações globais do ambiente operacional a reconhecerem o modo de teste.

3.2 test_criptografia.py - Testes Unitários
Tipo: Teste Unitário

Localização: tests/unit/test_criptografia.py

Objetivo: Validar a criptografia de senhas com bcrypt

3.2.1 Teste: test_criptografia_da_senha
Python
def test_criptografia_da_senha():
    senha_original = "123456"
    
    hash_gerado = senha_hash(senha_original)
    
    # VALIDAÇÃO 1: Hash != Senha (criptografia funcionando)
    assert hash_gerado != senha_original
    
    # VALIDAÇÃO 2: Senha correta retorna True
    assert verificar_senha(senha_original, hash_gerado) is True
    
    # VALIDAÇÃO 3: Senha errada retorna False
    assert verificar_senha("senha_errada", hash_gerado) is False
O que testa:

✅ Hash é diferente da senha (não texto puro)

✅ Função verificar_senha funciona com senha correta

✅ Função verificar_senha rejeita senha incorreta

Resultado esperado: ✅ PASSOU

Por que é importante: Garante segurança das senhas

3.3 test_smoke.py - Testes de Saúde
Tipo: Teste de Saúde (Smoke Test)

Localização: tests/unit/test_smoke.py

Objetivo: Verificar se a aplicação está "viva"

3.3.1 Teste: test_docs_available
Python
def test_docs_available(client):
    resp = client.get("/docs")
    assert resp.status_code == 200
O que testa: Se a documentação Swagger está disponível

Por que importa: Indica que a aplicação subiu corretamente

Resultado esperado: Status 200

3.3.2 Teste: test_docs_with_db_fixture
Python
def test_docs_with_db_fixture(client, override_get_session):
    resp = client.get("/docs")
    assert resp.status_code == 200
O que testa: Se a documentação funciona COM banco de testes

Por que importa: Valida que as fixtures não quebram a aplicação

3.3.3 Teste: test_api_subida_e_chamada_init_db_no_lifespan
Python
def test_api_subida_e_chamada_init_db_no_lifespan():
    with patch("backend.main.database.init_db") as mock_init_db:
        with TestClient(main_modulo.app) as client:
            response = client.get("/docs")
            assert response.status_code == 200
            assert mock_init_db.called is True
O que testa: Verifica que a aplicação sobe e que database.init_db() é chamada durante o processo de startup/lifespan.

Como funciona: o teste intercepta (patch) backend.main.database.init_db antes de instanciar o TestClient e então verifica se a chamada ocorreu quando o TestClient ativou o lifespan da aplicação.

Por que é importante: garante que a rotina de inicialização do banco (criação de tabelas, migrações ou checks) seja executada automaticamente no startup da aplicação. Útil para detectar regressões onde o lifespan não esteja disparando corretamente.

3.4 test_validacoes.py - Testes de Validação
Tipo: Teste de Entrada de Dados

Localização: tests/integracao/test_validacoes.py

Objetivo: Validar regras de integridade e payloads na API

Contém testes para:

Validação de formato de e-mail (mockado).

Rejeição de propriedades obrigatórias nulas via esquemas do Pydantic.

Tratamento e retorno do código padrão HTTP 422 Unprocessable Entity para payloads malformados estruturalmente.

3.5 test_api.py - Testes de Integração
Tipo: Teste de Integração

Localização: tests/integracao/test_api.py

Objetivo: Testar ciclos completos de endpoints simulando o comportamento de clientes reais

Contém testes para:

Criação e persistência de novos registros de usuários no ecossistema isolado.

Fluxo de autenticação e login (Verificação de credenciais corretas, senhas inválidas e restrição a contas inexistentes).

4. COMO EXECUTAR OS TESTES
4.1 Pré-requisitos
Bash
# Verificar Python
python --version
# Esperado: Python 3.8+

# Instalar dependências em modo editável
pip install -e .
pip install pytest pytest-asyncio httpx
4.2 Executar Todos os Testes
Bash
pytest
Output esperado:

tests/unit/test_criptografia.py::test_criptografia_da_senha PASSED
tests/unit/test_smoke.py::test_docs_available PASSED
tests/unit/test_smoke.py::test_docs_with_db_fixture PASSED
tests/integracao/test_validacoes.py::test_validacao_email_com_resposta_valid PASSED
tests/integracao/test_validacoes.py::test_validacao_email_com_resposta_invalid PASSED
tests/integracao/test_validacoes.py::test_pydantic_rejeita_campos_obrigatorios_ausentes PASSED
tests/integracao/test_validacoes.py::test_api_rejeita_payload_invalido_com_http_422 PASSED
tests/integracao/test_api.py::test_cadastro_usuario_com_sucesso PASSED
tests/integracao/test_api.py::test_fluxo_login_comportamento_real PASSED

================== 9 passed in 0.45s ==================
4.3 Executar Testes Específicos
Bash
# Apenas testes unitários
pytest tests/unit/

# Apenas testes de integração
pytest tests/integracao/

# Um teste específico
pytest tests/unit/test_criptografia.py::test_criptografia_da_senha -v

# Com mais verbosidade e prints expostos
pytest -v -s

# Com relatório HTML
pytest --html=report.html --self-contained-html

# Ver coverage (cobertura de código)
pytest --cov=backend --cov-report=html
5. ESTRUTURA E PADRÕES
5.1 Padrão AAA (Arrange-Act-Assert)
Todos os testes seguem rigorosamente este padrão:

Python
def test_exemplo(client):
    # ARRANGE: Preparar dados e payloads
    dados = {"nome": "Pedro Lucas", "email": "pedro@email.com"}
    
    # ACT: Executar ação / Disparar chamada HTTP
    response = client.post("/cadastro_usuario", json=dados)
    
    # ASSERT: Verificar e validar resultados esperados
    assert response.status_code == 200
5.2 Nomeação de Testes
Devem, obrigatoriamente, iniciar com o prefixo test_.

Nomes descritivos detalhados.

✅ test_cadastro_usuario_com_sucesso
✅ test_validacao_email_rejeita_invalido
❌ test_1
❌ test_algo
6. PROBLEMAS COMUNS E SOLUÇÕES
6.1 Erro: "no such table: usuario" (ou outra tabela do CPR)
Causa: Estrutura relacional do SQLAlchemy não carregada na memória RAM.

Solução: Garantir que o conftest.py execute a criação mapeada do ecossistema inteiro:

Python
Base.metadata.create_all(bind=engine)
6.2 Erro: "ModuleNotFoundError: No module named 'backend'"
Causa: O caminho do diretório de desenvolvimento local não foi mapeado no escopo do sys.path.

Solução: Rodar a instalação editável (pip install -e .) na pasta raiz ou incluir explicitamente no início dos scripts:

Python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
7. PRÓXIMAS ETAPAS
Testes e melhorias futuras de cobertura automatizada de código do fluxo de caixa e regras de validação financeira (CPR) serão documentados conforme forem implementados pela equipe de desenvolvimento.

8. REFERÊNCIA RÁPIDA
Executar Testes
Bash
pytest                              # Executa toda a suíte
pytest -v                           # Detalhado com logs
pytest tests/unit/                  # Executa apenas unitários
pytest -k "email"                   # Filtra testes por palavra-chave
pytest --cov=backend                # Relatório de cobertura de código
APÊNDICE: Arquivos Relacionados
conftest.py - Configurações de ambientes de injeção e fixtures globais.

pytest.ini - Parâmetros e marcas customizadas do framework.

requirements.txt - Gerenciamento de dependências.

RELATORIO_TESTES_UFPA.md - Compilação de relatórios acadêmicos.

Documentação oficial atualizada v0.2 Última modificação: Maio de 2026

Revisão técnica: Sincronizado com arquitetura global de tabelas do banco em memória.