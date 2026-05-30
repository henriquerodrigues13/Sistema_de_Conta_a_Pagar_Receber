/**
 * Alterna entre tabela de receitas e vendas.
 * @param {String} nomeTabela Nome da tabela.
 */
function alternaTabelaReceitaVenda(nomeTabela) {

    const tabelaReceita = obterElemento('tabela-receita');
    const tabelaVendas = obterElemento('tabela-vendas');

    const carregandoReceitas = obterElemento('carregando-receitas');
    const carregandoVendas = obterElemento('carregando-vendas');

    const totalReceitas = obterElemento('total-receitas');
    const totalVendas = obterElemento('total-vendas');

    const btnReceita = obterElemento('btn-adicionarReceita');
    const btnVenda = obterElemento('btn-adicionarVenda');

    const inputPesquisa = obterElemento('input-pesquisarReceitaVenda');

    const paginacao = obterElemento('paginacao-receitaVenda');

    const opcoesTabelas = obterElemento('opcoes-tabelas');
    const botoes = opcoesTabelas ? opcoesTabelas.querySelectorAll('button') : [];

    botoes.forEach(btn => btn.classList.remove('ativo'));

    if (tabelaReceita) tabelaReceita.style.display = 'none';
    if (tabelaVendas) tabelaVendas.style.display = 'none';
    if (paginacao) paginacao.style.display = 'none';

    if (nomeTabela === 'tabelaReceitas') {

        if (carregandoReceitas) carregandoReceitas.style.display = 'block';
        if (carregandoVendas) carregandoVendas.style.display = 'none';

        if (totalReceitas) totalReceitas.style.display = 'block';
        if (totalVendas) totalVendas.style.display = 'none';

        if (btnReceita) btnReceita.style.display = 'inline-block';
        if (btnVenda) btnVenda.style.display = 'none';

        if (inputPesquisa) {
            inputPesquisa.placeholder = 'Pesquisar receitas';
            inputPesquisa.value = '';
        }

        if (botoes[0]) botoes[0].classList.add('ativo');

        setTimeout(() => carregarReceitas(1), 500);

    } else if (nomeTabela === 'tabelaVendas') {

        if (carregandoReceitas) carregandoReceitas.style.display = 'none';
        if (carregandoVendas) carregandoVendas.style.display = 'block';

        if (totalReceitas) totalReceitas.style.display = 'none';
        if (totalVendas) totalVendas.style.display = 'block';

        if (btnReceita) btnReceita.style.display = 'none';
        if (btnVenda) btnVenda.style.display = 'inline-block';

        if (inputPesquisa) {
            inputPesquisa.placeholder = 'Pesquisar vendas';
            inputPesquisa.value = '';
        }

        if (botoes[1]) botoes[1].classList.add('ativo');

        setTimeout(() => carregarVendas(1), 500);
    }
}

/**
 * Busca as receitas do usuario na API e renderiza a tabela com paginação.
 * @param {number} [pagina=1] Numero da pagina a carregar.
 */
async function carregarReceitas(pagina = 1) {
    const emailUsuario = obterEmailUsuario();

    const carregando = obterElemento('carregando-receitas');

    if (carregando) carregando.style.display = 'block';

    try {

        const response = await fetch(`${API_BASE_URL}/get_receitas/${emailUsuario}?page=${pagina}`,
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

        const totalDeReceitas = parseInt(response.headers.get('X-Total-Items') || '0', 10);

        const totalDePages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);

        atualizarTotal(totalDeReceitas, 'span-total-receitas');

        renderizarTabelaReceitas(receitas);

        renderizarPaginacaoReceitaVenda(pagina, totalDePages, 'receitas');

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
 * Busca as vendas do usuario na API e carrega na tabela.
 * @param {number} [pagina=1] Numero da pagina.
 */
async function carregarVendas(pagina = 1) {

    const emailUsuario = obterEmailUsuario();

    const carregando = obterElemento('carregando-vendas');

    if (carregando) carregando.style.display = 'block';

    try {

        const response = await fetch(`${API_BASE_URL}/get_vendas/${emailUsuario}?page=${pagina}`,
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

        const totalDeVendas = parseInt(response.headers.get('X-Total-Items') || '0', 10);

        const totalDePages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);

        atualizarTotal(totalDeVendas, 'span-total-vendas');

        renderizarTabelaVendas(vendas);

        renderizarPaginacaoReceitaVenda(pagina, totalDePages, 'vendas');

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
 * Renderiza as linhas de receitas no tbody da tabela.
 * @param {object[]} receitas - Lista de receitas retornada pela API
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
            receita.identificador,
            receita.tipo_da_receita,
            receita.pagador_email,
            receita.valor_da_receita,
            receita.forma_de_pagamento,
            receita.data_da_receita.split('T')[0]
        ].forEach(valor => {
            const td = document.createElement('td');
            td.textContent = valor || '-';
            tr.appendChild(td);
        });

        const tdOpcoes = document.createElement('td');

        const divOpcoes = document.createElement('div');

        divOpcoes.className = 'opcoes-btns';

        divOpcoes.appendChild(
            criarBotaoAcao('./assets/imgs/icons/lapis.png', 'Editar', 'btn-editar', 'Editar receita', () => editarReceita(receita.identificador))
        );

        divOpcoes.appendChild(
            criarBotaoAcao(
                './assets/imgs/icons/lixeira.png',
                'Remover',
                'btn-remover',
                'Remover receita',
                () => removerReceita(receita.identificador)
            )
        );

        divOpcoes.appendChild(
            criarBotaoAcao(
                './assets/imgs/icons/taxa.png',
                'Nota',
                'btn-ver-nf',
                'Ver Nota Fiscal',
                () => verNotaReceita(receita.identificador)
            )
        );

        tdOpcoes.appendChild(divOpcoes);

        tr.appendChild(tdOpcoes);

        tbody.appendChild(tr);
    });
}

/**
 * Renderiza as linhas de vendas no tbody da tabela.
 * @param {object[]} vendas - Lista de vendas retornada pela API
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
            venda.identificador,
            venda.nome_do_produto || venda.nome_do_servico,
            venda.comprador_email,
            venda.valor_final,
            venda.forma_de_pagamento,
            venda.data_do_registro_venda.split('T')[0]
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
                () => editarVenda(venda.identificador)
            )
        );

        divOpcoes.appendChild(
            criarBotaoAcao(
                './assets/imgs/icons/lixeira.png',
                'Remover',
                'btn-remover',
                'Remover venda',
                () => removerVenda(venda.identificador)
            )
        );

        divOpcoes.appendChild(
            criarBotaoAcao(
                './assets/imgs/icons/taxa.png',
                'Nota',
                'btn-ver-nf',
                'Ver Nota Fiscal',
                () => verNotaVenda(venda.identificador)
            )
        );

        tdOpcoes.appendChild(divOpcoes);

        tr.appendChild(tdOpcoes);

        tbody.appendChild(tr);
    });
}

/**
 *Renderiza linha de 'nenhuma receita encontrada' na tabela de receitas.
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
 * Renderiza linha de 'nenhuma venda encontrada' na tabela de vendas.
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
 * Configura os botões de navegação e o indicador de página da paginação de receitas/vendas.
 * Desabilita o botão anterior na primeira página e o próximo na última.
 * @param {number} paginaAtual  - Página atualmente exibida.
 * @param {number} totalPaginas - Total de páginas disponíveis.
 * @param {string} [tipo='receitas'] - Tipo da tabela (receita ou venda).
 */
function renderizarPaginacaoReceitaVenda(paginaAtual, totalPaginas, tipo = 'receitas') {
    const paginacao = obterElemento('paginacao-receitaVenda');

    if (!paginacao) return;

    paginacao.style.display = 'flex';

    const carregar = tipo === 'vendas' ? carregarVendas : carregarReceitas;

    const btnProximo = obterElemento('btn-proximaPagina');

    const btnAnterior = obterElemento('btn-anteriorPagina');

    if (btnProximo) {
        btnProximo.onclick = () => {
            if (paginaAtual < totalPaginas) {
                carregar(paginaAtual + 1);
            }
        };

        btnProximo.disabled = paginaAtual >= totalPaginas;

        btnProximo.style.opacity = paginaAtual >= totalPaginas ? '0.1' : '0.9';
    }

    if (btnAnterior) {
        btnAnterior.onclick = () => {
            if (paginaAtual > 1) {
                carregar(paginaAtual - 1);
            }
        };

        btnAnterior.disabled = paginaAtual === 1;

        btnAnterior.style.opacity = paginaAtual === 1 ? '0.1' : '0.9';
    }

    const spanPagina = obterElemento('span-pagina');

    if (spanPagina) spanPagina.textContent = `Página ${paginaAtual} de ${totalPaginas}`;
}

/**
 * Solicita confirmação e envia requisição DELETE para remover uma receita.
 * Recarrega a tabela em caso de sucesso.
 * @param {string} identificador - Identificador único da receita.
 */
async function removerReceita(identificador) {
    if (!confirm('Deseja realmente remover esta receita?')) return;

    const emailUsuario = obterEmailUsuario();

    try {
        const response = await fetch(
            `${API_BASE_URL}/delete_receita/${emailUsuario}/${encodeURIComponent(identificador)}`,
            { method: 'DELETE', headers: { 'Content-Type': 'application/json' } }
        );

        if (!response.ok) {
            const erro = await response.json();
            alert(response.status === 404
                ? '❌ Receita não encontrada'
                : `❌ Erro ${response.status}: ${erro.detail || 'Erro desconhecido'}`
            );
            return;
        }

        alert('✅ Receita removida com sucesso');
        carregarReceitas(1);

    } catch (error) {
        console.error('Erro ao remover receita:', error);
        alert(`❌ Erro ao remover receita: ${error.message}`);
    }
}

/**
 * Solicita confirmação e envia requisição DELETE para remover uma venda.
 * Recarrega a tabela em caso de sucesso.
 * @param {string} identificador - Identificador único da venda.
 */
async function removerVenda(identificador) {
    if (!confirm('Deseja realmente remover esta venda?')) return;

    const emailUsuario = obterEmailUsuario();

    try {
        const response = await fetch(
            `${API_BASE_URL}/delete_venda/${emailUsuario}/${encodeURIComponent(identificador)}`,
            { method: 'DELETE', headers: { 'Content-Type': 'application/json' } }
        );

        if (!response.ok) {
            const erro = await response.json();
            alert(response.status === 404
                ? '❌ Venda não encontrada'
                : `❌ Erro ${response.status}: ${erro.detail || 'Erro desconhecido'}`
            );
            return;
        }

        alert('✅ Venda removida com sucesso');
        carregarVendas(1);

    } catch (error) {
        console.error('Erro ao remover venda:', error);
        alert(`❌ Erro ao remover venda: ${error.message}`);
    }
}

/**
 * Abre a página de cadastro de receita preenchida com os dados atuais para edição.
 * @param {string} identificador - Identificador único da receita.
 */
function editarReceita(identificador) {
    renderizarPagina('cadastroReceita');

    setTimeout(async () => {
        const emailUsuario = obterEmailUsuario();

        try {
            const response = await fetch(
                `${API_BASE_URL}/get_receitas/${emailUsuario}?page=1`,
                { method: 'GET', headers: { 'Content-Type': 'application/json' } }
            );

            if (!response.ok) {
                alert('❌ Erro ao carregar receita.');
                return;
            }

            const receitas = await response.json();
            const receita = receitas.find(r => r.identificador === identificador);

            if (!receita) {
                alert('❌ Receita não encontrada.');
                return;
            }

            document.getElementById('input-tipoReceita').value          = receita.tipo_da_receita   || '';
            document.getElementById('input-emailPagador').value         = receita.pagador_email      || '';
            document.getElementById('input-dataCadastroReceita').value  = receita.data_da_receita?.split('T')[0] || '';
            document.getElementById('input-valorReceita').value         = receita.valor_da_receita   || '';
            document.getElementById('opcoes-pagamentos').value          = receita.forma_de_pagamento || '';
            document.getElementById('input-observacaoReceita').value    = receita.observacao         || '';

            const btn = obterElemento('cadastrarReceita');
            btn.textContent = 'Atualizar';
            btn.onclick = () => atualizarReceita(identificador);

        } catch (error) {
            console.error('Erro ao carregar receita:', error);
            alert(`❌ Erro de conexão: ${error.message}`);
        }
    }, 0);
}

/**
 * Coleta os campos do formulário e envia PATCH para atualizar uma receita.
 * @param {string} identificador - Identificador único da receita.
 */
async function atualizarReceita(identificador) {
    const tipoReceita    = document.getElementById('input-tipoReceita').value.trim();
    const emailPagador   = document.getElementById('input-emailPagador').value.trim();
    const dataReceita    = document.getElementById('input-dataCadastroReceita').value;
    const valorRaw       = document.getElementById('input-valorReceita').value.trim();
    const formaPagamento = document.getElementById('opcoes-pagamentos').value;
    const observacao     = document.getElementById('input-observacaoReceita').value.trim();

    if (!tipoReceita)   return alert('O tipo ou nome da receita é obrigatório.');
    if (!dataReceita)   return alert('A data de cadastro é obrigatória.');

    const valorReceita = parseFloat(valorRaw.replace(',', '.'));
    if (!valorRaw || isNaN(valorReceita) || valorReceita <= 0)
        return alert('Informe um valor válido para a receita. Ex: 150,00');

    if (!formaPagamento) return alert('Selecione a forma de pagamento.');

    const body = {
        tipo_da_receita:    tipoReceita,
        data_da_receita:    dataReceita,
        valor_da_receita:   valorReceita,
        forma_de_pagamento: formaPagamento,
        ...(emailPagador && { pagador_email: emailPagador }),
        ...(observacao   && { observacao }),
    };

    const emailUsuario = obterEmailUsuario();

    try {
        const response = await fetch(
            `${API_BASE_URL}/update_receita/${emailUsuario}/${encodeURIComponent(identificador)}`,
            {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            }
        );

        if (!response.ok) {
            const erro = await response.json();
            alert(response.status === 404
                ? '❌ Receita não encontrada'
                : `❌ Erro ${response.status}: ${erro.detail || 'Erro desconhecido'}`
            );
            return;
        }

        alert('✅ Receita atualizada com sucesso!');
        renderizarPagina('usuarioLayout');

    } catch (error) {
        console.error('Erro ao atualizar receita:', error);
        alert(`❌ Erro de conexão: ${error.message}`);
    }
}

/**
 * Abre a página de cadastro de venda preenchida com os dados atuais para edição.
 * Detecta automaticamente se é venda de produto ou serviço pelo campo presente.
 * @param {string} identificador - Identificador único da venda.
 */
function editarVenda(identificador) {
    const emailUsuario = obterEmailUsuario();

    fetch(`${API_BASE_URL}/get_vendas/${emailUsuario}?page=1`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(res => {
            if (!res.ok) throw new Error('Erro ao buscar vendas');
            return res.json();
        })
        .then(vendas => {
            const venda = vendas.find(v => v.identificador === identificador);

            if (!venda) {
                alert('❌ Venda não encontrada.');
                return;
            }

            const isProduto = Boolean(venda.nome_do_produto);

            renderizarPagina(isProduto ? 'cadastroVendaProduto' : 'cadastroVendaServico');

            setTimeout(() => {
                if (isProduto) {
                    document.getElementById('input-nome-produto').value              = venda.nome_do_produto         || '';
                    document.getElementById('input-valor-produto').value             = venda.valor_da_venda          || '';
                    document.getElementById('input-quantidade-produto').value        = venda.quantidade              || 1;
                    document.getElementById('input-desconto-produto').value          = venda.porcentagem_do_desconto || 0;
                    document.getElementById('input-comprador-email-produto').value   = venda.comprador_email         || '';
                    document.getElementById('input-comprador-cpf-produto').value     = venda.comprador_cpf           || '';
                    document.getElementById('input-pagamento-produto').value         = venda.forma_de_pagamento      || '';
                    document.getElementById('input-descricao-produto').value         = venda.descricao_da_venda      || '';

                    const btn = obterElemento('btn-cadastrarVendaProduto');
                    btn.textContent = 'Atualizar';
                    btn.onclick = () => atualizarVenda(identificador, true);

                } else {
                    document.getElementById('input-nome-servico').value              = venda.nome_do_servico         || '';
                    document.getElementById('input-valor-servico').value             = venda.valor_da_venda          || '';
                    document.getElementById('input-desconto-servico').value          = venda.porcentagem_do_desconto || 0;
                    document.getElementById('input-comprador-email-servico').value   = venda.comprador_email         || '';
                    document.getElementById('input-comprador-cpf-servico').value     = venda.comprador_cpf           || '';
                    document.getElementById('input-pagamento-servico').value         = venda.forma_de_pagamento      || '';
                    document.getElementById('input-descricao-servico').value         = venda.descricao_da_venda      || '';

                    const btn = obterElemento('btn-cadastrarVendaServico');
                    btn.textContent = 'Atualizar';
                    btn.onclick = () => atualizarVenda(identificador, false);
                }
            }, 0);
        })
        .catch(error => {
            console.error('Erro ao carregar venda:', error);
            alert(`❌ Erro de conexão: ${error.message}`);
        });
}

/**
 * Coleta os campos do formulário e envia PATCH para atualizar uma venda.
 * @param {string} identificador - Identificador único da venda.
 * @param {boolean} isProduto - Indica se é venda de produto ou serviço.
 */
async function atualizarVenda(identificador, isProduto) {
    let nome, valor, desconto, quantidade, pagamento, descricao, compradorEmail, compradorCpf, nomeCampo;

    if (isProduto) {
        nome           = document.getElementById('input-nome-produto').value.trim();
        valor          = parseFloat(document.getElementById('input-valor-produto').value);
        quantidade     = parseInt(document.getElementById('input-quantidade-produto').value) || 1;
        desconto       = parseFloat(document.getElementById('input-desconto-produto').value) || 0;
        pagamento      = document.getElementById('input-pagamento-produto').value;
        descricao      = document.getElementById('input-descricao-produto').value.trim();
        compradorEmail = document.getElementById('input-comprador-email-produto').value.trim();
        compradorCpf   = document.getElementById('input-comprador-cpf-produto').value.trim();
        nomeCampo      = 'nome_do_produto';
    } else {
        nome           = document.getElementById('input-nome-servico').value.trim();
        valor          = parseFloat(document.getElementById('input-valor-servico').value);
        quantidade     = 1;
        desconto       = parseFloat(document.getElementById('input-desconto-servico').value) || 0;
        pagamento      = document.getElementById('input-pagamento-servico').value;
        descricao      = document.getElementById('input-descricao-servico').value.trim();
        compradorEmail = document.getElementById('input-comprador-email-servico').value.trim();
        compradorCpf   = document.getElementById('input-comprador-cpf-servico').value.trim();
        nomeCampo      = 'nome_do_servico';
    }

    if (!nome)                      return alert(`❌ Informe o nome do ${isProduto ? 'produto' : 'serviço'}.`);
    if (isNaN(valor) || valor <= 0) return alert('❌ Informe um valor válido.');
    if (!pagamento)                 return alert('❌ Selecione a forma de pagamento.');

    const valorFinal = calcularValorFinal(valor, quantidade, desconto);

    const body = {
        [nomeCampo]:             nome,
        valor_da_venda:          valor,
        quantidade,
        porcentagem_do_desconto: desconto,
        valor_final:             valorFinal,
        forma_de_pagamento:      pagamento,
        descricao_da_venda:      descricao || '',
        ...(compradorEmail && { comprador_email: compradorEmail }),
        ...(compradorCpf   && { comprador_cpf:   compradorCpf   }),
    };

    const emailUsuario  = obterEmailUsuario();
    const btnId         = isProduto ? 'btn-cadastrarVendaProduto' : 'btn-cadastrarVendaServico';
    const btn           = obterElemento(btnId);
    const textoOriginal = btn?.textContent;

    try {
        if (btn) { btn.disabled = true; btn.textContent = '⏳ Processando...'; }

        const response = await fetch(
            `${API_BASE_URL}/update_venda/${emailUsuario}/${encodeURIComponent(identificador)}`,
            {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            }
        );

        if (!response.ok) {
            const erro = await response.json();
            alert(response.status === 404
                ? '❌ Venda não encontrada'
                : `❌ Erro ${response.status}: ${erro.detail || 'Erro desconhecido'}`
            );
            return;
        }

        alert('✅ Venda atualizada com sucesso!');
        renderizarPagina('usuarioLayout');

    } catch (error) {
        console.error('Erro ao atualizar venda:', error);
        alert(`❌ Erro de conexão: ${error.message}`);
    } finally {
        if (btn) { btn.disabled = false; btn.textContent = textoOriginal; }
    }
}