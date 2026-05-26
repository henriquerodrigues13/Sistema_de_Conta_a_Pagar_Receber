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
          <button type="button" class="active" id="btn-dashboard">
            <img src="./assets/imgs/icons/casa.png" class="menu-icon" />
            Dashboard
          </button>
        </li>

        <li>
          <button type="button">
            <img src="./assets/imgs/icons/pagamento.png" class="menu-icon" />
            Contas a Pagar
          </button>
        </li>

        <li>
          <button type="button">
            <img src="./assets/imgs/icons/dinheiro.png" class="menu-icon" />
            Contas a Receber
          </button>
        </li>

        <li>
          <button type="button" onclick="renderizarSection('sectionFornecedor', event)" id="btn-sectionFornecedor">
            <img src="./assets/imgs/icons/fornecedor.png" class="menu-icon" />
            Fornecedores
          </button>
        </li>

        <li>
          <button type="button">
            <img src="./assets/imgs/icons/relatorio.png" class="menu-icon" />
            Relatórios
          </button>
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