function paginaCadastroUsuario(){
    return `
    <div id="tela-cadastroUsuario">
    <div class="left">
      <h1>REDFINANCE</h1>
    </div>

    <div id="right">
      <div id="top">
        <div class="icon"><img src="./assets/imgs/icons/do-utilizador.png"></div>
        <h2>Cadastre-se</h2>
        <p>Rápido e seguro</p>
      </div>

      <form>
        <div class="form-grid-cadastroUsuario">
          <div class="input-group-cadastroUsuario">
            <label>Nome Completo:</label>
            <input type="text" id="nome-completo"/>
          </div>

          <div class="input-group-cadastroUsuario">
            <label>Bairro:</label>
            <input type="text" id="bairro" />
          </div>

          <div class="input-group-cadastroUsuario">
            <label>Email:</label>
            <input type="email" id="email"/>
          </div>

          <div class="input-group-cadastroUsuario">
            <label>Estado:</label>
            <input type="text" id="estado"/>
          </div>

          <div class="input-group-cadastroUsuario">
            <label>Número de Telefone:</label>
            <input type="text" id="telefone"/>
          </div>

          <div class="input-group-cadastroUsuario">
            <label>Cidade:</label>
            <input type="text" id="cidade"/>
          </div>

          <div class="input-group-cadastroUsuario">
            <label>CEP:</label>
            <input type="text" id="cep"/>
          </div>

          <div class="input-group-cadastroUsuario">
            <label>Rua:</label>
            <input type="text" id="logradouro"/>
          </div>

          <div class="input-group-cadastroUsuario">
            <label>Senha:</label>
            <input type="password" id="senha"/>
          </div>

          <div class="input-group-cadastroUsuario">
            <label>Confirmar senha:</label>
            <input type="password" id="conf-senha"/>
          </div>
        </div>

        <div id="security-box">
          <strong>Seus dados estão seguros</strong>
          <p>Não compartilhamos suas informações com terceiros</p>
        </div>

        <div id="btn-area-cadastroUsuario">
          <button type="button" onclick="cadastrarUsuario()" id="btn-cadastrarUsuario">Cadastre-se</button>
        </div>
      </form>
      <div id="area-btnVoltarLogin">
        <p>
          Já possui login?
          <button type="button" onclick="renderizarPagina('login')" id="btn-voltar">Logar</button>
        </p>
      </div>
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