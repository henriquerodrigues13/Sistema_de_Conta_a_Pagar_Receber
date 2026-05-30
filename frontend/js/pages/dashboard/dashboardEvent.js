/**
 * Busca o total de itens de uma rota paginada pelo header X-Total-Items.
 * @param {string} url - URL completa da rota (page=1 é suficiente para obter o total).
 * @returns {Promise<number>} Total de itens ou 0 em caso de erro.
 */
async function buscarTotal(url) {
    try {
        const response = await fetch(`${url}?page=1`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });
 
        if (!response.ok) return 0;
 
        return parseInt(response.headers.get('X-Total-Items') || '0', 10);
 
    } catch {
        return 0;
    }
}
 
/**
 * Carrega os totais de receitas, despesas, produtos, serviços e vendas
 * em paralelo e preenche os cards do dashboard.
 */
async function carregarTotaisDashboard() {
    const email = obterEmailUsuario();
 
    const [totalReceitas, totalDespesas, totalProdutos, totalServicos, totalVendas] =
        await Promise.all([
            buscarTotal(`${API_BASE_URL}/get_receitas/${email}`),
            buscarTotal(`${API_BASE_URL}/get_despesas/${email}`),
            buscarTotal(`${API_BASE_URL}/get_produtos_usuario/${email}`),
            buscarTotal(`${API_BASE_URL}/get_servico_usuario/${email}`),
            buscarTotal(`${API_BASE_URL}/get_vendas/${email}`),
        ]);
 
    const el = (id) => document.getElementById(id);
 
    const elReceitas = el('dashboard-total-receitas');
    const elDespesas = el('dashboard-total-despesas');
    const elProdServ = el('dashboard-total-produtos-servicos');
    const elVendas   = el('dashboard-total-vendas');
 
    if (elReceitas) elReceitas.textContent = totalReceitas;
    if (elDespesas) elDespesas.textContent = totalDespesas;
    if (elProdServ) elProdServ.textContent = totalProdutos + totalServicos;
    if (elVendas)   elVendas.textContent   = totalVendas;
}