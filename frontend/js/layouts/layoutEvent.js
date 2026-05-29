function renderizarSection(secao, evento) {
    const section = document.getElementById('section');

    document.querySelectorAll('aside button').forEach(btn => {
        btn.classList.remove('active');
    });

    if (evento) {
        evento.target.classList.add('active');
        console.log(evento);
    } else {
        document.getElementById(`btn-${secao}`).classList.add('active');
    }

    switch (secao) {
        case 'sectionReceita':
            section.innerHTML = paginaReceita();
            setTimeout(() => carregarReceitas(1), 1000);
            break;
        case 'sectionDespesa':
            section.innerHTML = paginaDespesa();
            setTimeout(() => carregarDespesas(1), 1000);
            break;
        case 'sectionDashboard':
            section.innerHTML = paginaDashboard();
            break;
        case 'sectionProdutosServicos':
            section.innerHTML = paginaProdutosServicos();
            alternaTabela('tabelaProdutos');
            break;
        case 'sectionDespesa':
            section.innerHTML = paginaDespesa();
            break;
        default:
            section.innerHTML = '<p>Página não encontrada</p>';
    }
}