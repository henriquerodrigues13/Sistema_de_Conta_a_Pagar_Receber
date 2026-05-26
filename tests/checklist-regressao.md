# Checklist de Testes de Regressão — Sistema de Conta a Pagar e Receber (adaptado ao estado atual)

## 1. Backend & API (Pytest — integração / contratos)
- [ ] Persistência de Usuário: POST `/cadastro_usuario` cria um registro em `cpr.sqlite`; testar que a resposta contém `nome_completo` e que o registro no DB tem `email` único e `senha` armazenada (hash) (**Integração**).
- [ ] Login básico: POST `/login` valida credenciais e retorna os dados do usuário (200). Testar: senha correta retorna objeto com `nome_completo` / `email`; senha incorreta retorna 401; e usuário inexistente retorna 404 (**Integração**).
- [ ] Rotas de movimentação (receita/despesa/vendas): atualmente estão comentadas no código. Antes de testar, verificar se foram ativadas. Se não ativadas, marque como "não implementadas" e crie issue para implementação (**Integração**).
- [ ] Proteção de endpoints: atualmente NÃO existe JWT/session tokens — garantir que testes não assumam proteção; se planejar implementar autenticação, adicionar testes de 401 após essa mudança (**Integração**).

## 2. Lógica de Negócio e validações (Unitário)
- [ ] Hash de senha: teste unitário para `senha_hash` e `verificar_senha` em `backend/API/criptografia.py` (hash diferente do texto, `verificar_senha` retorna True para senha correta).
- [ ] Validações externas: `backend/API/validações.py` chama ZeroBounce com chave embutida — em testes, mockar `requests.get` e validar comportamento para respostas `valid` / `invalid` (não fazer requests reais). Persistir comportamento de `valid` permitindo cadastro.
- [ ] Sanidade de campos: testar que `cadastro_usuario` Pydantic valida email (EmailStr), que campos obrigatórios levantam erro 422 quando ausentes.

## 3. Infra & comportamentos auxiliares
- [ ] Backup automático: `backend/models/backup_db.py` usa `agenda_backup()` iniciado no `lifespan` da FastAPI; teste de integração: iniciar app e checar se um arquivo `backup_*.sqlite` aparece em `~/Documents/backup` e que apenas os últimos 3 backups são mantidos (rotacionamento). Para CI, mockar filesystem ou reduzir intervalo de tempo.
- [ ] Inicialização DB: `database.init_db()` é chamado no `lifespan` — testar que ao iniciar `uvicorn backend.main:app` o arquivo `cpr.sqlite` e tabelas são criados (em ambiente de teste usar tempdir e `DATABASE_URL` ajustado).

## 4. Frontend → Backend (Integração / E2E)
- [ ] Fluxo de cadastro + login (Happy Path): com backend rodando, simular formulário do frontend ou usar um teste E2E (Playwright / Cypress) que:
	- envia POST `/cadastro_usuario` com payload válido;
	- faz POST `/login` com credenciais criadas;
	- valida resposta 200 e que o frontend exibirá `nome_completo` (ou o backend retorna objeto esperado).
- [ ] Unhappy Path no login: senha incorreta retorna 401 e frontend exibe mensagem de erro (mockar UI se for teste automatizado). Caso o frontend não esteja servindo rotas, teste via requisição HTTP direta.

## 5. Notas de teste e segurança
- Não confie na API key presente em `backend/API/validações.py` durante testes — use mocks e mova a chave para `.env` (variáveis de ambiente) em produção.
- Em testes automatizados, use ambiente isolado (virtualenv) e banco temporário (`sqlite:///./test_cpr.sqlite` ou in-memory) para evitar poluição do DB de desenvolvimento.
- Ao escrever testes que interagem com arquivos (backups), garanta limpeza após execução.

## 6. Comandos úteis para rodar localmente
 - Criar venv e instalar dependências:
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -e .
```
- Rodar API:
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## 7. Próximos passos esperados
- Implementar proteção de rotas (JWT) e atualizar checklists para exigir testes de autorização (401/403).
- Ativar/implementar rotas comentadas (vendas/receita/despesas) e adicionar testes de integração para cada uma.
- Adicionar uma fixture pytest que inicialize uma DB temporária e anule chamadas a `requests.get` por padrão.
