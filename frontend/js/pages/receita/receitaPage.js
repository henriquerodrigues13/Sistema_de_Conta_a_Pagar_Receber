function paginaReceita(){
    return`
        <div id="container-receita">

        <h2>Receitas</h2>

        <input type="text" placeholder="Pesquisar receita" id="input-pesquisarReceita">

        <table id="tabela-receita">
            <thead>
                <tr id="cabecalho-tabela-receita">
                    <th>ID</th>
                    <th>Tipo de Receita</th>
                    <th>Email do pagador</th>
                    <th>Valor</th>
                    <th>Forma de pagamento</th>
                    <th>Data</th>
                    <th>Opções</th>
                </tr>
            </thead>    
            <tbody>
    
            </tbody>
        </table>

        <div id="paginacao-receita" style="display: none;">
            <button id="btn-anteriorPagina"><img src="./assets/imgs/icons/anterior.png"></button>
            <span id="span-pagina"></span>
            <button id="btn-proximaPagina"> <img src="./assets/imgs/icons/proximo.png"></button>
        </div>

        <div id="carregando" style="display: block; text-align: center; padding: 20px;">
            <p>⏳ Carregando receitas...</p>
        </div>

        <div id="baixo-sectionReceita">
            <button type="button" id="btn-adicionarReceita">+ Cadastrar Receita</button>
            <p id="total-receitas">Total de Receitas: <span id="span-total">0</span></p>
        </div>

    </div>
    `
}


