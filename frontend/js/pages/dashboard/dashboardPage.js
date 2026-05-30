/**
 * Gera o HTML da página do dashboard e dispara o carregamento dos totais.
 * @returns {string} HTML da página.
 */
function paginaDashboard() {
    const nome = obterNomeUsuario();
 
    return `
        <div id="content-dashboard">
 
            <div class="titulo-dashboard">
                <h1>Bem-vindo, ${nome}!</h1>
            </div>
 
            <div class="cards">
 
                <div class="card">
                    <div class="icon">
                        <img src="./assets/imgs/icons/ascendente.png" alt="Receitas">
                    </div>
                    <h2>Total de Receitas</h2>
                    <div class="value" id="dashboard-total-receitas">...</div>
                </div>
 
                <div class="card">
                    <div class="icon red">
                        <img src="./assets/imgs/icons/tendencia.png" alt="Despesas">
                    </div>
                    <h2>Total de Despesas</h2>
                    <div class="value red" id="dashboard-total-despesas">...</div>
                </div>
 
                <div class="card">
                    <div class="icon">
                        <img src="./assets/imgs/icons/caixas.png" alt="Produtos e serviços">
                    </div>
                    <h2>Total de produtos e serviços</h2>
                    <div class="value" id="dashboard-total-produtos-servicos">...</div>
                </div>
 
                <div class="card">
                    <div class="icon">
                        <img src="./assets/imgs/icons/cesta-de-compras-simples.png" alt="Vendas">
                    </div>
                    <h2>Vendas Registradas</h2>
                    <div class="value" id="dashboard-total-vendas">...</div>
                </div>
 
            </div>
 
        </div>
    `;
}