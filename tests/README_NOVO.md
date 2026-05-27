# Sistema de Contas a Pagar e Receber (CPR)

**Documentação dos Testes**

---

## 🎯 O Que É Este Projeto?

Este é um **sistema web** que ajuda empresas a gerenciar contas a pagar e receber. Pense nisto como um **livro de anotações digital** onde você:
- ✅ Cadastra usuários (clientes e fornecedores)
- ✅ Cria produtos/serviços
- ✅ Registra transações
- ✅ Controla pagamentos

**Onde roda?** Na internet, usando **FastAPI** (um framework Python para criar sites).

---

## 📊 Como o Projeto Está Organizado

```
seu-projeto/
├── backend/
│   ├── API/
│   │   ├── criptografia.py      ← Protege senhas
│   │   ├── validações.py        ← Verifica dados
│   │   └── routes.py            ← Rotas do site
│   ├── models/
│   │   ├── database.py          ← Banco de dados
│   │   ├── engine.py            ← Tabelas/estrutura
│   │   ├── logs.py              ← Registros
│   │   └── backup_db.py         ← Cópia de segurança
│   ├── main.py                  ← Inicia a aplicação
│
├── tests/
│   ├── conftest.py              ← ⭐ Configuração dos testes
│   ├── unit/
│   │   ├── test_criptografia.py ← Testa senhas
│   │   └── test_smoke.py        ← Testa se está online
│   └── integracao/
│       ├── test_api.py          ← Testa funcionalidades
│       └── test_validacoes.py   ← Testa validações
│
└── README.md                    ← Este arquivo!
```

---

## 🧬 Os 4 Tipos de Testes Deste Projeto

### 1. 🔐 Testes de Criptografia
**Arquivo:** `test_criptografia.py`

**O que testa?** Se as senhas estão protegidas corretamente.

```python
# ✅ Exemplo simples:
Você digita:  senha_secreta_123
Sistema salva: $2b$10$xK8x3J9... (código embaralhado)

Teste verifica:
  ✓ A senha original e o código são diferentes
  ✓ Quando você digita a senha correta, o sistema reconhece
  ✓ Quando você digita errado, o sistema rejeita
```

**Como rodar:**
```bash
pytest tests/unit/test_criptografia.py
```

---

### 2. 💓 Testes de Saúde (Smoke Tests)
**Arquivo:** `test_smoke.py`

**O que testa?** Se a aplicação está "viva" e funcionando basicamente.

```python
# ✅ Exemplos:
Teste 1: A documentação online está disponível? (GET /docs)
Teste 2: Quando a aplicação sobe, o banco de dados é criado?
Teste 3: Há algum erro crítico no startup?
```

**Como rodar:**
```bash
pytest tests/unit/test_smoke.py
```

---

### 3. ✔️ Testes de Validação
**Arquivo:** `test_validacoes.py`

**O que testa?** Se os dados que entram no sistema estão corretos.

```python
# ✅ Exemplos de validações:

1. EMAIL:
   ✓ email@valido.com → VÁLIDO ✅
   ✗ emailinvalido    → INVÁLIDO ❌

2. CNPJ (Código da empresa):
   ✓ 12.345.678/0001-99 → Aceita (remove pontos/barras) ✅
   ✗ 00000000000000      → INVÁLIDO ❌

3. CAMPOS OBRIGATÓRIOS:
   Se você não preenche "nome completo" → ERRO 422 ❌
```

**Como rodar:**
```bash
pytest tests/integracao/test_validacoes.py
```

---

### 4. 🚀 Testes de API (Integração Completa)
**Arquivo:** `test_api.py`

**O que testa?** Se o sistema inteiro funciona, do começo ao fim.

```python
# ✅ Exemplo 1: CADASTRO DE USUÁRIO
Passo 1: Envia dados (nome, email, senha)
Passo 2: Sistema valida e criptografa
Passo 3: Salva no banco de dados
Passo 4: Retorna confirmação
Teste verifica: Tudo funcionou? ✅

# ✅ Exemplo 2: LOGIN
Passo 1: Tenta fazer login com email correto
Passo 2: Sistema verifica senha
Passo 3: Se correto, retorna 200 ✅
Passo 4: Se errado, retorna 401 ❌
Passo 5: Se usuário não existe, retorna 404 ❌

# ✅ Exemplo 3: CADASTRAR PRODUTO
Passo 1: Primeiro cria um usuário
Passo 2: Cria um produto vinculado a esse usuário
Passo 3: Sistema salva e confirma
Teste verifica: Produto foi criado corretamente? ✅
```

**Como rodar:**
```bash
pytest tests/integracao/test_api.py
```

---

## 🚀 Como Executar os Testes

### Requisitos (O que você precisa ter instalado)
```bash
# Python 3.8 ou superior
python --version

# Instalar dependências
pip install pytest pytest-asyncio fastapi sqlalchemy bcrypt
```

### Rodar TODOS os testes
```bash
pytest
```

**Resultado esperado:**
```
tests/unit/test_criptografia.py::test_criptografia_da_senha PASSED ✅
tests/unit/test_smoke.py::test_docs_available PASSED ✅
tests/integracao/test_validacoes.py::... PASSED ✅
tests/integracao/test_api.py::... PASSED ✅

================== 16 passed in 2.45s ==================
```

### Rodar apenas UM tipo de teste
```bash
# Apenas testes unitários (rápido)
pytest tests/unit/

# Apenas testes de integração (mais lento)
pytest tests/integracao/

# Apenas um arquivo
pytest tests/unit/test_criptografia.py

# Apenas um teste específico
pytest tests/unit/test_criptografia.py::test_criptografia_da_senha
```

### Rodar com mais informações
```bash
# Modo verboso (mostra mais detalhes)
pytest -v

# Mostra os prints/mensagens do código
pytest -s

# Mostra ambos
pytest -v -s
```

---

## 📋 Entendendo os Testes

### Padrão AAA (Organize, Faça, Verifique)

Todo teste segue este padrão:

```python
def test_exemplo(client):
    
    # ARRANGE (Organizar): Preparar dados
    email = "pedro@email.com"
    senha = "123456"
    
    # ACT (Fazer): Executar a ação
    response = client.post("/login", json={"email": email, "senha": senha})
    
    # ASSERT (Verificar): Checar resultado
    assert response.status_code == 200  # ✅ Se passou
```

### O Que Significa `assert`?

```python
assert X == Y  # Verifica se X é igual a Y
```

Se for verdade → teste PASSA ✅  
Se for falso → teste FALHA ❌

---

## 🔧 Arquivo Especial: `conftest.py`

Este arquivo é como o **gerente dos testes**. Ele:

1. ✅ Cria um banco de dados vazio para cada teste
2. ✅ Isola os testes (um não interfere no outro)
3. ✅ Prepara dados de exemplo
4. ✅ Fornece um "cliente HTTP" para fazer requisições

### Por que isso é importante?

```
❌ Sem conftest.py:
   Teste 1 cria usuário "Pedro"
   Teste 2 também cria "Pedro" → ERRO! Já existe!

✅ Com conftest.py:
   Teste 1 roda em um banco zerado → cria "Pedro" ✅
   Teste 2 roda em OUTRO banco zerado → cria "Pedro" ✅
   Ninguém interfere com ninguém!
```

---

## 📁 Como os Testes Acessam o Sistema

### O Fluxo:

```
Teste (test_api.py)
    ↓
conftest.py cria um cliente HTTP simulado
    ↓
client.post("/login", json=dados)
    ↓
FastAPI recebe a requisição
    ↓
Executa a função em routes.py
    ↓
Salva no banco de dados em memória
    ↓
Retorna resposta ao teste
    ↓
Teste verifica: response.status_code == 200? ✅
```

---

## 🐛 Problemas Comuns e Soluções

### ❌ Erro: "ModuleNotFoundError: No module named 'backend'"

**Causa:** Python não consegue encontrar a pasta `backend`.

**Solução:**
```bash
# Rodar pytest DA PASTA RAIZ do projeto
cd /caminho/do/projeto
pytest

# OU: Instalar em modo editável
pip install -e .
```

### ❌ Erro: "no such table: usuarios"

**Causa:** O banco de dados em memória não foi criado.

**Solução:** Verificar se `conftest.py` tem:
```python
Base.metadata.create_all(bind=engine)  # Deve estar lá!
```

### ❌ Um teste falha, mas os outros passam

**Normal!** Isso significa:
- Os outros testes estão bons ✅
- Um teste encontrou um bug 🐛
- Você pode corrigir só aquele

---

## 📊 Interpretando Resultados

### ✅ Sucesso
```
PASSED ✅
test_criptografia_da_senha PASSED [100%]

================== 1 passed in 0.05s ==================
```

### ❌ Falha
```
FAILED ❌
test_criptografia_da_senha FAILED
AssertionError: assert False == True

================== 1 failed in 0.10s ==================
```

---

## 🎓 O Que Cada Arquivo Testa

| Arquivo | Testa | Por que importa |
|---------|-------|-----------------|
| `test_criptografia.py` | Se senhas ficam protegidas | Segurança |
| `test_smoke.py` | Se a aplicação está online | Disponibilidade |
| `test_validacoes.py` | Se dados estão corretos | Qualidade dos dados |
| `test_api.py` | Se funcionalidades funcionam | Experiência do usuário |

---

## 💡 Resumo Rápido

```python
# 1. Para rodar TODOS os testes:
pytest

# 2. Para rodar apenas um tipo:
pytest tests/unit/
pytest tests/integracao/

# 3. Para ver mais detalhes:
pytest -v -s

# 4. Para testar um arquivo específico:
pytest tests/unit/test_criptografia.py

# 5. Para testar uma função específica:
pytest tests/unit/test_criptografia.py::test_criptografia_da_senha
```

---

## 🔍 Checklist: Está Tudo Funcionando?

- [ ] Ao rodar `pytest`, todos os testes passam?
- [ ] A documentação Swagger está em `http://localhost:8000/docs`?
- [ ] Você consegue criar um usuário via API?
- [ ] Você consegue fazer login?
- [ ] Testes de criptografia passam?

Se tudo está verde ✅, o projeto está funcionando!

---
