# Changelog da Suite de Testes

---

## O que foi feito

Análise completa da suite de testes existente, correção de testes quebrados e adição de novos testes para cobrir as partes da API que não tinham nenhum teste.

---

## Arquivos modificados

### `tests/integracao/test_api.py` — Correções e novos testes

#### Bugs corrigidos nesse arquivo

**1. `PAYLOAD_RECEITA_VALIDO` tinha os campos errados**

O payload de receita usado nos testes tinha campos `descricao`, `valor` e `email_usuario` que não existem no modelo `request_receita` da API. O modelo real espera `recebedor_email`, `tipo_da_receita`, `valor_da_receita`, etc. Todos os testes de receita estavam usando um payload que ia dar 422.

```python
# ANTES (errado — campos não existem no modelo):
PAYLOAD_RECEITA_VALIDO = {
    "descricao": "Venda de Consultoria de TI",
    "valor": 4500.00,
    "data_da_receita": "2024-12-15",
    "email_usuario": "maria.teste@email.com"
}

# DEPOIS (correto — campos do modelo request_receita):
PAYLOAD_RECEITA_VALIDO = {
    "recebedor_email": "maria.teste@email.com",
    "tipo_da_receita": "Consultoria de TI",
    "data_da_receita": "2024-12-15T00:00:00",
    "valor_da_receita": 4500.00,
    "forma_de_pagamento": "PIX",
    "observacao": "Venda de Consultoria de TI"
}
```

**2. `test_listar_receitas_sucesso` chamava URL errada**

O teste chamava `GET /get_receitas` sem passar o email do usuário, mas o endpoint correto é `GET /get_receitas/{usuario_email}`. Sem o email, a API retorna 404 ou 422, não a lista de receitas.

```python
# ANTES (errado):
resposta = client.get("/get_receitas")

# DEPOIS (correto):
resposta = client.get(f"/get_receitas/{email_recebedor}")
```

**3. `test_update_venda` usava o nome do produto como identificador da venda**

O endpoint `PATCH /update_venda/{email}/{identificador}` espera o `identificador` da venda, que é um nanoid gerado automaticamente (ex: `"2xKF9Bm3Ly"`). O teste antigo passava `"Açaí da Roça"` (nome do produto) como identificador, o que nunca iria encontrar a venda no banco — sempre retornaria 404.

```python
# ANTES (errado — passava nome do produto como identificador):
response = client.patch(
    f"/update_venda/{email_teste}/Açaí da Roça",
    json={"valor_final": 25.00}
)

# DEPOIS (correto — busca o identificador real antes de atualizar):
resp_get = client.get(f"/get_vendas/{email_teste}")
identificador_real = resp_get.json()[0]["identificador"]

response = client.patch(
    f"/update_venda/{email_teste}/{identificador_real}",
    json={"valor_final": 25.00}
)
```

#### Novos testes adicionados

- `test_recuperacao_senha_usuario_existente` — testa que POST /recuperacao_senha retorna 201 para usuário existente (mock do envio de email)
- `test_recuperacao_senha_usuario_inexistente` — testa retorno 404 para email inexistente
- `test_reset_senha_com_token_valido` — fluxo completo: solicita recuperação com token fixo e depois reseta a senha
- `test_reset_senha_token_invalido` — testa retorno 404 para token que não existe
- `test_reset_senha_token_expirado` — testa retorno 400 para token com data de expiração no passado
- `test_get_fornecedor_lista_vazia` — verifica que GET /get_fornecedor retorna 200 (lista vazia no banco de testes)
- `test_get_vendas_usuario` — testa listagem de vendas por usuário
- `test_delete_venda` — testa deleção de venda e confirmação pela listagem
- `test_update_receita` — testa atualização de receita existente
- `test_delete_receita` — testa deleção de receita

---

## Arquivos criados

### `tests/integracao/test_servicos.py` — CRUD completo de serviços

Esse módulo de serviços não tinha nenhum teste. Foram criados 9 testes cobrindo:

| Teste | O que verifica |
|-------|----------------|
| `test_cadastro_servico_com_sucesso` | Cadastro com usuário existente → 200 |
| `test_cadastro_servico_usuario_inexistente` | Usuário não existe → 404 |
| `test_cadastro_servico_duplicado` | Mesmo serviço duas vezes → 409 |
| `test_get_servico_usuario` | Listagem com paginação |
| `test_get_servico_usuario_lista_vazia` | Usuário sem serviços → lista vazia |
| `test_update_servico_com_sucesso` | Atualização com dados válidos → 200 |
| `test_update_servico_payload_vazio` | Payload vazio → 400 |
| `test_update_servico_inexistente` | Serviço que não existe → 404 |
| `test_delete_servico` | Deleção e confirmação via listagem |
| `test_delete_servico_inexistente` | Serviço que não existe → 404 |

### `tests/integracao/test_despesas.py` — CRUD completo de despesas

Despesas não tinham nenhum teste de integração. Foram criados 9 testes:

| Teste | O que verifica |
|-------|----------------|
| `test_cadastro_despesa_com_sucesso` | Cadastro com usuário existente → 200 |
| `test_cadastro_despesa_pagador_inexistente` | Pagador não existe → 404 |
| `test_cadastro_despesa_payload_incompleto` | Payload com campos faltando → 422 |
| `test_get_despesas_usuario` | Listagem com paginação |
| `test_get_despesas_usuario_lista_vazia` | Usuário sem despesas → lista vazia |
| `test_update_despesa_com_sucesso` | Atualização com identificador real → 200 |
| `test_update_despesa_payload_vazio` | Payload vazio → 400 |
| `test_update_despesa_inexistente` | Identificador inválido → 404 |
| `test_delete_despesa` | Deleção e confirmação via listagem |
| `test_delete_despesa_inexistente` | Identificador inválido → 404 |

### `BUG_REPORT.md` — Relatório de bugs encontrados no código-fonte

Durante a análise dos testes foram encontrados 5 bugs no código de produção. Nenhum foi corrigido aqui (não é responsabilidade do QA alterar código de produção). Ver o arquivo para detalhes.

---

## Cobertura antes e depois

| Categoria | Antes | Depois |
|-----------|-------|--------|
| Testes totais | 27 | 57 |
| Endpoints testados | 9/29 (31%) | 22/29 (75%) |
| Testes de integração | 14 | 42 |
| Recuperação de senha | 0 testes | 5 testes |
| Serviços (CRUD) | 0 testes | 10 testes |
| Despesas (CRUD) | 0 testes | 10 testes |
| Vendas | 1 teste (quebrado) | 4 testes (corrigidos) |
| Receitas | 3 testes (1 quebrado, payload errado) | 5 testes (corrigidos) |

### Endpoints que ainda não têm teste

Esses endpoints ficaram de fora por causa de bugs ou limitações técnicas:

- `POST /cadastro_nota_fiscal` — tem bug de lógica invertida (BUG-001), impossível testar o caminho feliz sem corrigir o fonte
- `GET /get_produtos_fornecedor/{cnpj}` — bug de parâmetro (BUG-002), retorna 422 quando deveria retornar 200
- `GET /get_servicos_fornecedor/{cnpj}` — mesmo bug (BUG-003)
- `POST /cadastro_venda_servico` — não testado ainda, seria a próxima tarefa

---

## Observações técnicas

### Por que mockamos o envio de email nos testes de recuperação de senha?

A função `fast_mail.send_message` tenta se conectar ao servidor SMTP do Gmail de verdade. No ambiente de testes não temos (nem queremos) essa conexão. Sem o mock, os testes travavam ou falhavam com erro de conexão. Usamos `unittest.mock.AsyncMock` porque o método é assíncrono.

### Por que mockamos `gerador_de_token` e `limite_de_expiracao_token`?

Para testar o reset de senha, precisamos saber qual token foi salvo no banco. Como o token é gerado aleatoriamente, precisamos fixá-lo em um valor conhecido antes de testar. A expiração foi mockada para ano 2099 (válido) ou 2000 (expirado) para não ter problema de timing.

### Por que os testes de update/delete buscam o identificador antes de operar?

Os identificadores de vendas, receitas e despesas são nanoids gerados automaticamente (ex: `"2xKF9Bm3Ly"`). Não tem como saber o valor antes de criar o registro. O padrão correto é: criar → listar → pegar o identificador → operar.

---

## Testes E2E com Playwright (Adição Final)

### 4 testes E2E adicionados em `tests/e2e/test_fluxo_usuario.py`

1. **test_fluxo_login_admin_com_sucesso** — Login com admin/admin via navegador
2. **test_fluxo_cadastro_de_despesa_aparece_na_tabela** — CRUD completo de despesa (create + list)
3. **test_fluxo_navegacao_receitas** — Navegação para listagem de receitas
4. **test_fluxo_navegacao_servicos** — Navegação para listagem de serviços (com abas)

### Automação de backend em `tests/e2e/conftest.py`

- Fixture `reiniciar_backend()` mata qualquer uvicorn rodando e sobe um backend limpo
- Chromium é configurado para desabilitar bloqueio de "Private Network Access"
- Backend é automaticamente finalizado ao fim dos testes

### Como rodar tudo com E2E visível

```bash
pytest -v --headed
```

Resultado: 68 testes (64 passed + 4 xfailed), E2E com navegador visível.
