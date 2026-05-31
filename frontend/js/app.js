/**
 * Inicializa a aplicação após o carregamento da página.
 */
document.addEventListener('DOMContentLoaded', () => {
    verificarLogin();
});

/**
 * Renderiza páginas do sistema no container principal.
 * @param {string} pagina Nome da página.
 */
function renderizarPagina(pagina) {

    const app = document.getElementById('app');

    const paginas = {
        login: paginaLogin,
        paginaInicial: paginaInicial,
        cadastroUsuario: paginaCadastroUsuario,
        cadastroReceita: paginaCadastroReceita,
        cadastroDespesa: paginaCadastroDespesa,
        cadastroProduto: paginaCadastroProduto,
        cadastroServico: paginaCadastroServico,
        cadastroVendaProduto: paginaCadastroVendaProduto,
        cadastroVendaServico: paginaCadastroVendaServico,
        esquecerSenha: paginaEsqueciSenha,
        validarCod: paginaValidarCod,
        alterarSenha: paginaAlterarSenha,
    };

    if (pagina === 'usuarioLayout') {
        app.innerHTML = paginaLayoutUsuario();
        renderizarSection('sectionDashboard');
        return;
    }

    const paginaRenderizada = paginas[pagina];

    if (!paginaRenderizada) {
        app.innerHTML = '<p>Página não encontrada</p>';
        return;
    }

    app.innerHTML = paginaRenderizada();

    if (pagina === 'login') initLogin();
    if (pagina === 'cadastroDespesa') iniciarPaginaCadastroDespesa();
    if (pagina === 'esquecerSenha') initEsqueciSenha();
    if (pagina === 'validarCod') initValidarCod();
    if (pagina === 'alterarSenha') initAlterarSenha();
}