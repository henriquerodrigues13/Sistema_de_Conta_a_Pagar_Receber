function paginaFornecedor(){
    return`
        <div id="container-fornecedor">

        <h2>Fornecedores</h2>

        <input type="text" placeholder="Pesquisar fornecedores" id="input-pesquisarFornecedor">

        <table id="tabela-fornecedor">
            <tr id="cabecalho-tabela-fornecedor">
                <th>Nome</th>
                <th>Telefone</th>
                <th>E-mail</th>
                <th>Editar</th>
                <th>Remover</th>
            </tr>

            <!-- os dados dos fornecedores vão aparecer aqui pelo sistema -->
        </table>

        <div id="baixo-sectionFornecedor">
            <button type="button" id="btn-adicionarFornecedor">+ Adicionar fornecedor</button>
            <p>Total de fornecedores: 0</p>
        </div>

    </div>
    `
}