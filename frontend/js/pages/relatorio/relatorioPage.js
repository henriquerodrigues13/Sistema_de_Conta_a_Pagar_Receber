/**
 * Gera o HTML da seção de relatórios.
 * @returns {string} HTML da seção.
 */
function sectionRelatorio() {
    return `
        <div id="container-relatorio">

            <h2>Relatórios</h2>

            <div id="card-relatorio">

                <button 
                    type="button"
                    onclick="gerarRelatorio('pdf')"
                >
                    Gerar Relatório PDF
                </button>

                <button 
                    type="button"
                    onclick="gerarRelatorio('xls')"
                >
                    Gerar Relatório XLS
                </button>

                <button 
                    type="button"
                    onclick="gerarRelatorio('xml')"
                >
                    Gerar Relatório XML
                </button>

            </div>

        </div>
    `;
}

/**
 * Solicita a geração e download do relatório completo na API.
 * @param {string} formato - Formato do arquivo (pdf, xls, xml).
 */
async function gerarRelatorio(formato) {
    const emailUsuario = obterEmailUsuario();

    const botoes = document.querySelectorAll('#card-relatorio button');
    botoes.forEach(btn => btn.disabled = true);

    try {
        const response = await fetch(
            `${API_BASE_URL}/relatorio/${formato}/${emailUsuario}`,
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        if (!response.ok) {
            const erro = await response.json();
            alert(`❌ Erro ${response.status}: ${erro.detail || 'Erro desconhecido'}`);
            return;
        }

        const blob = await response.blob();

        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = `relatorio.${formato}`;
        a.click();

        URL.revokeObjectURL(url);

    } catch (error) {
        console.error('Erro ao gerar relatório:', error);
        alert(`❌ Erro ao gerar relatório: ${error.message}`);
    } finally {
        botoes.forEach(btn => btn.disabled = false);
    }
}