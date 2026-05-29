document.addEventListener('DOMContentLoaded', function () {
    verificarLogin();
});

function renderizarPagina(pagina) {
    const app = document.getElementById('app');

    switch (pagina) {
        case 'login':
            app.innerHTML = paginaLogin();
            break;
        case 'paginaInicial':
            app.innerHTML = paginaInicial();
            break;
        case 'cadastroUsuario':
            app.innerHTML = paginaCadastroUsuario();
            break;
        case 'usuarioLayout':
            app.innerHTML = paginaLayoutUsuario();
            renderizarSection('sectionDashboard');
            break;
        case 'cadastroReceita':
            app.innerHTML = paginaCadastroReceita();
            break;
        case 'cadastroProduto':
            app.innerHTML = paginaCadastroProduto();
            break;
        case 'cadastroServico':
            app.innerHTML = paginaCadastroServico();
            break;
        default:
            app.innerHTML = '<p>Página não encontrada</p>';
    }
}