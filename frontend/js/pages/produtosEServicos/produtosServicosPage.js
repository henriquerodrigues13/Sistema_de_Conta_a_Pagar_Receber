/**
 * Gera o HTML da seção de listagem de produtos e serviços.
 * @returns {string} HTML da seção.
 */
function sectionProdutosServicos() {
    return `
        <div id="container-produtoServico">
 
            <h2>Produtos e Serviços</h2>
 
            <div id="opcoes-tabelas">
                <button type="button" class="ativo" onclick="alternaTabelaProdutoServico('tabelaProdutos')">Produto</button>
                <button type="button" onclick="alternaTabelaProdutoServico('tabelaServicos')">Serviço</button>
            </div>
 
            <input 
                type="text" 
                placeholder="Pesquisar produtos" 
                id="input-pesquisarProdutosServicos"
            >
 
            <table id="tabela-produtos">
                <thead>
                    <tr id="cabecalho-tabela-produtos">
                        <th>Nome do Produto</th>
                        <th>Categoria do Produto</th>
                        <th>Quantidade</th>
                        <th>Unidade</th>
                        <th>Valor</th>
                        <th>Status</th>
                        <th>Opções</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
 
            <table id="tabela-servicos" style="display: none;">
                <thead>
                    <tr id="cabecalho-tabela-servicos">
                        <th>Nome do Serviço</th>
                        <th>Categoria do Serviço</th>
                        <th>Valor</th>
                        <th>Opções</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
 
            <div id="paginacao-produtosServicos" style="display: none;">
                <button id="btn-anteriorPagina">
                    <img src="./assets/imgs/icons/anterior.png">
                </button>
 
                <span id="span-paginaProdutoServico"></span>
 
                <button id="btn-proximaPagina">
                    <img src="./assets/imgs/icons/proximo.png">
                </button>
            </div>
 
            <div id="carregando-produtos" style="display: block; text-align: center; padding: 20px;">
                <p>⏳ Carregando produtos...</p>
            </div>
 
            <div id="carregando-servicos" style="display: none; text-align: center; padding: 20px;">
                <p>⏳ Carregando serviços...</p>
            </div>
 
            <div id="baixo-sectionProdutosServicos">
                <button 
                    type="button" 
                    id="btn-adicionarProduto" 
                    onclick="renderizarPagina('cadastroProduto')"
                >
                    + Adicionar Produto
                </button>
 
                <button 
                    type="button" 
                    id="btn-adicionarServico" 
                    onclick="renderizarPagina('cadastroServico')"
                    style="display: none;"
                >
                    + Adicionar Serviço
                </button>
 
                <p id="total-produtos">
                    Total de Produtos:
                    <span id="span-total-produtos">0</span>
                </p>
 
                <p id="total-servicos" style="display: none;">
                    Total de Serviços:
                    <span id="span-total-servicos">0</span>
                </p>
            </div>
 
        </div>
    `;
}