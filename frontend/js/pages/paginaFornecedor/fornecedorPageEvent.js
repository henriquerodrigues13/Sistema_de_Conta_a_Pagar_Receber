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
        const total = response.headers['X-Total-Items'] || 0;
        const totalPages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);

        console.log(total);
        console.log(totalPages)

        const spanTotal = document.getElementById('span-total');
        if (spanTotal) {
            spanTotal.textContent = total;
        }


        renderizarTabelaFornecedor(fornecedores);
        renderizarPaginacao(pagina, totalPages);
    } catch (error) {
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

        const td3 = document.createElement('td');
        td3.textContent = fornecedor.cidade || '-';

        const td4 = document.createElement('td');
        td4.textContent = 'lapis';

        const td5 = document.createElement('td');
        td5.textContent = 'x';

        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        tr.appendChild(td5);

        tbody.appendChild(tr);
    });
}

function renderizarTabelaVazia() {
    const tabela = document.getElementById('tabela-fornecedor');
    const linhas = tabela.querySelectorAll('tbody tr');
    linhas.forEach(linha => linha.remove());

    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.colSpan = 5;
    td.textContent = 'Nenhum fornecedor encontrado';
    td.style.textAlign = 'center';
    td.style.padding = '20px';
    td.style.color = 'black';
    td.style.border = '#333 solid 1px';
    tr.appendChild(td);
    tabela.appendChild(tr);
}

function renderizarPaginacao(paginaAtual, totalPaginas) {
    const paginacao = document.getElementById('paginacao');
    const btnProximo = document.getElementById('btn-proximaPagina');
    const btnAnterior = document.getElementById('btn-anteriorPagina');
    const paginas = document.getElementById('paginas');
    paginas.textContent = paginaAtual;
 
    // 🔧 CORRIGIDO: Limpar listeners antigos
    if (btnProximo) {
        btnProximo.onclick = null;
        btnProximo.onclick = () => {
            paginas.textContent = paginaAtual + 1;
            if (paginaAtual < 8) {
                carregarFornecedores(paginaAtual + 1);
            }
        };
        btnProximo.disabled = paginaAtual >= 8;
    }
 
    if (btnAnterior) {
        btnAnterior.onclick = null;
        btnAnterior.onclick = () => {
            paginas.textContent = paginaAtual - 1;
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

