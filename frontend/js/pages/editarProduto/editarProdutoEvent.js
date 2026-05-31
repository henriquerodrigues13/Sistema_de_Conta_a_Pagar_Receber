/**
 * Busca os dados de um produto pelo nome e renderiza a tela de edição.
 * @param {string} nomeProduto Nome do produto a ser editado.
 */
async function editarProduto(nomeProduto) {

    const emailUsuario = obterEmailUsuario();

    try {

        const response = await fetch(
            `${API_BASE_URL}/get_produtos_usuario/${emailUsuario}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        if (!response.ok) {
            throw new Error(
                'Erro ao buscar produto'
            );
        }

        const produtos = await response.json();

        const produto = produtos.find(
            produto =>
                produto.nome_do_produto === nomeProduto
        );

        if (!produto) {
            alert('❌ Produto não encontrado');
            return;
        }

        document.getElementById('app').innerHTML = paginaEditarProduto(produto);

    } catch (error) {
        console.error(error);
        alert(`❌ ${error.message}`);
    }
}

/**
 * Envia os dados atualizados do produto para a API.
 * @param {string} nomeProdutoOriginal Nome original do produto.
 */
async function salvarEdicaoProduto(nomeProdutoOriginal) {

    const emailUsuario = obterEmailUsuario();

    try {

        const dadosAtualizacao = {
            nome_do_produto:
                obterElemento('editar-nome-produto').value,

            categoria_do_produto:
                obterElemento('editar-categoria-produto').value,

            unidade_de_medida:
                obterElemento('editar-unidade-produto').value,

            quantidade_em_estoque: Number(
                obterElemento(
                    'editar-quantidade-produto'
                ).value
            ),

            valor_de_custo: parseFloat(
                obterElemento(
                    'editar-valorCusto-produto'
                ).value.replace(',', '.')
            ),

            valor_final: parseFloat(
                obterElemento(
                    'editar-valorVenda-produto'
                ).value.replace(',', '.')
            ),

            descricao_do_produto:
                obterElemento(
                    'editar-descricao-produto'
                ).value,

            status_do_produto:
                obterElemento(
                    'editar-status-produto'
                ).value
        };

        const response = await fetch(
            `${API_BASE_URL}/update_produto/${emailUsuario}/${encodeURIComponent(nomeProdutoOriginal)}`,
            {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(
                    dadosAtualizacao
                )
            }
        );

        if (!response.ok) {
            const erro = await response.json();
            alert(`❌ Erro ${response.status}: ${erro.detail || 'Erro ao atualizar produto'}`);
            return;
        }

        alert('✅ Produto atualizado com sucesso');

        renderizarPagina('usuarioLayout');

    } catch (error) {
        console.error(error);
    }
}