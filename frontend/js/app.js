document.addEventListener('DOMContentLoaded', function () {
    verificarLogin();
});

function renderizarPagina(pagina) {
    const app = document.getElementById('app');

    switch (pagina) {
        case 'login':
            app.innerHTML = paginaLogin();
            break;
        case 'cadastroUsuario':
            app.innerHTML = paginaCadastroUsuario();
            break;
        case 'usuarioLayout':
            app.innerHTML = paginaLayoutUsuario();
            renderizarSection('sectionDashboard');
            break;
        default:
            app.innerHTML = '<p>Página não encontrada</p>';
    }
}