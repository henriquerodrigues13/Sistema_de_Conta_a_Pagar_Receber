function paginaInicial(){
    return`
    <div id="container-paginaInicial">

    <div class="left">

      <h1>
        Gerencie suas contas a pagar e receber <br>
        com <strong>praticidade e eficiência.</strong>
      </h1>

      <div class="dashboard">
        <img src="./assets/imgs/dashboard.png" alt="Dashboard">
      </div>

    </div>

    <div class="right">

      <div class="login-box">

        <img 
          class="logo"
          src="./assets/imgs/logo/logo.png"
          alt="Logo"
        >

        <div class="titulo">
          Sistema de <br>
          <span>Contas a Pagar <br> e Receber</span>
        </div>

        <div class="descricao">
          Gerencie suas finanças com praticidade
          e tenha o controle total do seu negócio.
        </div>

        <button class="btn btn-login" onclick="renderizarPagina('login')">
            <img src="./assets/imgs/icons/acessar.png" class="icon">
          Acessar
        </button>

        <button class="btn btn-cadastro" onclick="renderizarPagina('cadastroUsuario')">
            <img src="./assets/imgs/icons/cadastrar.png" class="icon">
          Cadastrar-se
        </button>

        <div class="seguranca">
          🔒 Seus dados estão seguros conosco.
        </div>

      </div>

    </div>

  </div>
    `
}