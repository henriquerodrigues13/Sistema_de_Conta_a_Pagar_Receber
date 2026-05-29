/**
 * Obtém o tipo do usuário salvo no localStorage.
 * @returns {string|null} Tipo do usuário.
 */
function obterTipoUsuario() {

    return localStorage.getItem(
        'tipoUsuario'
    );
}

/**
 * Obtém o CPF ou CNPJ do usuário salvo no localStorage.
 * @returns {string|null} CPF ou CNPJ do usuário.
 */
function obterCfpCnpjUsuario() {

    return localStorage.getItem(
        'cfpcnpj'
    );
}

/**
 * Verifica se existe usuário autenticado.
 * @returns {boolean} Status do login.
 */
function estaLogado() {

    return (
        localStorage.getItem('usuario') !== null
    );
}

/**
 * Verifica o login do usuário e renderiza a página correta.
 */
function verificarLogin() {

    if (estaLogado()) {

        renderizarPagina(
            'usuarioLayout'
        );

        return;
    }

    renderizarPagina(
        'paginaInicial'
    );
}

/**
 * Remove os dados do usuário do localStorage.
 */
function logout() {

    localStorage.removeItem(
        'usuario'
    );

    localStorage.removeItem(
        'email'
    );

    renderizarPagina('login');
}

/**
 * Obtém o nome do usuário salvo no localStorage.
 * @returns {string} Nome do usuário.
 */
function obterNomeUsuario() {

    const usuario = localStorage.getItem(
        'usuario'
    );

    return usuario || 'Usuário';
}

/**
 * Obtém o e-mail do usuário salvo no localStorage.
 * @returns {string} E-mail do usuário.
 */
function obterEmailUsuario() {

    const emailUsuario = localStorage.getItem(
        'email'
    );

    return emailUsuario || 'Null';
}