# Checklist de Testes Iniciais — Sistema de Conta a Pagar e Receber (ajustado ao estado atual)

>
## 1. Backend/API
- [x] API sobe sem erros (rodar `uvicorn backend.main:app --reload`) e chama `database.init_db()` no lifespan (**Smoke**)
- [x] `POST /cadastro_usuario`: testa que cria o usuário, retorna `reponsa_usuario` com `nome_completo`, grava `email` único e armazena `senha` como hash (não texto) (**Integração**)
- [x] `POST /login`: testa comportamento real: credenciais corretas retornam 200 com dados do usuário; senha incorreta retorna 401; usuário inexistente retorna 404 (**Integração**)
- [ ] Rotas de lançamentos (`receita`, `despesas`, `vendas`) estão comentadas no código: confirmar estado antes de escrever testes; marque-as como "não implementadas" até ativadas (**Manual / Integração**)

## 2. Regras de Negócio e validações
- [x] `senha_hash` e `verificar_senha` em `backend/API/criptografia.py`: unit tests para validar que o hash não é igual ao texto e `verificar_senha` retorna True para senha correta (**Unitário**)
- [ ] Validação de email em `backend/API/validações.py`: mockar `requests.get` em testes (não chamar ZeroBounce real). Validar que resposta `valid` permite cadastro e `invalid` impede cadastro (**Unitário / Integração com Mock**)
- [ ] Pydantic validações: testar que `cadastro_usuario` rejeita email inválido e campos obrigatórios ausentes (HTTP 422) (**Unitário**)

## 3. Infra e comportamentos auxiliares
- [ ] Backup automático: `backend/models/backup_db.py` inicia `agenda_backup()` no `lifespan`; teste que arquivos `backup_*.sqlite` aparecem em `~/Documents/backup` e que apenas 3 backups são mantidos (rotacionamento). Em CI, reduzir/alterar intervalo ou mockar filesystem (**Integração/Mock**)
- [ ] DB de teste: use `sqlite:///./test_cpr.sqlite` ou in-memory para fixtures, e backup/destruição após testes para não poluir `cpr.sqlite` de desenvolvimento (**Fixture**)

## 4. Frontend → Backend (E2E / Interface)
- [ ] Fluxo cadastro + login (Happy Path): com backend rodando, enviar POST `/cadastro_usuario`, depois `/login`; validar status 200 e campos retornados. O frontend é estático em `frontend/index.html` e pode ser testado via requisições HTTP diretas ou E2E (Playwright/Cypress) se você expor o frontend por um servidor estático (**E2E/Integração**)
- [ ] Unhappy Path no login: senha incorreta retorna 401 e frontend deve exibir mensagem — se não houver UI testada, valide via requisição HTTP direta (**E2E/Integração**)

## 5. Notas de segurança e práticas de teste
- Não use a API key embutida em `backend/API/validações.py` durante testes — sempre mockar `requests.get` e mover a chave para `.env` em produção.
- Em testes automáticos, inicialize um ambiente isolado (venv) e um DB temporário para evitar estados compartilhados.
- Limpe arquivos de backup criados por testes que tocam o filesystem.

## 6. Comandos rápidos para dev/test
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
