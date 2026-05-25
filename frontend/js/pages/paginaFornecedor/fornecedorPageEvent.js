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

        if(!response.ok){
            const erro = await response.json();
            alert(`Erro ${erro.status}: ${erro.detail}`);
        }

        const fornecedores = await response.json();
        const total = response.headers.get('X-Total-Items') || 0;

        const spanTotal = document.getElementById('span-total');
        if(spanTotal) {
            spanTotal.textContent = total;
        }
        

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
            <td>${fornecedor.cidade || '-'}</td>
            <td>✏️</td>
            <td>🗑️</td>
        `;
        tabela.appendChild(tr);
    });

    console.log(fornecedores)
    console.log(fornecedores.length)
}

function renderizarPaginacao(paginaAtual, totalPaginas) {
    const paginacao = document.getElementById('paginacao');
    paginacao.innerHTML = '';
    
    for (let i = 1; i <= totalPaginas; i++) {
        const btn = document.createElement('button');
        btn.textContent = i;
        btn.className = i === paginaAtual ? 'ativo' : '';
        btn.onclick = () => carregarFornecedores(i);
        paginacao.appendChild(btn);
    }
}