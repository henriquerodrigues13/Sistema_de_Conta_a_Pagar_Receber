/**
 * Renderiza a página de validação do código de recuperação de senha.
 * @returns {string} Estrutura HTML da página.
 */
function paginaValidarCod() {
    return `
        <div id="container-validarCodigo">
            <div class="topo">
                <img src="./assets/imgs/logo/logo.png" alt="Logo" class="logoImg">
                <h1 class="logoTexto">RED FINANCE</h1>
            </div>
            <div class="conteudo">
                <h2>Insira o código enviado</h2>
                <div class="form-group">
                    <label>Código</label>
                    <input type="text" id="tokenRecuperacao" placeholder="Digite o código">
                    <span id="erroToken" style="color:red; display:none;"></span>
                    <button id="btnValidarCodigo">Validar código</button>
                    <button id="btnVoltarEsqueciSenha" class="voltar">Voltar</button>
                </div>
            </div>
        </div>
    `;
}

/**
 * Inicializa os eventos da página de validação do código.
 */
function initValidarCod() {
    document.getElementById('btnValidarCodigo').addEventListener('click', () => {
        const token = document.getElementById('tokenRecuperacao').value.trim();
        const erro = document.getElementById('erroToken');

        if (!token) {
            erro.textContent = 'Informe o código recebido no email.';
            erro.style.display = 'block';
            return;
        }

        sessionStorage.setItem('tokenRecuperacao', token);
        renderizarPagina('alterarSenha');
    });

    document.getElementById('btnVoltarEsqueciSenha').addEventListener('click', () => {
        renderizarPagina('esquecerSenha');
    });
}