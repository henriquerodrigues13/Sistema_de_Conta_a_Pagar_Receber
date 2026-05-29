/**
 * Renderiza a página de cadastro de serviços.
 * @returns {string} Estrutura HTML da página.
 */
function paginaCadastroServico() {
    return `
        <div id="container-cadastroServicos">
            <div class="logo">
                <img
                    src="https://cdn-icons-png.flaticon.com/512/3081/3081559.png"
                    alt="logo"
                />
            </div>

            <h1>Cadastro de Serviços</h1>

            <form id="form-cadastroServicos">

                <div class="campo">
                    <label>Nome do serviço</label>

                    <input 
                        type="text"
                        id="nome-servico"
                    />
                </div>

                <div class="campo">
                    <label>Descrição</label>

                    <textarea id="descricao-servico"></textarea>
                </div>

                <div class="campo">
                    <label>Valor do serviço total ou por hora</label>

                    <input 
                        type="text"
                        id="valor-servico"
                    />
                </div>

                <div class="campo">
                    <label>Categoria</label>

                    <select id="categoria-servico">
                        <option selected disabled>Selecione</option>
                        <option value="manutenção">Manutenção</option>
                        <option value="consultoria">Consultoria</option>
                        <option value="tecnologia">Tecnologia</option>
                        <option value="designer">Designer</option>
                        <option value="marketing">Marketing</option>
                        <option value="transporte">Transporte</option>
                        <option value="limpeza">Limpeza</option>
                        <option value="eventos">Eventos</option>
                        <option value="telecommunicações">Telecommunicações</option>
                        <option value="estetética">Estetética</option>
                        <option value="fotografia">Fotografia</option>
                        <option value="delivery">Delivery</option>
                        <option value="suporte">Suporte tecnólogico</option>
                        <option value="outros">Outros...</option>
                    </select>
                </div>

                <div class="botoes">
                    <button 
                        type="button" 
                        id="btn-cadastrarServicos" 
                        onclick="cadastrarServico()"
                    >
                        Cadastrar
                    </button>

                    <button 
                        type="button" 
                        id="btn-voltarDashboard"
                        onclick="renderizarPagina('usuarioLayout')"
                    >
                        Voltar
                    </button>
                </div>
            </form>
        </div>
    `;
}