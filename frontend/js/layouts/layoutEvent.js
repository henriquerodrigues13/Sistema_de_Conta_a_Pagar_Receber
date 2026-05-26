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
        case 'sectionFornecedor':
            section.innerHTML = paginaFornecedor();
            setTimeout(() => carregarFornecedores(1), 1000);
            break;
        case 'sectionDashboard':
            section.innerHTML = paginaDashboard();
            break;
        default:
            section.innerHTML = '<p>Página não encontrada</p>';
    }
}