function paginaNfEmitente() {
    return `
        <div id="container-notaVendaEmitente">
        
        <div class="logo">
            <img src="./assets/imgs/logo/logo.png" alt="Logo">
        </div>

        <h1>Emitir nota de venda - Emitente</h1>

        <form id="form-notaVendaEmitente">

            <div class="linha">
                <div class="campo">
                    <label>Razão social</label>
                    <input type="text" id="input-razaoSocial-emitente">
                </div>

                <div class="campo">
                    <label>CNPJ</label>
                    <input type="text" id="input-cnpj-emitente">
                </div>
            </div>

            <div class="linha">
                <div class="campo">
                    <label>Inscrição</label>
                    <input type="text" id="input-inscricao-emitente">
                </div>

                <div class="campo">
                    <label>Código município</label>
                    <input type="text" id="input-codigoMunicipio-emitente">
                </div>
            </div>

            <div class="linha">
                <div class="campo">
                    <label>CEP</label>
                    <input type="text" id="input-cep-emitente">
                </div>

                <div class="campo">
                    <label>UF</label>
                    <input type="text" id="input-uf-emitente">
                </div>
            </div>

            <div class="linha">
                <div class="campo">
                    <label>Município</label>
                    <input type="text" id="input-municipio-emitente">
                </div>

                <div class="campo">
                    <label>Logradouro</label>
                    <input type="text" id="input-logradouro-emitente">
                </div>
            </div>

            <div class="linha">
                <div class="campo">
                    <label>Bairro</label>
                    <input type="text" id="input-bairro-emitente">
                </div>

                <div class="campo">
                    <label>País</label>
                    <input type="text" id="input-pais-emitente">
                </div>
            </div>

            <div class="linha">
                <div class="campo">
                    <label>Número</label>
                    <input type="text" id="input-numero-emitente">
                </div>

                <div class="campo">
                    <label>Regime tributário</label>
                    <input type="text" id="input-regimeTributario-emitente">
                </div>
            </div>
        </form>

        <button id="btn-cadastrarNota" type="button" onclick="cadastrarNotaEmitente()">
                Cadastrar
        </button>

        <button class="voltar" onclick="renderizarPagina('usuarioLayout')">Voltar</button>

    </div>
    `
}

function cadastrarNotaEmitente() {
    const razaoSocial = document.getElementById('input-razaoSocial-emitente').value.trim();
    const cnpj = document.getElementById('input-cnpj-emitente').value.trim();
    const inscricao = document.getElementById('input-inscricao-emitente').value.trim();
    const codigoMunicipio = document.getElementById('input-codigoMunicipio-emitente').value.trim();
    const cep = document.getElementById('input-cep-emitente').value.trim();
    const uf = document.getElementById('input-uf-emitente').value.trim();
    const municipio = document.getElementById('input-municipio-emitente').value.trim();
    const logradouro = document.getElementById('input-logradouro-emitente').value.trim();
    const bairro = document.getElementById('input-bairro-emitente').value.trim();
    const pais = document.getElementById('input-pais-emitente').value.trim();
    const numero = document.getElementById('input-numero-emitente').value.trim();
    const regimeTributario = document.getElementById('input-regimeTributario-emitente').value.trim();

    if (!razaoSocial || !cnpj || !inscricao || !codigoMunicipio || !cep || !uf || !municipio || !logradouro || !bairro || !pais || !numero || !regimeTributario) {
        alert('Preencha todos os campos antes de continuar.');
        return;
    }

    alert('Nota Fiscal de Venda - Emitente cadastrado com sucesso');
    renderizarPagina('paginaCliente');
}