function obterElemento(id) {
    const elemento = document.getElementById(id);
    if (!elemento) {
        console.warn(`⚠️ Elemento com ID "${id}" não encontrado`);
    }
    return elemento;
}

async function carregarProdutos(pagina = 1) {
    const emailUsuario = obterEmailUsuario();

    try {
        const carregando = obterElemento('carregando-produtos');
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

        const spanTotal = obterElemento('span-total-produtos');
        if (spanTotal) {
            spanTotal.textContent = total;
        }

        renderizarTabelaProdutos(produtosUsuario);
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
        if (carregando) carregando.style.display = 'none';
    }
}

async function carregarServicos(pagina = 1) {
    const emailUsuario = obterEmailUsuario();
 
    try {
        const carregando = obterElemento('carregando-servicos');
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
 
        const spanTotal = obterElemento('span-total-servicos');
        if (spanTotal) {
            spanTotal.textContent = total;
        }
 
        renderizarTabelaServicos(servicosUsuario);
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
        if (carregando) carregando.style.display = 'none';
    }
}

function alternaTabela(nomeTabela) {
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
    }
}

function renderizarTabelaProdutos(produtosUsuario) {
    const tabela = obterElemento('tabela-produtos');
    
    if (!tabela) return;

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
        btnEditar.onclick = () => editarProduto(produto.nome_do_produto);  
 
        const btnRemover = document.createElement('button');
        const imgRemover = document.createElement('img');
        imgRemover.src = './assets/imgs/icons/lixeira.png';
        imgRemover.alt = 'Remover';
        btnRemover.appendChild(imgRemover);
        btnRemover.className = 'btn-remover';
        btnRemover.title = 'Remover produto';
        btnRemover.onclick = () => removerProduto(produto.nome_do_produto);

        divOpcoes.appendChild(btnEditar);
        divOpcoes.appendChild(btnRemover);

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
    const tabela = obterElemento('tabela-servicos');
    
    if (!tabela) return;
 
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
        td1.textContent = servico.categoria_do_servico || '-';
 
        const td2 = document.createElement('td');
        td2.textContent = servico.nome_do_servico || '-';
 
        const td3 = document.createElement('td');
        td3.textContent = servico.valor_do_servico || '-';
 
        const td4 = document.createElement('td');
 
        const divOpcoes = document.createElement('div');
        divOpcoes.className = 'opcoes-btns';
 
        const btnEditar = document.createElement('button');
        const imgEditar = document.createElement('img');
        imgEditar.src = './assets/imgs/icons/lapis.png';
        imgEditar.alt = 'Editar';
        btnEditar.appendChild(imgEditar);
        btnEditar.className = 'btn-editar';
        btnEditar.title = 'Editar serviço';
        btnEditar.onclick = () => editarServico(servico.nome_do_servico);
 
        const btnRemover = document.createElement('button');
        const imgRemover = document.createElement('img');
        imgRemover.src = './assets/imgs/icons/lixeira.png';
        imgRemover.alt = 'Remover';
        btnRemover.appendChild(imgRemover);
        btnRemover.className = 'btn-remover';
        btnRemover.title = 'Remover serviço';
        btnRemover.onclick = () => removerServico(servico.nome_do_servico);
 
        divOpcoes.appendChild(btnEditar);
        divOpcoes.appendChild(btnRemover);
 
        td4.appendChild(divOpcoes);
 
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
 
        tbody.appendChild(tr);
    });
}

function renderizarTabelaVaziaProdutos() {
    const tabela = obterElemento('tabela-produtos');

    if (!tabela) return;
    
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
    const tabela = obterElemento('tabela-servicos');
 
    if (!tabela) return;
    
    const tbody = tabela.querySelector('tbody') || tabela;
    const linhas = tbody.querySelectorAll('tr');
    linhas.forEach(linha => linha.remove());
 
    const tr = document.createElement('tr');
    const td = document.createElement('td');
    td.colSpan = 4;
    td.textContent = 'Nenhum serviço encontrado';
    td.style.textAlign = 'center';
    td.style.padding = '20px';
    td.style.color = 'black';
    td.style.border = '#B8B8B8 solid 1px';
    tr.appendChild(td);
    tbody.appendChild(tr);
}

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
        btnAnterior.onclick = carregarPaginaAnterior;
        
        if (paginaAtual === 1) {
            btnAnterior.disabled = true;
            btnAnterior.style.opacity = '0.1';
        } else {
            btnAnterior.disabled = false;
            btnAnterior.style.opacity = '0.9';
        }
    }

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
}

async function editarServico(nomeServico) {
    const emailUsuario = obterEmailUsuario();

    try {
        // Buscar serviços atuais
        const response = await fetch(
            `${API_BASE_URL}/get_servico_usuario/${emailUsuario}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        if (!response.ok) {
            throw new Error('Erro ao buscar serviço');
        }

        const servicos = await response.json();

        const servico = servicos.find(
            s => s.nome_do_servico === nomeServico
        );

        if (!servico) {
            alert('❌ Serviço não encontrado');
            return;
        }

        // Pegando novos valores
        const novoNome = prompt(
            'Novo nome do serviço:',
            servico.nome_do_servico
        );

        if (novoNome === null) return;

        const novaCategoria = prompt(
            'Nova categoria:',
            servico.categoria_do_servico
        );

        if (novaCategoria === null) return;

        const novoValor = prompt(
            'Novo valor do serviço:',
            servico.valor_do_servico
        );

        if (novoValor === null) return;

        const novaDescricao = prompt(
            'Nova descrição:',
            servico.descricao_do_servico || ''
        );

        if (novaDescricao === null) return;

        // Dados para atualização
        const dadosAtualizacao = {
            nome_do_servico: novoNome,
            categoria_do_servico: novaCategoria,
            valor_do_servico: Number(novoValor),
            descricao_do_servico: novaDescricao
        };

        // Atualizar serviço
        const updateResponse = await fetch(
            `${API_BASE_URL}/update_servico/${emailUsuario}/${encodeURIComponent(nomeServico)}`,
            {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dadosAtualizacao)
            }
        );

        if (!updateResponse.ok) {
            const erro = await updateResponse.json();

            alert(
                `❌ Erro ${updateResponse.status}: ${
                    erro.detail || 'Erro ao atualizar serviço'
                }`
            );

            return;
        }

        alert('✅ Serviço atualizado com sucesso');

        carregarServicos(1);

    } catch (error) {
        console.error(error);
        alert(`❌ ${error.message}`);
    }
}