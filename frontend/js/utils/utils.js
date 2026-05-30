/**
 * Verifica se existe usuário logado.
 * @returns {boolean} Status do login.
 */
function estaLogado() {
    return (localStorage.getItem('usuario') !== null);
}

/**
 * Verifica o login do usuário e renderiza a página correta.
 */
function verificarLogin() {
    if (estaLogado()) {
        renderizarPagina('usuarioLayout');
        return;
    }
    renderizarPagina('paginaInicial');
}

/**
 * Remove os dados do usuário do localStorage e renderiza a pagina de login.
 */
function logout() {
    localStorage.removeItem('usuario');
    localStorage.removeItem('email');
    renderizarPagina('login');
}

/**
 * Obtém o nome do usuário salvo no localStorage.
 * @returns {string} Nome do usuário.
 */
function obterNomeUsuario() {
    const usuario = localStorage.getItem('usuario');
    return usuario || 'Usuário';
}

/**
 * Obtém o e-mail do usuário salvo no localStorage.
 * @returns {string} E-mail do usuário.
 */
function obterEmailUsuario() {
    const emailUsuario = localStorage.getItem('email');
    return emailUsuario || 'Null';
}

/**
 * Retorna o elemento do DOM pelo ID informado.
 * Emite um aviso no console caso o elemento não seja encontrado.
 * @param {string} id - ID do elemento.
 * @returns {HTMLElement|null}
 */
function obterElemento(id) {
    const elemento = document.getElementById(id);
    if (!elemento) {
        console.warn(`⚠️ Elemento com ID "${id}" não encontrado`);
    }
    return elemento;
}

/**
 * Cria um botão de ação (editar/remover/vender) com ícone para as tabelas.
 * @param {string} srcImg   - Caminho do ícone.
 * @param {string} altImg   - Texto alternativo da imagem.
 * @param {string} className - Classe CSS do botão.
 * @param {string} title    - Tooltip do botão.
 * @param {Function} handler - Função executada ao clicar.
 * @returns {HTMLButtonElement}
 */
function criarBotaoAcao(srcImg, altImg, className, title, handler) {
    const btn = document.createElement('button');
    const img = document.createElement('img');
    img.src = srcImg;
    img.alt = altImg;
    btn.appendChild(img);
    btn.className = className;
    btn.title = title;
    btn.onclick = handler;
    return btn;
}

/**
 * Limpa o tbody de uma tabela e remove todas as linhas existentes.
 * @param {HTMLElement} tabela - Elemento da tabela.
 * @returns {HTMLElement} tbody limpo.
 */
function limparTbody(tabela) {
    const tbody = tabela.querySelector('tbody') || tabela;
    tbody.querySelectorAll('tr').forEach(linha => linha.remove());
    return tbody;
}

/**
 * Insere uma única linha centralizada com mensagem de lista vazia em uma tabela.
 * @param {HTMLElement} tabela   - Elemento da tabela.
 * @param {number}      colSpan  - Número de colunas a mesclar.
 * @param {string}      mensagem - Texto a exibir.
 */
function _renderizarLinhaVazia(tabela, colSpan, mensagem) {
    const tbody = limparTbody(tabela);
    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.colSpan = colSpan;
    td.textContent = mensagem;
    td.style.textAlign = 'center';  
    td.style.padding = '20px';
    td.style.color = 'black';
    td.style.border = '#B8B8B8 solid 1px';
    tr.appendChild(td);
    tbody.appendChild(tr);
}

/**
 * Atualiza o contador de total exibido na tela.
 * @param {number} total - Quantidade total de despesas.
 * @param {string} span - ID do elemento do contador de total.
 */
function atualizarTotal(total, span) {
    const spanTotal = obterElemento(span);
    if (spanTotal) spanTotal.textContent = total;
}