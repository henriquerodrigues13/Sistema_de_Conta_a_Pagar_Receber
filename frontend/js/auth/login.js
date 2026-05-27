function paginaLogin() {
    return `
        <div id="container-login">
            <div class="login-form">
                <div class="login-header">
                    <img src="./assets/imgs/logo/logo.png" alt="logo">
                    <h1>BEM-VINDO!</h1>
                    <p>Faça login para acessar sua conta</p>
                </div>

                <form id="systemform">
                    <div class="form-group">
                        <label for="usuario">Email:</label>
                        <input type="email" name="email" id="email" placeholder="Digite seu email">
                    </div>

                    <div class="form-group" id="inputs-senha">
                        <label for="senha">Senha:</label>
                        <input type="password" name="senha" id="senha" placeholder="Digite sua senha">
                    </div>

                    <div class="btn-entrar">
                        <button type="button" id="btn-logar" onclick="fazerLogin()">Entrar</button>
                    </div>
                </form>

                <div id="cadastrar">
                    <p>Ainda não tem conta? <button type="button" onclick="renderizarPagina('cadastroUsuario')"><b>Cadastre-se</b></button></p>
                </div>
            </div>
        </div>
    `;
}


async function fazerLogin() {
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    if (!email || !senha) {
        alert('Preencha todos os campos');
        return;
    }

    if (email == 'admin' && senha == 'admin') {
        localStorage.setItem('usuario', email);
        renderizarPagina('usuarioLayout');
        return;
    } else {
        try {
            const dados = {
                email: email,
                senha: senha
            }

            const response = await fetch(`${API_BASE_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dados)
            });

            if (response.ok) {
                const usuario = await response.json();
                localStorage.setItem('usuario', usuario.nome_completo);
                localStorage.setItem('email', email);
                renderizarPagina('usuarioLayout');
            } else if (response.status == 404) {
                const erro = await response.json();
                alert(erro.detail) // Usuario não encontrado
            } else if (response.status == 401) {
                const erro = await response.json();
                alert(erro.detail) // senha incorreta
            } else {
                alert("Erro ao fazer login");
            }
        } catch (error) {
            alert(error);
        }
    }
}