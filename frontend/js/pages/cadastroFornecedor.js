function paginaCadastroFornecedor(){
    return`
        <div class="container-cadastroFornecedor">

        <h1>Cadastro de Fornecedor</h1>

        <form id="form-cadastroFornecedor">
            <div class="form-group-cadastroFornecedor">
                <label>CNPJ:</label>
                <input type="text" placeholder="Digite o cnpj do fornecedor">
            </div>

        </form>

        <div class="btn-area-cadastroFornecedor">
            <button type="button" id="btn-cadastroFornecedor">Cadastrar</button>
        </div>

        <p class="voltar">
            <button type="button" id="voltar-telaFornecedor" onclick="renderizarPagina('usuarioLayout')">Voltar</button>
        </p>

    </div>
    `
}