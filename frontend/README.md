# 📋 Projeto

## Como rodar

**1. Instale o servidor HTTP globalmente (só na primeira vez):**
```bash
npm install -g http-server
```

**2. Na pasta do projeto, suba o servidor:**
```bash
http-server .
```

**3. Acesse no navegador:**
```
http://localhost:8080 ou a porta do seu pc
```

---

## Como funciona a renderização

O projeto é uma **SPA (Single Page Application)** simples, sem frameworks. Toda a navegação acontece dentro de um único elemento `#app` no `index.html`.

### Páginas

A função `renderizarPagina(pagina)` é responsável por trocar o conteúdo do `#app`. Cada página tem uma função que retorna o HTML correspondente.

```
renderizarPagina('login')         → chama paginaLogin()
renderizarPagina('usuarioLayout') → chama paginaLayoutUsuario() e inicializa o dashboard
renderizarPagina('cadastroReceita') → chama paginaCadastroReceita()
...
```

Algumas páginas possuem uma função de inicialização (`init`) que é chamada logo após o HTML ser inserido — por exemplo, para registrar eventos ou carregar dados da API.

### Seções

Dentro do layout do usuário (`usuarioLayout`), a navegação entre seções é feita pela função `renderizarSection(section)`, que substitui apenas o conteúdo interno da área principal, sem recarregar o layout todo.

```
renderizarSection('sectionDashboard')
renderizarSection('sectionReceita')
...
```

### Fluxo ao abrir o app

```
DOMContentLoaded
    └── verificarLogin()
            ├── usuário logado   → renderizarPagina('usuarioLayout')
            └── não logado       → renderizarPagina('paginaInicial')
```