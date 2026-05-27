async function carregarReceitas(pagina = 1) {
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

        const receitas = await response.json();
        const total = parseInt(response.headers.get('X-Total-Items') || '0', 10);
        const totalPages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);

        const spanTotal = document.getElementById('span-total');
        if (spanTotal) {
            spanTotal.textContent = total;
        }

        renderizarTabelaReceita(receitas);
        renderizarPaginacao(pagina, totalPages);
    } catch (error) {
        console.log(error.message)
        renderizarTabelaVazia();
    } finally {
        const carregando = document.getElementById('carregando');
        if (carregando) carregando.style.display = 'none';
    }
}

function renderizarTabelaReceita(receitas) {
    const tabela = document.getElementById('tabela-receita');


    const tbody = tabela.querySelector('tbody') || tabela;
    const linhasExistentes = tbody.querySelectorAll('tr');
    linhasExistentes.forEach(linha => linha.remove());

    if (receitas.length === 0) {
        renderizarTabelaVazia();
        return;
    }

    receitas.forEach(receita => {
        const tr = document.createElement('tr');

        const td1 = document.createElement('td');
        td1.textContent = receita.id || '-';

        const td2 = document.createElement('td');
        td2.textContent = receita.tipo || '-';

         const td3 = document.createElement('td');
        td3.textContent = receita.email || '-';
 
        const td4 = document.createElement('td');
        td4.textContent = receita.valor || '-';
 
        const td5 = document.createElement('td');
        td5.textContent = receita.forma_de_pagamento || '-';
 
        const td6 = document.createElement('td');
        td6.textContent = receita.data || '-';

        const td7 = document.createElement('td');


        const divOpcoes = document.createElement('div');
        divOpcoes.className = 'opcoes-btns';

        const btnEditar = document.createElement('button');
        const imgEditar = document.createElement('img');
        imgEditar.src = './assets/imgs/icons/lapis.png';
        imgEditar.alt = 'Editar';
        btnEditar.appendChild(imgEditar);
        btnEditar.className = 'btn-editar';
        btnEditar.title = 'Editar receita';
        btnEditar.onclick = () => editarReceita(receita.id);
 
        const btnRemover = document.createElement('button');
        const imgRemover = document.createElement('img');
        imgRemover.src = './assets/imgs/icons/lixeira.png';
        imgRemover.alt = 'Remover';
        btnRemover.appendChild(imgRemover);
        btnRemover.className = 'btn-remover';
        btnRemover.title = 'Remover receita';
        btnRemover.onclick = () => removerReceita(receita.id);

        const btnVerNf = document.createElement('button');
        const imgVerNf = document.createElement('img');
        imgVerNf.src = './assets/imgs/icons/taxa.png';
        imgVerNf.alt = 'Ver NF';
        btnVerNf.appendChild(imgVerNf);
        btnVerNf.className = 'btn-ver-nf';
        btnVerNf.title = 'Ver Nota Fiscal';
        btnVerNf.onclick = () => verNota(receita.id);

        divOpcoes.appendChild(btnEditar);
        divOpcoes.appendChild(btnRemover);
        divOpcoes.appendChild(btnVerNf);

        td7.appendChild(divOpcoes);

        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        tr.appendChild(td5);
        tr.appendChild(td6);
        tr.appendChild(td7);

        tbody.appendChild(tr);
    });
}

function renderizarTabelaVazia() {
    const tabela = document.getElementById('tabela-receita');
    const tbody = tabela.querySelector('tbody') || tabela;
    const linhas = tbody.querySelectorAll('tr');
    linhas.forEach(linha => linha.remove());

    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.colSpan = 7;
    td.textContent = 'Nenhuma receita encontrada';
    td.style.textAlign = 'center';
    td.style.padding = '20px';
    td.style.color = 'black';
    td.style.border = '#B8B8B8 solid 1px';
    tr.appendChild(td);
    tbody.appendChild(tr);
}

function renderizarPaginacao(paginaAtual, totalPaginas) {
    const paginacao = document.getElementById('paginacao-receita');
    const btnProximo = document.getElementById('btn-proximaPagina');
    const btnAnterior = document.getElementById('btn-anteriorPagina');

    paginacao.style.display = 'flex';


    if (btnProximo) {
        btnProximo.onclick = null;
        btnProximo.onclick = () => {
            if (paginaAtual < totalPaginas) {
                carregarReceitas(paginaAtual + 1);
            }
        };
        if (paginaAtual >= totalPaginas) {
            btnProximo.disabled = true;
            btnProximo.style.opacity = '0.1';
        } else {
            btnProximo.disabled = false;
            btnProximo.style.opacity = '0.9';
        }
    }

    if (btnAnterior) {
        btnAnterior.onclick = null;
        btnAnterior.onclick = () => {
            if (paginaAtual > 1) {
                carregarReceitas(paginaAtual - 1);
            }
        };
        if (paginaAtual === 1) {
            btnAnterior.disabled = true;
            btnAnterior.style.opacity = '0.1';
        } else {
            btnAnterior.disabled = false;
            btnAnterior.style.opacity = '0.9';
        }
    }

    const spanPagina = document.getElementById('span-pagina');
    if (spanPagina) {
        spanPagina.textContent = `Página ${paginaAtual} de ${totalPaginas}`;
    }
}

// function editarReceita(id) {
//     console.log('Editar receita:', id);
//     // Implementar lógica de edição
// }
 
// function removerReceita(id) {
//     console.log('Remover receita:', id);
//     // Implementar lógica de remoção
// }
 
// function verNota(id) {
//     console.log('Ver nota fiscal:', id);
//     // Implementar lógica para visualizar nota
// }