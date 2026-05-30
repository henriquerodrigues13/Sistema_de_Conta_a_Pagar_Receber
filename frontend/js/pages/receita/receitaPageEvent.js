/**
 * Alterna entre tabela de receitas e vendas.
 */
function alternaTabelaReceitaVenda(nomeTabela) {

    const tabelaReceita      = obterElemento('tabela-receita');
    const tabelaVendas       = obterElemento('tabela-vendas');

    const carregandoReceitas = obterElemento('carregando-receitas');
    const carregandoVendas   = obterElemento('carregando-vendas');

    const totalReceitas      = obterElemento('total-receitas');
    const totalVendas        = obterElemento('total-vendas');

    const btnReceita         = obterElemento('btn-adicionarReceita');
    const btnVenda           = obterElemento('btn-adicionarVenda');

    const inputPesquisa      = obterElemento('input-pesquisarReceitaVenda');

    const paginacao          = obterElemento('paginacao-receitaVenda');

    const opcoesTabelas      = obterElemento('opcoes-tabelas');
    const botoes             = opcoesTabelas
        ? opcoesTabelas.querySelectorAll('button')
        : [];

    botoes.forEach(btn => btn.classList.remove('ativo'));

    if (tabelaReceita) tabelaReceita.style.display = 'none';
    if (tabelaVendas)  tabelaVendas.style.display  = 'none';

    if (paginacao) paginacao.style.display = 'none';

    if (nomeTabela === 'tabelaReceitas') {

        if (carregandoReceitas) carregandoReceitas.style.display = 'block';
        if (carregandoVendas)   carregandoVendas.style.display   = 'none';

        if (totalReceitas) totalReceitas.style.display = 'block';
        if (totalVendas)   totalVendas.style.display   = 'none';

        if (btnReceita) btnReceita.style.display = 'inline-block';
        if (btnVenda)   btnVenda.style.display   = 'none';

        if (inputPesquisa) {
            inputPesquisa.placeholder = 'Pesquisar receitas';
            inputPesquisa.value = '';
        }

        if (botoes[0]) botoes[0].classList.add('ativo');

        setTimeout(() => carregarReceitas(1), 500);

    } else if (nomeTabela === 'tabelaVendas') {

        if (carregandoReceitas) carregandoReceitas.style.display = 'none';
        if (carregandoVendas)   carregandoVendas.style.display   = 'block';

        if (totalReceitas) totalReceitas.style.display = 'none';
        if (totalVendas)   totalVendas.style.display   = 'block';

        if (btnReceita) btnReceita.style.display = 'none';
        if (btnVenda)   btnVenda.style.display   = 'inline-block';

        if (inputPesquisa) {
            inputPesquisa.placeholder = 'Pesquisar vendas';
            inputPesquisa.value = '';
        }

        if (botoes[1]) botoes[1].classList.add('ativo');

        setTimeout(() => carregarVendas(1), 500);
    }
}

/**
 * Carrega receitas.
 */
async function carregarReceitas(pagina = 1) {

    const emailUsuario = obterEmailUsuario();

    const carregando = obterElemento('carregando-receitas');

    if (carregando) carregando.style.display = 'block';

    try {

        const response = await fetch(
            `${API_BASE_URL}/get_receitas/${emailUsuario}?page=${pagina}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        if (!response.ok) {
            const erro = await response.json();
            alert(`Erro ${erro.status}: ${erro.detail}`);
            return;
        }

        const receitas = await response.json();
        console.log(receitas);

        const total = parseInt(
            response.headers.get('X-Total-Items') || '0',
            10
        );

        const totalPages = parseInt(
            response.headers.get('X-Total-Pages') || '1',
            10
        );

        const spanTotal = obterElemento('span-total-receitas');

        if (spanTotal) spanTotal.textContent = total;

        renderizarTabelaReceitas(receitas);

        renderizarPaginacaoReceitaVenda(
            pagina,
            totalPages,
            'receitas'
        );

        const tabela = obterElemento('tabela-receita');

        if (tabela) tabela.style.display = 'table';

    } catch (error) {

        console.error(error.message);

        renderizarTabelaVaziaReceitas();

    } finally {

        if (carregando) carregando.style.display = 'none';
    }
}

/**
 * Carrega vendas.
 */
async function carregarVendas(pagina = 1) {

    const emailUsuario = obterEmailUsuario();

    const carregando = obterElemento('carregando-vendas');

    if (carregando) carregando.style.display = 'block';

    try {

        const response = await fetch(
            `${API_BASE_URL}/get_vendas/${emailUsuario}?page=${pagina}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        if (!response.ok) {

            const erro = await response.json();

            alert(`Erro ${response.status}: ${erro.detail}`);

            return;
        }

        const vendas = await response.json();
        console.log(vendas);

        const total = parseInt(
            response.headers.get('X-Total-Items') || '0',
            10
        );

        const totalPages = parseInt(
            response.headers.get('X-Total-Pages') || '1',
            10
        );

        const spanTotal = obterElemento('span-total-vendas');

        if (spanTotal) spanTotal.textContent = total;

        renderizarTabelaVendas(vendas);

        renderizarPaginacaoReceitaVenda(
            pagina,
            totalPages,
            'vendas'
        );

        const tabela = obterElemento('tabela-vendas');

        if (tabela) tabela.style.display = 'table';

    } catch (error) {

        console.error(error.message);

        renderizarTabelaVaziaVendas();

    } finally {

        if (carregando) carregando.style.display = 'none';
    }
}

/**
 * Renderiza tabela de receitas.
 */
function renderizarTabelaReceitas(receitas) {

    const tabela = obterElemento('tabela-receita');

    if (!tabela) return;

    const tbody = limparTbody(tabela);

    if (receitas.length === 0) {

        renderizarTabelaVaziaReceitas();

        return;
    }

    receitas.forEach(receita => {

        const tr = document.createElement('tr');

        [
            receita.id,
            receita.tipo_da_receita,
            receita.pagador_email,
            receita.valor_da_receita,
            receita.forma_de_pagamento,
            receita.data_da_receita
        ].forEach(valor => {

            const td = document.createElement('td');

            td.textContent = valor || '-';

            tr.appendChild(td);
        });

        const tdOpcoes = document.createElement('td');

        const divOpcoes = document.createElement('div');

        divOpcoes.className = 'opcoes-btns';

        divOpcoes.appendChild(
            criarBotaoAcao(
                './assets/imgs/icons/lapis.png',
                'Editar',
                'btn-editar',
                'Editar receita',
                () => editarReceita(receita.id)
            )
        );

        divOpcoes.appendChild(
            criarBotaoAcao(
                './assets/imgs/icons/lixeira.png',
                'Remover',
                'btn-remover',
                'Remover receita',
                () => removerReceita(receita.id)
            )
        );

        divOpcoes.appendChild(
            criarBotaoAcao(
                './assets/imgs/icons/taxa.png',
                'Nota',
                'btn-ver-nf',
                'Ver Nota Fiscal',
                () => verNotaReceita(receita.id)
            )
        );

        tdOpcoes.appendChild(divOpcoes);

        tr.appendChild(tdOpcoes);

        tbody.appendChild(tr);
    });
}

/**
 * Renderiza tabela de vendas.
 */
function renderizarTabelaVendas(vendas) {

    const tabela = obterElemento('tabela-vendas');

    if (!tabela) return;

    const tbody = limparTbody(tabela);

    if (vendas.length === 0) {

        renderizarTabelaVaziaVendas();

        return;
    }

    vendas.forEach(venda => {

        const tr = document.createElement('tr');

        [
            venda.id,
            venda.nome_do_produto || venda.nome_do_servico,
            venda.comprador_email,
            venda.valor_final,
            venda.forma_de_pagamento,
            venda.data_do_registro_venda
        ].forEach(valor => {

            const td = document.createElement('td');

            td.textContent = valor || '-';

            tr.appendChild(td);
        });

        const tdOpcoes = document.createElement('td');

        const divOpcoes = document.createElement('div');

        divOpcoes.className = 'opcoes-btns';

        divOpcoes.appendChild(
            criarBotaoAcao(
                './assets/imgs/icons/lapis.png',
                'Editar',
                'btn-editar',
                'Editar venda',
                () => editarVenda(venda.id)
            )
        );

        divOpcoes.appendChild(
            criarBotaoAcao(
                './assets/imgs/icons/lixeira.png',
                'Remover',
                'btn-remover',
                'Remover venda',
                () => removerVenda(venda.id)
            )
        );

        divOpcoes.appendChild(
            criarBotaoAcao(
                './assets/imgs/icons/taxa.png',
                'Nota',
                'btn-ver-nf',
                'Ver Nota Fiscal',
                () => verNotaVenda(venda.id)
            )
        );

        tdOpcoes.appendChild(divOpcoes);

        tr.appendChild(tdOpcoes);

        tbody.appendChild(tr);
    });
}

/**
 * Tabela vazia receitas.
 */
function renderizarTabelaVaziaReceitas() {

    const tabela = obterElemento('tabela-receita');

    if (!tabela) return;

    _renderizarLinhaVazia(
        tabela,
        7,
        'Nenhuma receita encontrada'
    );
}

/**
 * Tabela vazia vendas.
 */
function renderizarTabelaVaziaVendas() {

    const tabela = obterElemento('tabela-vendas');

    if (!tabela) return;

    _renderizarLinhaVazia(
        tabela,
        7,
        'Nenhuma venda encontrada'
    );
}

/**
 * Paginação receitas/vendas.
 */
function renderizarPaginacaoReceitaVenda(
    paginaAtual,
    totalPaginas,
    tipo = 'receitas'
) {

    const paginacao = obterElemento('paginacao-receitaVenda');

    if (!paginacao) return;

    paginacao.style.display = 'flex';

    const carregar = tipo === 'vendas'
        ? carregarVendas
        : carregarReceitas;

    const btnProximo = obterElemento('btn-proximaPagina');

    const btnAnterior = obterElemento('btn-anteriorPagina');

    if (btnProximo) {

        btnProximo.onclick = () => {

            if (paginaAtual < totalPaginas) {

                carregar(paginaAtual + 1);
            }
        };

        btnProximo.disabled = paginaAtual >= totalPaginas;

        btnProximo.style.opacity =
            paginaAtual >= totalPaginas
                ? '0.1'
                : '0.9';
    }

    if (btnAnterior) {

        btnAnterior.onclick = () => {

            if (paginaAtual > 1) {

                carregar(paginaAtual - 1);
            }
        };

        btnAnterior.disabled = paginaAtual === 1;

        btnAnterior.style.opacity =
            paginaAtual === 1
                ? '0.1'
                : '0.9';
    }

    const spanPagina = obterElemento('span-pagina');

    if (spanPagina) {

        spanPagina.textContent =
            `Página ${paginaAtual} de ${totalPaginas}`;
    }
}