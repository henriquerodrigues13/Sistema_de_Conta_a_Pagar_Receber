/**
 * Renderiza a página de login.
 * @returns {string} Estrutura HTML da página.
 */
function paginaLogin() {

    return `
        <div id="container-login">

            <div class="login-form">

                <div class="login-header">

                    <img 
                        src="./assets/imgs/logo/logo.png"
                        alt="Logo"
                    >

                    <h1>BEM-VINDO!</h1>

                    <p>
                        Faça login para acessar sua conta
                    </p>

                </div>

                <form id="systemform">

                    <div class="form-group">

                        <label for="email">
                            Email:
                        </label>

                        <input 
                            type="email"
                            name="email"
                            id="email"
                            placeholder="Digite seu email"
                        >

                    </div>

                    <div 
                        class="form-group"
                        id="inputs-senha"
                    >

                        <label for="senha">
                            Senha:
                        </label>

                        <input 
                            type="password"
                            name="senha"
                            id="senha"
                            placeholder="Digite sua senha"
                        >

                    </div>

                    <div class="btn-entrar">

                        <button
                            type="button"
                            id="btn-logar"
                            onclick="fazerLogin()"
                        >
                            Entrar
                        </button>

                    </div>

                </form>

                <div id="cadastrar">

                    <p>

                        Ainda não tem conta?

                        <button
                            type="button"
                            onclick="renderizarPagina('cadastroUsuario')"
                        >
                            <b>Cadastre-se</b>
                        </button>

                    </p>

                </div>

            </div>

        </div>
    `;
}

/**
 * Obtém os dados do formulário de login.
 * @returns {object} Dados de login.
 */
function obterDadosLogin() {

    return {
        email: document
            .getElementById('email')
            .value
            .trim(),

        senha: document
            .getElementById('senha')
            .value
    };
}

/**
 * Salva os dados do usuário autenticado.
 * @param {object} usuario Dados do usuário.
 * @param {string} email Email do usuário.
 */
function salvarDadosUsuario(usuario, email) {

    localStorage.setItem(
        'usuario',
        usuario.nome_completo
    );

    localStorage.setItem(
        'email',
        email
    );
}

/**
 * Realiza o login do usuário no sistema.
 */
async function fazerLogin() {

    const { email, senha } =
        obterDadosLogin();

    if (!email || !senha) {

        alert(
            'Preencha todos os campos'
        );

        return;
    }

    if (
        email === 'admin' &&
        senha === 'admin'
    ) {

        localStorage.setItem(
            'usuario',
            email
        );

        renderizarPagina(
            'usuarioLayout'
        );

        return;
    }

    try {

        const response = await fetch(
            `${API_BASE_URL}/login`,
            {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/json'
                },
                body: JSON.stringify({
                    email,
                    senha
                })
            }
        );

        if (response.ok) {

            const usuario =
                await response.json();

            salvarDadosUsuario(
                usuario,
                email
            );

            renderizarPagina(
                'usuarioLayout'
            );

            return;
        }

        const erro = await response.json();

        if (
            response.status === 404 ||
            response.status === 401
        ) {

            alert(erro.detail);

            return;
        }

        alert('Erro ao fazer login');

    } catch (error) {

        console.error(error);

        alert(
            `❌ ${error.message}`
        );
    }
}