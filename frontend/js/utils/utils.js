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
        renderizarPagina('layout');
        return true;
    } else {
        renderizarPagina('login');
        return false;
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