/**
 * Renderiza a página de cadastro de usuário.
 * @returns {string} Estrutura HTML da página.
 */
function paginaCadastroUsuario() {

    return `
        <div id="tela-cadastroUsuario">

            <div class="left">

                <h1>
                    RED FINANCE
                </h1>

            </div>

            <div id="right">

                <div id="top">

                    <div class="icon">

                        <img 
                            src="./assets/imgs/icons/do-utilizador.png"
                            alt="Usuário"
                        >

                    </div>

                    <h2>
                        Cadastre-se
                    </h2>

                    <p>
                        Rápido e seguro
                    </p>

                </div>

                <form>

                    <div class="form-grid-cadastroUsuario">

                        <div class="input-group-cadastroUsuario">

                            <label>
                                Nome Completo:
                            </label>

                            <input
                                type="text"
                                id="nome-completo"
                            />

                        </div>

                        <div class="input-group-cadastroUsuario">

                            <label>
                                Bairro:
                            </label>

                            <input
                                type="text"
                                id="bairro"
                            />

                        </div>

                        <div class="input-group-cadastroUsuario">

                            <label>
                                Email:
                            </label>

                            <input
                                type="email"
                                id="email"
                            />

                        </div>

                        <div class="input-group-cadastroUsuario">

                            <label>
                                Estado:
                            </label>

                            <input
                                type="text"
                                id="estado"
                            />

                        </div>

                        <div class="input-group-cadastroUsuario">

                            <label>
                                Número de Telefone:
                            </label>

                            <input
                                type="text"
                                id="telefone"
                            />

                        </div>

                        <div class="input-group-cadastroUsuario">

                            <label>
                                Cidade:
                            </label>

                            <input
                                type="text"
                                id="cidade"
                            />

                        </div>

                        <div class="input-group-cadastroUsuario">

                            <label>
                                CEP:
                            </label>

                            <input
                                type="text"
                                id="cep"
                            />

                        </div>

                        <div class="input-group-cadastroUsuario">

                            <label>
                                Rua:
                            </label>

                            <input
                                type="text"
                                id="logradouro"
                            />

                        </div>

                        <div class="input-group-cadastroUsuario">

                            <label>
                                Senha:
                            </label>

                            <input
                                type="password"
                                id="senha"
                            />

                        </div>

                        <div class="input-group-cadastroUsuario">

                            <label>
                                Confirmar senha:
                            </label>

                            <input
                                type="password"
                                id="conf-senha"
                            />

                        </div>

                    </div>

                    <div id="security-box">

                        <strong>
                            Seus dados estão seguros
                        </strong>

                        <p>
                            Não compartilhamos suas informações com terceiros
                        </p>

                    </div>

                    <div id="btn-area-cadastroUsuario">

                        <button
                            type="button"
                            id="btn-cadastrarUsuario"
                            onclick="cadastrarUsuario()"
                        >
                            Cadastre-se
                        </button>

                    </div>

                </form>

                <div id="area-btnVoltarLogin">

                    <p>

                        Já possui login?

                        <button
                            type="button"
                            id="btn-voltar"
                            onclick="renderizarPagina('login')"
                        >
                            Logar
                        </button>

                    </p>

                </div>

            </div>

        </div>
    `;
}

/**
 * Obtém os dados do formulário de cadastro.
 * @returns {object} Dados do usuário.
 */
function obterDadosCadastroUsuario() {

    return {
        nome_completo: document
            .getElementById('nome-completo')
            .value
            .trim(),

        email: document
            .getElementById('email')
            .value
            .trim(),

        numero_telefone: document
            .getElementById('telefone')
            .value
            .replace(/\D/g, ''),

        cep: document
            .getElementById('cep')
            .value
            .trim(),

        bairro: document
            .getElementById('bairro')
            .value
            .trim(),

        estado: document
            .getElementById('estado')
            .value
            .trim(),

        cidade: document
            .getElementById('cidade')
            .value
            .trim(),

        logradouro: document
            .getElementById('logradouro')
            .value
            .trim(),

        senha: document
            .getElementById('senha')
            .value,

        confirmarSenha: document
            .getElementById('conf-senha')
            .value
    };
}

/**
 * Valida os dados do formulário.
 * @param {object} dados Dados do usuário.
 * @returns {boolean}
 */
function validarCadastroUsuario(dados) {

    const {
        nome_completo,
        email,
        numero_telefone,
        cep,
        bairro,
        estado,
        cidade,
        logradouro,
        senha,
        confirmarSenha
    } = dados;

    if (
        !nome_completo ||
        !email ||
        !numero_telefone ||
        !cep ||
        !bairro ||
        !estado ||
        !cidade ||
        !logradouro ||
        !senha ||
        !confirmarSenha
    ) {

        alert(
            'Preencha todos os campos obrigatórios!'
        );

        return false;
    }

    if (senha !== confirmarSenha) {

        alert(
            'As senhas não conferem'
        );

        return false;
    }

    if (senha.length < 6) {

        alert(
            'A senha deve ter no mínimo 6 caracteres'
        );

        return false;
    }

    return true;
}

/**
 * Realiza o cadastro do usuário.
 */
async function cadastrarUsuario() {

    const dadosUsuario =
        obterDadosCadastroUsuario();

    if (
        !validarCadastroUsuario(
            dadosUsuario
        )
    ) {
        return;
    }

    try {

        const response = await fetch(
            `${API_BASE_URL}/cadastro_usuario`,
            {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/json'
                },
                body: JSON.stringify({
                    nome_completo:
                        dadosUsuario.nome_completo,

                    senha:
                        dadosUsuario.senha,

                    email:
                        dadosUsuario.email,

                    numero_telefone:
                        dadosUsuario.numero_telefone,

                    cep:
                        dadosUsuario.cep,

                    estado:
                        dadosUsuario.estado,

                    cidade:
                        dadosUsuario.cidade,

                    bairro:
                        dadosUsuario.bairro,

                    logradouro:
                        dadosUsuario.logradouro
                })
            }
        );

        if (response.ok) {

            alert(
                'Usuário cadastrado com sucesso'
            );

            renderizarPagina('login');

            return;
        }

        const erro = await response.json();

        alert(
            `❌ Erro ao cadastrar: ${
                erro.detail || 'Erro desconhecido'
            }`
        );

    } catch (error) {

        console.error(error);

        alert(
            `❌ Erro ao conectar com o servidor: ${error.message}`
        );
    }
}