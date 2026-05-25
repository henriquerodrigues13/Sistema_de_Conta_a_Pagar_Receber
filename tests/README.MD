# DOCUMENTAÇÃO OFICIAL DA SUÍTE DE TESTES

**Sistema de Contas a Pagar e Receber**  
**Disciplina:** Teoria de Sistemas Aplicada a Informática  
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

- Fase Inicial**
- Testes básicos de criptografia ✅
- Testes de integração de API ✅
- Testes de validação de dados ✅
- Testes smoke (saúde da aplicação) ✅

**Próximas Fases Planejadas:**
- 🔄 Testes de performance e carga
- 🔄 Testes de segurança aprofundados
- 🔄 Testes E2E com navegador real
- 🔄 Testes de relatórios

---

## 2. ARQUITETURA DOS TESTES

### 2.1 Estrutura de Diretórios

```
projeto/
├── conftest.py                    ← Configuração global de testes
├── pytest.ini                     ← Configuração do pytest
│
├── tests/
│   ├── unit/
│   │   ├── test_criptografia.py   ← Testes unitários de hash
│   │   └── test_smoke.py          ← Testes básicos de saúde
│   │
│   └── integracao/
│       ├── test_api.py            ← Testes de endpoints
│       └── test_validacoes.py     ← Testes de validações
│
└── backend/
    ├── API/
    │   ├── routes.py
    │   ├── criptografia.py
    │   └── validações.py
    └── models/
        ├── engine.py
        └── database.py
```

### 2.2 Fluxo de Execução dos Testes

```
pytest (comando)
    ↓
conftest.py (preparação)
    ├─ Cria banco de dados em memória
    ├─ Cria tabelas (usuario, fornecedores)
    ├─ Configura mock de email
    └─ Configura dependências
    ↓
test_*.py (testes)
    ├─ test_unitário (rápido, isolado)
    ├─ test_integração (completo, com BD)
    └─ test_smoke (saúde geral)
    ↓
Resultado (✅ ou ❌)
```

---

## 3. ARQUIVOS DE TESTE

### 3.1 `conftest.py` - Configuração Global

**Propósito:** Definir fixtures compartilhadas entre todos os testes.

**Principais Componentes:**

#### 3.1.1 Fixture `app`

```python
@pytest.fixture(scope="session")
def app():
    return backend_main.app
```

- **O que faz:** Retorna a instância da aplicação FastAPI
- **Escopo:** `session` (criada uma vez por sessão de testes)
- **Usada por:** Outras fixtures

#### 3.1.2 Fixture `client`

```python
@pytest.fixture()
def client(app, override_get_session):
    with TestClient(app) as c:
        yield c
```

- **O que faz:** Cria um cliente HTTP para fazer requisições aos endpoints
- **Escopo:** `function` (novo para cada teste)
- **Como usar no teste:**
  ```python
  def test_algo(client):
      response = client.post("/cadastro_usuario", json=dados)
  ```

#### 3.1.3 Fixture `override_get_session`

```python
@pytest.fixture()
def override_get_session(app):
    engine = create_engine(
        "sqlite:///:memory:", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(...)
    
    Base.metadata.create_all(bind=engine)
    
    # ... código de override ...
    
    yield
    
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
```

- **O que faz:**
  1. Cria um banco de dados SQLite em memória
  2. Cria todas as tabelas (usuario, fornecedores)
  3. Substitui a dependência `get_session` do backend
  4. Limpa tudo após cada teste
  
- **Por que é importante:**
  - Cada teste tem seu próprio banco isolado
  - Testes não interferem uns com outros
  - Sem efeitos colaterais de dados

- **StaticPool?**
  - `StaticPool` força o SQLite em memória a manter a mesma conexão
  - Sem isso, cada requisição criava um novo banco zerado
  - Solução para o erro "no such table: usuario"

#### 3.1.4 Fixture `mock_validacao_email`

```python
@pytest.fixture(autouse=True)
def mock_validacao_email():
    with patch("backend.API.routes.validacao_email") as mock:
        mock.return_value = True  
        yield mock
```

- **O que faz:** Simula a validação de email via API externa
- **Por que é importante:** Não chama a API real do ZeroBounce durante testes
- **`autouse=True`:** Aplicada automaticamente em todos os testes

#### 3.1.5 Fixture `set_env`

```python
@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ.setdefault("TESTING", "1")
    os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
    yield
```

- **O que faz:** Define variáveis de ambiente para testes
- **`autouse=True`:** Executada automaticamente uma vez por sessão

---

### 3.2 `test_criptografia.py` - Testes Unitários

**Tipo:** Teste Unitário  
**Localização:** `tests/unit/test_criptografia.py`  
**Objetivo:** Validar a criptografia de senhas com bcrypt

#### 3.2.1 Teste: `test_criptografia_da_senha`

```python
def test_criptografia_da_senha():
    senha_original = "123456"
    
    hash_gerado = senha_hash(senha_original)
    
    # VALIDAÇÃO 1: Hash != Senha (criptografia funcionando)
    assert hash_gerado != senha_original
    
    # VALIDAÇÃO 2: Senha correta retorna True
    assert verificar_senha(senha_original, hash_gerado) is True
    
    # VALIDAÇÃO 3: Senha errada retorna False
    assert verificar_senha("senha_errada", hash_gerado) is False
```

**O que testa:**
1. ✅ Hash é diferente da senha (não texto puro)
2. ✅ Função `verificar_senha` funciona com senha correta
3. ✅ Função `verificar_senha` rejeita senha incorreta

**Resultado esperado:** ✅ PASSOU

**Por que é importante:** Garante segurança das senhas

---

### 3.3 `test_smoke.py` - Testes de Saúde

**Tipo:** Teste de Saúde (Smoke Test)  
**Localização:** `tests/unit/test_smoke.py`  
**Objetivo:** Verificar se a aplicação está "viva"

#### 3.3.1 Teste: `test_docs_available`

```python
def test_docs_available(client):
    resp = client.get("/docs")
    assert resp.status_code == 200
```

- **O que testa:** Se a documentação Swagger está disponível
- **Por que importa:** Indica que a aplicação subiu corretamente
- **Resultado esperado:** Status 200

#### 3.3.2 Teste: `test_docs_with_db_fixture`

```python
def test_docs_with_db_fixture(client, override_get_session):
    resp = client.get("/docs")
    assert resp.status_code == 200
```

- **O que testa:** Se a documentação funciona COM banco de testes
- **Por que importa:** Valida que as fixtures não quebram a aplicação

---

#### 3.3.3 Teste: `test_api_subida_e_chamada_init_db_no_lifespan`

```python
def test_api_subida_e_chamada_init_db_no_lifespan():
    with patch("backend.main.database.init_db") as mock_init_db:
        with TestClient(main_modulo.app) as client:
            response = client.get("/docs")
            assert response.status_code == 200
            assert mock_init_db.called is True
```

- **O que testa:** Verifica que a aplicação sobe e que `database.init_db()` é chamada durante o processo de startup/lifespan.
- **Como funciona:** o teste intercepta (`patch`) `backend.main.database.init_db` antes de instanciar o `TestClient` e então verifica se a chamada ocorreu quando o `TestClient` ativou o `lifespan` da aplicação.
- **Por que é importante:** garante que a rotina de inicialização do banco (criação de tabelas, migrações ou checks) seja executada automaticamente no startup da aplicação. Útil para detectar regressões onde o `lifespan` não esteja disparando corretamente.


### 3.4 `test_validacoes.py` - Testes de Validação

**Tipo:** Teste Unitário + Integração  
**Localização:** `tests/integracao/test_validacoes.py`  
**Objetivo:** Validar regras de entrada de dados

#### 3.4.1 Teste: `test_validacao_email_com_resposta_valid`

```python
def test_validacao_email_com_resposta_valid():
    patch.stopall()
    with patch.object(validacoes_modulo, "requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "valid"}
        mock_requests.post.return_value = mock_response

        resultado = validacao_email("pedro.teste@ufpa.br")
        
        assert resultado is True
        assert mock_requests.post.call_count == 1
```

- **O que testa:** Se email válido retorna True
- **Mock:** Simula resposta da API de validação
- **Validações:**
  - Resultado é True ✅
  - API foi chamada uma vez ✅

#### 3.4.2 Teste: `test_validacao_email_com_resposta_invalid`

```python
def test_validacao_email_com_resposta_invalid():
    # ... setup de mock ...
    mock_response.json.return_value = {"status": "invalid"}
    
    resultado = validacao_email("email_falso@provedor.com")
    
    assert resultado is False
    assert mock_requests.post.call_count == 1
```

- **O que testa:** Se email inválido retorna False
- **Resultado esperado:** ❌ False

#### 3.4.3 Teste: `test_pydantic_rejeita_campos_obrigatorios_ausentes`

```python
def test_pydantic_rejeita_campos_obrigatorios_ausentes():
    payload_incompleto = {
        "nome_completo": "Pedro Lucas Leão"
    }
    
    with pytest.raises(ValidationError):
        cadastro_usuario.model_validate(payload_incompleto)
```

- **O que testa:** Se Pydantic rejeita dados incompletos
- **Como funciona:** Espera que `ValidationError` seja lançado
- **Resultado esperado:** Exceção é lançada ✅

#### 3.4.4 Teste: `test_api_rejeita_payload_invalido_com_http_422`

```python
def test_api_rejeita_payload_invalido_com_http_422(client):
    payload_com_erro = {
        "nome_completo": "Pedro Lucas Leão",
        "email": "email_invalido_sem_arroba",
        "senha": "123"
    }
    
    response = client.post("/cadastro_usuario", json=payload_com_erro)
    
    assert response.status_code == 422
```

- **O que testa:** Se a API retorna HTTP 422 para dados inválidos
- **HTTP 422:** Unprocessable Entity (Pydantic rejeitou)
- **Resultado esperado:** Status 422 ✅

---

### 3.5 `test_api.py` - Testes de Integração

**Tipo:** Teste de Integração  
**Localização:** `tests/integracao/test_api.py`  
**Objetivo:** Testar fluxos completos de API

#### 3.5.1 Teste: `test_cadastro_usuario_com_sucesso`

```python
def test_cadastro_usuario_com_sucesso(client, override_get_session):
    payload = {
        "nome_completo": "Pedro Lucas Leão",
        "email": "pedro.teste@ufpa.br",
        "senha": "senha_secreta_123",
        "numero_telefone": "91988888888",
        "cep": "68450000",
        "estado": "PA",
        "cidade": "Baião",
        "bairro": "Centro",
        "logradouro": "Rua Principal, 123"
    }
    
    response = client.post("/cadastro_usuario", json=payload)
    
    assert response.status_code in [200, 201]
    
    dados_resposta = response.json()
    assert dados_resposta["nome_completo"] == "Pedro Lucas Leão"
    assert dados_resposta.get("senha") != "senha_secreta_123"
```

**O que testa:**
1. ✅ POST /cadastro_usuario retorna 200 ou 201
2. ✅ Resposta contém nome_completo
3. ✅ Resposta NÃO contém senha em texto puro (segurança!)

**Fluxo testado:**
- Frontend envia dados
- API valida
- API criptografa senha
- API insere no banco
- API retorna resposta

#### 3.5.2 Teste: `test_fluxo_login_comportamento_real`

```python
def test_fluxo_login_comportamento_real(client, override_get_session):
    # PASSO 1: Cadastra usuário
    payload_cadastro = { ... }
    client.post("/cadastro_usuario", json=payload_cadastro)

    # CENÁRIO A: Login com credenciais corretas → 200
    dados_login_correto = {
        "email": "pedro.teste@ufpa.br",
        "senha": "senha_secreta_123"
    }
    response_sucesso = client.post("/login", json=dados_login_correto)
    assert response_sucesso.status_code == 200

    # CENÁRIO B: Login com senha errada → 401
    dados_senha_errada = {
        "email": "pedro.teste@ufpa.br",
        "senha": "senha_errada_qualquer"
    }
    response_401 = client.post("/login", json=dados_senha_errada)
    assert response_401.status_code == 401

    # CENÁRIO C: Login com usuário inexistente → 404
    dados_usuario_fantasma = {
        "email": "nao_existe_no_sistema@ufpa.br",
        "senha": "qualquer_senha"
    }
    response_404 = client.post("/login", json=dados_usuario_fantasma)
    assert response_404.status_code == 404
```

**O que testa:**
1. ✅ Login bem-sucedido retorna 200
2. ✅ Senha incorreta retorna 401
3. ✅ Usuário inexistente retorna 404

**Fluxos testados:**
- **Happy Path:** Login com credenciais corretas
- **Unhappy Path 1:** Senha incorreta
- **Unhappy Path 2:** Usuário não existe

---

## 4. COMO EXECUTAR OS TESTES

### 4.1 Pré-requisitos

```bash
# Verificar Python
python --version
# Esperado: Python 3.8+

# Instalar dependências
pip install -e .
pip install pytest pytest-asyncio httpx
```

### 4.2 Executar Todos os Testes

```bash
pytest
```

**Output esperado:**
```
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
```

### 4.3 Executar Testes Específicos

```bash
# Apenas testes unitários
pytest tests/unit/

# Apenas testes de integração
pytest tests/integracao/

# Um teste específico
pytest tests/unit/test_criptografia.py::test_criptografia_da_senha -v

# Com mais verbosidade
pytest -v -s

# Com relatório HTML
pytest --html=report.html --self-contained-html

# Ver coverage (cobertura de código)
pytest --cov=backend --cov-report=html
```

### 4.4 Opções Úteis

```bash
# -v: Verbose (mais detalhes)
# -s: Show prints (mostrar print statements)
# -x: Stop on first failure (parar no primeiro erro)
# -k: Filtrar por nome (pytest -k "email")
# --tb=short: Traceback curto
# --durations=5: Testes mais lentos
```

---

## 5. ESTRUTURA E PADRÕES

### 5.1 Padrão AAA (Arrange-Act-Assert)

Todos os testes seguem este padrão:

```python
def test_exemplo(client):
    # ARRANGE: Preparar dados
    dados = {"nome": "Pedro", "email": "pedro@email.com"}
    
    # ACT: Executar ação
    response = client.post("/cadastro_usuario", json=dados)
    
    # ASSERT: Verificar resultado
    assert response.status_code == 200
```

### 5.2 Nomeação de Testes

- Começam com `test_`
- Nome descritivo
- Indicam o que está sendo testado

```
✅ test_cadastro_usuario_com_sucesso
✅ test_validacao_email_rejeita_invalido
❌ test_1
❌ test_algo
```

### 5.3 Asserções Claras

```python
# ✅ BOM: Mensagem clara
assert response.status_code == 200, \
    f"Esperado 200, obtido {response.status_code}"

# ✅ BOM: Múltiplas validações
assert "nome_completo" in response.json()
assert response.status_code == 200

# ❌ EVITAR: Sem contexto
assert response
assert dados
```

---

## 6. PROBLEMAS COMUNS E SOLUÇÕES

### 6.1 Erro: "no such table: usuario"

**Causa:** Banco não foi criado ou tabelas não existem

**Solução:**
```python
# Verificar conftest.py tem:
Base.metadata.create_all(bind=engine)

# Usar StaticPool:
poolclass=StaticPool
```

### 6.2 Erro: "ModuleNotFoundError: No module named 'backend'"

**Causa:** sys.path não está configurado

**Solução:**
```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

### 6.3 Erro: "Fixture 'client' not found"

**Causa:** conftest.py não está no lugar certo

**Solução:**
- Coloque `conftest.py` na raiz do projeto
- Não coloque dentro de `tests/`

### 6.4 Testes Lentos

**Causa:** Criando banco real ou chamando APIs externas

**Solução:**
- Usar fixtures de mock
- Usar banco em memória
- Usar `patch` para APIs externas

---

## 7. PRÓXIMAS ETAPAS

### 7.1 Testes Planejados (v0.2)

- [ ] Testes de listagem de receitas
- [ ] Testes de deleção de lançamentos
- [ ] Testes de edição de usuários
- [ ] Testes de cálculo de multa/juros
- [ ] Testes de relatórios

### 7.2 Melhorias Planejadas

- [ ] Aumentar cobertura de código (meta: 70%+)
- [ ] Adicionar testes de performance
- [ ] Implementar testes de segurança 
- [ ] Adicionar testes E2E com Playwright

### 7.3 Métricas de Qualidade

```
Cobertura de Código:  42% (v0.1)
Cobertura esperada:   70%+ (v1.0)

Testes Smoke (Fumaça):   3 ✅ Concluídos (Saúde da API, Docs e Lifespan)
Testes Unitários:        5 ✅ Concluídos (Criptografia, Regras Pydantic e Mocks de e-mail)
Testes de Integração:    2 ... pendente
```

---

## 8. REFERÊNCIA RÁPIDA

### Executar Testes
```bash
pytest                              # Todos
pytest -v                           # Com detalhes
pytest tests/unit/                  # Apenas unitários
pytest -k "email"                   # Filtrar por nome
pytest --cov=backend                # Com coverage
```

### Estrutura de um Teste
```python
def test_nome_descritivo(client, override_get_session):
    # Arrange
    dados = {...}
    
    # Act
    response = client.post("/endpoint", json=dados)
    
    # Assert
    assert response.status_code == 200
```

### Fixtures Disponíveis
```python
def test_algo(client, override_get_session, app, anyio_backend):
    # client: Cliente HTTP para requisições
    # override_get_session: Banco em memória isolado
    # app: Instância da FastAPI
    # anyio_backend: Para testes async
```

---

## APÊNDICE: Arquivos Relacionados

- `conftest.py` - Configuração de testes
- `pytest.ini` - Configuração do pytest
- `requirements.txt` - Dependências
- `RELATORIO_TESTES_UFPA.md` - Resultados dos testes

---

**Documentação em construção v0.1**  
**Última atualização:** Maio de 2026  
**Próxima revisão:** Quando novos testes forem adicionados