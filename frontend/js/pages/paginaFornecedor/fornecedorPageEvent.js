async function carregarFornecedores(pagina = 1) {
    try {
        const carregando = document.getElementById('carregando');
        if (carregando) carregando.style.display = 'block';

        const response = await fetch(`${API_BASE_URL}/get_fornecedor?page=${pagina}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const erro = await response.json();
            alert(`Erro ${erro.status}: ${erro.detail}`);
            return;
        }

        const fornecedores = await response.json();
        const total = parseInt(response.headers.get('X-Total-Items') || '0', 10);
        const totalPages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);

        const spanTotal = document.getElementById('span-total');
        if (spanTotal) {
            spanTotal.textContent = total;
        }

        renderizarTabelaFornecedor(fornecedores);
        renderizarPaginacao(pagina, totalPages);
    } catch (error) {
        console.log(error.message)
        renderizarTabelaVazia();
    } finally {
        const carregando = document.getElementById('carregando');
        if (carregando) carregando.style.display = 'none';
    }
}

function renderizarTabelaFornecedor(fornecedores) {
    const tabela = document.getElementById('tabela-fornecedor');


    const tbody = tabela.querySelector('tbody') || tabela;
    const linhasExistentes = tbody.querySelectorAll('tr');
    linhasExistentes.forEach(linha => linha.remove());

    if (fornecedores.length === 0) {
        renderizarTabelaVazia();
        return;
    }

    fornecedores.forEach(fornecedor => {
        const tr = document.createElement('tr');
        const tabela = document.getElementById('tabela-fornecedor');

        const td1 = document.createElement('td');
        td1.textContent = fornecedor.nome_oficial_empresa || '-';

        const td2 = document.createElement('td');
        td2.textContent = fornecedor.cnpj || '-';

        tr.appendChild(td1);
        tr.appendChild(td2);

        tbody.appendChild(tr);
    });
}

function renderizarTabelaVazia() {
    const tabela = document.getElementById('tabela-fornecedor');
    const tbody = tabela.querySelector('tbody') || tabela;
    const linhas = tbody.querySelectorAll('tr');
    linhas.forEach(linha => linha.remove());

    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.colSpan = 2;
    td.textContent = 'Nenhum fornecedor encontrado';
    td.style.textAlign = 'center';
    td.style.padding = '20px';
    td.style.color = 'black';
    td.style.border = '#333 solid 1px';
    tr.appendChild(td);
    tbody.appendChild(tr);
}

function renderizarPaginacao(paginaAtual, totalPaginas) {
    const paginacao = document.getElementById('paginacao');
    const btnProximo = document.getElementById('btn-proximaPagina');
    const btnAnterior = document.getElementById('btn-anteriorPagina');


    if (btnProximo) {
        btnProximo.onclick = null;
        btnProximo.onclick = () => {
            if (paginaAtual < totalPaginas) {
                carregarFornecedores(paginaAtual + 1);
            }
        };
        btnProximo.disabled = paginaAtual >= totalPaginas;
    }

    if (btnAnterior) {
        btnAnterior.onclick = null;
        btnAnterior.onclick = () => {
            if (paginaAtual > 1) {
                carregarFornecedores(paginaAtual - 1);
            }
        };
        btnAnterior.disabled = paginaAtual === 1;
    }

    // Atualizar informação de página
    const spanPagina = document.getElementById('span-pagina');
    if (spanPagina) {
        spanPagina.textContent = `Página ${paginaAtual} de ${totalPaginas}`;
    }
}

