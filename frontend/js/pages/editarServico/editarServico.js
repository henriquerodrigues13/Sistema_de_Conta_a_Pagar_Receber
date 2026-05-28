function paginaEditarServico(servico) {
    return `
        <div id="container-editarServicos">
            <div class="logo">
                <img
                    src="./assets/imgs/logo/logo.png"
                    alt="Logo"
                />
            </div>

            <h1>Editar Serviço</h1>

            <form id="form-editarServico">

                <div class="campo">
                    <label>Nome do serviço <span style="color: red;">*</span></label>
                    <input 
                        type="text" 
                        placeholder="Digite o nome do serviço" 
                        id="editar-nome-servico"
                        maxlength="100"
                        value="${servico.nome_do_servico || ''}"
                        required
                    />
                </div>

                <div class="campo">
                    <label>Categoria <span style="color: red;">*</span></label>

                    <select id="editar-categoria-servico" required>
                        <option value="informatica" ${servico.categoria_do_servico === 'informatica' ? 'selected' : ''}>Informática</option>

                        <option value="manutencao" ${servico.categoria_do_servico === 'manutencao' ? 'selected' : ''}>Manutenção</option>

                        <option value="design" ${servico.categoria_do_servico === 'design' ? 'selected' : ''}>Design</option>

                        <option value="consultoria" ${servico.categoria_do_servico === 'consultoria' ? 'selected' : ''}>Consultoria</option>

                        <option value="marketing" ${servico.categoria_do_servico === 'marketing' ? 'selected' : ''}>Marketing</option>

                        <option value="educacao" ${servico.categoria_do_servico === 'educacao' ? 'selected' : ''}>Educação</option>

                        <option value="limpeza" ${servico.categoria_do_servico === 'limpeza' ? 'selected' : ''}>Limpeza</option>

                        <option value="transporte" ${servico.categoria_do_servico === 'transporte' ? 'selected' : ''}>Transporte</option>

                        <option value="outros" ${servico.categoria_do_servico === 'outros' ? 'selected' : ''}>Outros</option>
                    </select>
                </div>

                <div class="campo">
                    <label>Valor do serviço <span style="color: red;">*</span></label>

                    <input 
                        type="text" 
                        placeholder="0,00" 
                        id="editar-valor-servico"
                        value="${servico.valor_do_servico || ''}"
                        pattern="[0-9]+([,\.][0-9]{1,2})?"
                        required
                        class="input-valor"
                    />

                    <small style="color: #999;">
                        Ex: 150,00 ou 150.00
                    </small>
                </div>

                <div class="campo">
                    <label>Descrição <span style="color: red;">*</span></label>

                    <textarea 
                        placeholder="Descrição do serviço"
                        id="editar-descricao-servico"
                        minlength="10"
                        maxlength="500"
                        rows="4"
                        required
                    >${servico.descricao_do_servico || ''}</textarea>
                </div>

                <div id="erro-validacao" style="
                    display: none;
                    background-color: #ffe6e6;
                    color: #c0392b;
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 15px;
                    border-left: 4px solid #c0392b;
                "></div>

                <div class="botoes">

                    <button 
                        type="button"
                        id="btn-editarServico"
                        onclick="salvarEdicaoServico('${servico.nome_do_servico}')"
                    >
                        Salvar Alterações
                    </button>

                    <button 
                        type="button"
                        id="voltar-telaProdutoServico"
                        style="cursor: pointer;"
                        onclick="renderizarSection('sectionProdutosServicos', event)"
                    >
                        Voltar
                    </button>

                </div>

            </form>
        </div>
    `;
}