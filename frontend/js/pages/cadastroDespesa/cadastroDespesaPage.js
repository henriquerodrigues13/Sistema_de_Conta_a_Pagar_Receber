function paginaCadastroDespesa(){
    return`
         <div id="container-cadastroDespesa">

        <div class="logo">
            <img src="./assets/imgs/logo/logo.png" alt="Logo">
        </div>

        <h1>Cadastro de Despesas</h1>

        <form id="form-cadastroReceita">

            <div class="form-group">
                <label>Tipo da Despesa</label>
                <input type="text" id="input-tipoDespesa">
            </div>

            <div class="form-group">
                <label>Descrição</label>
                <textarea name="" id="input-descricaoDespesa"></textarea>
            </div>

            <div class="form-group">
                <label>Valor Total</label>
                <input type="number" id="input-valorTotalDespesa">
            </div>

            <div class="form-group">
                <label>Forma de Pagamento</label>
                <select id="opcoes-pagamentosDespesa">
                    <option value="">Selecione</option>
                            <option value="Pix">Pix</option>
                            <option value="Débito">Débito</option>
                            <option value="Crédito">Crédito</option>
                            <option value="Boleto">Boleto</option>
                            <option value="Dinheiro">Dinheiro</option>
                </select>
            </div>

            <div class="form-group">
                <label>Valor pago por unidade</label>
                <input type="number" id="input-valorUnidadeDespesa">
            </div>

            <div class="form-group">
                <label>Anexar documento</label>
                <input type="file" id="files" accept=".pdf, .doc, .docx, .txt">
            </div>

            <div class="form-group">
                <div class="content-form-group">
                    <div class="form-group-group">
                        <label for="">Revenda</label>
                        <input type="radio" name="opc-tipoDespesa" id="input-revenda">
                    </div>
                    <div class="form-group-group">
                        <label for="">Despesa</label>
                        <input type="radio" name="opc-tipoDespesa" id="input-despesaPessoal">
                    </div>

                </div>
            </div>

            <div class="form-group">
                <label>Observação</label>
                <input type="text" id="input-observacaoReceita">
            </div>

        </form>
        <div id="form-group-footer" style="display: none;">
            <div class="form-group">
                <label>Valor da Revenda</label>
                <input type="number" id="input-valorUnidadeRevenda">
            </div>

            <div class="form-group">
                <label>Unidade de medida</label>
                <input type="text" id="input-unidadeMedidaRevenda">
            </div>
        </div>

        <button type="button" id="cadastrarDespesa" onclick="cadastrarDespesa()">
            Cadastrar
        </button>

        <button id="voltar-layout" onclick="renderizarPagina('usuarioLayout')">
            < Voltar
        </button>

    </div>
    `
}