/**
 * Busca as receitas do usuário na API e renderiza a tabela com paginação.
 * Em caso de erro na requisição, renderiza a tabela vazia.
 * @param {number} [pagina=1] - Número da página a carregar.
 */
async function carregarReceitas(pagina = 1) {
    const emailUsuario = obterEmailUsuario();
 
    const carregando = document.getElementById('carregando');
    if (carregando) carregando.style.display = 'block';
 
    try {
        const response = await fetch(
            `${API_BASE_URL}/get_vendas/${emailUsuario}?page=${pagina}`,
            { method: 'GET', headers: { 'Content-Type': 'application/json' } }
        );
 
        if (!response.ok) {
            const erro = await response.json();
            alert(`Erro ${erro.status || response.status}: ${erro.detail}`);
            return;
        }
 
        const receitas   = await response.json();
        const total      = parseInt(response.headers.get('X-Total-Items') || '0', 10);
        const totalPages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);
 
        const spanTotal = document.getElementById('span-total');
        if (spanTotal) spanTotal.textContent = total;
 
        renderizarTabelaReceita(receitas);
        renderizarPaginacaoReceita(pagina, totalPages);
 
    } catch (error) {
        console.error(error.message);
        renderizarTabelaVazia();
    } finally {
        if (carregando) carregando.style.display = 'none';
    }
}
 
/**
 * Renderiza as linhas de receitas no tbody da tabela.
 * Exibe tabela vazia caso a lista esteja vazia.
 * @param {Object[]} receitas - Lista de receitas retornada pela API.
 */
function renderizarTabelaReceita(receitas) {
    const tabela = document.getElementById('tabela-receita');
    if (!tabela) return;
 
    const tbody = tabela.querySelector('tbody') || tabela;
    tbody.querySelectorAll('tr').forEach(linha => linha.remove());
 
    if (receitas.length === 0) {
        renderizarTabelaVazia();
        return;
    }
 
    receitas.forEach(receita => {
        const tr = document.createElement('tr');
 
        [
            receita.id,
            receita.nome_do_servico || receita.nome_do_produto,
            receita.comprador_email,
            receita.valor_final,
            receita.forma_de_pagamento,
            receita.descricao_da_venda
        ].forEach(valor => {
            const td = document.createElement('td');
            td.textContent = valor || '-';
            tr.appendChild(td);
        });
 
        const tdOpcoes  = document.createElement('td');
        const divOpcoes = document.createElement('div');
        divOpcoes.className = 'opcoes-btns';
 
        divOpcoes.appendChild(criarBotaoAcao('./assets/imgs/icons/lapis.png',  'Editar',  'btn-editar',   'Editar receita',      () => editarReceita(receita.id)));
        divOpcoes.appendChild(criarBotaoAcao('./assets/imgs/icons/lixeira.png','Remover', 'btn-remover',  'Remover receita',     () => removerReceita(receita.id)));
        divOpcoes.appendChild(criarBotaoAcao('./assets/imgs/icons/taxa.png',   'Ver NF',  'btn-ver-nf',   'Ver Nota Fiscal',     () => verNota(receita.id)));
 
        tdOpcoes.appendChild(divOpcoes);
        tr.appendChild(tdOpcoes);
        tbody.appendChild(tr);
    });
}
 
/**
 * Exibe uma linha de "nenhuma receita encontrada" na tabela de receitas.
 */
function renderizarTabelaVazia() {
    const tabela = document.getElementById('tabela-receita');
    if (!tabela) return;
 
    const tbody = tabela.querySelector('tbody') || tabela;
    tbody.querySelectorAll('tr').forEach(linha => linha.remove());
 
    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.colSpan         = 7;
    td.textContent     = 'Nenhuma receita encontrada';
    td.style.textAlign = 'center';
    td.style.padding   = '20px';
    td.style.color     = 'black';
    td.style.border    = '#B8B8B8 solid 1px';
    tr.appendChild(td);
    tbody.appendChild(tr);
}
 
/**
 * Configura os botões de navegação e o indicador de página da paginação de receitas.
 * Desabilita o botão anterior na primeira página e o próximo na última.
 * @param {number} paginaAtual  - Página atualmente exibida.
 * @param {number} totalPaginas - Total de páginas disponíveis.
 */
function renderizarPaginacaoReceita(paginaAtual, totalPaginas) {
    const paginacao = document.getElementById('paginacao-receita');
    if (!paginacao) return;
 
    paginacao.style.display = 'flex';
 
    const btnProximo  = document.getElementById('btn-proximaPagina');
    const btnAnterior = document.getElementById('btn-anteriorPagina');
 
    if (btnProximo) {
        btnProximo.onclick       = () => { if (paginaAtual < totalPaginas) carregarReceitas(paginaAtual + 1); };
        btnProximo.disabled      = paginaAtual >= totalPaginas;
        btnProximo.style.opacity = paginaAtual >= totalPaginas ? '0.1' : '0.9';
    }
 
    if (btnAnterior) {
        btnAnterior.onclick       = () => { if (paginaAtual > 1) carregarReceitas(paginaAtual - 1); };
        btnAnterior.disabled      = paginaAtual === 1;
        btnAnterior.style.opacity = paginaAtual === 1 ? '0.1' : '0.9';
    }
 
    const spanPagina = document.getElementById('span-pagina');
    if (spanPagina) spanPagina.textContent = `Página ${paginaAtual} de ${totalPaginas}`;
}