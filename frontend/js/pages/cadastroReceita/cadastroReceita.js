function paginaCadastroReceita() {
    return `
        <div id="container-cadastroReceita">

        <div class="logo">
            <img src="./assets/imgs/logo/logo.png" alt="Logo">
        </div>

        <h1>Cadastro de Receitas</h1>

        <form id="form-cadastroReceita">
            <div class="form-group">
                <label>Tipo ou nome da receita</label>
                <input type="text">
            </div>

            <div class="form-group">
                <label>Email do pagador</label>
                <input type="email">
            </div>

            <div class="form-group">
                <label>Data de cadastro</label>
                <input type="date">
            </div>

            <div class="form-group">
                <label>Valor</label>
                <input type="text">
            </div>


            <div class="form-group">
                <label>Forma de Pagamento</label>
                <select name="" id="opcoes-pagamentos">
                    <option value="">Escolha a forma de pagamento</option>
                    <option value="ct-credito">Cartão de credito</option>
                    <option value="ct-debito">Cartão de debito</option>
                    <option value="pix">Pix</option>
                    <option value="dinheiro">Dinheiro</option>
                    <option value="outros">outros</option>
                </select>
            </div>

            <div class="form-group">
                <label>Anexar documento</label>
                <input type="file" id="files" accept=".pdf, .doc, .docx, .txt">
            </div>

            <div class="form-group-footer">
                <label>Observação</label>
                <input type="text">
            </div>

        </form>

        <button type="button" id="cadastrarReceita">
            Cadastrar
        </button>

        <button id="voltar-layout" onclick="renderizarPagina('usuarioLayout')">
            Voltar
        </button>

    </div>
    `
}