## Checklist de Testes — Sistema de Conta a Pagar e Receber (atualizado)

## 1. Backend/API
[x] API sobe sem erros (rodar uvicorn backend.main:app --reload) e chama database.init_db() no lifespan (Smoke)

[x] POST /cadastro_usuario: cria usuário, retorna reponsa_usuario com nome_completo, confirma que senha não é exposta na resposta, grava email único; email duplicado retorna 409 (Integração)

[x] POST /login: credenciais corretas retornam 200; senha incorreta retorna 401; usuário inexistente retorna 404 (Integração)

[x] Swagger docs acessível (Smoke)

[ ] Rotas de lançamentos (receita, despesas, vendas) ainda comentadas: marcar como "não implementadas" até ativadas (Manual/Integração)

[x] POST /cadastro_produtos: sucesso vinculado a usuário existente; produto duplicado retorna 409; usuário inexistente retorna 404 (Integração)

[x] GET /get_produtos_usuario: retorna lista paginada de produtos ativos do usuário com headers X-Total-Items e X-Total-Pages (Integração)

[ ] GET /get_produtos_fornecedor: rota existe mas depende de fornecedor; testes só quando fluxo de fornecedor estiver ativo (Integração futura)

[x] DELETE /delete_produto: marca produto como indisponível e produto some da listagem (Integração)

[x] PATCH /update_produto: atualiza dados do produto com sucesso; produto inexistente retorna 404; payload vazio retorna 400 (Integração)

[ ] GET /get_fornecedor: rota existe mas depende de dados de fornecedor; testes só quando fluxo estiver ativo (Integração futura)

[x] POST /cadastro_servico: sucesso vinculado a usuário existente; serviço duplicado retorna 409; usuário inexistente retorna 404 (Integração)

[x] GET /get_servico_usuario: retorna lista paginada de serviços ativos do usuário com headers X-Total-Items e X-Total-Pages (Integração)

[x] DELETE /delete_servico: marca serviço como deletado e some da listagem (Integração)

[x] PATCH /update_servico: atualiza dados do serviço com sucesso; serviço inexistente retorna 404; payload vazio retorna 400 (Integração)

## 2. Regras de Negócio e Validações
[x] Criptografia: senha_hash gera hash diferente da senha original; verificar_senha retorna True para senha correta e False para errada (Unitário)

[x] Validação de email: mock de requests.post, resposta "valid" retorna True; resposta "invalid" retorna False (Unitário)

[x] Tratamento de erro HTTP em validação de email: exceção de conexão retorna False em vez de explodir (graceful degradation) (Unitário)

[x] Pydantic: rejeita campos obrigatórios ausentes com ValidationError; rota retorna HTTP 422 para payload com email inválido (Unitário)

[x] Validação de CNPJ removida: não há mais cadastro de fornecedor pelo usuário. Testes de CNPJ removidos. Novo fluxo será testado em receitas/despesas quando implementado (Integração futura)

## 3. Infra e Comportamentos Auxiliares
[x] DB de teste isolado: sqlite in-memory via conftest.py com StaticPool; banco zerado a cada teste via override_get_session (Fixture)

[x] Backup — rotacionamento: mantém no máximo 3 arquivos, removendo os mais antigos quando há mais de 3 (Unitário)

[x] Backup — rotacionamento com menos de 3 arquivos: nenhum arquivo é removido (Unitário)

[ ] Backup — criação de arquivo e envio por email: depende de refatoração do backup_db.py para aceitar caminhos como parâmetro; pendente para quando isso for feito

## 4. Frontend → Backend (E2E / Interface)
[ ] Fluxo cadastro + login (Happy Path): via frontend estático com Playwright (E2E futura)

[ ] Unhappy Path login: senha incorreta retorna 401 e frontend exibe mensagem (E2E futura)

[ ] Fluxo de lançamento de receita/despesa (E2E futura)

## 5. Notas de Segurança e Práticas de Teste
[x] validacao_email mockada em todos os testes de integração via fixture autouse no conftest.py — API key não exposta nos testes

[x] Senha nunca retornada nas respostas da API (response_model reponsa_usuario só expõe nome_completo)

[ ] Mover API keys (ZeroBounce, credenciais de email) para .env em produção

[ ] Testes de isolamento de ambiente (venv + DB temporário documentado)

## 6. Testes Futuros Recomendados
[ ] Testes de carga (stress test básico) para rotas de login e cadastro

[ ] Testes de concorrência: múltiplos cadastros simultâneos

[ ] Fluxo de receitas/despesas quando rotas forem descomentadas e ativadas

## 7. Bugs Conhecidos e Corrigidos
[x] BUG — DELETE /delete_produto e DELETE /delete_servico nunca retornavam 404:
    session.execute(update(...)) sempre retorna um objeto CursorResult truthy,
    fazendo o if ser sempre verdadeiro independente de o registro existir.
    Corrigido substituindo por select + verificação explícita antes do update.
    Testes: test_delete_produto_inexistente, test_delete_servico_inexistente