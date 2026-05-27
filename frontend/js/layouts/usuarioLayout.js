function paginaLayoutUsuario() {
  return `
        <div id="usuarioLayout">
    <aside class="sidebar">
      <div class="marcaagua"></div>
      <div class="logo">
        <img src="./assets/imgs/logo/logoextensa.png" alt="Logo" />
      </div>

      <ul class="menu">
        <li>
          <button type="button" id="btn-sectionDashboard" onclick="renderizarSection('sectionDashboard', event)">
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
          <button type="button" onclick="renderizarSection('sectionReceita', event)">
            <img src="./assets/imgs/icons/dinheiro.png" class="menu-icon" />
            Contas a Receber
          </button>
        </li>

        <li>
          <button type="button" id="btn-sectionEstoque">
            <img src="./assets/imgs/icons/fornecedor.png" class="menu-icon" />
            Produtos e Serviços
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
            <img src="./assets/imgs/icons/saida.png" class="menu-icon" />
            Sair
          </button>
        </li>
      </ul>
    </aside>
    <div id="section"></div>
  </div>
    `
}