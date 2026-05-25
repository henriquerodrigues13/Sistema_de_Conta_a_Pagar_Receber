async function carregarFornecedores(pagina = 1) {
    try {
        const carregando = document.getElementById('carregando');
        if(carregando) carregando.style.display = 'block';
        
        const response = await fetch(`${API_BASE_URL}/get_fornecedor?page=${pagina}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const fornecedores = await response.json();
        const total = fornecedores.length;

        const spanTotal = document.getElementById('total-fornecedores');
        spanTotal.textContent += total;
        

        renderizarTabelaFornecedor(fornecedores);
    } catch (error) {
        alert("Erro ao carregar fornecedores: " + error.message);
    }finally{
        const carregando = document.getElementById('carregando');
        if(carregando) carregando.style.display = 'none';
    }
}

function renderizarTabelaFornecedor(fornecedores){
    const tabela = document.getElementById('tabela-fornecedor');

    const linhas = tabela.querySelectorAll('tr:not(#cabecalho-tabela-fornecedor)');
    linhas.forEach(linha => linha.remove());

    if (fornecedores.length === 0){
        const tr = document.createElement('tr');
        tr.innerHTML = '<td colspan="5" style="text-align: center; padding: 20px;">Nenhum fornecedor encontrado</td>';
        tabela.appendChild(tr);
        return;
    }

    fornecedores.forEach(fornecedor => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${fornecedor.nome_oficial_empresa || '-'}</td>
            <td>${fornecedor.cnpj || '-'}</td>
            <td>${fornecedor.email || '-'}</td>
            <td>✏️</td>
            <td>🗑️</td>
        `;
        tabela.appendChild(tr);
    });

    console.log(fornecedores)
    console.log(fornecedores.length)
}