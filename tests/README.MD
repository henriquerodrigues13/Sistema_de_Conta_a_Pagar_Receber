# Documentação da Suite de Testes

**Sistema:** Contas a Pagar/Receber  
**Última atualização:** 2026-05-31  
**Suite Status:** ✅ **64 passed + 4 xfailed = 68 testes**

---

## Instalação

```bash
# 1. Ative o virtualenv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux/Mac

# 2. Instale as dependências (só precisa fazer uma vez)
pip install -e ".[test]"
playwright install chromium     # Para E2E tests (necessário uma única vez)
```

## Como rodar os testes

```bash
# SUITE COMPLETA — 68 testes (unit + integração + E2E com navegador visível)
pytest -v --headed

# SEM NAVEGADOR — unit + integração apenas (mais rápido)
pytest tests/unit/ tests/integracao/ -v

# SÓ E2E — com navegador
pytest tests/e2e/ -v --headed

# SÓ unit
pytest tests/unit/ -v

# SÓ integração
pytest tests/integracao/ -v
```

**Importante:** O comando `pytest -v --headed` automaticamente:
- Mata qualquer uvicorn rodando
- Sobe um novo backend limpo (via `conftest.py`)
- Roda todos os 68 testes (unit, integração, E2E)
- E2E testes aparecem no Chromium (não headless)
- Mata o backend ao final

---

## Estrutura dos arquivos

```
tests/
├── unit/                              testes de funções isoladas (sem API, sem banco)
│   ├── test_backup.py                 lógica de rotação de backups
│   ├── test_criptografia.py           hash e verificação de senha
│   ├── test_validacoes.py             validação de email e schemas Pydantic
│   └── test_smoke.py                  verifica se a API sobe corretamente
│
├── integracao/                        testes que chamam a API de verdade (banco em memória)
│   ├── test_api.py                    usuários, login, produtos, vendas, receitas, recuperação de senha
│   ├── test_servicos.py               CRUD completo de serviços
│   ├── test_despesas.py               CRUD completo de despesas
│   └── test_endpoints_com_bug.py      endpoints com bugs conhecidos (marcados como xfail)
│
├── e2e/                               testes com navegador real (requer Playwright)
│   ├── conftest.py                    configura Chromium e reinicia backend automaticamente
│   └── test_fluxo_usuario.py          4 fluxos: login, despesa, receitas, serviços
│
└── conftest.py (global)               fixtures compartilhadas entre unit, integração e E2E
```

---

## O que cada arquivo testa

### Testes unitários

| Arquivo | O que testa |
|---------|-------------|
| `test_criptografia.py` | Hash da senha é diferente da original; senha certa → True; senha errada → False |
| `test_validacoes.py` | API externa retorna "valid" → True; retorna "invalid" → False; conexão cai → False; Pydantic rejeita campos faltando → 422 |
| `test_backup.py` | Rotacionamento mantém no máximo 3 backups; com menos de 3 não deleta nada |
| `test_smoke.py` | GET /docs retorna 200; init_db() é chamado no startup |

### Testes de integração — test_api.py

**Usuários e login:**
- Cadastro com sucesso → 200, nome correto na resposta, senha não aparece
- Email duplicado → 409
- Login com senha certa → 200
- Login com senha errada → 401
- Login com usuário inexistente → 404

**Recuperação de senha:**
- Usuário existe → 201 (email mockado, não envia de verdade)
- Usuário não existe → 404
- Reset com token válido (não expirado) → 200
- Reset com token inexistente → 404
- Reset com token expirado → 400

**Produtos:**
- Cadastro com sucesso
- Cadastro com usuário inexistente → 404
- Produto duplicado → 409
- Listagem com headers X-Total-Items e X-Total-Pages
- Atualização de valor e estoque
- Atualização com payload vazio → 400
- Atualização de produto inexistente → 404
- Deleção e confirmação pela listagem

**Fornecedores:**
- GET /get_fornecedor → 200 (lista vazia no banco de testes)

**Vendas de produto e serviço:**
- Listagem por usuário com headers de paginação
- Atualização pelo identificador real (nanoid)
- Deleção e confirmação
- Venda de serviço com sucesso
- Venda de serviço com vendedor inexistente → 404
- Venda de serviço com serviço inexistente → 404
- Venda de serviço aparece na listagem

**Receitas:**
- Cadastro com sucesso
- Dados inválidos (email e data errados) → 422
- Listagem por email do recebedor
- Atualização de valor e observação
- Deleção e confirmação

### Testes de integração — test_endpoints_com_bug.py

Esses testes documentam o comportamento **esperado** de endpoints que têm bugs no fonte.
Todos são marcados com `@pytest.mark.xfail` — falham esperadamente até os bugs serem corrigidos.
Quando o dev corrigir um bug, o teste vai mostrar **XPASS** (passou inesperadamente) — sinal pra remover o xfail.

| Teste | Bug | Comportamento esperado → atual |
|-------|-----|-------------------------------|
| `test_cadastro_nota_fiscal_usuario_existente_deve_retornar_sucesso` | BUG-001 | 200 → 404 |
| `test_cadastro_nota_fiscal_usuario_inexistente_deve_retornar_404` | BUG-001 | 404 → 200 |
| `test_get_produtos_fornecedor_retorna_lista_por_cnpj` | BUG-002 | 200 → 422 |
| `test_get_servicos_fornecedor_retorna_lista_por_cnpj` | BUG-003 | 200 → 422 |

### Testes de integração — test_servicos.py

- Cadastro com sucesso
- Cadastro com usuário inexistente → 404
- Serviço duplicado → 409
- Listagem com paginação
- Usuário sem serviços → lista vazia
- Atualização de valor
- Atualização com payload vazio → 400
- Atualização de serviço inexistente → 404
- Deleção e confirmação
- Deleção de serviço inexistente → 404

### Testes de integração — test_despesas.py

- Cadastro com sucesso
- Cadastro com pagador inexistente → 404
- Payload incompleto → 422
- Listagem com paginação
- Usuário sem despesas → lista vazia
- Atualização pelo identificador real
- Atualização com payload vazio → 400
- Atualização de identificador inválido → 404
- Deleção e confirmação
- Deleção de identificador inválido → 404

### Testes E2E — test_fluxo_usuario.py

| Teste | O que simula no navegador |
|-------|--------------------------|
| `test_fluxo_login_admin_com_sucesso` | Abre o sistema, clica em login, entra com admin/admin, verifica o layout |
| `test_fluxo_cadastro_de_despesa_aparece_na_tabela` | Login real, preenche formulário de despesa, verifica na tabela |
| `test_fluxo_navegacao_receitas` | Login real, navega para receitas, verifica tabela carregada |
| `test_fluxo_navegacao_servicos` | Login real, navega para serviços (com aba), verifica tabela |

---

## Como os testes de integração funcionam

Os testes **não tocam o banco de dados real**. O `conftest.py` na raiz cria um banco SQLite em memória RAM para cada teste. Quando o teste termina, o banco é descartado. Isso significa que:

- Cada teste começa com banco limpo
- Um teste não afeta o outro
- Não precisa configurar nenhum banco antes de rodar

A validação de email (que chamaria a API do ZeroBounce de verdade) também é mockada automaticamente, então os testes funcionam sem internet.

---

## Testes E2E — requer configuração especial

Os testes em `tests/e2e/` abrem um navegador de verdade e clicam na tela. Para rodar:

```bash
# Dependências extras
pip install pytest-playwright
playwright install chromium

# Subir o backend antes de rodar
uvicorn backend.main:app --reload

# Rodar os testes E2E
pytest tests/e2e/ -v
```

Se o backend não estiver rodando, os testes E2E são **pulados automaticamente** (não falham).

---

## Endpoints sem teste (e o motivo)

Todos os 29 endpoints têm testes. Os 3 com bugs têm testes com `xfail` que documentam o comportamento esperado e falham de forma controlada até os bugs serem corrigidos.

| Endpoint | Status |
|----------|--------|
| `POST /cadastro_nota_fiscal` | `xfail` — BUG-001 (lógica invertida) |
| `GET /get_produtos_fornecedor/{cnpj}` | `xfail` — BUG-002 (parâmetro errado) |
| `GET /get_servicos_fornecedor/{cnpj}` | `xfail` — BUG-003 (parâmetro errado) |

---

## Contagem de testes

| Tipo | Quantidade |
|------|-----------|
| Unitários | 11 |
| Integração | 53 (49 passando + 4 xfail) |
| E2E | 4 (login, despesa, receita, serviço) |
| **Total** | **68** |

Cobertura de endpoints: **29 de 29** (100% com testes, 3 falhando por bug no fonte)

---

## Problemas comuns

**"ModuleNotFoundError: No module named 'backend'"**  
Rode `pip install -e .` na raiz do projeto.

**"no such table: usuarios"**  
Provavelmente o `override_get_session` não está sendo passado como parâmetro da função de teste.

**Testes de reset de senha falhando**  
Verifique se o mock do `fast_mail.send_message` está correto. Precisa ser `AsyncMock` porque o método é assíncrono.

---

## Configuração em máquinas diferentes (CI/CD)

**Windows:**
```bash
.venv\Scripts\activate
pip install -e ".[test]"
playwright install chromium
pytest -v --headed
```

**Linux/Mac:**
```bash
source .venv/bin/activate
pip install -e ".[test]"
playwright install chromium
pytest -v --headed
```

O `pyproject.toml` declara todas as dependências, então `pip install -e ".[test]"` instala tudo automaticamente em qualquer PC.

---

## Arquivos relacionados

- `conftest.py` — fixtures globais (banco em memória, mock de email)
- `BUG_REPORT.md` — bugs encontrados no código de produção
- `CHANGELOG_TESTES.md` — o que foi mudado na suite e por quê
- `pyproject.toml` — configuração do pytest e dependências
- `../requirements.txt` — export de todas as versões exatas (gerado via `pip freeze`)
