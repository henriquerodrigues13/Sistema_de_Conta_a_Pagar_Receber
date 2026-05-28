function paginaProdutosServicos() {
    return `
       <div id="container-produtoServico">

        <h2>Produtos e Serviços</h2>

        <div id="opcoes-tabelas">
<<<<<<< HEAD
            <button type="button" onclick="alternaTabela('tabelaProdutos')">Produto</button>
            <button type="button" onclick="alternaTabela('tabelaServicos')">Servico</button>
        </div>

        <input type="text" placeholder="Pesquisar Produtos e serviços" id="input-pesquisarProdutosServicos">
=======
            <button type="button" class="ativo" onclick="alternaTabela('tabelaProdutos')">Produto</button>
            <button type="button" onclick="alternaTabela('tabelaServicos')">Serviço</button>
        </div>

        <input 
            type="text" 
            placeholder="Pesquisar produtos" 
            id="input-pesquisarProdutosServicos"
        >
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf

        <table id="tabela-produtos">
            <thead>
                <tr id="cabecalho-tabela-produtos">
                    <th>Categorias</th>
                    <th>Nome</th>
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
<<<<<<< HEAD
                    <th>ID</th>
                    <th>Tipo</th>
                    <th>Email</th>
                    <th>Valor</th>
                    <th>Forma de Pagamento</th>
                    <th>Data</th>
=======
                    <th>Categoria do Serviço</th>
                    <th>Nome do Serviço</th>
                    <th>Valor</th>
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
                    <th>Opções</th>
                </tr>
            </thead>    
            <tbody></tbody>
        </table>

        <div id="paginacao-produtosServicos" style="display: none;">
            <button id="btn-anteriorPagina">
                <img src="./assets/imgs/icons/anterior.png">
            </button>

            <span id="span-pagina"></span>
<<<<<<< HEAD
            <button id="btn-proximaPagina"><img src="./assets/imgs/icons/proximo.png"></button>
=======

            <button id="btn-proximaPagina">
                <img src="./assets/imgs/icons/proximo.png">
            </button>
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
        </div>

        <div id="carregando-produtos" style="display: block; text-align: center; padding: 20px;">
            <p>⏳ Carregando produtos...</p>    
        </div>

        <div id="carregando-servicos" style="display: none; text-align: center; padding: 20px;">
            <p>⏳ Carregando serviços...</p>
        </div>

        <div id="baixo-sectionProdutosServicos">
<<<<<<< HEAD
            <button type="button" id="btn-adicionarProduto" onclick="renderizarPagina('cadastroProduto')">+ Adicionar Produto</button>
            <button type="button" id="btn-adicionarServico" onclick="renderizarPagina('cadastroServico')">+ Adicionar Serviço</button>
            <p id="total-produtos">Total de Produtos: <span id="span-total-produtos">0</span></p>
            <p id="total-servicos" style="display: none;">Total de Serviços: <span id="span-total-servicos">0</span></p>
=======
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
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
        </div>

    </div> 
    `
}