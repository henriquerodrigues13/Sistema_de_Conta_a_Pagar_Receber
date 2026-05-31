/**
 * Remove a classe active de todos os botões do menu.
 */
function limparBotoesAtivos() {
    document.querySelectorAll('aside button').forEach(botao => {
        botao.classList.remove('active');
    });
}

/**
 * Define o botão ativo no menu lateral.
 * @param {string} secao Nome da seção.
 * @param {Event} evento Evento do clique.
 */
function definirBotaoAtivo(secao, evento) {

    if (evento) {
        evento.currentTarget.classList.add('active');
        return;
    }

    const botao = document.getElementById(`btn-${secao}`);

    if (botao) {
        botao.classList.add('active');
    }
}

/**
 * Renderiza a seção selecionada do sistema.
 * @param {string} secao Nome da seção.
 * @param {Event} evento Evento do clique.
 */
function renderizarSection(secao, evento) {
    const section = document.getElementById('section');

    limparBotoesAtivos();

    definirBotaoAtivo(secao, evento);

    switch (secao) {
        case 'sectionReceita':
            section.innerHTML = sectionReceita();
            setTimeout(() => {
                alternaTabelaReceitaVenda('tabelaReceitas');
            }, 500);
            break;
        case 'sectionDespesa':
            section.innerHTML = sectionDespesa();
            setTimeout(() => {
                carregarDespesas(1);
            }, 1000);
            break;
        case 'sectionDashboard':
            section.innerHTML = sectionDashboard();
            setTimeout(() => {
                carregarTotaisDashboard();
            }, 1000);
            break;
        case 'sectionProdutosServicos':
            section.innerHTML = sectionProdutosServicos();
            setTimeout(() => {
                alternaTabelaProdutoServico('tabelaProdutos');
            }, 500);
            break;
        case 'sectionRelatorio':
            section.innerHTML = sectionRelatorio();
            break;

        default:
            section.innerHTML =
                '<p>Página não encontrada</p>';
    }
}