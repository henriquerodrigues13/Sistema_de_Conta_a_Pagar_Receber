function paginaDashboard(){
    return`
        <div class="content-dashboard">
        <h1>Bem-vindo, nome!</h1>
        <div class="cards">

            <div class="card">
                <div class="icon">
                    <img src="./assets/imgs/icons/ascendente.png">
                </div>

                <h2>Total de Receitas</h2>

                <div class="value">
                    R$ 100.000,00
                </div>
            </div>

            <div class="card">
                <div class="icon red">
                    <img src="./assets/imgs/icons/tendencia.png">
                </div>

                <h2>Total de Despesas</h2>

                <div class="value red">
                    R$ 100.000,00
                </div>
            </div>

            <div class="card">
                <div class="icon">
                    <img src="./assets/imgs/icons/caixas.png">
                </div>

                <h2>Total de produtos cadastrados</h2>

                <div class="value">
                    100
                </div>
            </div>

            <div class="card">
                <div class="icon">
                    <img src="./assets/imgs/icons/cesta-de-compras-simples.png">
                </div>

                <h2>Vendas Registradas</h2>

                <div class="value">
                    100
                </div>
            </div>

        </div>

    </div>
    `
}