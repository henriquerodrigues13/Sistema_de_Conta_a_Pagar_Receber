/**
 * Valida os dados do formulário de produto.
 * @param {object} dados Dados do produto.
 * @returns {string|null} Mensagem de erro ou null.
 */
function validarProduto(dados) {
    const {
        nomeProduto,
        categoria,
        unidade,
        quantidade,
        valorCusto,
        valorVenda,
        descricao
    } = dados;

    if (!nomeProduto) {
        return '❌ Por favor, digite o nome do produto';
    }

    if (nomeProduto.length < 3) {
        return '❌ O nome do produto deve ter pelo menos 3 caracteres';
    }

    if (!categoria) {
        return '❌ Por favor, selecione uma categoria';
    }

    if (!unidade) {
        return '❌ Por favor, digite a unidade de medida';
    }

    if (!quantidade || isNaN(quantidade) || parseInt(quantidade) <= 0) {
        return '❌ Por favor, digite uma quantidade válida (maior que 0)';
    }

    if (!valorCusto) {
        return '❌ Por favor, digite o valor de custo';
    }

    if (!valorVenda) {
        return '❌ Por favor, digite o valor de venda';
    }

    if (!descricao || descricao.length < 10) {
        return '❌ A descrição deve ter pelo menos 10 caracteres';
    }

    const valorCustoFloat = parseFloat(valorCusto.replace(/,/g, '.'));
    const valorVendaFloat = parseFloat(valorVenda.replace(/,/g, '.'));

    if (isNaN(valorCustoFloat) || valorCustoFloat <= 0) {
        return '❌ O valor de custo deve ser um número válido maior que 0';
    }

    if (isNaN(valorVendaFloat) || valorVendaFloat <= 0) {
        return '❌ O valor de venda deve ser um número válido maior que 0';
    }

    if (valorVendaFloat < valorCustoFloat) {
        return '❌ O valor de venda deve ser maior ou igual ao valor de custo';
    }

    return null;
}

/**
 * Realiza o cadastro de um produto na API.
 */
async function cadastrarProduto() {
    const nomeProduto = document.getElementById('nome-produto').value.trim();
    const categoria = document.getElementById('categoria-produto').value;
    const unidade = document.getElementById('unidade-produto').value.trim();
    const quantidade = document.getElementById('quantidade-produto').value.trim();
    const valorVenda = document.getElementById('valorVenda-produto').value.trim();
    const valorCusto = document.getElementById('valorCusto-produto').value.trim();
    const descricao = document.getElementById('descricao-produto').value.trim();

    const emailUsuario = obterEmailUsuario();

    const dadosFormulario = {
        nomeProduto,
        categoria,
        unidade,
        quantidade,
        valorCusto,
        valorVenda,
        descricao
    };

    const erroValidacao = validarProduto(dadosFormulario);

    if (erroValidacao) {
        alert(erroValidacao);
        return;
    }

    const dadosProduto = {
        nome_do_produto: nomeProduto,
        proprietario_usuario: emailUsuario,
        unidade_de_medida: unidade,
        quantidade_em_estoque: parseInt(quantidade),
        categoria_do_produto: categoria,
        valor_de_custo: parseFloat(valorCusto.replace(/,/g, '.')),
        valor_final: parseFloat(valorVenda.replace(/,/g, '.')),
        descricao_do_produto: descricao
    };

    const btnCadastrar = document.getElementById('btn-cadastrarProduto');
    const textoOriginal = btnCadastrar.textContent;

    try {
        btnCadastrar.disabled = true;
        btnCadastrar.textContent = '⏳ Cadastrando...';

        const response = await fetch(`${API_BASE_URL}/cadastro_produtos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dadosProduto)
        });

        if (!response.ok) {
            const erro = await response.json();

            if (response.status === 409) {
                alert(`❌ Já existe um produto com o nome "${nomeProduto}" no seu cadastro`);
            } else if (response.status === 404) {
                alert('❌ Usuário não encontrado. Faça login novamente');
            } else {
                alert(
                    `❌ Erro ${response.status}: ${erro.detail || erro.message || 'Erro desconhecido'
                    }`
                );
            }

            return;
        }

        alert('✅ Produto cadastrado com sucesso!');

    } catch (error) {
        console.error('Erro ao cadastrar produto:', error);

        alert(`❌ Erro ao cadastrar produto: ${error.message}`);

    } finally {
        btnCadastrar.disabled = false;
        btnCadastrar.textContent = textoOriginal;
    }
}