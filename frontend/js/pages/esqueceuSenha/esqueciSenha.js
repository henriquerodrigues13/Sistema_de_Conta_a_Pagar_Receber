function paginaEsqueciSenha() {
    return `
        <div id="container-esqueciSenha">

            <div class="topo">
                <img src="./assets/imgs/logo/logo.png" alt="Logo" class="logoImg">
                <h1 class="logoTexto">RED FINANCE</h1>
            </div>

            <div class="conteudo">

                <h1 class="textoSenha">Esqueci minha senha</h1>

                <p class="texto">
                    Para redefinir sua senha, informe o email cadastrado
                    na sua conta e lhe enviaremos um código para seu email
                    para a recuperação.
                </p>

                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="emailRecuperacao" placeholder="Digite o seu email">

                    <span id="erroEsqueciSenha" style="color:red; display:none;"></span>

                    <button id="btnEnviarCodigo">Enviar código</button>
                    <button id="btnVoltarLogin" class="voltar">< Voltar</button>
                </div>

            </div>

        </div>
    `;
}

function initEsqueciSenha() {
    const btnEnviar = document.getElementById('btnEnviarCodigo');
    const btnVoltar = document.getElementById('btnVoltarLogin');

    if (!btnEnviar || !btnVoltar) {
        console.error('Elemento não encontrado!');
        return;
    }

    btnEnviar.addEventListener('click', async (e) => {
        e.preventDefault();
        e.stopPropagation();
        console.log('1 - clique capturado');

        const email = document.getElementById('emailRecuperacao').value.trim();
        console.log('2 - email:', email);

        const erro = document.getElementById('erroEsqueciSenha');
        console.log('3 - erro element:', erro);

        if (!email) {
            erro.textContent = 'Informe o email.';
            erro.style.display = 'block';
            return;
        }

        console.log('4 - antes do fetch');

        try {
            const resposta = await fetch(`${API_BASE_URL}/recuperacao_senha`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            });
            console.log('5 - resposta:', resposta.status);
            console.log('5.1 - status type:', typeof resposta.status, resposta.status === 201);

            if (resposta.status === 201) {
                console.log('6 - navegando para validarCod');
                sessionStorage.setItem('emailRecuperacao', email);
                renderizarPagina('validarCod');
                console.log('7 - renderizarPagina chamado');
            } else if (resposta.status === 404) {
                erro.textContent = 'Email não encontrado.';
                erro.style.display = 'block';
            } else {
                erro.textContent = 'Erro ao enviar código. Tente novamente.';
                erro.style.display = 'block';
            }

        } catch (err) {
            console.error('erro:', err);
            erro.textContent = 'Erro de conexão. Tente novamente.';
            erro.style.display = 'block';
        }
    });

    btnVoltar.addEventListener('click', (e) => {
        e.preventDefault();
        renderizarPagina('login');
    });
}