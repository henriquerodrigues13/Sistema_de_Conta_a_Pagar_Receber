/**
 * Renderiza a tela de edição de produto.
 * @param {object} produto Dados do produto.
 * @returns {string} Estrutura HTML da página.
 */
function paginaEditarProduto(produto) {

    return `
        <div id="container-editarProdutos">

            <div class="logo">
                <img
                    src="./assets/imgs/logo/logo.png"
                    alt="Logo"
                />
            </div>

            <h1>Atualizar Produto</h1>

            <form id="form-editarProduto">

                <div class="campo">

                    <label>
                        Nome do produto 
                        <span style="color: red;">*</span>
                    </label>

                    <input 
                        type="text" 
                        placeholder="Digite o nome" 
                        id="editar-nome-produto"
                        maxlength="100"
                        value="${produto.nome_do_produto || ''}"
                        required
                    />

                </div>

                <div class="campo">

                    <label>
                        Categoria 
                        <span style="color: red;">*</span>
                    </label>

                    <select 
                        id="editar-categoria-produto" 
                        required
                    >
                        <option value="informatica" ${produto.categoria_do_produto === 'informatica' ? 'selected' : ''}>Informática</option>

                        <option value="eletronicos" ${produto.categoria_do_produto === 'eletronicos' ? 'selected' : ''}>Eletrônicos</option>

                        <option value="papelaria" ${produto.categoria_do_produto === 'papelaria' ? 'selected' : ''}>Papelaria</option>

                        <option value="limpeza" ${produto.categoria_do_produto === 'limpeza' ? 'selected' : ''}>Limpeza</option>

                        <option value="cosmeticos" ${produto.categoria_do_produto === 'cosmeticos' ? 'selected' : ''}>Cosméticos</option>

                        <option value="alimentos" ${produto.categoria_do_produto === 'alimentos' ? 'selected' : ''}>Alimentos</option>

                        <option value="bebidas" ${produto.categoria_do_produto === 'bebidas' ? 'selected' : ''}>Bebidas</option>

                        <option value="construcao" ${produto.categoria_do_produto === 'construcao' ? 'selected' : ''}>Construção</option>

                        <option value="roupas" ${produto.categoria_do_produto === 'roupas' ? 'selected' : ''}>Roupas</option>

                        <option value="moveis" ${produto.categoria_do_produto === 'moveis' ? 'selected' : ''}>Móveis</option>

                        <option value="medicamentos" ${produto.categoria_do_produto === 'medicamentos' ? 'selected' : ''}>Medicamentos</option>

                        <option value="automotivo" ${produto.categoria_do_produto === 'automotivo' ? 'selected' : ''}>Automotivo</option>

                        <option value="outros" ${produto.categoria_do_produto === 'outros' ? 'selected' : ''}>Outros</option>
                    </select>

                </div>

                <div class="campo">

                    <label>
                        Unidade de medida 
                        <span style="color: red;">*</span>
                    </label>

                    <input 
                        type="text" 
                        placeholder="Ex: kg, l, unidade, etc" 
                        id="editar-unidade-produto"
                        maxlength="20"
                        value="${produto.unidade_de_medida || ''}"
                        required
                    />

                </div>

                <div class="campo">

                    <label>
                        Quantidade em estoque 
                        <span style="color: red;">*</span>
                    </label>

                    <input 
                        type="number" 
                        placeholder="Digite a quantidade" 
                        id="editar-quantidade-produto"
                        min="1"
                        step="1"
                        value="${produto.quantidade_em_estoque || 1}"
                        required
                    />

                    <small style="color: #999;">
                        Mínimo: 1
                    </small>

                </div>

                <div 
                    style="
                        display: grid;
                        grid-template-columns: 1fr 1fr;
                        gap: 15px;
                    "
                >

                    <div class="campo">

                        <label>
                            Valor de custo 
                            <span style="color: red;">*</span>
                        </label>

                        <input 
                            type="text" 
                            placeholder="0,00" 
                            id="editar-valorCusto-produto"
                            value="${produto.valor_de_custo || ''}"
                            pattern="[0-9]+([,\\.][0-9]{1,2})?"
                            required
                            class="input-valor"
                        />

                    </div>

                    <div class="campo">

                        <label>
                            Valor de venda 
                            <span style="color: red;">*</span>
                        </label>

                        <input 
                            type="text" 
                            placeholder="0,00" 
                            id="editar-valorVenda-produto"
                            value="${produto.valor_final || ''}"
                            pattern="[0-9]+([,\\.][0-9]{1,2})?"
                            required
                            class="input-valor"
                        />

                    </div>

                </div>

                <div class="campo">

                    <label>
                        Descrição 
                        <span style="color: red;">*</span>
                    </label>

                    <textarea 
                        placeholder="Descrição do produto"
                        id="editar-descricao-produto"
                        minlength="10"
                        maxlength="500"
                        rows="4"
                        required
                    >${produto.descricao_do_produto || ''}</textarea>

                </div>

                <div class="campo">

                    <label>Status</label>

                    <select id="editar-status-produto">

                        <option 
                            value="ativo" 
                            ${produto.status_do_produto === 'ativo' ? 'selected' : ''}
                        >
                            Ativo
                        </option>

                        <option 
                            value="indisponivel" 
                            ${produto.status_do_produto === 'indisponivel' ? 'selected' : ''}
                        >
                            Indisponível
                        </option>

                    </select>

                </div>

                <div class="botoes">

                    <button 
                        type="button"
                        id="btn-editarProduto"
                        onclick="salvarEdicaoProduto('${produto.nome_do_produto}')"
                    >
                        Atualizar
                    </button>

                    <button 
                        type="button"
                        id="voltar-telaProdutoServico"
                        style="cursor: pointer;"
                        onclick="renderizarPagina('usuarioLayout')"
                    >
                        Voltar
                    </button>

                </div>

            </form>

        </div>
    `;
}