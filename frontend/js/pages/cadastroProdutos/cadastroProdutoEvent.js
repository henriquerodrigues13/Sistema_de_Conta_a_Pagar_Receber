async function cadastrarProduto() {
    // Obter dados do formulário
    const nomeProduto = document.getElementById('nome-produto').value.trim();
    const categoria = document.getElementById('categoria-produto').value;
    const unidade = document.getElementById('unidade-produto').value.trim();
    const quantidade = document.getElementById('quantidade-produto').value.trim();
    const valorVenda = document.getElementById('valorVenda-produto').value.trim();
    const valorCusto = document.getElementById('valorCusto-produto').value.trim();
    const descricao = document.getElementById('descricao-produto').value.trim();
    const divErro = document.getElementById('erro-validacao');

    const emailUsuario = obterEmailUsuario();

    // ✅ VALIDAÇÕES
    if (!nomeProduto) {
        alert('❌ Por favor, digite o nome do produto');
        return;
    }

    if (nomeProduto.length < 3) {
        alert('❌ O nome do produto deve ter pelo menos 3 caracteres');
        return;
    }

    if (!categoria) {
        alert('❌ Por favor, selecione uma categoria');
        return;
    }

    if (!unidade) {
        alert('❌ Por favor, digite a unidade de medida');
        return;
    }

    if (!quantidade || isNaN(quantidade) || parseInt(quantidade) <= 0) {
        alert('❌ Por favor, digite uma quantidade válida (maior que 0)');
        return;
    }

    if (!valorCusto) {
        alert('❌ Por favor, digite o valor de custo');
        return;
    }

    if (!valorVenda) {
        alert('❌ Por favor, digite o valor de venda');
        return;
    }

    if (!descricao || descricao.length < 10) {
        alert('❌ A descrição deve ter pelo menos 10 caracteres');
        return;
    }

    const valorCustoFloat = parseFloat(valorCusto.replace(/,/g, '.'));
    const valorVendaFloat = parseFloat(valorVenda.replace(/,/g, '.'));

    if (isNaN(valorCustoFloat) || valorCustoFloat <= 0) {
        alert('❌ O valor de custo deve ser um número válido maior que 0');
        return;
    }

    if (isNaN(valorVendaFloat) || valorVendaFloat <= 0) {
        alert('❌ O valor de venda deve ser um número válido maior que 0');
        return;
    }

    if (valorVendaFloat < valorCustoFloat) {
        alert('❌ O valor de venda deve ser maior ou igual ao valor de custo');
        return;
    }

    const dadosProduto = {
        nome_do_produto: nomeProduto,
        proprietario_usuario: emailUsuario,
        unidade_de_medida: unidade,
        quantidade_em_estoque: parseInt(quantidade),
        categoria_do_produto: categoria,
        valor_de_custo: valorCustoFloat,
        valor_final: valorVendaFloat,
        descricao_do_produto: descricao
    };

    try {
        const btnCadastrar = document.getElementById('btn-cadastrarProduto');
        const textoOriginal = btnCadastrar.textContent;
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
                alert(`❌ Usuário não encontrado. Faça login novamente`);
            } else {
                alert(`❌ Erro ${response.status}: ${erro.detail || erro.message || 'Erro desconhecido'}`);
            }

            btnCadastrar.disabled = false;
            btnCadastrar.textContent = textoOriginal;
            return;
        }
        
        alert(`✅ Produto cadastrado com sucesso!`);

    } catch (error) {
        console.error('Erro ao cadastrar produto:', error);
        alert(`❌ Erro ao cadastrar produto: ${error.message}`);

        const btnCadastrar = document.getElementById('btn-cadastrarProduto');
        btnCadastrar.disabled = false;
        btnCadastrar.textContent = textoOriginal;
    }
}