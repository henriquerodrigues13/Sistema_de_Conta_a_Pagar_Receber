/**
 * Carrega as despesas da API e renderiza a tabela.
 * @param {number} pagina Página atual.
 */
async function carregarDespesas(pagina = 1) {

    const carregando = document.getElementById(
        'carregando'
    );

    try {

        if (carregando) {
            carregando.style.display = 'block';
        }

        const response = await fetch(
            `${API_BASE_URL}/get_fornecedor?page=${pagina}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        if (!response.ok) {

            const erro = await response.json();

            alert(
                `Erro ${erro.status}: ${erro.detail}`
            );

            return;
        }

        const despesas = await response.json();

        const total = parseInt(
            response.headers.get('X-Total-Items') || '0',
            10
        );

        const totalPaginas = parseInt(
            response.headers.get('X-Total-Pages') || '1',
            10
        );

        atualizarTotalDespesas(total);

        renderizarTabelaDespesa(despesas);

        renderizarPaginacaoDespesa(
            pagina,
            totalPaginas
        );

    } catch (error) {

        console.log(error.message);

        renderizarTabelaVaziaDespesa();

    } finally {

        if (carregando) {
            carregando.style.display = 'none';
        }
    }
}

/**
 * Atualiza o total exibido na tela.
 * @param {number} total Quantidade total.
 */
function atualizarTotalDespesas(total) {

    const spanTotal = document.getElementById(
        'span-total'
    );

    if (spanTotal) {
        spanTotal.textContent = total;
    }
}

/**
 * Remove todas as linhas da tabela.
 * @param {HTMLElement} tbody Corpo da tabela.
 */
function limparTabelaDespesa(tbody) {

    const linhas = tbody.querySelectorAll('tr');

    linhas.forEach(linha => linha.remove());
}

/**
 * Cria um botão de ação da tabela.
 * @param {object} config Configuração do botão.
 * @returns {HTMLButtonElement} Botão criado.
 */
function criarBotaoDespesa(config) {

    const {
        imagem,
        alt,
        classe,
        titulo,
        evento
    } = config;

    const botao = document.createElement('button');

    const img = document.createElement('img');

    img.src = imagem;
    img.alt = alt;

    botao.appendChild(img);

    botao.className = classe;

    botao.title = titulo;

    botao.onclick = evento;

    return botao;
}

/**
 * Cria uma célula da tabela.
 * @param {string} valor Conteúdo da célula.
 * @returns {HTMLTableCellElement} Célula criada.
 */
function criarColunaTabela(valor) {

    const td = document.createElement('td');

    td.textContent = valor || '-';

    return td;
}

/**
 * Renderiza a tabela de despesas.
 * @param {Array} despesas Lista de despesas.
 */
function renderizarTabelaDespesa(despesas) {

    const tabela = document.getElementById(
        'tabela-despesa'
    );

    const tbody = tabela.querySelector('tbody');

    limparTabelaDespesa(tbody);

    if (!despesas.length) {

        renderizarTabelaVaziaDespesa();

        return;
    }

    despesas.forEach(despesa => {

        const tr = document.createElement('tr');

        const tdId = criarColunaTabela(
            despesa.id
        );

        const tdTipo = criarColunaTabela(
            despesa.tipo
        );

        const tdDescricao = criarColunaTabela(
            despesa.email
        );

        const tdValor = criarColunaTabela(
            despesa.valor
        );

        const tdOpcoes = document.createElement('td');

        const divOpcoes = document.createElement('div');

        divOpcoes.className = 'opcoes-btns-despesa';

        const btnEditar = criarBotaoDespesa({
            imagem: './assets/imgs/icons/lapis.png',
            alt: 'Editar',
            classe: 'btn-editar-despesa',
            titulo: 'Editar Despesa',
            evento: () => editarDespesa(despesa.id)
        });

        const btnRemover = criarBotaoDespesa({
            imagem: './assets/imgs/icons/lixeira.png',
            alt: 'Remover',
            classe: 'btn-remover',
            titulo: 'Remover Despesa',
            evento: () => removerDespesa(despesa.id)
        });

        const btnVerNf = criarBotaoDespesa({
            imagem: './assets/imgs/icons/taxa.png',
            alt: 'Ver NF',
            classe: 'btn-ver-nf',
            titulo: 'Ver Nota Fiscal',
            evento: () => verNota(despesa.id)
        });

        divOpcoes.appendChild(btnEditar);

        divOpcoes.appendChild(btnRemover);

        divOpcoes.appendChild(btnVerNf);

        tdOpcoes.appendChild(divOpcoes);

        tr.appendChild(tdId);
        tr.appendChild(tdTipo);
        tr.appendChild(tdDescricao);
        tr.appendChild(tdValor);
        tr.appendChild(tdOpcoes);

        tbody.appendChild(tr);
    });
}

/**
 * Renderiza mensagem de tabela vazia.
 */
function renderizarTabelaVaziaDespesa() {

    const tabela = document.getElementById(
        'tabela-despesa'
    );

    const tbody = tabela.querySelector('tbody');

    limparTabelaDespesa(tbody);

    const tr = document.createElement('tr');

    const td = document.createElement('td');

    td.colSpan = 5;

    td.textContent = 'Nenhuma Despesa encontrada';

    td.style.textAlign = 'center';
    td.style.padding = '20px';
    td.style.color = 'black';
    td.style.border = '#B8B8B8 solid 1px';

    tr.appendChild(td);

    tbody.appendChild(tr);
}

/**
 * Renderiza os controles de paginação.
 * @param {number} paginaAtual Página atual.
 * @param {number} totalPaginas Total de páginas.
 */
function renderizarPaginacaoDespesa(
    paginaAtual,
    totalPaginas
) {

    const paginacao = document.getElementById(
        'paginacao-despesa'
    );

    const btnProximo = document.getElementById(
        'btn-proximaPagina'
    );

    const btnAnterior = document.getElementById(
        'btn-anteriorPagina'
    );

    const spanPagina = document.getElementById(
        'span-pagina'
    );

    paginacao.style.display = 'flex';

    configurarBotaoPaginacao({
        botao: btnProximo,
        ativo: paginaAtual < totalPaginas,
        acao: () => carregarDespesas(paginaAtual + 1)
    });

    configurarBotaoPaginacao({
        botao: btnAnterior,
        ativo: paginaAtual > 1,
        acao: () => carregarDespesas(paginaAtual - 1)
    });

    if (spanPagina) {

        spanPagina.textContent = `
            Página ${paginaAtual} de ${totalPaginas}
        `;
    }
}

/**
 * Configura um botão da paginação.
 * @param {object} config Configuração do botão.
 */
function configurarBotaoPaginacao(config) {

    const {
        botao,
        ativo,
        acao
    } = config;

    if (!botao) {
        return;
    }

    botao.onclick = ativo ? acao : null;

    botao.disabled = !ativo;

    botao.style.opacity = ativo ? '0.9' : '0.1';
}

// function editarDespesa(id) {
//     console.log('Editar despesa:', id);
// }

// function removerDespesa(id) {
//     console.log('Remover despesa:', id);
// }

// function verNota(id) {
//     console.log('Ver nota fiscal:', id);
// }