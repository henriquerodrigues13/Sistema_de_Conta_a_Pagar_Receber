/**
 * Renderiza a página de alteração de senha.
 * @returns {string} Estrutura HTML da página.
 */
function paginaAlterarSenha() {
    return `
        <div id="container-alterarSenha">
            <div class="topo">
                <img src="./assets/imgs/logo/logo.png" alt="Logo" class="logoImg">
                <h1 class="logoTexto">RED FINANCE</h1>
            </div>
            <div class="conteudo">
                <h2>Alteração de Senha</h2>
                <div class="form-group">
                    <label>Nova Senha</label>
                    <input type="password" id="novaSenha" placeholder="Digite a nova senha">
                    <label>Confirme a Nova Senha</label>
                    <input type="password" id="confirmarSenha" placeholder="Confirme a nova senha">
                    <span id="erroAlterarSenha" style="color:red; display:none;"></span>
                    <button id="btnMudarSenha">Mudar senha</button>
                    <button id="btnVoltarValidarCod" class="voltar">Voltar</button>
                </div>
            </div>
        </div>
    `;
}

/**
 * Inicializa os eventos da página de alteração de senha.
 */
function initAlterarSenha() {
    document.getElementById('btnMudarSenha').addEventListener('click', async () => {
        const novaSenha = document.getElementById('novaSenha').value;
        const confirmarSenha = document.getElementById('confirmarSenha').value;
        const erro = document.getElementById('erroAlterarSenha');
        const token = sessionStorage.getItem('tokenRecuperacao');

        if (!novaSenha || !confirmarSenha) {
            erro.textContent = 'Preencha todos os campos.';
            erro.style.display = 'block';
            return;
        }

        if (novaSenha !== confirmarSenha) {
            erro.textContent = 'As senhas não coincidem.';
            erro.style.display = 'block';
            return;
        }

        if (!token) {
            erro.textContent = 'Token inválido. Reinicie o processo.';
            erro.style.display = 'block';
            return;
        }

        try {
            const resposta = await fetch(`${API_BASE_URL}/reset_senha`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token, senha: novaSenha })
            });

            if (resposta.status === 200) {
                sessionStorage.removeItem('tokenRecuperacao');
                sessionStorage.removeItem('emailRecuperacao');
                alert('Senha alterada com sucesso!');
                renderizarPagina('login');
            } else if (resposta.status === 400) {
                erro.textContent = 'Código expirado. Solicite um novo.';
                erro.style.display = 'block';
            } else if (resposta.status === 404) {
                erro.textContent = 'Código inválido.';
                erro.style.display = 'block';
            } else {
                erro.textContent = 'Erro ao alterar senha. Tente novamente.';
                erro.style.display = 'block';
            }
        } catch (err) {
            console.error(err);
            erro.textContent = 'Erro de conexão. Tente novamente.';
            erro.style.display = 'block';
        }
    });

    document.getElementById('btnVoltarValidarCod').addEventListener('click', () => {
        renderizarPagina('validarCod');
    });
}