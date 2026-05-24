function paginaLayoutUsuario(){
    return`
        <div id="usuarioLayout">
    <aside class="sidebar">
      <div class="marcaagua"></div>
      <div class="logo">
        <img src="./assets/imgs/logo/logoextensa.png" alt="Logo" />
      </div>

      <ul class="menu">
        <li>
          <a href="#" class="active">
            <img src="./assets/imgs/icons/casa.png" class="menu-icon" />
            Dashboard
          </a>
        </li>

        <li>
          <a href="#">
            <img src="./assets/imgs/icons/pagamento.png" class="menu-icon" />
            Contas a Pagar
          </a>
        </li>

        <li>
          <a href="#">
            <img src="./assets/imgs/icons/dinheiro.png" class="menu-icon" />
            Contas a Receber
          </a>
        </li>

        <li>
          <a href="#">
            <img src="./assets/imgs/icons/cliente.png" class="menu-icon" />
            Clientes
          </a>
        </li>

        <li>
          <a href="#">
            <img src="./assets/imgs/icons/fornecedor.png" class="menu-icon" />
            Fornecedores
          </a>
        </li>

        <li>
          <a href="#">
            <img src="./assets/imgs/icons/relatorio.png" class="menu-icon" />
            Relatórios
          </a>
        </li>
        <li>
          <button type="button" onclick="logout()">
            Sair
          </button>
        </li>
      </ul>
    </aside>
    <div id="section"></div>
  </div>
    `
}