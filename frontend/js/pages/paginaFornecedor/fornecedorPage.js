function paginaFornecedor(){
    return`
        <div id="container-fornecedor">

        <h2>Fornecedores</h2>

        <input type="text" placeholder="Pesquisar fornecedores" id="input-pesquisarFornecedor">

        <table id="tabela-fornecedor">
            <thead>
                <tr id="cabecalho-tabela-fornecedor">
                    <th>Nome</th>
                    <th>CNPJ</th>
                </tr>
            </thead>    
            <tbody>
                <!-- os dados dos fornecedores vão aparecer aqui pelo sistema -->
            </tbody>
        </table>

        <div id="paginacao">
            <button id="btn-anteriorPagina"><- voltar</button>
            <span id="span-pagina"></span>
            <button id="btn-proximaPagina">proximo -></button>
        </div>

        <div id="carregando" style="display: block; text-align: center; padding: 20px;">
            <p>⏳ Carregando fornecedores...</p>
        </div>

        <div id="baixo-sectionFornecedor">
            <p id="total-fornecedores">Total de fornecedores: <span id="span-total">0</span></p>
        </div>

    </div>
    `
}


