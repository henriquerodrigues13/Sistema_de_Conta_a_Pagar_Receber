/**
 * Busca os dados de um serviço pelo nome e renderiza a página de edição.
 * @param {string} nomeServico - Nome do serviço a ser editado.
 */
async function editarServico(nomeServico) {
    const emailUsuario = obterEmailUsuario();
 
    try {
        const response = await fetch(
            `${API_BASE_URL}/get_servico_usuario/${emailUsuario}`,
            {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            }
        );
 
        if (!response.ok) {
            throw new Error('Erro ao buscar serviço');
        }
 
        const servicos = await response.json();
 
        const servico = servicos.find(s => s.nome_do_servico === nomeServico);
 
        if (!servico) {
            alert('❌ Serviço não encontrado');
            return;
        }
 
        document.getElementById('section').innerHTML = paginaEditarServico(servico);
 
    } catch (error) {
        console.error(error);
        alert(`❌ ${error.message}`);
    }
}
 
/**
 * Coleta os dados do formulário, envia o PATCH para a API e redireciona
 * o usuário em caso de sucesso.
 * @param {string} nomeServicoOriginal - Nome original do serviço, usado como
 *                                       identificador na rota da API.
 */
async function salvarEdicaoServico(nomeServicoOriginal) {
    const emailUsuario = obterEmailUsuario();
 
    try {
        const dadosAtualizacao = {
            nome_do_servico:      obterElemento('editar-nome-servico').value,
            categoria_do_servico: obterElemento('editar-categoria-servico').value,
            valor_do_servico:     parseFloat(
                obterElemento('editar-valor-servico').value.replace(',', '.')
            ),
            descricao_do_servico: obterElemento('editar-descricao-servico').value
        };
 
        const response = await fetch(
            `${API_BASE_URL}/update_servico/${emailUsuario}/${encodeURIComponent(nomeServicoOriginal)}`,
            {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dadosAtualizacao)
            }
        );
 
        if (!response.ok) {
            const erro = await response.json();
            alert(`❌ Erro ${response.status}: ${erro.detail || 'Erro ao atualizar serviço'}`);
            return;
        }
 
        alert('✅ Serviço atualizado com sucesso');
 
        renderizarPagina('usuarioLayout');
 
    } catch (error) {
        console.error(error);
    }
}