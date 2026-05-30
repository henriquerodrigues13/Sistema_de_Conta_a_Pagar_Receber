function paginaCadastroDespesa(){
    return`
         <div id="container-cadastroDespesa">

        <div class="logo">
            <img src="" alt="Logo">
        </div>

        <h1>Cadastro de Despesas</h1>

        <form id="form-cadastroReceita">

            <div class="form-group">
                <label>Tipo ou nome da Despesa</label>
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
                    <option value="">Escolha a forma de pagamento</option>
                    <option value="ct-credito">Cartão de crédito</option>
                    <option value="ct-debito">Cartão de débito</option>
                    <option value="pix">Pix</option>
                    <option value="dinheiro">Dinheiro</option>
                    <option value="outros">Outros</option>
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

        <div id="erro-validacao" style="
                display: none;
                background-color: #ffe6e6;
                color: #c0392b;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 15px;
                border-left: 4px solid #c0392b;
            "></div>

        <button type="button" id="cadastrarReceita" onclick="cadastrarDespesa()">
            Cadastrar
        </button>

        <button id="voltar-layout" onclick="renderizarPagina('usuarioLayout')">
            Voltar
        </button>

    </div>
    `
}