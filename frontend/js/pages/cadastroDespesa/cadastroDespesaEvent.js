async function cadastrarDespesa() {
    const tipoDespesa    = document.getElementById('input-tipoDespesa').value.trim();
    const descricao      = document.getElementById('input-descricaoDespesa').value.trim();
    const valorTotal     = document.getElementById('input-valorTotalDespesa').value;
    const formaPagamento = document.getElementById('opcoes-pagamentosDespesa').value;
    const valorUnidade   = document.getElementById('input-valorUnidadeDespesa').value;
    const isRevenda      = document.getElementById('input-revenda').checked;
    const valorRevenda   = document.getElementById('input-valorUnidadeRevenda')?.value || null;

    if (!tipoDespesa) return alert('Informe o tipo ou nome da despesa.');
    if (!valorTotal || Number(valorTotal) <= 0) return alert('Informe um valor total válido.');
    if (!formaPagamento) return alert('Selecione a forma de pagamento.');
    if (isRevenda && (!valorRevenda || Number(valorRevenda) <= 0)) return alert('Informe o valor de revenda.');

    const body = {
        pagador_email:          obterEmailUsuario(),
        tipo_da_despesa:        tipoDespesa,
        descricao_da_despesa:   descricao || null,
        valor_total_da_despesa: Number(valorTotal),
        forma_de_pagamento:     formaPagamento,
        valor_por_unidade:      valorUnidade ? Number(valorUnidade) : null,
        documento_anexado:      null,
        valor_de_revenda:       isRevenda ? Number(valorRevenda) : null,
    };

    try {
        const response = await fetch(`${API_BASE_URL}/cadastro_despesa`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            const erro = await response.json();
            return alert(erro.detail || 'Erro ao cadastrar despesa.');
        }

        alert('Despesa cadastrada com sucesso!');
        renderizarPagina('usuarioLayout');

    } catch (error) {
        alert('Erro de conexão. Tente novamente.');
    }
}

function iniciarPaginaCadastroDespesa() {
    const footer      = document.getElementById('form-group-footer');
    const radioRevenda = document.getElementById('input-revenda');
    const radios      = document.querySelectorAll('input[name="opc-tipoDespesa"]');

    radios.forEach(radio => {
        radio.addEventListener('change', () => {
            footer.style.display = radioRevenda.checked ? "grid" : "none";
        });
    });
}