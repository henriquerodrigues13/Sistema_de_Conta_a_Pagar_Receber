## Checklist de Testes — Sistema de Conta a Pagar e Receber (atualizado)
## 1. Backend/API
[x] API sobe sem erros (rodar uvicorn backend.main:app --reload) e chama database.init_db() no lifespan (Smoke)

[x] POST /cadastro_usuario: cria usuário, retorna resposta_usuario com nome_completo, grava email único e armazena senha como hash (Integração)

[x] POST /login: credenciais corretas retornam 200; senha incorreta retorna 401; usuário inexistente retorna 404 (Integração)

[x] Swagger docs acessível (Smoke)

[ ] Rotas de lançamentos (receita, despesas, vendas) ainda comentadas: marcar como "não implementadas" até ativadas (Manual/Integração)

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
[x] Fluxo cadastro + login (Happy Path): validar status 200 e campos retornados (E2E)

[x] Unhappy Path login: senha incorreta retorna 401 e frontend exibe mensagem (E2E)

[ ] Testes E2E com frontend estático (frontend/index.html) via Playwright/Cypress (E2E)

[ ] Fluxo de lançamento de receita/despesa com CNPJ inexistente → abertura de ticket (E2E futura)

5. Notas de Segurança e Práticas de Teste
[x] API key não usada em testes — sempre mockar requests.get e mover chave para .env em produção

[ ] Testes de isolamento de ambiente (venv + DB temporário)

[ ] Limpeza de backups criados por testes que tocam filesystem

6. Novos Testes Recomendados
[x] Cadastro de produto vinculado a usuário existente (Integração)

[x] Cadastro de produto com usuário inexistente (404) (Integração)

[ ] Testes de carga (stress test básico) para API de login/cadastro

[ ] Testes de concorrência: múltiplos cadastros simultâneos

[ ] Testes de fluxo de ticket quando CNPJ não encontrado em receitas/despesas (Integração futura)

[ ] Cobertura de CI/CD: rodar testes automáticos em pipeline