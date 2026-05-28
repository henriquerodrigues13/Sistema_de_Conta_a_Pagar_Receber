async function carregarProdutos(pagina = 1) {
    const emailUsuario = obterEmailUsuario();

    try {
        const carregando = document.getElementById('carregando-produtos');
        if (carregando) carregando.style.display = 'block';

        const response = await fetch(`${API_BASE_URL}/get_produtos_usuario/${emailUsuario}?page=${pagina}`, {
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

        const produtosUsuario = await response.json();
        console.log(produtosUsuario);
        const total = parseInt(response.headers.get('X-Total-Items') || '0', 10);
        const totalPages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);

        const spanTotal = document.getElementById('span-total-produtos');
        if (spanTotal) {
            spanTotal.textContent = total;
        }

        renderizarTabelaProdutos(produtosUsuario);
        renderizarPaginacao(pagina, totalPages);
    } catch (error) {
        console.log(error.message)
        renderizarTabelaVaziaProdutos();
    } finally {
        const carregando = document.getElementById('carregando-produtos');
        if (carregando) carregando.style.display = 'none';
    }
}

async function carregarServicos(pagina = 1) {
    const emailUsuario = obterEmailUsuario();
 
    try {
        const carregando = document.getElementById('carregando-servicos');
        if (carregando) carregando.style.display = 'block';
 
        const response = await fetch(`${API_BASE_URL}/get_servico_usuario/${emailUsuario}?page=${pagina}`, {
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
 
        const servicosUsuario = await response.json();
        console.log(servicosUsuario);
        const total = parseInt(response.headers.get('X-Total-Items') || '0', 10);
        const totalPages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);
 
        const spanTotal = document.getElementById('span-total-servicos');
        if (spanTotal) {
            spanTotal.textContent = total;
        }
 
        renderizarTabelaServicos(servicosUsuario);
        renderizarPaginacao(pagina, totalPages);
    } catch (error) {
        console.log(error.message)
        renderizarTabelaVaziaServicos();
    } finally {
        const carregando = document.getElementById('carregando-servicos');
        if (carregando) carregando.style.display = 'none';
    }
}

function alternaTabela(nomeTabela) {
    const tabelaProdutos = document.getElementById('tabela-produtos');
    const tabelaServicos = document.getElementById('tabela-servicos');
    
    const botoes = document.querySelectorAll('#opcoes-tabelas button');
    
    if (!tabelaProdutos || !tabelaServicos) {
        console.error('Elementos das tabelas não encontrados');
        return;
    }
    
    botoes.forEach(botao => botao.classList.remove('ativo'));
    
    function limparMensagensVazias(tabela) {
        if (!tabela) return;
        const tbody = tabela.querySelector('tbody') || tabela;
        const linhas = tbody.querySelectorAll('tr');
        
        linhas.forEach(linha => {
            const td = linha.querySelector('td');
            if (td && td.colSpan === 7 && 
                (td.textContent.includes('Nenhum produto') || 
                 td.textContent.includes('Nenhum serviço'))) {
                linha.remove();
            }
        });
    }
    
    // Mostra/esconde as tabelas e seus carregadores
    if (nomeTabela === 'tabelaProdutos') {
        tabelaProdutos.style.display = 'table';
        tabelaServicos.style.display = 'none';
        
        limparMensagensVazias(tabelaProdutos);
        limparMensagensVazias(tabelaServicos);
        
        const carregandoProdutos = document.getElementById('carregando-produtos');
        const carregandoServicos = document.getElementById('carregando-servicos');
        
        if (carregandoProdutos) carregandoProdutos.style.display = 'block';
        if (carregandoServicos) carregandoServicos.style.display = 'none';
        
        const totalProdutos = document.getElementById('total-produtos');
        const totalServicos = document.getElementById('total-servicos');
        
        if (totalProdutos) totalProdutos.style.display = 'block';
        if (totalServicos) totalServicos.style.display = 'none';
        
        const btnAdicionarProduto = document.getElementById('btn-adicionarProduto');
        const btnAdicionarServico = document.getElementById('btn-adicionarServico');
        
        if (btnAdicionarProduto) btnAdicionarProduto.style.display = 'inline-block';
        if (btnAdicionarServico) btnAdicionarServico.style.display = 'none';
        
        botoes[0].classList.add('ativo');
        
        setTimeout(() => carregarProdutos(1), 1000);
        
    } else if (nomeTabela === 'tabelaServicos') {
        tabelaProdutos.style.display = 'none';
        tabelaServicos.style.display = 'table';
        
        limparMensagensVazias(tabelaProdutos);
        limparMensagensVazias(tabelaServicos);
        
        const carregandoProdutos = document.getElementById('carregando-produtos');
        const carregandoServicos = document.getElementById('carregando-servicos');
        
        if (carregandoProdutos) carregandoProdutos.style.display = 'none';
        if (carregandoServicos) carregandoServicos.style.display = 'block';
        
        const totalProdutos = document.getElementById('total-produtos');
        const totalServicos = document.getElementById('total-servicos');
        
        if (totalProdutos) totalProdutos.style.display = 'none';
        if (totalServicos) totalServicos.style.display = 'block';
        
        const btnAdicionarProduto = document.getElementById('btn-adicionarProduto');
        const btnAdicionarServico = document.getElementById('btn-adicionarServico');
        
        if (btnAdicionarProduto) btnAdicionarProduto.style.display = 'none';
        if (btnAdicionarServico) btnAdicionarServico.style.display = 'inline-block';
        
        botoes[1].classList.add('ativo');
        
        setTimeout(() => carregarServicos(1), 1000);
    }
}

function renderizarTabelaProdutos(produtosUsuario) {
    const tabela = document.getElementById('tabela-produtos');
    
    if (!tabela) {
        console.error('Elemento #tabela-produtos não encontrado');
        return;
    }

    const tbody = tabela.querySelector('tbody') || tabela;
    const linhasExistentes = tbody.querySelectorAll('tr');
    linhasExistentes.forEach(linha => linha.remove());

    if (produtosUsuario.length === 0) {
        renderizarTabelaVaziaProdutos();
        return;
    }

    produtosUsuario.forEach(produto => {
        const tr = document.createElement('tr');

        const td1 = document.createElement('td');
        td1.textContent = produto.id || '-';

        const td2 = document.createElement('td');
        td2.textContent = produto.tipo || '-';

        const td3 = document.createElement('td');
        td3.textContent = produto.email || '-';

        const td4 = document.createElement('td');
        td4.textContent = produto.valor || '-';

        const td5 = document.createElement('td');
        td5.textContent = produto.forma_de_pagamento || '-';

        const td6 = document.createElement('td');
        td6.textContent = produto.data || '-';

        const td7 = document.createElement('td');

        const divOpcoes = document.createElement('div');
        divOpcoes.className = 'opcoes-btns';

        const btnEditar = document.createElement('button');
        const imgEditar = document.createElement('img');
        imgEditar.src = './assets/imgs/icons/lapis.png';
        imgEditar.alt = 'Editar';
        btnEditar.appendChild(imgEditar);
        btnEditar.className = 'btn-editar';
        btnEditar.title = 'Editar produto';
        btnEditar.onclick = () => editarProduto(produto.id);  // ✅ CORRIGIDO
 
        const btnRemover = document.createElement('button');
        const imgRemover = document.createElement('img');
        imgRemover.src = './assets/imgs/icons/lixeira.png';
        imgRemover.alt = 'Remover';
        btnRemover.appendChild(imgRemover);
        btnRemover.className = 'btn-remover';
        btnRemover.title = 'Remover produto';
        btnRemover.onclick = () => removerProduto(produto.id);  // ✅ CORRIGIDO

        const btnVerNf = document.createElement('button');
        const imgVerNf = document.createElement('img');
        imgVerNf.src = './assets/imgs/icons/taxa.png';
        imgVerNf.alt = 'Ver NF';
        btnVerNf.appendChild(imgVerNf);
        btnVerNf.className = 'btn-ver-nf';
        btnVerNf.title = 'Ver Nota Fiscal';
        btnVerNf.onclick = () => verNota(produto.id);  // ✅ CORRIGIDO

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

function renderizarTabelaServicos(servicosUsuario) {
    const tabela = document.getElementById('tabela-servicos');
    
    // ✅ Verifica se existe
    if (!tabela) {
        console.error('Elemento #tabela-servicos não encontrado');
        return;
    }
 
    const tbody = tabela.querySelector('tbody') || tabela;
    const linhasExistentes = tbody.querySelectorAll('tr');
    linhasExistentes.forEach(linha => linha.remove());
 
    if (servicosUsuario.length === 0) {
        renderizarTabelaVaziaServicos();
        return;
    }
 
    servicosUsuario.forEach(servico => {
        const tr = document.createElement('tr');
 
        const td1 = document.createElement('td');
        td1.textContent = servico.id || '-';
 
        const td2 = document.createElement('td');
        td2.textContent = servico.tipo || '-';
 
        const td3 = document.createElement('td');
        td3.textContent = servico.email || '-';
 
        const td4 = document.createElement('td');
        td4.textContent = servico.valor || '-';
 
        const td5 = document.createElement('td');
        td5.textContent = servico.forma_de_pagamento || '-';
 
        const td6 = document.createElement('td');
        td6.textContent = servico.data || '-';
 
        const td7 = document.createElement('td');
 
        const divOpcoes = document.createElement('div');
        divOpcoes.className = 'opcoes-btns';
 
        // ✅ Botão Editar
        const btnEditar = document.createElement('button');
        const imgEditar = document.createElement('img');
        imgEditar.src = './assets/imgs/icons/lapis.png';
        imgEditar.alt = 'Editar';
        btnEditar.appendChild(imgEditar);
        btnEditar.className = 'btn-editar';
        btnEditar.title = 'Editar serviço';
        btnEditar.onclick = () => editarServico(servico.id);
 
        // ✅ Botão Remover
        const btnRemover = document.createElement('button');
        const imgRemover = document.createElement('img');
        imgRemover.src = './assets/imgs/icons/lixeira.png';
        imgRemover.alt = 'Remover';
        btnRemover.appendChild(imgRemover);
        btnRemover.className = 'btn-remover';
        btnRemover.title = 'Remover serviço';
        btnRemover.onclick = () => removerServico(servico.id);
 
        // ✅ Botão Ver Nota Fiscal
        const btnVerNf = document.createElement('button');
        const imgVerNf = document.createElement('img');
        imgVerNf.src = './assets/imgs/icons/taxa.png';
        imgVerNf.alt = 'Ver NF';
        btnVerNf.appendChild(imgVerNf);
        btnVerNf.className = 'btn-ver-nf';
        btnVerNf.title = 'Ver Nota Fiscal';
        btnVerNf.onclick = () => verNota(servico.id);
 
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

function renderizarTabelaVaziaProdutos() {
    const tabela = document.getElementById('tabela-produtos');

    if (!tabela) {
        console.error('Elemento #tabela-produtos não encontrado');
        return;
    }
    
    const tbody = tabela.querySelector('tbody') || tabela;
    const linhas = tbody.querySelectorAll('tr');
    linhas.forEach(linha => linha.remove());

    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.colSpan = 7;
    td.textContent = 'Nenhum produto encontrado';
    td.style.textAlign = 'center';
    td.style.padding = '20px';
    td.style.color = 'black';
    td.style.border = '#B8B8B8 solid 1px';
    tr.appendChild(td);
    tbody.appendChild(tr);
}

function renderizarTabelaVaziaServicos() {
    const tabela = document.getElementById('tabela-servicos');
 
    if (!tabela) {
        console.error('Elemento #tabela-servicos não encontrado');
        return;
    }
    
    const tbody = tabela.querySelector('tbody') || tabela;
    const linhas = tbody.querySelectorAll('tr');
    linhas.forEach(linha => linha.remove());
 
    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.colSpan = 7;
    td.textContent = 'Nenhum serviço encontrado';
    td.style.textAlign = 'center';
    td.style.padding = '20px';
    td.style.color = 'black';
    td.style.border = '#B8B8B8 solid 1px';
    tr.appendChild(td);
    tbody.appendChild(tr);
}

function renderizarPaginacao(paginaAtual, totalPaginas) {
    const paginacao = document.getElementById('paginacao-produtosServicos');
    
    // ✅ Verifica se existe
    if (!paginacao) {
        console.error('Elemento #paginacao-produtosServicos não encontrado');
        return;
    }
    
    const btnProximo = document.getElementById('btn-proximaPagina');
    const btnAnterior = document.getElementById('btn-anteriorPagina');

    paginacao.style.display = 'flex';

    if (btnProximo) {
        btnProximo.onclick = null;
        btnProximo.onclick = () => {
            if (paginaAtual < totalPaginas) {
                carregarProdutos(paginaAtual + 1);  // ✅ CORRIGIDO
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
                carregarProdutos(paginaAtual - 1);  // ✅ CORRIGIDO
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