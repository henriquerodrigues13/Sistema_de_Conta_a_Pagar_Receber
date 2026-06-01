# Bug Report — Sistema de Conta a Pagar/Receber
**Arquivos inspecionados:** `backend/API/rotas.py`, `backend/API/validações.py`, `backend/API/criptografia.py`

---

> Este relatório lista os bugs encontrados durante a criação da suite de testes.
> Nenhum código de produção foi alterado — só foram criados/modificados arquivos de teste.
> Os bugs abaixo precisam ser corrigidos pela equipe de desenvolvimento.

---

## BUG-001 — Lógica invertida no endpoint `POST /cadastro_nota_fiscal`

**Arquivo:** `backend/API/rotas.py` — linha 597  
**Severidade:** Crítica  
**Status:** Aberto

### O que acontece

A condição `if not` está na posição errada. O código que cria a nota fiscal está dentro do bloco que roda quando o usuário **NÃO existe**, e o erro 404 é lançado quando o usuário **SIM existe**.

### Trecho do código com o problema

```python
# COMO ESTÁ (errado):
if not (usuario_existe := session.execute(...).scalar_one_or_none()):
    # esse bloco roda quando o usuário NÃO existe — errado!
    nova_nota = nota_fiscal(...)
    session.commit()
    return JSONResponse(...)

raise HTTPException(status_code=404, detail="Usuario não encontrado")
# o 404 roda quando o usuário EXISTE — errado!
```

### Como deveria ser

```python
# COMO DEVERIA SER:
if not (usuario_existe := session.execute(...).scalar_one_or_none()):
    raise HTTPException(status_code=404, detail="Usuario não encontrado")

# aqui embaixo cria a nota (usuário existe)
nova_nota = nota_fiscal(...)
session.commit()
return JSONResponse(...)
```

### Como reproduzir

1. Cadastrar um usuário via `POST /cadastro_usuario`
2. Chamar `POST /cadastro_nota_fiscal` com o email desse usuário
3. **Resultado atual:** retorna 404 (usuário não encontrado)
4. **Resultado esperado:** retorna 200/201 (nota criada com sucesso)

---

## BUG-002 — Parâmetro de path errado em `GET /get_produtos_fornecedor/{cnpj}`

**Arquivo:** `backend/API/rotas.py` — linha 247  
**Severidade:** Alta  
**Status:** Aberto

### O que acontece

O endpoint tem `/{cnpj}` na URL, mas o parâmetro da função se chama `fornecedor_cnpj`. O FastAPI não consegue ligar os dois porque os nomes são diferentes. Aí o `fornecedor_cnpj` vira um query parameter obrigatório, e quem chama a rota sem passar `?fornecedor_cnpj=...` recebe um erro 422.

### Trecho do código com o problema

```python
# URL tem {cnpj}...
@router.get('/get_produtos_fornecedor/{cnpj}', ...)
async def get_produtos_fornecedor(
    fornecedor_cnpj: str,   # mas o parâmetro tem nome diferente!
    ...
```

### Como deveria ser

```python
@router.get('/get_produtos_fornecedor/{cnpj}', ...)
async def get_produtos_fornecedor(
    cnpj: str,   # nome tem que casar com o {cnpj} da URL
    ...
```

### Como reproduzir

1. Chamar `GET /get_produtos_fornecedor/12345678000190`
2. **Resultado atual:** retorna 422 (campo `fornecedor_cnpj` é obrigatório)
3. **Resultado esperado:** retorna 200 com lista de produtos do fornecedor

---

## BUG-003 — Mesmo problema de parâmetro em `GET /get_servicos_fornecedor/{cnpj}`

**Arquivo:** `backend/API/rotas.py` — linha 383  
**Severidade:** Alta  
**Status:** Aberto

### O que acontece

Mesmo bug do BUG-002, mas no endpoint de serviços do fornecedor.

```python
# URL tem {cnpj}...
@router.get('/get_servicos_fornecedor/{cnpj}', ...)
async def get_servicos_fornecedor(
    fornecedor_cnpj: str,   # nome errado aqui também
    ...
```

### Como corrigir

Renomear `fornecedor_cnpj` para `cnpj` na assinatura da função (mesma correção do BUG-002).

---

## BUG-004 — Mensagem de sucesso errada no `POST /cadastro_despesa`

**Arquivo:** `backend/API/rotas.py` — linha 768  
**Severidade:** Baixa (só mensagem, funcionalidade ok)  
**Status:** Aberto

### O que acontece

O endpoint de cadastro de despesa retorna uma mensagem dizendo "receita" no lugar de "despesa".

### Trecho do código com o problema

```python
return JSONResponse(
    content={'mensagem': f'A receita foi cadastrada com sucesso'},  # <-- errado
    media_type='text/plain')
```

### Como deveria ser

```python
return JSONResponse(
    content={'mensagem': f'A despesa foi cadastrada com sucesso'},
    media_type='text/plain')
```

### Impacto

Qualquer cliente (frontend, app mobile) que valide a mensagem de retorno vai receber texto incorreto. Pode confundir o usuário ou quebrar validações no frontend.

---

## BUG-005 — Credenciais sensíveis hardcoded no código-fonte

**Arquivos:** `backend/API/rotas.py` (linha 17-18), `backend/API/validações.py` (linha 5), `backend/API/criptografia.py` (linha — chave não encontrada aqui, mas padrão de risco existe)  
**Severidade:** Alta (segurança)  
**Status:** Aberto

### O que acontece

Credenciais reais estão escritas diretamente no código, o que significa que qualquer pessoa com acesso ao repositório consegue ver a senha do email e as chaves de API.

### Exemplos encontrados

```python
# rotas.py - credenciais de email expostas
MAIL_USERNAME="henriquefnaf2680@gmail.com",
MAIL_PASSWORD="tuqq rxpr rxyy jome",

# validações.py - chave de API exposta
api_key = '3f1c2d022729488da21f370e1a81ccf9'

# validações.py - outra chave de API
api_key = '3d45d9df5d6151e9532292e11cf726b9f3f7db2a76209bcf290ad8117a15d546'
```

### Como corrigir

Mover todas as credenciais para variáveis de ambiente (arquivo `.env`) e usar `python-dotenv` para carregá-las:

```python
# .env (nunca commitar esse arquivo!)
MAIL_USERNAME=henriquefnaf2680@gmail.com
MAIL_PASSWORD=tuqq rxpr rxyy jome
ZEROBOUNCE_API_KEY=3f1c2d022729488da21f370e1a81ccf9

# rotas.py
import os
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
```

**Ação imediata recomendada:** Trocar as senhas/chaves que já foram expostas, mesmo que o repositório seja privado.

---

## Resumo

| # | Bug | Arquivo | Severidade | Status |
|---|-----|---------|-----------|--------|
| BUG-001 | Lógica invertida em `/cadastro_nota_fiscal` | rotas.py:597 | Crítica | Aberto |
| BUG-002 | Parâmetro errado em `/get_produtos_fornecedor/{cnpj}` | rotas.py:247 | Alta | Aberto |
| BUG-003 | Parâmetro errado em `/get_servicos_fornecedor/{cnpj}` | rotas.py:383 | Alta | Aberto |
| BUG-004 | Mensagem "receita" no endpoint de despesa | rotas.py:768 | Baixa | Aberto |
| BUG-005 | Credenciais hardcoded no código | rotas.py, validações.py | Alta | Aberto |
