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
 * Busca os produtos do usuário na API e renderiza a tabela com paginação.
 * Em caso de erro na requisição, renderiza a tabela vazia.
 * @param {number} [pagina=1] - Número da página a carregar.
 */
async function carregarProdutos(pagina = 1) {
    const emailUsuario = obterEmailUsuario();
 
    const carregando = obterElemento('carregando-produtos');
    if (carregando) carregando.style.display = 'block';
 
    try {
        const response = await fetch(
            `${API_BASE_URL}/get_produtos_usuario/${emailUsuario}?page=${pagina}`,
            { method: 'GET', headers: { 'Content-Type': 'application/json' } }
        );
 
        if (!response.ok) {
            const erro = await response.json();
            alert(`Erro ${erro.status}: ${erro.detail}`);
            return;
        }
 
        const produtosUsuario = await response.json();
        const total      = parseInt(response.headers.get('X-Total-Items') || '0', 10);
        const totalPages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);
 
        const spanTotal = obterElemento('span-total-produtos');
        if (spanTotal) spanTotal.textContent = total;
 
        renderizarTabelaProdutos(produtosUsuario);
        renderizarPaginacao(pagina, totalPages, 'produtos');
 
        const tabelaProdutos = obterElemento('tabela-produtos');
        if (tabelaProdutos) tabelaProdutos.style.display = 'table';
 
        const paginacao = obterElemento('paginacao-produtosServicos');
        if (paginacao) paginacao.style.display = 'flex';
 
    } catch (error) {
        console.error(error.message);
        renderizarTabelaVaziaProdutos();
        const tabelaProdutos = obterElemento('tabela-produtos');
        if (tabelaProdutos) tabelaProdutos.style.display = 'table';
    } finally {
        if (carregando) carregando.style.display = 'none';
    }
}
 
/**
 * Busca os serviços do usuário na API e renderiza a tabela com paginação.
 * Em caso de erro na requisição, renderiza a tabela vazia.
 * @param {number} [pagina=1] - Número da página a carregar.
 */
async function carregarServicos(pagina = 1) {
    const emailUsuario = obterEmailUsuario();
 
    const carregando = obterElemento('carregando-servicos');
    if (carregando) carregando.style.display = 'block';
 
    try {
        const response = await fetch(
            `${API_BASE_URL}/get_servico_usuario/${emailUsuario}?page=${pagina}`,
            { method: 'GET', headers: { 'Content-Type': 'application/json' } }
        );
 
        if (!response.ok) {
            const erro = await response.json();
            alert(`Erro ${erro.status}: ${erro.detail}`);
            return;
        }
 
        const servicosUsuario = await response.json();
        const total      = parseInt(response.headers.get('X-Total-Items') || '0', 10);
        const totalPages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);
 
        const spanTotal = obterElemento('span-total-servicos');
        if (spanTotal) spanTotal.textContent = total;
 
        renderizarTabelaServicos(servicosUsuario);
        renderizarPaginacao(pagina, totalPages, 'servicos');
 
        const tabelaServicos = obterElemento('tabela-servicos');
        if (tabelaServicos) tabelaServicos.style.display = 'table';
 
        const paginacao = obterElemento('paginacao-produtosServicos');
        if (paginacao) paginacao.style.display = 'flex';
 
    } catch (error) {
        console.error(error.message);
        renderizarTabelaVaziaServicos();
        const tabelaServicos = obterElemento('tabela-servicos');
        if (tabelaServicos) tabelaServicos.style.display = 'table';
    } finally {
        if (carregando) carregando.style.display = 'none';
    }
}
 
/**
 * Alterna a visibilidade entre as tabelas de produtos e serviços,
 * ajustando botões, totais, placeholder e carregando os dados correspondentes.
 * @param {'tabelaProdutos'|'tabelaServicos'} nomeTabela - Tabela a ser exibida.
 */
function alternaTabela(nomeTabela) {
    const tabelaProdutos      = obterElemento('tabela-produtos');
    const tabelaServicos      = obterElemento('tabela-servicos');
    const carregandoProdutos  = obterElemento('carregando-produtos');
    const carregandoServicos  = obterElemento('carregando-servicos');
    const totalProdutos       = obterElemento('total-produtos');
    const totalServicos       = obterElemento('total-servicos');
    const btnAdicionarProduto = obterElemento('btn-adicionarProduto');
    const btnAdicionarServico = obterElemento('btn-adicionarServico');
    const inputPesquisa       = obterElemento('input-pesquisarProdutosServicos');
    const paginacao           = obterElemento('paginacao-produtosServicos');
    const opcoesTabelas       = obterElemento('opcoes-tabelas');
    const botoes              = opcoesTabelas ? opcoesTabelas.querySelectorAll('button') : [];
 
    botoes.forEach(botao => botao.classList.remove('ativo'));
 
    if (tabelaProdutos) tabelaProdutos.style.display = 'none';
    if (tabelaServicos) tabelaServicos.style.display = 'none';
    if (paginacao)      paginacao.style.display      = 'none';
 
    if (nomeTabela === 'tabelaProdutos') {
        if (carregandoProdutos)  carregandoProdutos.style.display  = 'block';
        if (carregandoServicos)  carregandoServicos.style.display  = 'none';
        if (totalProdutos)       totalProdutos.style.display       = 'block';
        if (totalServicos)       totalServicos.style.display       = 'none';
        if (btnAdicionarProduto) btnAdicionarProduto.style.display = 'inline-block';
        if (btnAdicionarServico) btnAdicionarServico.style.display = 'none';
        if (inputPesquisa) { inputPesquisa.placeholder = 'Pesquisar produtos'; inputPesquisa.value = ''; }
        if (botoes[0]) botoes[0].classList.add('ativo');
        setTimeout(() => carregarProdutos(1), 500);
 
    } else if (nomeTabela === 'tabelaServicos') {
        if (carregandoProdutos)  carregandoProdutos.style.display  = 'none';
        if (carregandoServicos)  carregandoServicos.style.display  = 'block';
        if (totalProdutos)       totalProdutos.style.display       = 'none';
        if (totalServicos)       totalServicos.style.display       = 'block';
        if (btnAdicionarProduto) btnAdicionarProduto.style.display = 'none';
        if (btnAdicionarServico) btnAdicionarServico.style.display = 'inline-block';
        if (inputPesquisa) { inputPesquisa.placeholder = 'Pesquisar serviços'; inputPesquisa.value = ''; }
        if (botoes[1]) botoes[1].classList.add('ativo');
        setTimeout(() => carregarServicos(1), 500);
    }
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
    btn.title     = title;
    btn.onclick   = handler;
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
 * Renderiza as linhas de produtos no tbody da tabela de produtos.
 * Exibe tabela vazia caso a lista esteja vazia.
 * @param {Object[]} produtosUsuario - Lista de produtos retornada pela API.
 */
function renderizarTabelaProdutos(produtosUsuario) {
    const tabela = obterElemento('tabela-produtos');
    if (!tabela) return;
 
    const tbody = limparTbody(tabela);
 
    if (produtosUsuario.length === 0) {
        renderizarTabelaVaziaProdutos();
        return;
    }
 
    produtosUsuario.forEach(produto => {
        const tr = document.createElement('tr');
 
        [
            produto.nome_do_produto,
            produto.categoria_do_produto,
            produto.quantidade_em_estoque,
            produto.unidade_de_medida,
            produto.valor_final,
            produto.status_do_produto
        ].forEach(valor => {
            const td = document.createElement('td');
            td.textContent = valor || '-';
            tr.appendChild(td);
        });
 
        const tdOpcoes   = document.createElement('td');
        const divOpcoes  = document.createElement('div');
        divOpcoes.className = 'opcoes-btns';
 
        divOpcoes.appendChild(criarBotaoAcao('./assets/imgs/icons/lapis.png',   'Editar',  'btn-editar',  'Editar produto',  () => editarProduto(produto.nome_do_produto)));
        divOpcoes.appendChild(criarBotaoAcao('./assets/imgs/icons/lixeira.png', 'Remover', 'btn-remover', 'Remover produto', () => removerProduto(produto.nome_do_produto)));
        divOpcoes.appendChild(criarBotaoAcao('./assets/imgs/icons/venda.png',   'Vender',  'btn-vender',  'Vender Produto',  () => venderProduto(produto.nome_do_produto)));
 
        tdOpcoes.appendChild(divOpcoes);
        tr.appendChild(tdOpcoes);
        tbody.appendChild(tr);
    });
}
 
/**
 * Renderiza as linhas de serviços no tbody da tabela de serviços.
 * Exibe tabela vazia caso a lista esteja vazia.
 * @param {Object[]} servicosUsuario - Lista de serviços retornada pela API.
 */
function renderizarTabelaServicos(servicosUsuario) {
    const tabela = obterElemento('tabela-servicos');
    if (!tabela) return;
 
    const tbody = limparTbody(tabela);
 
    if (servicosUsuario.length === 0) {
        renderizarTabelaVaziaServicos();
        return;
    }
 
    servicosUsuario.forEach(servico => {
        const tr = document.createElement('tr');
 
        [
            servico.nome_do_servico,
            servico.categoria_do_servico,
            servico.valor_do_servico
        ].forEach(valor => {
            const td = document.createElement('td');
            td.textContent = valor || '-';
            tr.appendChild(td);
        });
 
        const tdOpcoes  = document.createElement('td');
        const divOpcoes = document.createElement('div');
        divOpcoes.className = 'opcoes-btns';
 
        divOpcoes.appendChild(criarBotaoAcao('./assets/imgs/icons/lapis.png',   'Editar',  'btn-editar',  'Editar serviço',  () => editarServico(servico.nome_do_servico)));
        divOpcoes.appendChild(criarBotaoAcao('./assets/imgs/icons/lixeira.png', 'Remover', 'btn-remover', 'Remover serviço', () => removerServico(servico.nome_do_servico)));
        divOpcoes.appendChild(criarBotaoAcao('./assets/imgs/icons/venda.png',   'Vender',  'btn-vender',  'Vender Serviço',  () => venderServico(servico.nome_do_servico)));
 
        tdOpcoes.appendChild(divOpcoes);
        tr.appendChild(tdOpcoes);
        tbody.appendChild(tr);
    });
}
 
/**
 * Exibe uma linha de "nenhum produto encontrado" na tabela de produtos.
 */
function renderizarTabelaVaziaProdutos() {
    const tabela = obterElemento('tabela-produtos');
    if (!tabela) return;
    _renderizarLinhaVazia(tabela, 7, 'Nenhum produto encontrado');
}
 
/**
 * Exibe uma linha de "nenhum serviço encontrado" na tabela de serviços.
 */
function renderizarTabelaVaziaServicos() {
    const tabela = obterElemento('tabela-servicos');
    if (!tabela) return;
    _renderizarLinhaVazia(tabela, 4, 'Nenhum serviço encontrado');
}
 
/**
 * Insere uma única linha centralizada com mensagem de lista vazia em uma tabela.
 * @param {HTMLElement} tabela   - Elemento da tabela.
 * @param {number}      colSpan  - Número de colunas a mesclar.
 * @param {string}      mensagem - Texto a exibir.
 */
function _renderizarLinhaVazia(tabela, colSpan, mensagem) {
    const tbody = limparTbody(tabela);
    const tr    = document.createElement('tr');
    const td    = document.createElement('td');
    td.colSpan           = colSpan;
    td.textContent       = mensagem;
    td.style.textAlign   = 'center';
    td.style.padding     = '20px';
    td.style.color       = 'black';
    td.style.border      = '#B8B8B8 solid 1px';
    tr.appendChild(td);
    tbody.appendChild(tr);
}
 
/**
 * Configura os botões de navegação e o indicador de página da paginação.
 * Desabilita o botão anterior na primeira página e o próximo na última.
 * @param {number} paginaAtual  - Página atualmente exibida.
 * @param {number} totalPaginas - Total de páginas disponíveis.
 * @param {'produtos'|'servicos'} tipo - Tipo de dado paginado.
 */
function renderizarPaginacao(paginaAtual, totalPaginas, tipo = 'produtos') {
    const paginacao = obterElemento('paginacao-produtosServicos');
    if (!paginacao) {
        console.error('❌ Elemento #paginacao-produtosServicos não encontrado');
        return;
    }
 
    paginacao.style.display = 'flex';
 
    const carregar = tipo === 'servicos' ? carregarServicos : carregarProdutos;
 
    const btnProximo   = obterElemento('btn-proximaPagina');
    const btnAnterior  = obterElemento('btn-anteriorPagina');
 
    if (btnProximo) {
        btnProximo.onclick          = () => { if (paginaAtual < totalPaginas) carregar(paginaAtual + 1); };
        btnProximo.disabled         = paginaAtual >= totalPaginas;
        btnProximo.style.opacity    = paginaAtual >= totalPaginas ? '0.1' : '0.9';
    }
 
    if (btnAnterior) {
        btnAnterior.onclick         = () => { if (paginaAtual > 1) carregar(paginaAtual - 1); };
        btnAnterior.disabled        = paginaAtual === 1;
        btnAnterior.style.opacity   = paginaAtual === 1 ? '0.1' : '0.9';
    }
 
    const spanPagina = obterElemento('span-pagina');
    if (spanPagina) spanPagina.textContent = `Página ${paginaAtual} de ${totalPaginas}`;
}
 
/**
 * Solicita confirmação e envia requisição DELETE para remover um produto.
 * Recarrega a tabela em caso de sucesso.
 * @param {string} nomeProduto - Nome do produto a ser removido.
 */
async function removerProduto(nomeProduto) {
    if (!confirm(`Deseja realmente remover o produto "${nomeProduto}"?`)) return;
 
    const emailUsuario = obterEmailUsuario();
 
    try {
        const response = await fetch(
            `${API_BASE_URL}/delete_produto/${emailUsuario}/${encodeURIComponent(nomeProduto)}`,
            { method: 'DELETE', headers: { 'Content-Type': 'application/json' } }
        );
 
        if (!response.ok) {
            const erro = await response.json();
            alert(response.status === 404
                ? '❌ Produto não encontrado'
                : `❌ Erro ${response.status}: ${erro.detail || 'Erro desconhecido'}`
            );
            return;
        }
 
        alert(`✅ Produto "${nomeProduto}" removido com sucesso`);
        carregarProdutos(1);
 
    } catch (error) {
        console.error('Erro ao remover produto:', error);
        alert(`❌ Erro ao remover produto: ${error.message}`);
    }
}
 
/**
 * Solicita confirmação e envia requisição DELETE para remover um serviço.
 * Recarrega a tabela em caso de sucesso.
 * @param {string} nomeServico - Nome do serviço a ser removido.
 */
async function removerServico(nomeServico) {
    if (!confirm(`Deseja realmente remover o serviço "${nomeServico}"?`)) return;
 
    const emailUsuario = obterEmailUsuario();
 
    try {
        const response = await fetch(
            `${API_BASE_URL}/delete_servico/${emailUsuario}/${encodeURIComponent(nomeServico)}`,
            { method: 'DELETE', headers: { 'Content-Type': 'application/json' } }
        );
 
        if (!response.ok) {
            const erro = await response.json();
            alert(response.status === 404
                ? '❌ Serviço não encontrado'
                : `❌ Erro ${response.status}: ${erro.detail || 'Erro desconhecido'}`
            );
            return;
        }
 
        alert(`✅ Serviço "${nomeServico}" removido com sucesso`);
        carregarServicos(1);
 
    } catch (error) {
        console.error('Erro ao remover serviço:', error);
        alert(`❌ Erro ao remover serviço: ${error.message}`);
    }
}
 
/**
 * Navega para a página de venda de produto e preenche o campo de nome
 * após o DOM ser renderizado.
 * @param {string} nomeProduto - Nome do produto a pré-preencher.
 */
function venderProduto(nomeProduto) {
    renderizarPagina('cadastroVendaProduto');
    setTimeout(() => {
        const input = document.getElementById('input-nome-produto');
        if (input) input.value = nomeProduto;
    }, 0);
}
 
/**
 * Navega para a página de venda de serviço e preenche o campo de nome
 * após o DOM ser renderizado.
 * @param {string} nomeServico - Nome do serviço a pré-preencher.
 */
function venderServico(nomeServico) {
    renderizarPagina('cadastroVendaServico');
    setTimeout(() => {
        const input = document.getElementById('input-nome-servico');
        if (input) input.value = nomeServico;
    }, 0);
}