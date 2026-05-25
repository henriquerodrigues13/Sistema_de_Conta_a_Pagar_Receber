function paginaCadastroFornecedor(){
    return`
        <div class="container-cadastroFornecedor">

        <h1>Cadastro de Fornecedor</h1>

        <form id="form-cadastroFornecedor">
            <div class="form-group-cadastroFornecedor">
                <label>CNPJ:</label>
                <input type="text" placeholder="Digite o cnpj do fornecedor" id="cnpj-fornecedor">
            </div>

        </form>

        <div class="btn-area-cadastroFornecedor">
            <button type="button" id="btn-cadastroFornecedor" onclick="cadastrarFornecedor()">Cadastrar</button>
        </div>

        <p class="voltar">
            <button type="button" id="voltar-telaFornecedor" onclick="renderizarPagina('usuarioLayout')">Voltar</button>
        </p>

    </div>
    `
}

async function cadastrarFornecedor() {
    const cnpj = document.getElementById('cnpj-fornecedor').value.replace(/\D/g, '');

    if(!cnpj){
        alert("Preencha o campo obrigatorio");
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/cadastro_fornecedor`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                cnpj: cnpj
            })
        });

        if(response.ok){
            alert('Fornecedor cadastrado com sucesso');
        }else{
            const erro = await response.json();
            console.log(erro);
            alert(`Erro ao cadastrar: ${erro.detail}`);
        }
    } catch (error) {
        alert(`Erro ao conectar ao servidor: ${error.message}`);
    }
}