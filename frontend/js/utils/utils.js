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
        renderizarPagina('login');
        return;
    }
}

function logout() {

    localStorage.removeItem('usuario');
    localStorage.removeItem('tipoUsuario');
    localStorage.removeItem('cfpcnpj');

    renderizarPagina('login');
}

function obterNomeUsuario() {
    const usuario = localStorage.getItem('usuario');
    return usuario ? usuario : 'Usuário';
}