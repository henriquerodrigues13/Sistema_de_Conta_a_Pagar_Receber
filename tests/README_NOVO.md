**Documentação dos Testes**

---

## O Que É Este Projeto?

Este é um **sistema web** que ajuda empresas a gerenciar contas a pagar e receber. Pense nisto como um **livro de anotações digital** onde você:
- Cadastra usuários
- Cria produtos e serviços
- Registra transações
- Controla pagamentos

Roda na internet usando **FastAPI** (framework Python).

---

## Como o Projeto Está Organizado

```
seu-projeto/
├── backend/
│   ├── API/
│   │   ├── criptografia.py      ← Protege senhas
│   │   ├── validações.py        ← Verifica dados (email)
│   │   └── routes.py            ← Rotas da API
│   ├── models/
│   │   ├── database.py          ← Banco de dados
│   │   ├── engine.py            ← Tabelas/estrutura
│   │   ├── logs.py              ← Registros
│   │   └── backup_db.py         ← Cópia de segurança (implementado, aguardando ativação)
│   └── main.py                  ← Inicia a aplicação
│
└── tests/
    ├── conftest.py              ← Configuração dos testes (fixtures, banco in-memory)
    ├── unit/
    │   ├── test_criptografia.py ← Testa senhas
    │   ├── test_smoke.py        ← Testa se a API está online
    │   └── test_backup.py       ← Testa lógica de rotacionamento de backups
    └── integracao/
        ├── test_api.py          ← Testa funcionalidades completas
        └── test_validacoes.py   ← Testa validações de dados
```

---

## Os 5 Tipos de Testes

### 1. Testes de Criptografia
**Arquivo:** `test_criptografia.py`

Verifica se as senhas estão sendo protegidas corretamente.

```
Você digita:  senha_secreta_123
Sistema salva: $2b$10$xK8x3J9... (hash bcrypt)

Testes verificam:
  ✓ Hash é diferente da senha original
  ✓ Senha correta é reconhecida pelo sistema
  ✓ Senha errada é rejeitada pelo sistema
```

```bash
pytest tests/unit/test_criptografia.py
```

---

### 2. Testes de Saúde (Smoke Tests)
**Arquivo:** `test_smoke.py`

Verifica se a aplicação sobe e inicializa corretamente.

```
✓ Documentação Swagger disponível em /docs
✓ Banco de dados é inicializado no lifespan (init_db chamado)
✓ Nenhum erro crítico no startup
```

```bash
pytest tests/unit/test_smoke.py
```

---

### 3. Testes de Backup
**Arquivo:** `test_backup.py`

Verifica a lógica de rotacionamento de arquivos de backup.
Usa `tmp_path` (fixture nativa do pytest) para criar arquivos temporários
sem tocar no filesystem real — tudo é limpo automaticamente ao final.

```
✓ Com 5 backups: remove os 2 mais antigos, mantém os 3 mais recentes
✓ Com 2 backups: não remove nada (abaixo do limite de 3)
```

```bash
pytest tests/unit/test_backup.py
```

---

### 4. Testes de Validação
**Arquivo:** `test_validacoes.py`

Verifica se os dados que entram no sistema estão corretos.

```
EMAIL:
  ✓ Serviço externo responde "valid"   → retorna True
  ✗ Serviço externo responde "invalid" → retorna False
  ✗ Erro de conexão                    → retorna False (graceful degradation)

PYDANTIC:
  ✗ Campos obrigatórios ausentes → ValidationError
  ✗ Email inválido no payload    → HTTP 422
```

```bash
pytest tests/integracao/test_validacoes.py
```

---

### 5. Testes de API (Integração)
**Arquivo:** `test_api.py`

Testa as funcionalidades completas do sistema, do início ao fim.

```
USUÁRIOS:
  ✓ POST /cadastro_usuario         → cria usuário, senha não exposta na resposta
  ✓ POST /cadastro_usuario         → email duplicado retorna 409
  ✓ POST /login (senha correta)    → 200
  ✓ POST /login (senha errada)     → 401
  ✓ POST /login (usuário inexiste) → 404

PRODUTOS:
  ✓ POST /cadastro_produtos (usuário existe)    → sucesso
  ✓ POST /cadastro_produtos (usuário inexiste)  → 404
  ✓ POST /cadastro_produtos (duplicado)         → 409
  ✓ GET  /get_produtos_usuario                  → lista paginada com headers X-Total-Items e X-Total-Pages
  ✓ DELETE /delete_produto (existe)             → marca como indisponível, some da listagem
  ✓ DELETE /delete_produto (inexistente)        → 404
  ✓ PATCH /update_produto (dados válidos)       → atualiza com sucesso
  ✓ PATCH /update_produto (produto inexistente) → 404
  ✓ PATCH /update_produto (payload vazio)       → 400

SERVIÇOS:
  ✓ POST /cadastro_servico (usuário existe)    → sucesso
  ✓ POST /cadastro_servico (usuário inexiste)  → 404
  ✓ POST /cadastro_servico (duplicado)         → 409
  ✓ GET  /get_servico_usuario                  → lista paginada com headers X-Total-Items e X-Total-Pages
  ✓ DELETE /delete_servico (existe)            → marca como deletado, some da listagem
  ✓ DELETE /delete_servico (inexistente)       → 404
  ✓ PATCH /update_servico (dados válidos)      → atualiza com sucesso
  ✓ PATCH /update_servico (serviço inexiste)   → 404
  ✓ PATCH /update_servico (payload vazio)      → 400
```

```bash
pytest tests/integracao/test_api.py
```

---

## Como Executar os Testes

### Requisitos
```bash
pip install -r requirements.txt
pip install -e .
```

### Rodar todos os testes
```bash
pytest
```

### Rodar por tipo
```bash
pytest tests/unit/
pytest tests/integracao/
```

### Rodar com mais detalhes
```bash
pytest -v -s
```

---

## O conftest.py — Como Funciona o Isolamento

O `conftest.py` garante que cada teste roda de forma completamente isolada:

- Cria um banco SQLite **em memória** exclusivo por teste via `override_get_session`
- Ao final de cada teste o banco é descartado — nenhum dado vaza entre testes
- A `validacao_email` é **mockada automaticamente** em todos os testes de integração (fixture `autouse`), evitando chamadas reais à API do ZeroBounce

---

## Bug Corrigido — DELETE sem 404

As rotas `DELETE /delete_produto` e `DELETE /delete_servico` tinham um bug onde o HTTP 404 nunca era retornado, mesmo para registros inexistentes. O motivo é que `session.execute(update(...))` sempre retorna um objeto truthy, fazendo o `if` ser sempre verdadeiro. A correção foi substituir pela busca com `select` antes de executar o update. Os testes `test_delete_produto_inexistente` e `test_delete_servico_inexistente` documentam e cobrem esse comportamento.

---

## Resultado Esperado ao Rodar Todos os Testes

```
tests/unit/test_criptografia.py::test_criptografia_da_senha PASSED
tests/unit/test_smoke.py::test_docs_available PASSED
tests/unit/test_smoke.py::test_docs_with_db_fixture PASSED
tests/unit/test_smoke.py::test_api_subida_e_chamada_init_db_no_lifespan PASSED
tests/unit/test_backup.py::test_backup_rotacionamento PASSED
tests/unit/test_backup.py::test_backup_rotacionamento_menos_de_3 PASSED
tests/integracao/test_validacoes.py::test_validacao_email_com_resposta_valid PASSED
tests/integracao/test_validacoes.py::test_validacao_email_com_resposta_invalid PASSED
tests/integracao/test_validacoes.py::test_pydantic_rejeita_campos_obrigatorios_ausentes PASSED
tests/integracao/test_validacoes.py::test_api_rejeita_payload_invalido_com_http_422 PASSED
tests/integracao/test_validacoes.py::test_validacao_email_erro_http PASSED
tests/integracao/test_api.py::test_cadastro_usuario_com_sucesso PASSED
tests/integracao/test_api.py::test_cadastro_usuario_email_duplicado PASSED
tests/integracao/test_api.py::test_fluxo_login_comportamento_real PASSED
tests/integracao/test_api.py::test_cadastro_produto_com_sucesso PASSED
tests/integracao/test_api.py::test_cadastro_produto_usuario_inexistente PASSED
tests/integracao/test_api.py::test_cadastro_produto_duplicado PASSED
tests/integracao/test_api.py::test_get_produtos_usuario PASSED
tests/integracao/test_api.py::test_delete_produto PASSED
tests/integracao/test_api.py::test_delete_produto_inexistente PASSED
tests/integracao/test_api.py::test_update_produto_com_sucesso PASSED
tests/integracao/test_api.py::test_update_produto_inexistente PASSED
tests/integracao/test_api.py::test_update_produto_payload_vazio PASSED
tests/integracao/test_api.py::test_cadastro_servico_com_sucesso PASSED
tests/integracao/test_api.py::test_cadastro_servico_usuario_inexistente PASSED
tests/integracao/test_api.py::test_cadastro_servico_duplicado PASSED
tests/integracao/test_api.py::test_get_servicos_usuario PASSED
tests/integracao/test_api.py::test_delete_servico PASSED
tests/integracao/test_api.py::test_delete_servico_inexistente PASSED
tests/integracao/test_api.py::test_update_servico_com_sucesso PASSED
tests/integracao/test_api.py::test_update_servico_payload_vazio PASSED
tests/integracao/test_api.py::test_update_servico_inexistente PASSED

================== 32 passed ==================
```

---

## O Que Cada Arquivo Testa

| Arquivo | Cobre | Tipo |
|---|---|---|
| `test_criptografia.py` | Hash e verificação de senhas | Unitário |
| `test_smoke.py` | API online, init_db no startup | Smoke |
| `test_backup.py` | Rotacionamento de arquivos de backup | Unitário |
| `test_validacoes.py` | Validação de email, Pydantic 422 | Unitário/Integração |
| `test_api.py` | Usuários, login, produtos e serviços (CRUD completo) | Integração |

---

## O Que Ainda Não Tem Teste

- **Backup — criação de arquivo e envio por email**: as funções `backup_sqlite()` e `enviar_backup()` têm caminhos hardcoded internamente, o que torna o mock frágil. Para testá-las de forma confiável é necessário refatorar o `backup_db.py` para aceitar os caminhos como parâmetro
- Rotas de **receitas e despesas** — ainda comentadas no código
- **Testes E2E** via Playwright (frontend + backend)