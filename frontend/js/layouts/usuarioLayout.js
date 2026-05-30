/**
 * Renderiza o layout principal do usuário.
 * @returns {string} Estrutura HTML da página.
 */
function paginaLayoutUsuario() {

    return `
        <div id="usuarioLayout">

            <aside class="sidebar">

                <div class="marcaagua"></div>

                <div class="logo">

                    <img 
                        src="./assets/imgs/logo/logoextensa.png"
                        alt="Logo"
                    />

                </div>

                <ul class="menu">

                    <li>

                        <button
                            type="button"
                            id="btn-sectionDashboard"
                            onclick="renderizarSection('sectionDashboard', event)"
                        >

                            <img 
                                src="./assets/imgs/icons/casa.png"
                                class="menu-icon"
                                alt="Dashboard"
                            />

                            Dashboard

                        </button>

                    </li>

                    <li>

                        <button
                            type="button"
                            id="btn-sectionDespesa"
                            onclick="renderizarSection('sectionDespesa', event)"
                        >

                            <img 
                                src="./assets/imgs/icons/pagamento.png"
                                class="menu-icon"
                                alt="Contas a pagar"
                            />

                            Contas a Pagar

                        </button>

                    </li>

                    <li>

                        <button
                            type="button"
                            id="btn-sectionReceita"
                            onclick="renderizarSection('sectionReceita', event)"
                        >

                            <img 
                                src="./assets/imgs/icons/dinheiro.png"
                                class="menu-icon"
                                alt="Contas a receber"
                            />

                            Contas a Receber

                        </button>

                    </li>

                    <li>

                        <button
                            type="button"
                            id="btn-sectionProdutosServicos"
                            onclick="renderizarSection('sectionProdutosServicos', event)"
                        >

                            <img 
                                src="./assets/imgs/icons/armazem.png"
                                class="menu-icon"
                                alt="Produtos e serviços"
                            />

                            Produtos e Serviços

                        </button>

                    </li>

                    <li>

                        <button type="button" id="sectionRelatorio" onclick="renderizarSection('sectionRelatorio', event)">

                            <img 
                                src="./assets/imgs/icons/relatorio.png"
                                class="menu-icon"
                                alt="Relatórios"
                            />

                            Relatórios

                        </button>

                    </li>

                    <li>

                        <button
                            type="button"
                            onclick="logout()"
                        >

                            <img 
                                src="./assets/imgs/icons/saida.png"
                                class="menu-icon"
                                alt="Sair"
                            />

                            Sair

                        </button>

                    </li>

                </ul>

            </aside>

            <div id="section"></div>

        </div>
    `;
}