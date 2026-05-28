async function cadastrarServico() {

    // ✅ Obter campos
    const nomeServico = document.querySelector('#form-cadastroServicos input[type="text"]').value.trim();

    const descricao = document.querySelector('#form-cadastroServicos textarea').value.trim();

    const valorServico = document.querySelectorAll('#form-cadastroServicos input[type="text"]')[1].value.trim();

    const categoria = document.querySelector('#form-cadastroServicos select').value;

    const emailUsuario = obterEmailUsuario();

    // ✅ VALIDAÇÕES

    if (!nomeServico) {
        alert('❌ Digite o nome do serviço');
        return;
    }

    if (nomeServico.length < 3) {
        alert('❌ O nome do serviço deve ter pelo menos 3 caracteres');
        return;
    }

    if (!descricao) {
        alert('❌ Digite a descrição do serviço');
        return;
    }

    if (descricao.length < 10) {
        alert('❌ A descrição deve ter pelo menos 10 caracteres');
        return;
    }

    if (!valorServico) {
        alert('❌ Digite o valor do serviço');
        return;
    }

    const valorServicoFloat = parseFloat(
        valorServico.replace(',', '.')
    );

    if (isNaN(valorServicoFloat) || valorServicoFloat <= 0) {
        alert('❌ Digite um valor válido maior que 0');
        return;
    }

    if (!categoria || categoria === 'Selecione') {
        alert('❌ Selecione uma categoria');
        return;
    }

    // ✅ Dados da API
    const dadosServico = {
        nome_do_servico: nomeServico,
        prestador_servico_usuario: emailUsuario,
        descricao_do_servico: descricao,
        valor_do_servico: valorServicoFloat,
        categoria_do_servico: categoria
    };

    try {

        const btnCadastrar = document.getElementById('btn-cadastrarServicos');

        const textoOriginal = btnCadastrar.textContent;

        btnCadastrar.disabled = true;
        btnCadastrar.textContent = '⏳ Cadastrando...';

        // ✅ Requisição
        const response = await fetch(`${API_BASE_URL}/cadastro_servico`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dadosServico)
        });

        // ✅ Tratamento de erro
        if (!response.ok) {

            const erro = await response.json();

            if (response.status === 409) {

                alert(`❌ Já existe um serviço chamado "${nomeServico}"`);

            } else if (response.status === 404) {

                alert('❌ Usuário não encontrado. Faça login novamente');

            } else {

                alert(`❌ Erro ${response.status}: ${erro.detail || 'Erro desconhecido'}`);
            }

            btnCadastrar.disabled = false;
            btnCadastrar.textContent = textoOriginal;

            return;
        }

        // ✅ Sucesso
        alert('✅ Serviço cadastrado com sucesso!');

        // ✅ Limpar formulário
        document.querySelectorAll('#form-cadastroServicos input[type="text"]')[0].value = '';

        document.querySelector('#form-cadastroServicos textarea').value = '';

        document.querySelectorAll('#form-cadastroServicos input[type="text"]')[1].value = '';

        document.querySelector('#form-cadastroServicos select').selectedIndex = 0;

        btnCadastrar.disabled = false;
        btnCadastrar.textContent = textoOriginal;

    } catch (error) {

        console.error('Erro ao cadastrar serviço:', error);

        alert(`❌ Erro ao cadastrar serviço: ${error.message}`);

        const btnCadastrar = document.getElementById('btn-cadastrarServicos');

        btnCadastrar.disabled = false;
        btnCadastrar.textContent = 'Cadastrar';
    }
}