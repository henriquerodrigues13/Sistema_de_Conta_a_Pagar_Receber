<<<<<<< HEAD
=======
function obterElemento(id) {
    const elemento = document.getElementById(id);
    if (!elemento) {
        console.warn(`⚠️ Elemento com ID "${id}" não encontrado`);
    }
    return elemento;
}

>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
async function carregarProdutos(pagina = 1) {
    const emailUsuario = obterEmailUsuario();

    try {
<<<<<<< HEAD
        const carregando = document.getElementById('carregando-produtos');
=======
        const carregando = obterElemento('carregando-produtos');
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
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
<<<<<<< HEAD
        const total = parseInt(response.headers.get('X-Total-Items') || '0', 10);
        const totalPages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);

        // ✅ CORRIGIDO: usar ID único
        const spanTotal = document.getElementById('span-total-produtos');
=======
        console.log(produtosUsuario);
        const total = parseInt(response.headers.get('X-Total-Items') || '0', 10);
        const totalPages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);

        const spanTotal = obterElemento('span-total-produtos');
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
        if (spanTotal) {
            spanTotal.textContent = total;
        }

        renderizarTabelaProdutos(produtosUsuario);
<<<<<<< HEAD
        renderizarPaginacao(pagina, totalPages);
    } catch (error) {
        console.log(error.message)
        renderizarTabelaVaziaProdutos();
    } finally {
        const carregando = document.getElementById('carregando-produtos');
=======
        renderizarPaginacao(pagina, totalPages, 'produtos');

        const tabelaProdutos = obterElemento('tabela-produtos');
        if (tabelaProdutos) tabelaProdutos.style.display = 'table';

        const paginacao = obterElemento('paginacao-produtosServicos');
        if (paginacao) paginacao.style.display = 'flex';

    } catch (error) {
        console.log(error.message)
        renderizarTabelaVaziaProdutos();
        const tabelaProdutos = obterElemento('tabela-produtos');
        if (tabelaProdutos) tabelaProdutos.style.display = 'table';
    } finally {
        const carregando = obterElemento('carregando-produtos');
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
        if (carregando) carregando.style.display = 'none';
    }
}

async function carregarServicos(pagina = 1) {
    const emailUsuario = obterEmailUsuario();
 
    try {
<<<<<<< HEAD
        const carregando = document.getElementById('carregando-servicos');
        if (carregando) carregando.style.display = 'block';
 
        const response = await fetch(`${API_BASE_URL}/get_servicos_usuario/${emailUsuario}?page=${pagina}`, {
=======
        const carregando = obterElemento('carregando-servicos');
        if (carregando) carregando.style.display = 'block';
 
        const response = await fetch(`${API_BASE_URL}/get_servico_usuario/${emailUsuario}?page=${pagina}`, {
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
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
<<<<<<< HEAD
        const total = parseInt(response.headers.get('X-Total-Items') || '0', 10);
        const totalPages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);
 
        // ✅ Atualizar o total de serviços
        const spanTotal = document.getElementById('span-total-servicos');
=======
        console.log(servicosUsuario);
        const total = parseInt(response.headers.get('X-Total-Items') || '0', 10);
        const totalPages = parseInt(response.headers.get('X-Total-Pages') || '1', 10);
 
        const spanTotal = obterElemento('span-total-servicos');
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
        if (spanTotal) {
            spanTotal.textContent = total;
        }
 
        renderizarTabelaServicos(servicosUsuario);
<<<<<<< HEAD
        renderizarPaginacao(pagina, totalPages);
    } catch (error) {
        console.log(error.message)
        renderizarTabelaVaziaServicos();
    } finally {
        const carregando = document.getElementById('carregando-servicos');
=======
        renderizarPaginacao(pagina, totalPages, 'servicos');

        const tabelaServicos = obterElemento('tabela-servicos');
        if (tabelaServicos) tabelaServicos.style.display = 'table';

        const paginacao = obterElemento('paginacao-produtosServicos');
        if (paginacao) paginacao.style.display = 'flex';

    } catch (error) {
        console.log(error.message)
        renderizarTabelaVaziaServicos();
        const tabelaServicos = obterElemento('tabela-servicos');
        if (tabelaServicos) tabelaServicos.style.display = 'table';
    } finally {
        const carregando = obterElemento('carregando-servicos');
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
        if (carregando) carregando.style.display = 'none';
    }
}

function alternaTabela(nomeTabela) {
<<<<<<< HEAD
    // Obtém as tabelas
    const tabelaProdutos = document.getElementById('tabela-produtos');
    const tabelaServicos = document.getElementById('tabela-servicos');
    
    // Obtém os botões das abas
    const botoes = document.querySelectorAll('#opcoes-tabelas button');
    
    // ✅ Verifica se os elementos existem
    if (!tabelaProdutos || !tabelaServicos) {
        console.error('Elementos das tabelas não encontrados');
        return;
    }
    
    // Limpa o estado ativo de todos os botões
    botoes.forEach(botao => botao.classList.remove('ativo'));
    
    // Mostra/esconde as tabelas e seus carregadores
    if (nomeTabela === 'tabelaProdutos') {
        // ✅ Mostra tabela de Produtos
        tabelaProdutos.style.display = 'table';
        tabelaServicos.style.display = 'none';
        
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
        
        // ✅ Marca o botão de Produtos como ativo
        botoes[0].classList.add('ativo');
        
        // ✅ Carrega os produtos
        carregarProdutos(1);
        
    } else if (nomeTabela === 'tabelaServicos') {
        // ✅ Mostra tabela de Serviços
        tabelaProdutos.style.display = 'none';
        tabelaServicos.style.display = 'table';
        
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
        
        // ✅ Marca o botão de Serviços como ativo
        botoes[1].classList.add('ativo');
        
        // ✅ Carrega os serviços
        carregarServicos(1);
=======
    const tabelaProdutos = obterElemento('tabela-produtos');
    const tabelaServicos = obterElemento('tabela-servicos');
    const carregandoProdutos = obterElemento('carregando-produtos');
    const carregandoServicos = obterElemento('carregando-servicos');
    const totalProdutos = obterElemento('total-produtos');
    const totalServicos = obterElemento('total-servicos');
    const btnAdicionarProduto = obterElemento('btn-adicionarProduto');
    const btnAdicionarServico = obterElemento('btn-adicionarServico');
    const inputPesquisa = obterElemento('input-pesquisarProdutosServicos');
    const paginacao = obterElemento('paginacao-produtosServicos');
    const opcoesTabelas = obterElemento('opcoes-tabelas');
    const botoes = opcoesTabelas ? opcoesTabelas.querySelectorAll('button') : [];

    botoes.forEach(botao => {
        botao.classList.remove('ativo');
    });

    if (tabelaProdutos) tabelaProdutos.style.display = 'none';
    if (tabelaServicos) tabelaServicos.style.display = 'none';
    if (paginacao) paginacao.style.display = 'none';

    if (nomeTabela === 'tabelaProdutos') {
        if (carregandoProdutos) carregandoProdutos.style.display = 'block';
        if (carregandoServicos) carregandoServicos.style.display = 'none';
        if (totalProdutos) totalProdutos.style.display = 'block';
        if (totalServicos) totalServicos.style.display = 'none';
        if (btnAdicionarProduto) btnAdicionarProduto.style.display = 'inline-block';
        if (btnAdicionarServico) btnAdicionarServico.style.display = 'none';
        if (inputPesquisa) {
            inputPesquisa.placeholder = 'Pesquisar produtos';
            inputPesquisa.value = '';
        }
        if (botoes[0]) botoes[0].classList.add('ativo');
        setTimeout(() => {
            carregarProdutos(1);
        }, 500);
    }
    else if (nomeTabela === 'tabelaServicos') {
        if (carregandoProdutos) carregandoProdutos.style.display = 'none';
        if (carregandoServicos) carregandoServicos.style.display = 'block';
        if (totalProdutos) totalProdutos.style.display = 'none';
        if (totalServicos) totalServicos.style.display = 'block';
        if (btnAdicionarProduto) btnAdicionarProduto.style.display = 'none';
        if (btnAdicionarServico) btnAdicionarServico.style.display = 'inline-block';
        if (inputPesquisa) {
            inputPesquisa.placeholder = 'Pesquisar serviços';
            inputPesquisa.value = '';
        }
        if (botoes[1]) botoes[1].classList.add('ativo');
        setTimeout(() => {
            carregarServicos(1);
        }, 500);
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
    }
}

function renderizarTabelaProdutos(produtosUsuario) {
<<<<<<< HEAD
    const tabela = document.getElementById('tabela-produtos');
    
    // ✅ Verifica se existe
    if (!tabela) {
        console.error('Elemento #tabela-produtos não encontrado');
        return;
    }
=======
    const tabela = obterElemento('tabela-produtos');
    
    if (!tabela) return;
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf

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
<<<<<<< HEAD
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
=======
        td1.textContent = produto.categoria_do_produto || '-';

        const td2 = document.createElement('td');
        td2.textContent = produto.nome_do_produto || '-';

        const td3 = document.createElement('td');
        td3.textContent = produto.quantidade_em_estoque || '-';

        const td4 = document.createElement('td');
        td4.textContent = produto.unidade_de_medida || '-';

        const td5 = document.createElement('td');
        td5.textContent = produto.valor_final || '-';

        const td6 = document.createElement('td');
        td6.textContent = produto.status_do_produto || '-';
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf

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
<<<<<<< HEAD
        btnEditar.onclick = () => editarProduto(produto.id);  // ✅ CORRIGIDO
=======
        btnEditar.onclick = () => editarProduto(produto.nome_do_produto);  
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
 
        const btnRemover = document.createElement('button');
        const imgRemover = document.createElement('img');
        imgRemover.src = './assets/imgs/icons/lixeira.png';
        imgRemover.alt = 'Remover';
        btnRemover.appendChild(imgRemover);
        btnRemover.className = 'btn-remover';
        btnRemover.title = 'Remover produto';
<<<<<<< HEAD
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
=======
        btnRemover.onclick = () => removerProduto(produto.nome_do_produto);

        divOpcoes.appendChild(btnEditar);
        divOpcoes.appendChild(btnRemover);
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf

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
<<<<<<< HEAD
    const tabela = document.getElementById('tabela-servicos');
    
    // ✅ Verifica se existe
    if (!tabela) {
        console.error('Elemento #tabela-servicos não encontrado');
        return;
    }
=======
    const tabela = obterElemento('tabela-servicos');
    
    if (!tabela) return;
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
 
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
<<<<<<< HEAD
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
=======
        td1.textContent = servico.categoria_do_servico || '-';
 
        const td2 = document.createElement('td');
        td2.textContent = servico.nome_do_servico || '-';
 
        const td3 = document.createElement('td');
        td3.textContent = servico.valor_do_servico || '-';
 
        const td4 = document.createElement('td');
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
 
        const divOpcoes = document.createElement('div');
        divOpcoes.className = 'opcoes-btns';
 
<<<<<<< HEAD
        // ✅ Botão Editar
=======
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
        const btnEditar = document.createElement('button');
        const imgEditar = document.createElement('img');
        imgEditar.src = './assets/imgs/icons/lapis.png';
        imgEditar.alt = 'Editar';
        btnEditar.appendChild(imgEditar);
        btnEditar.className = 'btn-editar';
        btnEditar.title = 'Editar serviço';
<<<<<<< HEAD
        btnEditar.onclick = () => editarServico(servico.id);
 
        // ✅ Botão Remover
=======
        btnEditar.onclick = () => editarServico(servico.nome_do_servico);
 
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
        const btnRemover = document.createElement('button');
        const imgRemover = document.createElement('img');
        imgRemover.src = './assets/imgs/icons/lixeira.png';
        imgRemover.alt = 'Remover';
        btnRemover.appendChild(imgRemover);
        btnRemover.className = 'btn-remover';
        btnRemover.title = 'Remover serviço';
<<<<<<< HEAD
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
=======
        btnRemover.onclick = () => removerServico(servico.nome_do_servico);
 
        divOpcoes.appendChild(btnEditar);
        divOpcoes.appendChild(btnRemover);
 
        td4.appendChild(divOpcoes);
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
 
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
<<<<<<< HEAD
        tr.appendChild(td5);
        tr.appendChild(td6);
        tr.appendChild(td7);
=======
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
 
        tbody.appendChild(tr);
    });
}

function renderizarTabelaVaziaProdutos() {
<<<<<<< HEAD
    const tabela = document.getElementById('tabela-produtos');

    if (!tabela) {
        console.error('Elemento #tabela-produtos não encontrado');
        return;
    }
=======
    const tabela = obterElemento('tabela-produtos');

    if (!tabela) return;
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
    
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
<<<<<<< HEAD
    const tabela = document.getElementById('tabela-servicos');
 
    if (!tabela) {
        console.error('Elemento #tabela-servicos não encontrado');
        return;
    }
=======
    const tabela = obterElemento('tabela-servicos');
 
    if (!tabela) return;
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
    
    const tbody = tabela.querySelector('tbody') || tabela;
    const linhas = tbody.querySelectorAll('tr');
    linhas.forEach(linha => linha.remove());
 
    const tr = document.createElement('tr');
    const td = document.createElement('td');
<<<<<<< HEAD
    td.colSpan = 7;
=======
    td.colSpan = 4;
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
    td.textContent = 'Nenhum serviço encontrado';
    td.style.textAlign = 'center';
    td.style.padding = '20px';
    td.style.color = 'black';
    td.style.border = '#B8B8B8 solid 1px';
    tr.appendChild(td);
    tbody.appendChild(tr);
}

<<<<<<< HEAD
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
=======
function renderizarPaginacao(paginaAtual, totalPaginas, tipo = 'produtos') {
    const paginacao = obterElemento('paginacao-produtosServicos');
    
    if (!paginacao) {
        console.error('❌ Elemento #paginacao-produtosServicos não encontrado');
        return;
    }
    
    const btnProximo = obterElemento('btn-proximaPagina');
    const btnAnterior = obterElemento('btn-anteriorPagina');

    paginacao.style.display = 'flex';

    function carregarProximaPagina() {
        if (paginaAtual < totalPaginas) {
            if (tipo === 'servicos') {
                carregarServicos(paginaAtual + 1);
            } else {
                carregarProdutos(paginaAtual + 1);
            }
        }
    }

    function carregarPaginaAnterior() {
        if (paginaAtual > 1) {
            if (tipo === 'servicos') {
                carregarServicos(paginaAtual - 1);
            } else {
                carregarProdutos(paginaAtual - 1);
            }
        }
    }

    if (btnProximo) {
        btnProximo.onclick = null;
        btnProximo.onclick = carregarProximaPagina;
        
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
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
<<<<<<< HEAD
        btnAnterior.onclick = () => {
            if (paginaAtual > 1) {
                carregarProdutos(paginaAtual - 1);  // ✅ CORRIGIDO
            }
        };
=======
        btnAnterior.onclick = carregarPaginaAnterior;
        
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
        if (paginaAtual === 1) {
            btnAnterior.disabled = true;
            btnAnterior.style.opacity = '0.1';
        } else {
            btnAnterior.disabled = false;
            btnAnterior.style.opacity = '0.9';
        }
    }

<<<<<<< HEAD
    const spanPagina = document.getElementById('span-pagina');
    if (spanPagina) {
        spanPagina.textContent = `Página ${paginaAtual} de ${totalPaginas}`;
    }
=======
    const spanPagina = obterElemento('span-pagina');
    if (spanPagina) {
        spanPagina.textContent = `Página ${paginaAtual} de ${totalPaginas}`;
    }
}

async function removerProduto(nomeProduto) {
    const confirmar = confirm(
        `Deseja realmente remover o produto "${nomeProduto}"?`
    );

    if (!confirmar) {
        return;
    }

    const emailUsuario = obterEmailUsuario();

    try {
        const response = await fetch(
            `${API_BASE_URL}/delete_produto/${emailUsuario}/${encodeURIComponent(nomeProduto)}`,
            {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        if (!response.ok) {
            const erro = await response.json();

            if (response.status === 404) {
                alert('❌ Produto não encontrado');
            } else {
                alert(
                    `❌ Erro ${response.status}: ${
                        erro.detail || 'Erro desconhecido'
                    }`
                );
            }

            return;
        }

        alert(`✅ Produto "${nomeProduto}" removido com sucesso`);
        carregarProdutos(1);

    } catch (error) {
        console.error('Erro ao remover produto:', error);
        alert(`❌ Erro ao remover produto: ${error.message}`);
    }
}

async function removerServico(nomeServico) {
    const confirmar = confirm(
        `Deseja realmente remover o serviço "${nomeServico}"?`
    );

    if (!confirmar) {
        return;
    }

    const emailUsuario = obterEmailUsuario();

    try {
        const response = await fetch(
            `${API_BASE_URL}/delete_servico/${emailUsuario}/${encodeURIComponent(nomeServico)}`,
            {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        if (!response.ok) {
            const erro = await response.json();

            if (response.status === 404) {
                alert('❌ Serviço não encontrado');
            } else {
                alert(
                    `❌ Erro ${response.status}: ${
                        erro.detail || 'Erro desconhecido'
                    }`
                );
            }

            return;
        }

        alert(`✅ Serviço "${nomeServico}" removido com sucesso`);
        carregarServicos(1);

    } catch (error) {
        console.error('Erro ao remover serviço:', error);
        alert(`❌ Erro ao remover serviço: ${error.message}`);
    }
>>>>>>> f40f0a205b27cef1b93735be253a9cb94bdc65bf
}