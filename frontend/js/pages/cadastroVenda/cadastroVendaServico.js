/**
 * Renderiza a página de venda de serviços.
 * @returns {string} Estrutura HTML da página.
 */
function paginaCadastroVendaServico() {
    return `
        <div id="container-cadastroVendaServicos">

            <div class="logo">
                <img src="logo.png" alt="Logo">
            </div>

            <h1>Venda de Serviço</h1>

            <form id="form-cadastroVendaServico">

                <div class="linha">

                    <div class="campo">
                        <label>Nome do serviço</label>

                        <input 
                            type="text" 
                            id="input-nome-servico" 
                            readonly
                        >
                    </div>

                    <div class="campo">
                        <label>Valor do serviço (R$)</label>

                        <input 
                            type="number" 
                            id="input-valor-servico" 
                            placeholder="0,00" 
                            step="0.01"
                            oninput="calcularResumoServico()"
                        >
                    </div>

                </div>

                <div class="linha">

                    <div class="campo">
                        <label>Desconto (%)</label>

                        <input 
                            type="number" 
                            id="input-desconto-servico" 
                            placeholder="0"
                            min="0"
                            max="100"
                            value="0"
                            oninput="calcularResumoServico()"
                        >
                    </div>

                    <div class="campo"></div>

                </div>

                <div class="linha">

                    <div class="campo">
                        <label>E-mail do comprador</label>

                        <input 
                            type="email" 
                            id="input-comprador-email-servico" 
                            placeholder="Opcional"
                        >
                    </div>

                    <div class="campo">
                        <label>CPF do comprador</label>

                        <input 
                            type="text" 
                            id="input-comprador-cpf-servico" 
                            placeholder="Opcional"
                            maxlength="14"
                            oninput="mascaraCpfServico(this)"
                        >
                    </div>

                </div>

                <div class="linha">

                    <div class="campo">
                        <label>Forma de pagamento</label>

                        <select id="input-pagamento-servico">
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
                            id="input-descricao-servico" 
                            placeholder="Opcional"
                        >
                    </div>

                </div>

                <div class="valores">

                    <p>
                        Valor: R$ 
                        <span id="span-valor-servico">0,00</span>
                    </p>

                    <p>
                        Desconto: 
                        <span id="span-desconto-servico">0</span>%
                    </p>

                    <p>
                        Valor final: R$ 
                        <span id="span-valorFinal-servico">0,00</span>
                    </p>

                </div>

            </form>

            <button 
                type="button" 
                id="btn-cadastrarVendaServico" 
                onclick="submitVendaServico()"
            >
                Realizar Venda
            </button>

            <a 
                onclick="renderizarPagina('usuarioLayout')" 
                class="voltar"
            >
                Voltar
            </a>

        </div>
    `;
}

/**
 * Formata um valor monetário para o padrão brasileiro.
 * @param {number} valor Valor numérico.
 * @returns {string} Valor formatado.
 */
function formatarValor(valor) {

    return valor.toFixed(2).replace('.', ',');
}

/**
 * Calcula o valor final do serviço.
 * @param {number} valor Valor original.
 * @param {number} desconto Desconto em porcentagem.
 * @returns {number} Valor final.
 */
function calcularValorFinalServico(valor, desconto) {

    return valor * (1 - desconto / 100);
}

/**
 * Atualiza os valores exibidos no resumo da venda.
 */
function calcularResumoServico() {

    const valor = parseFloat(
        document.getElementById('input-valor-servico')?.value
    ) || 0;

    const desconto = parseFloat(
        document.getElementById('input-desconto-servico')?.value
    ) || 0;

    const valorFinal = calcularValorFinalServico(
        valor,
        desconto
    );

    const spanValor = document.getElementById(
        'span-valor-servico'
    );

    const spanDesconto = document.getElementById(
        'span-desconto-servico'
    );

    const spanValorFinal = document.getElementById(
        'span-valorFinal-servico'
    );

    if (spanValor) {
        spanValor.textContent = formatarValor(valor);
    }

    if (spanDesconto) {
        spanDesconto.textContent = desconto.toFixed(0);
    }

    if (spanValorFinal) {
        spanValorFinal.textContent = formatarValor(valorFinal);
    }
}

/**
 * Aplica máscara de CPF no campo informado.
 * @param {HTMLInputElement} elemento Campo de CPF.
 */
function mascaraCpfServico(elemento) {

    let valor = elemento.value
        .replace(/\D/g, '')
        .slice(0, 11);

    if (valor.length > 9) {

        valor = valor.replace(
            /(\d{3})(\d{3})(\d{3})(\d{0,2})/,
            '$1.$2.$3-$4'
        );

    } else if (valor.length > 6) {

        valor = valor.replace(
            /(\d{3})(\d{3})(\d{0,3})/,
            '$1.$2.$3'
        );

    } else if (valor.length > 3) {

        valor = valor.replace(
            /(\d{3})(\d{0,3})/,
            '$1.$2'
        );
    }

    elemento.value = valor;
}

/**
 * Valida os dados da venda de serviço.
 * @param {object} dados Dados da venda.
 * @returns {string|null} Mensagem de erro ou null.
 */
function validarVendaServico(dados) {

    const {
        nomeServico,
        valor,
        pagamento
    } = dados;

    if (!nomeServico) {
        return '❌ Nome do serviço é obrigatório';
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
 * Realiza o cadastro da venda de um serviço na API.
 */
async function submitVendaServico() {

    const emailUsuario = obterEmailUsuario();

    const nomeServico = document
        .getElementById('input-nome-servico')
        ?.value
        ?.trim();

    const valor = parseFloat(
        document.getElementById('input-valor-servico')?.value
    );

    const desconto = parseFloat(
        document.getElementById('input-desconto-servico')?.value
    ) || 0;

    const pagamento = document
        .getElementById('input-pagamento-servico')
        ?.value;

    const descricao = document
        .getElementById('input-descricao-servico')
        ?.value
        ?.trim();

    const compradorEmail = document
        .getElementById('input-comprador-email-servico')
        ?.value
        ?.trim();

    const compradorCpf = document
        .getElementById('input-comprador-cpf-servico')
        ?.value
        ?.trim();

    const dadosFormulario = {
        nomeServico,
        valor,
        pagamento
    };

    const erroValidacao = validarVendaServico(
        dadosFormulario
    );

    if (erroValidacao) {
        alert(erroValidacao);
        return;
    }

    const valorFinal = parseFloat(
        calcularValorFinalServico(
            valor,
            desconto
        ).toFixed(2)
    );

    const body = {
        nome_do_servico: nomeServico,
        vendedor_email: emailUsuario,
        valor_da_venda: valor,
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
        'btn-cadastrarVendaServico'
    );

    const textoOriginal = btnCadastrar.textContent;

    try {

        btnCadastrar.disabled = true;

        btnCadastrar.textContent = '⏳ Processando...';

        const response = await fetch(
            `${API_BASE_URL}/cadastro_venda_servico`,
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

            alert(
                `❌ Erro ${response.status}: ${
                    erro.detail || 'Erro desconhecido'
                }`
            );

            return;
        }

        alert(
            `✅ Venda de "${nomeServico}" registrada com sucesso!`
        );

        renderizarPagina('usuarioLayout');

    } catch (error) {

        console.error(
            'Erro ao registrar venda de serviço:',
            error
        );

        alert(
            `❌ Erro ao registrar venda: ${error.message}`
        );

    } finally {

        btnCadastrar.disabled = false;

        btnCadastrar.textContent = textoOriginal;
    }
}