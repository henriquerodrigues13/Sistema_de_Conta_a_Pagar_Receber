function paginaCadastroUsuario(){
    return `
    <div id="tela-cadastroUsuario">

        <h1>Cadastro de Usuario</h1>

        <form id="formCadastroUsuario">
            <div class="form-grid">

                <div class="input-group">
                    <label>Nome Completo:</label>
                    <input type="text" id="nome-completo" required>
                </div>

                <div class="input-group">
                    <label>Email:</label>
                    <input type="email" id="email" required>
                </div>

                <div class="input-group">
                    <label>Número de Telefone:</label>
                    <input type="text" id="telefone" required>
                </div>

                <div class="input-group">
                    <label>CEP:</label>
                    <input type="text" id="cep" required>
                </div>

                <div class="input-group">
                    <label>Bairro:</label>
                    <input type="text" id="bairro" required>
                </div>

                <div class="input-group">
                    <label>Estado:</label>
                    <input type="text" id="estado" required>
                </div>

                <div class="input-group">
                    <label>Cidade:</label>
                    <input type="text" id="cidade" required>
                </div>

                <div class="input-group">
                    <label>Rua:</label>
                    <input type="text" id="logradouro" required>
                </div>

                <div class="input-group">
                    <label>Senha:</label>
                    <input type="password" id="senha" required>
                </div>

                <div class="input-group">
                    <label>Confirmar senha:</label>
                    <input type="password" id="conf-senha" required>
                </div>

            </div>

            <div class="btn-area">
                <button id="btn-cadastrar" type="button" onclick="cadastrarUsuario()">Cadastrar-se</button>
            </div>

        </form>

        <div class="footer-login">
            <p>Ja tem conta? <button id="tela-login" onclick="renderizarPagina('login')">Fazer login</button></p>
        </div>

    </div>
    `
}

async function cadastrarUsuario(){
    const nome = document.getElementById('nome-completo').value;
    const email = document.getElementById('email').value;
    const telefone = document.getElementById('telefone').value.replace(/\D/g, '');
    const cep = document.getElementById('cep').value;
    const bairro = document.getElementById('bairro').value;
    const estado = document.getElementById('estado').value;
    const cidade = document.getElementById('cidade').value;
    const rua = document.getElementById('logradouro').value;
    const senha = document.getElementById('senha').value;
    const confSenha = document.getElementById('conf-senha').value;

    if(!nome || !email || !telefone || !cep || !bairro || !estado || !cidade || !rua || !senha || !confSenha){
        alert('Preencha todos os campos obrigatorios!');
        return;
    }

    if (senha !== confSenha){
        alert('As senhas não conferem');
        return;
    }

    if(senha.length < 6){
        alert('A senha deve ter no minimo 6 caracteres');
        return;
    }

    try{
        const dados = {
            nome_completo: nome,
            senha: senha,
            email: email,
            numero_telefone: telefone,
            cep: cep,
            estado: estado,
            cidade: cidade,
            bairro: bairro,
            logradouro: rua
        }

        const response = await fetch(`${API_BASE_URL}/cadastro_usuario`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        if(response.ok){
            alert('Usuario cadastrado com sucesso');
        }else{
            const erro = await response.json();
            alert(`Erro ao cadastrar: ${erro.detail}`);
        }
    }catch (erro){
        alert('Error ao conectar com o servidor: ', erro);
    }
}