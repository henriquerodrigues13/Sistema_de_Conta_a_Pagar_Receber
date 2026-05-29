/**
 * Valida os dados do formulário de serviço.
 * @param {object} dados Dados do serviço.
 * @returns {string|null} Mensagem de erro ou null.
 */
function validarServico(dados) {

    const {
        nomeServico,
        descricao,
        valorServico,
        categoria
    } = dados;

    if (!nomeServico) {
        return '❌ Digite o nome do serviço';
    }

    if (nomeServico.length < 3) {
        return '❌ O nome do serviço deve ter pelo menos 3 caracteres';
    }

    if (!descricao) {
        return '❌ Digite a descrição do serviço';
    }

    if (descricao.length < 10) {
        return '❌ A descrição deve ter pelo menos 10 caracteres';
    }

    if (!valorServico) {
        return '❌ Digite o valor do serviço';
    }

    const valorServicoFloat = parseFloat(
        valorServico.replace(',', '.')
    );

    if (isNaN(valorServicoFloat) || valorServicoFloat <= 0) {
        return '❌ Digite um valor válido maior que 0';
    }

    if (!categoria || categoria === 'Selecione') {
        return '❌ Selecione uma categoria';
    }

    return null;
}

/**
 * Limpa os campos do formulário de serviços.
 */
function limparFormularioServico() {

    document.getElementById('nome-servico').value = '';

    document.getElementById('descricao-servico').value = '';

    document.getElementById('valor-servico').value = '';

    document.getElementById('categoria-servico').selectedIndex = 0;
}

/**
 * Realiza o cadastro de um serviço na API.
 */
async function cadastrarServico() {

    const nomeServico = document.getElementById('nome-servico').value.trim();

    const descricao = document.getElementById('descricao-servico').value.trim();

    const valorServico = document.getElementById('valor-servico').value.trim();

    const categoria = document.getElementById('categoria-servico').value;

    const emailUsuario = obterEmailUsuario();

    const dadosFormulario = {
        nomeServico,
        descricao,
        valorServico,
        categoria
    };

    const erroValidacao = validarServico(dadosFormulario);

    if (erroValidacao) {
        alert(erroValidacao);
        return;
    }

    const dadosServico = {
        nome_do_servico: nomeServico,
        prestador_do_servico_usuario: emailUsuario,
        descricao_do_servico: descricao,
        valor_do_servico: parseFloat(
            valorServico.replace(',', '.')
        ),
        categoria_do_servico: categoria
    };

    const btnCadastrar = document.getElementById('btn-cadastrarServicos');

    const textoOriginal = btnCadastrar.textContent;

    try {

        btnCadastrar.disabled = true;

        btnCadastrar.textContent = '⏳ Cadastrando...';

        const response = await fetch(`${API_BASE_URL}/cadastro_servico`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dadosServico)
        });

        if (!response.ok) {

            const erro = await response.json();

            if (response.status === 409) {

                alert(`❌ Já existe um serviço chamado "${nomeServico}"`);

            } else if (response.status === 404) {

                alert('❌ Usuário não encontrado. Faça login novamente');

            } else {

                alert(
                    `❌ Erro ${response.status}: ${
                        erro.detail || 'Erro desconhecido'
                    }`
                );
            }

            return;
        }

        alert('✅ Serviço cadastrado com sucesso!');

        limparFormularioServico();

    } catch (error) {

        console.error('Erro ao cadastrar serviço:', error);

        alert(`❌ Erro ao cadastrar serviço: ${error.message}`);

    } finally {

        btnCadastrar.disabled = false;

        btnCadastrar.textContent = textoOriginal;
    }
}