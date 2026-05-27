function paginaProdutosServicos() {
    return `
       <div id="container-produtoServico">

        <h2>Produtos e Serviços</h2>

        <input type="text" placeholder="Pesquisar Produtos e serviços" id="input-pesquisarProdutosServicos">

        <table id="tabela-produtos">
            <thead>
                <tr id="cabecalho-tabela-produtos">
                    <th>Categorias</th>
                    <th>Nome do produto</th>
                    <th>Quantidade</th>
                    <th>Unidade</th>
                    <th>Valor</th>
                    <th>Status</th>
                    <th>Opções</th>
                </tr>
            </thead>    
            <tbody>
    
            </tbody>
        </table>

        <table id="tabela-servicos" style="display: none;">
            <thead>
                <tr id="cabecalho-tabela-servicos">
                    <th>Categorias</th>
                    <th>Nome do Serviço</th>
                    <th>Quantidade</th>
                    <th>Unidade</th>
                    <th>Valor</th>
                    <th>Status</th>
                    <th>Opções</th>
                </tr>
            </thead>    
            <tbody>
    
            </tbody>
        </table>

        <div id="paginacao-produtosServicos" style="display: none;">
            <button id="btn-anteriorPagina"><img src="./assets/imgs/icons/anterior.png"></button>
            <span id="span-pagina"></span>
            <button id="btn-proximaPagina"> <img src="./assets/imgs/icons/proximo.png"></button>
        </div>

        <div id="carregando" style="display: block; text-align: center; padding: 20px;">
            <p>⏳ Carregando receitas...</p>
        </div>

        <div id="baixo-sectionProdutosServicos">
            <button type="button" id="btn-adicionarProduto" onclick="renderizarPagina('cadastroProduto')">+ Adicionar Produto</button>
            <button type="button" id="btn-adicionarServico" onclick="renderizarPagina('cadastroReceita')">+ Adicionar Serviço</button>
            <p id="total-produtos">Total de Produtos: <span id="span-total">0</span></p>
            <p id="total-servicos" style="display: none;">Total de Serviços: <span id="span-total">0</span></p>
        </div>

    </div> 
    `
}