/**
 * Renderiza a página de despesas.
 * @returns {string} Estrutura HTML da página.
 */
function paginaDespesa() {

    return `
        <div id="container-despesa">

            <h2>Despesas</h2>

            <input 
                type="text" 
                placeholder="Pesquisar receita" 
                id="input-pesquisarDespesa"
            >

            <table id="tabela-despesa">

                <thead>

                    <tr id="cabecalho-tabela-despesa">
                        <th>ID</th>
                        <th>Tipo de Despesa</th>
                        <th>Descrição</th>
                        <th>Valor</th>
                        <th>Opções</th>
                    </tr>

                </thead>

                <tbody></tbody>

            </table>

            <div 
                id="paginacao-despesa" 
                style="display: none;"
            >

                <button id="btn-anteriorPagina">
                    <img 
                        src="./assets/imgs/icons/anterior.png"
                        alt="Página anterior"
                    >
                </button>

                <span id="span-pagina"></span>

                <button id="btn-proximaPagina">
                    <img 
                        src="./assets/imgs/icons/proximo.png"
                        alt="Próxima página"
                    >
                </button>

            </div>

            <div 
                id="carregando" 
                style="
                    display: block;
                    text-align: center;
                    padding: 20px;
                "
            >
                <p>⏳ Carregando despesas...</p>
            </div>

            <div id="baixo-sectionDespesa">

                <button 
                    type="button" 
                    id="btn-adicionarDespesa" 
                    onclick="renderizarPagina('cadastroDespesa')"
                >
                    + Cadastrar Despesa
                </button>

                <p id="total-receitas">
                    Total de Receitas: 
                    <span id="span-total">0</span>
                </p>

            </div>

        </div>
    `;
}