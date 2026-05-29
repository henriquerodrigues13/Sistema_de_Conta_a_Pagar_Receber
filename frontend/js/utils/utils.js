function obterTipoUsuario() {
    return localStorage.getItem('tipoUsuario');
}

function obterCfpCnpjUsuario(){
    return localStorage.getItem('cfpcnpj');
}

function estaLogado() {
    return localStorage.getItem('usuario') !== null;
}

function verificarLogin() {
    if (estaLogado()) {
        renderizarPagina('usuarioLayout');
        return;
    } else {
        renderizarPagina('paginaInicial');
        return;
    }
}

function logout() {

    localStorage.removeItem('usuario');
    localStorage.removeItem('email');

    renderizarPagina('login');
}

function obterNomeUsuario() {
    const usuario = localStorage.getItem('usuario');
    return usuario ? usuario : 'Usuário';
}

function obterEmailUsuario() {
    const emailUsuario = localStorage.getItem('email');
    return emailUsuario ? emailUsuario : 'Null';
}