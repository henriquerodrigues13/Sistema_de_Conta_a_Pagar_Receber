/**
 * Renderiza a página de venda de produtos.
 * @returns {string} Estrutura HTML da página.
 */
function paginaCadastroVendaProduto() {
    return `
        <div id="container-cadastroVendaProdutos">

            <div class="logo">
                <img src="./assets/imgs/logo/logo.png" alt="Logo">
            </div>

            <h1>Venda de Produto</h1>

            <form id="form-cadastroVendaProduto">

                <div class="linha">

                    <div class="campo">
                        <label>Nome do produto</label>

                        <input 
                            type="text" 
                            id="input-nome-produto" 
                            readonly
                        >
                    </div>

                    <div class="campo">
                        <label>Valor unitário (R$)</label>

                        <input 
                            type="number" 
                            id="input-valor-produto" 
                            placeholder="0,00" 
                            step="0.01"
                        >
                    </div>

                </div>

                <div class="linha">

                    <div class="campo">
                        <label>Quantidade</label>

                        <input 
                            type="number" 
                            id="input-quantidade-produto" 
                            placeholder="1" 
                            min="1" 
                            value="1"
                        >
                    </div>

                    <div class="campo">
                        <label>Desconto (%)</label>

                        <input 
                            type="number" 
                            id="input-desconto-produto" 
                            placeholder="0" 
                            min="0" 
                            max="100" 
                            value="0"
                        >
                    </div>

                </div>

                <div class="linha">

                    <div class="campo">
                        <label>E-mail do comprador</label>

                        <input 
                            type="email" 
                            id="input-comprador-email-produto" 
                            placeholder="Opcional"
                        >
                    </div>

                    <div class="campo">
                        <label>CPF do comprador</label>

                        <input 
                            type="text" 
                            id="input-comprador-cpf-produto" 
                            placeholder="Opcional"
                        >
                    </div>

                </div>

                <div class="linha">

                    <div class="campo">
                        <label>Forma de pagamento</label>

                        <select id="input-pagamento-produto">
                            <option value="">Selecione</option>
                            <option value="Pix">Pix</option>
                            <option value="Débito">Débito</option>
                            <option value="Crédito">Crédito</option>
                            <option value="Boleto">Boleto</option>
                            <option value="Dinheiro">Dinheiro</option>
                        </select>
                    </div>

                    <div class="campo">
                        <label>Descrição</label>

                        <input 
                            type="text" 
                            id="input-descricao-produto" 
                            placeholder="Opcional"
                        >
                    </div>

                </div>

                <div class="valores">
                    <p>
                        Subtotal: R$ 
                        <span id="span-subtotal-produto">0,00</span>
                    </p>

                    <p>
                        Desconto: 
                        <span id="span-desconto-produto">0</span>%
                    </p>

                    <p>
                        Valor final: R$ 
                        <span id="span-valorFinal-produto">0,00</span>
                    </p>
                </div>

            </form>

            <button
                type="button" 
                id="btn-cadastrarVendaProduto" 
                onclick="submitVendaProduto()"
            >
                Realizar Venda
            </button>

            <button
                onclick="renderizarPagina('usuarioLayout')" 
                class="voltar"
            >
               < Voltar
            </button>

        </div>
    `;
}

/**
 * Valida os dados da venda de produto.
 * @param {object} dados Dados da venda.
 * @returns {string|null} Mensagem de erro ou null.
 */
function validarVendaProduto(dados) {

    const {
        nomeProduto,
        valor,
        pagamento
    } = dados;

    if (!nomeProduto) {
        return '❌ Nome do produto é obrigatório';
    }

    if (isNaN(valor) || valor <= 0) {
        return '❌ Informe um valor válido';
    }

    if (!pagamento) {
        return '❌ Selecione a forma de pagamento';
    }

    return null;
}

/**
 * Calcula o valor final da venda.
 * @param {number} valor Valor unitário.
 * @param {number} quantidade Quantidade.
 * @param {number} desconto Desconto em porcentagem.
 * @returns {number} Valor final.
 */
function calcularValorFinal(valor, quantidade, desconto) {

    return parseFloat(
        (valor * quantidade * (1 - desconto / 100)).toFixed(2)
    );
}

/**
 * Realiza o cadastro da venda de um produto na API.
 */
async function submitVendaProduto() {

    const emailUsuario = obterEmailUsuario();

    const nomeProduto = document
        .getElementById('input-nome-produto')
        ?.value
        ?.trim();

    const valor = parseFloat(
        document.getElementById('input-valor-produto')?.value
    );

    const quantidade = parseInt(
        document.getElementById('input-quantidade-produto')?.value
    ) || 1;

    const desconto = parseFloat(
        document.getElementById('input-desconto-produto')?.value
    ) || 0;

    const pagamento = document
        .getElementById('input-pagamento-produto')
        ?.value;

    const descricao = document
        .getElementById('input-descricao-produto')
        ?.value
        ?.trim();

    const compradorEmail = document
        .getElementById('input-comprador-email-produto')
        ?.value
        ?.trim();

    const compradorCpf = document
        .getElementById('input-comprador-cpf-produto')
        ?.value
        ?.trim();

    const dadosFormulario = {
        nomeProduto,
        valor,
        pagamento
    };

    const erroValidacao = validarVendaProduto(dadosFormulario);

    if (erroValidacao) {
        alert(erroValidacao);
        return;
    }

    const valorFinal = calcularValorFinal(
        valor,
        quantidade,
        desconto
    );

    const body = {
        nome_do_produto: nomeProduto,
        vendedor_email: emailUsuario,
        valor_da_venda: valor,
        quantidade,
        forma_de_pagamento: pagamento,
        porcentagem_do_desconto: desconto,
        valor_final: valorFinal,
        descricao_da_venda: descricao || ''
    };

    if (compradorEmail) {
        body.comprador_email = compradorEmail;
    }

    if (compradorCpf) {
        body.comprador_cpf = compradorCpf;
    }

    const btnCadastrar = document.getElementById(
        'btn-cadastrarVendaProduto'
    );

    const textoOriginal = btnCadastrar.textContent;

    try {

        btnCadastrar.disabled = true;

        btnCadastrar.textContent = '⏳ Processando...';

        const response = await fetch(
            `${API_BASE_URL}/cadastro_venda_produto`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            }
        );

        if (!response.ok) {

            const erro = await response.json();

            console.log(erro);

            alert(
                `❌ Erro ${response.status}: ${
                    erro.detail || 'Erro desconhecido'
                }`
            );

            return;
        }

        alert(
            `✅ Venda de "${nomeProduto}" registrada com sucesso!`
        );

        renderizarPagina('usuarioLayout');

    } catch (error) {

        console.error('Erro ao registrar venda:', error);

        alert(
            `❌ Erro ao registrar venda: ${error.message}`
        );

    } finally {

        btnCadastrar.disabled = false;

        btnCadastrar.textContent = textoOriginal;
    }
}