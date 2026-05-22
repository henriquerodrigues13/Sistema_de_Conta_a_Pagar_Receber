function paginaLogin() {
    return `
        <div id="container-login">
            <div class="login-form">
                <div class="login-header">
                    <img src="./assets/imgs/icons/logo.png" alt="logo">
                    <h1>BEM-VINDO!</h1>
                    <p>Faça login para acessar sua conta</p>
                </div>

                <form id="systemform">
                    <div class="form-group">
                        <label for="usuario">Email:</label>
                        <input type="email" name="email" id="email" placeholder="Digite seu email" maxlength="14">
                    </div>

                    <div class="form-group" id="inputs-senha">
                        <label for="senha">Senha:</label>
                        <input type="password" name="senha" id="senha" placeholder="Digite sua senha">
                    </div>

                    <div class="btn-entrar">
                        <button type="button" id="btn-logar" onclick="fazerLoginTeste()">Entrar</button>
                    </div>
                </form>

                <div id="cadastrar">
                    <p>Ainda não tem conta? <button type="button" onclick="renderizarPagina('cadastroUsuario')"><b>Cadastre-se</b></button></p>
                </div>
            </div>
        </div>
    `;
}