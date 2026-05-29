/**
 * Gera o HTML da página de listagem de receitas e vendas.
 * @returns {string} HTML da página.
 */
function paginaReceita() {
    return `
        <div id="container-receita">

            <h2>Receitas e Vendas</h2>

            <div id="opcoes-tabelas">
                <button 
                    type="button" 
                    class="ativo"
                    onclick="alternaTabelaReceitaVenda('tabelaReceitas')"
                >
                    Receitas
                </button>

                <button 
                    type="button"
                    onclick="alternaTabelaReceitaVenda('tabelaVendas')"
                >
                    Vendas
                </button>
            </div>

            <input 
                type="text" 
                placeholder="Pesquisar receitas"
                id="input-pesquisarReceitaVenda"
            >

            <!-- TABELA RECEITAS -->
            <table id="tabela-receita">
                <thead>
                    <tr id="cabecalho-tabela-receita">
                        <th>ID</th>
                        <th>Tipo de Receita</th>
                        <th>Email do Pagador</th>
                        <th>Valor</th>
                        <th>Forma de Pagamento</th>
                        <th>Data</th>
                        <th>Opções</th>
                    </tr>
                </thead>

                <tbody></tbody>
            </table>

            <!-- TABELA VENDAS -->
            <table id="tabela-vendas" style="display: none;">
                <thead>
                    <tr id="cabecalho-tabela-vendas">
                        <th>ID</th>
                        <th>Produto/Serviço</th>
                        <th>Comprador</th>
                        <th>Valor</th>
                        <th>Forma de Pagamento</th>
                        <th>Data</th>
                        <th>Opções</th>
                    </tr>
                </thead>

                <tbody></tbody>
            </table>

            <!-- PAGINAÇÃO -->
            <div id="paginacao-receitaVenda" style="display: none;">
                <button id="btn-anteriorPagina">
                    <img src="./assets/imgs/icons/anterior.png">
                </button>

                <span id="span-pagina"></span>

                <button id="btn-proximaPagina">
                    <img src="./assets/imgs/icons/proximo.png">
                </button>
            </div>

            <!-- LOADING RECEITAS -->
            <div 
                id="carregando-receitas" 
                style="display: block; text-align: center; padding: 20px;"
            >
                <p>⏳ Carregando receitas...</p>
            </div>

            <!-- LOADING VENDAS -->
            <div 
                id="carregando-vendas" 
                style="display: none; text-align: center; padding: 20px;"
            >
                <p>⏳ Carregando vendas...</p>
            </div>

            <div id="baixo-sectionReceita">

                <button 
                    type="button"
                    id="btn-adicionarReceita"
                    onclick="renderizarPagina('cadastroReceita')"
                >
                    + Cadastrar Receita
                </button>

                <button 
                    type="button"
                    id="btn-adicionarVenda"
                    onclick="renderizarPagina('cadastroVendaProduto')"
                    style="display: none;"
                >
                    + Registrar Venda
                </button>

                <p id="total-receitas">
                    Total de Receitas:
                    <span id="span-total-receitas">0</span>
                </p>

                <p id="total-vendas" style="display: none;">
                    Total de Vendas:
                    <span id="span-total-vendas">0</span>
                </p>

            </div>

        </div>
    `;
}

