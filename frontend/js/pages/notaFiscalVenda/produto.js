function paginaNfProduto() {
    return `
        <div id="container-notaVendaProduto">

        <div class="logo">
            <img src="./assets/imgs/logo/logo.png" alt="Logo">
        </div>

        <h1>Emitir nota de venda - Produto</h1>

        <form id="form-notaVendaProduto">

            <div class="linha">
                <div class="campo">
                    <label>Código</label>
                    <input type="text" id="input-codigo-produto">
                </div>

                <div class="campo">
                    <label>Valor unidade comercial</label>
                    <input type="text" id="input-valorUnidade-produto">
                </div>
            </div>

            <div class="linha">
                <div class="campo">
                    <label>Quantidade comercial</label>
                    <input type="text" id="input-quantidade-produto">
                </div>

                <div class="campo">
                    <label>Informações adicionais</label>
                    <input type="text" id="input-infoAdicionais-produto">
                </div>
            </div>

            <div class="linha">
            <div class="campo">
                <label>Forma de pagamento</label>
                <select id="input-pagamento-produto">
                    <option value="">Selecione</option>
                    <option value="Pix">Pix</option>
                    <option value="Débito">Débito</option>
                    <option value="Crédito">Crédito</option>
                    <option value="Boleto">Boleto</option>
                    <option value="Dinheiro">Dinheiro</option>
                </select>
            </div>

            <div class="campo">
                    <label>Modalidade do Frete</label>
                    <input type="text" id="input-modalidadeFrete-produto">
                </div>

                
            </div>
        </form>

        <button id="btn-cadastrarNotaProduto" type="button" onclick="cadastrarNotaProduto()">
                Cadastrar
        </button>

        <button class="voltar" onclick="renderizarPagina('usuarioLayout')">Voltar</button>

    </div>
    `
}

function cadastrarNotaProduto() {
    const codigo = document.getElementById('input-codigo-produto').value.trim();
    const valorUnidade = document.getElementById('input-valorUnidade-produto').value.trim();
    const quantidade = document.getElementById('input-quantidade-produto').value.trim();
    const infoAdicionais = document.getElementById('input-infoAdicionais-produto').value.trim();
    const pagamento = document.getElementById('input-pagamento-produto').value.trim();
    const modalidadeFrete = document.getElementById('input-modalidadeFrete-produto').value.trim();

    if (!codigo || !valorUnidade || !quantidade || !infoAdicionais || !pagamento || !modalidadeFrete) {
        alert('Preencha todos os campos antes de continuar.');
        return;
    }

    alert('Nota Fiscal de Venda - Produto cadastrado com sucesso');
    renderizarPagina('usuarioLayout');
}