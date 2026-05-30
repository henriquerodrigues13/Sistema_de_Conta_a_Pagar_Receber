 /**
 * Coleta, valida e envia os dados do formulário para cadastrar uma nova receita.
 * Rota: POST /cadastro_receita
 *
 * Campos obrigatórios: tipo_da_receita, data_da_receita, valor_da_receita, forma_de_pagamento.
 * Campos opcionais:    pagador_email, observacao, documento_anexado.
 */
async function cadastrarReceita(){
 
    const emailUsuario    = obterEmailUsuario();
    const tipoReceita     = document.getElementById('input-tipoReceita')?.value.trim();
    const emailPagador    = document.getElementById('input-emailPagador')?.value.trim();
    const dataReceita     = document.getElementById('input-dataCadastroReceita')?.value;
    const valorRaw        = document.getElementById('input-valorReceita')?.value.trim();
    const formaPagamento  = document.getElementById('opcoes-pagamentos')?.value;
    const observacao      = document.getElementById('input-observacaoReceita')?.value.trim();
    const arquivoInput    = document.getElementById('files');
 
    // Validações dos campos obrigatórios
    if (!tipoReceita) {
        alert('O tipo ou nome da receita é obrigatório.');
        return;
    }
 
    if (!dataReceita) {
        alert('A data de cadastro é obrigatória.');
        return;
    }
 
    const valorReceita = parseFloat(valorRaw.replace(',', '.'));
    if (!valorRaw || isNaN(valorReceita) || valorReceita <= 0) {
        alert('Informe um valor válido para a receita. Ex: 150,00');
        return;
    }
 
    if (!formaPagamento) {
        alert('Selecione a forma de pagamento.');
        return;
    }

    const payload = {
        recebedor_email:   emailUsuario,
        tipo_da_receita:   tipoReceita,
        data_da_receita:   dataReceita,
        valor_da_receita:  valorReceita,
        forma_de_pagamento: formaPagamento,
        ...(emailPagador   && { pagador_email:       emailPagador }),
        ...(observacao     && { observacao:           observacao   }),
        ...(arquivoInput?.files[0] && { documento_anexado: arquivoInput.files[0].name }),
    };
 
    try {
        const response = await fetch(
            `${API_BASE_URL}/cadastro_receita`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            }
        );
 
        if (!response.ok) {
            const erro = await response.json();
            alert(`Erro ${response.status}: ${erro.detail || 'Erro ao cadastrar receita'}`);
            return;
        }
 
        alert('✅ Receita cadastrada com sucesso');
        renderizarPagina('usuarioLayout');
 
    } catch (error) {
        console.error('Erro ao cadastrar receita:', error);
        alert('Erro de conexão. Verifique se o servidor está online.');
    }
}
 