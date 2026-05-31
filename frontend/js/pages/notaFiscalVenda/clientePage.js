function paginaNfCliente() {
    return `
        <div id="container-notaVendaCliente">
        
        <div class="logo">
            <img src="./assets/imgs/logo/logo.png" alt="Logo">
        </div>

        <h1>Emitir nota de venda - Cliente</h1>

        <form id="form-notaVendaCliente">

            <div class="linha">
                <div class="campo">
                    <label>Razão social / Nome Completo</label>
                    <input type="text" id="input-razaoSocial-cliente">
                </div>

                <div class="campo">
                    <label>CNPJ/CPF</label>
                    <input type="text" id="input-cnpjCpf-cliente">
                </div>
            </div>

            <div class="linha">
                <div class="campo">
                    <label>Indicador IE</label>
                    <input type="text" id="input-indicadorIE-cliente">
                </div>

                <div class="campo">
                    <label>Código município</label>
                    <input type="text" id="input-codigoMunicipio-cliente">
                </div>
            </div>

            <div class="linha">
                <div class="campo">
                    <label>CEP</label>
                    <input type="text" id="input-cep-cliente">
                </div>

                <div class="campo">
                    <label>UF</label>
                    <input type="text" id="input-uf-cliente">
                </div>
            </div>

            <div class="linha">
                <div class="campo">
                    <label>Município</label>
                    <input type="text" id="input-municipio-cliente">
                </div>

                <div class="campo">
                    <label>Logradouro</label>
                    <input type="text" id="input-logradouro-cliente">
                </div>
            </div>

            <div class="linha">
                <div class="campo">
                    <label>Bairro</label>
                    <input type="text" id="input-bairro-cliente">
                </div>

                <div class="campo">
                    <label>País</label>
                    <input type="text" id="input-pais-cliente">
                </div>
            </div>

            <div class="linha">
                <div class="campo">
                    <label>Número</label>
                    <input type="text" id="input-numero-cliente">
                </div>
            </div>
        </form>

        <button id="btn-cadastrarNotaCliente" type="button" onclick="cadastrarNotaCliente()">
                Cadastrar
        </button>

        <p class="voltar">Voltar</p>

    </div>
    `
}

function cadastrarNotaCliente() {
    const razaoSocial = document.getElementById('input-razaoSocial-cliente').value.trim();
    const cnpjCpf = document.getElementById('input-cnpjCpf-cliente').value.trim();
    const indicadorIE = document.getElementById('input-indicadorIE-cliente').value.trim();
    const codigoMunicipio = document.getElementById('input-codigoMunicipio-cliente').value.trim();
    const cep = document.getElementById('input-cep-cliente').value.trim();
    const uf = document.getElementById('input-uf-cliente').value.trim();
    const municipio = document.getElementById('input-municipio-cliente').value.trim();
    const logradouro = document.getElementById('input-logradouro-cliente').value.trim();
    const bairro = document.getElementById('input-bairro-cliente').value.trim();
    const pais = document.getElementById('input-pais-cliente').value.trim();
    const numero = document.getElementById('input-numero-cliente').value.trim();

    if (!razaoSocial || !cnpjCpf || !indicadorIE || !codigoMunicipio || !cep || !uf || !municipio || !logradouro || !bairro || !pais || !numero) {
        alert('Preencha todos os campos antes de continuar.');
        return;
    }

    alert('Nota Fiscal de Venda - Cliente cadastrado com sucesso');
    renderizarPagina('paginaProduto');
}