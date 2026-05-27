function paginaCadastroReceita(){
    return`
        
    <div class="container-cadastroReceita">

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
            <button type="button" id="voltar-telaFornecedor">Voltar</button>
        </p>

    </div>
    `
}