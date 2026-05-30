/**
 * Busca as despesas do usuário na API e renderiza a tabela com paginação.
 * Em caso de erro na requisição, renderiza a tabela vazia.
 * Rota: GET /get_despesas/{usuario_email}
 * @param {number} [pagina=1] - Número da página a carregar.
 */
async function carregarDespesas(pagina = 1) {
    const emailUsuario = obterEmailUsuario();
 
    const carregando = document.getElementById('carregando');
    if (carregando) carregando.style.display = 'block';
 
    try {
        const response = await fetch(
            `${API_BASE_URL}/get_despesas/${emailUsuario}?page=${pagina}`,
            { method: 'GET', headers: { 'Content-Type': 'application/json' } }
        );
 
        if (!response.ok) {
            const erro = await response.json();
            alert(`Erro ${erro.status || response.status}: ${erro.detail}`);
            return;
        }
 
        const despesas  = await response.json();
        const total      = parseInt(response.headers.get('X-Total-Items') || '0', 10);
        const totalPages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);
 
        atualizarTotalDespesas(total);
        renderizarTabelaDespesa(despesas);
        renderizarPaginacaoDespesa(pagina, totalPages);
 
    } catch (error) {
        console.error(error.message);
        renderizarTabelaVaziaDespesa();
    } finally {
        if (carregando) carregando.style.display = 'none';
    }
}
 
/**
 * Atualiza o contador de total de despesas exibido na tela.
 * @param {number} total - Quantidade total de despesas.
 */
function atualizarTotalDespesas(total) {
    const spanTotal = document.getElementById('span-total');
    if (spanTotal) spanTotal.textContent = total;
}
 
/**
 * Remove todas as linhas existentes no tbody da tabela.
 * @param {HTMLElement} tbody - Corpo da tabela a ser limpo.
 */
function limparTabelaDespesa(tbody) {
    tbody.querySelectorAll('tr').forEach(linha => linha.remove());
}
 
/**
 * Cria um botão de ação com ícone para a tabela de despesas.
 * @param {string}   imagem - Caminho do ícone.
 * @param {string}   alt    - Texto alternativo da imagem.
 * @param {string}   classe - Classe CSS do botão.
 * @param {string}   titulo - Tooltip do botão.
 * @param {Function} evento - Handler do clique.
 * @returns {HTMLButtonElement}
 */
function criarBotaoDespesa(imagem, alt, classe, titulo, evento) {
    const botao = document.createElement('button');
    const img   = document.createElement('img');
    img.src  = imagem;
    img.alt  = alt;
    botao.appendChild(img);
    botao.className = classe;
    botao.title     = titulo;
    botao.onclick   = evento;
    return botao;
}
 
/**
 * Renderiza as linhas de despesas no tbody da tabela.
 * Exibe tabela vazia caso a lista esteja vazia.
 * Campos exibidos: identificador, tipo_da_despesa, descricao_da_despesa, valor_total_da_despesa.
 * @param {Object[]} despesas - Lista de despesas retornada pela API.
 */
function renderizarTabelaDespesa(despesas) {
    const tabela = document.getElementById('tabela-despesa');
    if (!tabela) return;
 
    const tbody = tabela.querySelector('tbody');
    limparTabelaDespesa(tbody);
 
    if (!despesas.length) {
        renderizarTabelaVaziaDespesa();
        return;
    }
 
    despesas.forEach(despesa => {
        const tr = document.createElement('tr');
 
        [
            despesa.identificador,
            despesa.tipo_da_despesa,
            despesa.descricao_da_despesa,
            despesa.valor_total_da_despesa
        ].forEach(valor => {
            const td = document.createElement('td');
            td.textContent = valor || '-';
            tr.appendChild(td);
        });
 
        const tdOpcoes  = document.createElement('td');
        const divOpcoes = document.createElement('div');
        divOpcoes.className = 'opcoes-btns-despesa';
 
        divOpcoes.appendChild(criarBotaoDespesa('./assets/imgs/icons/lapis.png',   'Editar',  'btn-editar-despesa', 'Editar Despesa',  () => editarDespesa(despesa.identificador)));
        divOpcoes.appendChild(criarBotaoDespesa('./assets/imgs/icons/lixeira.png', 'Remover', 'btn-remover',        'Remover Despesa', () => removerDespesa(despesa.identificador)));
        divOpcoes.appendChild(criarBotaoDespesa('./assets/imgs/icons/taxa.png',    'Ver NF',  'btn-ver-nf',         'Ver Nota Fiscal', () => verNota(despesa.identificador)));
 
        tdOpcoes.appendChild(divOpcoes);
        tr.appendChild(tdOpcoes);
        tbody.appendChild(tr);
    });
}
 
/**
 * Exibe uma linha de "nenhuma despesa encontrada" na tabela de despesas.
 */
function renderizarTabelaVaziaDespesa() {
    const tabela = document.getElementById('tabela-despesa');
    if (!tabela) return;
 
    const tbody = tabela.querySelector('tbody');
    limparTabelaDespesa(tbody);
 
    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.colSpan         = 5;
    td.textContent     = 'Nenhuma despesa encontrada';
    td.style.textAlign = 'center';
    td.style.padding   = '20px';
    td.style.color     = 'black';
    td.style.border    = '#B8B8B8 solid 1px';
    tr.appendChild(td);
    tbody.appendChild(tr);
}
 
/**
 * Configura os botões de navegação e o indicador de página da paginação de despesas.
 * Desabilita o botão anterior na primeira página e o próximo na última.
 * @param {number} paginaAtual  - Página atualmente exibida.
 * @param {number} totalPaginas - Total de páginas disponíveis.
 */
function renderizarPaginacaoDespesa(paginaAtual, totalPaginas) {
    const paginacao = document.getElementById('paginacao-despesa');
    if (!paginacao) return;
 
    paginacao.style.display = 'flex';
 
    const btnProximo  = document.getElementById('btn-proximaPagina');
    const btnAnterior = document.getElementById('btn-anteriorPagina');
 
    if (btnProximo) {
        btnProximo.onclick       = () => { if (paginaAtual < totalPaginas) carregarDespesas(paginaAtual + 1); };
        btnProximo.disabled      = paginaAtual >= totalPaginas;
        btnProximo.style.opacity = paginaAtual >= totalPaginas ? '0.1' : '0.9';
    }
 
    if (btnAnterior) {
        btnAnterior.onclick       = () => { if (paginaAtual > 1) carregarDespesas(paginaAtual - 1); };
        btnAnterior.disabled      = paginaAtual === 1;
        btnAnterior.style.opacity = paginaAtual === 1 ? '0.1' : '0.9';
    }
 
    const spanPagina = document.getElementById('span-pagina');
    if (spanPagina) spanPagina.textContent = `Página ${paginaAtual} de ${totalPaginas}`;
}
 
/**
 * Solicita confirmação e envia requisição DELETE (soft delete) para remover uma despesa.
 * Rota: DELETE /delete_despesa/{usuario_email}/{identificador}
 * Recarrega a tabela em caso de sucesso.
 * @param {string} identificador - Identificador único da despesa.
 */
async function removerDespesa(identificador) {
    if (!confirm(`Deseja realmente remover esta despesa?`)) return;
 
    const emailUsuario = obterEmailUsuario();
 
    try {
        const response = await fetch(
            `${API_BASE_URL}/delete_despesa/${emailUsuario}/${encodeURIComponent(identificador)}`,
            { method: 'DELETE', headers: { 'Content-Type': 'application/json' } }
        );
 
        if (!response.ok) {
            const erro = await response.json();
            alert(response.status === 404
                ? '❌ Despesa não encontrada'
                : `❌ Erro ${response.status}: ${erro.detail || 'Erro desconhecido'}`
            );
            return;
        }
 
        alert('✅ Despesa removida com sucesso');
        carregarDespesas(1);
 
    } catch (error) {
        console.error('Erro ao remover despesa:', error);
        alert(`❌ Erro ao remover despesa: ${error.message}`);
    }
}

/**
 * Abre a página de cadastro de despesa preenchida com os dados atuais para edição.
 * Rota: PATCH /update_despesa/{usuario_email}/{identificador}
 * @param {string} identificador - Identificador único da despesa.
 */
function editarDespesa(identificador) {
    renderizarPagina('cadastroDespesa');

    // Aguarda o HTML ser inserido no DOM antes de preencher os campos
    setTimeout(async () => {
        const emailUsuario = obterEmailUsuario();

        try {
            const response = await fetch(
                `${API_BASE_URL}/get_despesas/${emailUsuario}?page=1`,
                { method: 'GET', headers: { 'Content-Type': 'application/json' } }
            );

            if (!response.ok) {
                alert('❌ Erro ao carregar despesa.');
                return;
            }

            const despesas = await response.json();
            const despesa  = despesas.find(d => d.identificador === identificador);

            if (!despesa) {
                alert('❌ Despesa não encontrada.');
                return;
            }

            // Preenche os campos com os dados da despesa
            document.getElementById('input-tipoDespesa').value        = despesa.tipo_da_despesa        || '';
            document.getElementById('input-descricaoDespesa').value   = despesa.descricao_da_despesa   || '';
            document.getElementById('input-valorTotalDespesa').value  = despesa.valor_total_da_despesa || '';
            document.getElementById('opcoes-pagamentosDespesa').value = despesa.forma_de_pagamento     || '';
            document.getElementById('input-valorUnidadeDespesa').value= despesa.valor_por_unidade      || '';
            document.getElementById('input-observacaoReceita').value  = despesa.observacao             || '';

            if (despesa.valor_de_revenda) {
                document.getElementById('input-revenda').checked              = true;
                document.getElementById('form-group-footer').style.display   = 'grid';
                document.getElementById('input-valorUnidadeRevenda').value   = despesa.valor_de_revenda;
            }

            // Troca o botão de cadastrar para atualizar
            const btn = document.getElementById('cadastrarReceita');
            btn.textContent = 'Atualizar';
            btn.onclick     = () => atualizarDespesa(identificador);

        } catch (error) {
            console.error('Erro ao carregar despesa:', error);
            alert(`❌ Erro de conexão: ${error.message}`);
        }
    }, 0);
}

/**
 * Coleta os campos do formulário e envia PATCH para atualizar a despesa.
 * Rota: PATCH /update_despesa/{usuario_email}/{identificador}
 * @param {string} identificador - Identificador único da despesa.
 */
async function atualizarDespesa(identificador) {
    const tipoDespesa    = document.getElementById('input-tipoDespesa').value.trim();
    const descricao      = document.getElementById('input-descricaoDespesa').value.trim();
    const valorTotal     = document.getElementById('input-valorTotalDespesa').value;
    const formaPagamento = document.getElementById('opcoes-pagamentosDespesa').value;
    const valorUnidade   = document.getElementById('input-valorUnidadeDespesa').value;
    const isRevenda      = document.getElementById('input-revenda').checked;
    const valorRevenda   = document.getElementById('input-valorUnidadeRevenda')?.value || null;

    if (!tipoDespesa) return alert('Informe o tipo ou nome da despesa.');
    if (!valorTotal || Number(valorTotal) <= 0) return alert('Informe um valor total válido.');
    if (!formaPagamento) return alert('Selecione a forma de pagamento.');
    if (isRevenda && (!valorRevenda || Number(valorRevenda) <= 0)) return alert('Informe o valor de revenda.');

    const body = {
        tipo_da_despesa:        tipoDespesa,
        descricao_da_despesa:   descricao      || null,
        valor_total_da_despesa: Number(valorTotal),
        forma_de_pagamento:     formaPagamento,
        valor_por_unidade:      valorUnidade   ? Number(valorUnidade) : null,
        valor_de_revenda:       isRevenda      ? Number(valorRevenda) : null,
    };

    const emailUsuario = obterEmailUsuario();

    try {
        const response = await fetch(
            `${API_BASE_URL}/update_despesa/${emailUsuario}/${encodeURIComponent(identificador)}`,
            {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            }
        );

        if (!response.ok) {
            const erro = await response.json();
            alert(response.status === 404
                ? '❌ Despesa não encontrada'
                : `❌ Erro ${response.status}: ${erro.detail || 'Erro desconhecido'}`
            );
            return;
        }

        alert('✅ Despesa atualizada com sucesso!');
        renderizarPagina('usuarioLayout');

    } catch (error) {
        console.error('Erro ao atualizar despesa:', error);
        alert(`❌ Erro de conexão: ${error.message}`);
    }
}