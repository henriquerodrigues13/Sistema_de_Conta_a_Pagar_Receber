## Checklist de Testes — Sistema de Conta a Pagar e Receber (atualizado)
## 1. Backend/API
[x] API sobe sem erros (rodar uvicorn backend.main:app --reload) e chama database.init_db() no lifespan (Smoke)

[x] POST /cadastro_usuario: cria usuário, retorna resposta_usuario com nome_completo, grava email único e armazena senha como hash (Integração)

[x] POST /login: credenciais corretas retornam 200; senha incorreta retorna 401; usuário inexistente retorna 404 (Integração)

[x] Swagger docs acessível (Smoke)

[ ] Rotas de lançamentos (receita, despesas, vendas) ainda comentadas: marcar como "não implementadas" até ativadas (Manual/Integração)

[x] POST /cadastro_produtos: sucesso vinculado a usuário existente; erro 404 se usuário não existe (Integração)

[x] GET /get_produtos_usuario: retorna lista paginada de produtos do usuário (Integração)

[ ] GET /get_produtos_fornecedor: rota existe mas depende de fornecedor; testes só quando fluxo de fornecedor estiver ativo (Integração futura)

[x] DELETE /delete_produto: marca produto como indisponível (Integração)

[x] PATCH /update_produto: atualiza dados do produto; erro 400 se payload vazio (Integração)

[ ] GET /get_fornecedor: rota existe mas depende de dados de fornecedor; testes só quando fluxo estiver ativo (Integração futura)

## 2. Regras de Negócio e Validações
[x] Criptografia: senha_hash e verificar_senha em backend/API/criptografia.py (Unitário)

[x] Validação de email em backend/API/validações.py: mock de requests.get, respostas valid permitem cadastro e invalid impedem (Unitário/Integração)

[x] Tratamento de erro HTTP em validação de email (graceful degradation) (Unitário)

[x] Pydantic validações: rejeita email inválido e campos obrigatórios ausentes (HTTP 422) (Unitário)

[ ] Validação de CNPJ removida: não há mais cadastro de fornecedor. Novo fluxo será testado em receitas/despesas → se CNPJ não encontrado, abrir ticket (Integração futura)

## 3. Infra e Comportamentos Auxiliares
[ ] Backup automático: backend/models/backup_db.py inicia agenda_backup(); testar criação de arquivos backup_*.sqlite e rotacionamento (máx. 3) (Integração/Mock)

[ ] DB de teste isolado: usar sqlite:///./test_cpr.sqlite ou in-memory; garantir limpeza após testes (Fixture)

## 4. Frontend → Backend (E2E / Interface)
[ ] Fluxo cadastro + login (Happy Path): via frontend estático (frontend/index.html) com Playwright (E2E futura)

[ ] Unhappy Path login: senha incorreta retorna 401 e frontend exibe mensagem (E2E futura)

[ ] Fluxo de lançamento de receita/despesa com CNPJ inexistente → abertura de ticket (E2E futura)

## 5. Notas de Segurança e Práticas de Teste
[x] API key não usada em testes — sempre mockar requests.get e mover chave para .env em produção

[ ] Testes de isolamento de ambiente (venv + DB temporário)

[ ] Limpeza de backups criados por testes que tocam filesystem

## 6. Novos Testes Recomendados
[ ] Testes de carga (stress test básico) para API de login/cadastro

[ ] Testes de concorrência: múltiplos cadastros simultâneos

[ ] Testes de fluxo de ticket quando CNPJ não encontrado em receitas/despesas (Integração futura)