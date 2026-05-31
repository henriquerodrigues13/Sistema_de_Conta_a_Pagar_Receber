/**
 * Renderiza a página de cadastro de receitas.
 * @returns {string} Estrutura HTML da página.
 */
function paginaCadastroReceita() {

    return `
        <div id="container-cadastroReceita">

            <div class="logo">

                <img 
                    src="./assets/imgs/logo/logo.png" 
                    alt="Logo"
                >

            </div>

            <h1>Cadastro de Receitas</h1>

            <form id="form-cadastroReceita">

                <div class="form-group">

                    <label>
                        Tipo da receita
                    </label>

                    <input 
                        type="text"
                        id="input-tipoReceita"
                    >

                </div>

                <div class="form-group">

                    <label>
                        Email do pagador
                    </label>

                    <input 
                        type="email"
                        id="input-emailPagador"
                        placeholder="Opcional"
                    >

                </div>

                <div class="form-group">

                    <label>
                        Data de cadastro
                    </label>

                    <input 
                        type="date"
                        id="input-dataCadastroReceita"
                    >

                </div>

                <div class="form-group">

                    <label>
                        Valor
                    </label>

                    <input 
                        type="text"
                        id="input-valorReceita"
                    >

                </div>

                <div class="form-group">

                    <label>
                        Forma de Pagamento
                    </label>

                    <select id="opcoes-pagamentos">
                        <option value="">Selecione</option>
                        <option value="Pix">Pix</option>
                        <option value="Débito">Débito</option>
                        <option value="Crédito">Crédito</option>
                        <option value="Boleto">Boleto</option>
                        <option value="Dinheiro">Dinheiro</option>
                    </select>

                </div>

                <div class="form-group">

                    <label>
                        Anexar documento
                    </label>

                    <input 
                        type="file"
                        id="files"
                        accept=".pdf, .doc, .docx, .txt"
                    >

                </div>

                <div class="form-group-footer">

                    <label>
                        Observação
                    </label>

                    <input 
                        type="text"
                        id="input-observacaoReceita"
                    >

                </div>

            </form>

            <button 
                type="button"
                id="cadastrarReceita"
                onclick="cadastrarReceita()"
            >
                Cadastrar
            </button>

            <button 
                id="voltar-layout"
                onclick="renderizarPagina('usuarioLayout')"
            >
                < Voltar
            </button>

        </div>
    `;
}