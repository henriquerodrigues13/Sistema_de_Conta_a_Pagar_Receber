document.addEventListener('DOMContentLoaded', () => {
    verificarLogin();
});

/**
 * Renderiza páginas do sistema no container principal.
 * @param {string} pagina - Nome da página a renderizar.
 */
function renderizarPagina(pagina) {
    const app = obterElemento('app');

    if (pagina === 'usuarioLayout') {
        app.innerHTML = paginaLayoutUsuario();
        renderizarSection('sectionDashboard');
        return;
    }

    const paginas = {
        login:                 { render: paginaLogin },
        paginaInicial:         { render: paginaInicial },
        cadastroUsuario:       { render: paginaCadastroUsuario },
        cadastroReceita:       { render: paginaCadastroReceita },
        cadastroDespesa:       { render: paginaCadastroDespesa,      init: iniciarPaginaCadastroDespesa },
        cadastroProduto:       { render: paginaCadastroProduto },
        cadastroServico:       { render: paginaCadastroServico },
        cadastroVendaProduto:  { render: paginaCadastroVendaProduto },
        cadastroVendaServico:  { render: paginaCadastroVendaServico },
        esquecerSenha:         { render: paginaEsqueciSenha,         init: initEsqueciSenha },
        validarCod:            { render: paginaValidarCod,           init: initValidarCod },
        alterarSenha:          { render: paginaAlterarSenha,         init: initAlterarSenha },
        login:                 { render: paginaLogin,                init: initLogin },
        paginaEmitente: { render: paginaNfEmitente},
        paginaCliente: {render: paginaNfCliente},
        paginaProduto: {render: paginaNfProduto},
    };

    const entrada = paginas[pagina];

    if (!entrada) {
        app.innerHTML = '<p>Página não encontrada</p>';
        return;
    }

    app.innerHTML = entrada.render();
    entrada.init?.();
}