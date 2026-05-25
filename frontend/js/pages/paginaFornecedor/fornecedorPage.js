function paginaFornecedor(){
    return`
        <div id="container-fornecedor">

        <h2>Fornecedores</h2>

        <input type="text" placeholder="Pesquisar fornecedores" id="input-pesquisarFornecedor">

        <table id="tabela-fornecedor">
            <tr id="cabecalho-tabela-fornecedor">
                <th>Nome</th>
                <th>CNPJ</th>
                <th>E-mail</th>
                <th>Editar</th>
                <th>Remover</th>
            </tr>

            <!-- os dados dos fornecedores vão aparecer aqui pelo sistema -->
        </table>

        <div id="carregando" style="display: none; text-align: center; padding: 20px;">
            <p>⏳ Carregando fornecedores...</p>
        </div>

        <div id="baixo-sectionFornecedor">
            <button type="button" id="btn-adicionarFornecedor" onclick="renderizarPagina('cadastroFornecedor')">+ Adicionar fornecedor</button>
            <p id="total-fornecedores">Total de fornecedores: </p>
        </div>

    </div>
    `
}


