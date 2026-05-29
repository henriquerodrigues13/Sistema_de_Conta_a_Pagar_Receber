function paginaCadastroProduto(){
    return`
        <div id="container-cadastroProdutos">
      <div class="logo">
        <img
          src="./assets/imgs/logo/logo.png"
          alt="Logo"
        />
      </div>
 
      <h1>Cadastro de Produtos</h1>
 
      <form id="form-cadastroProduto">
        <div class="campo">
          <label>Nome do produto <span style="color: red;">*</span></label>
          <input 
            type="text" 
            placeholder="Digite o nome" 
            id="nome-produto"
            maxlength="100"
            required
          />
        </div>
 
        <div class="campo">
          <label>Categoria <span style="color: red;">*</span></label>
          <select id="categoria-produto" required>
            <option value="" disabled selected>Selecione uma categoria</option>
            <option value="informatica">Informática</option>
            <option value="eletronicos">Eletrônicos</option>
            <option value="papelaria">Papelaria</option>
            <option value="limpeza">Limpeza</option>
            <option value="cosmeticos">Cosméticos</option>
            <option value="alimentos">Alimentos</option>
            <option value="bebidas">Bebidas</option>
            <option value="construcao">Construção</option>
            <option value="roupas">Roupas</option>
            <option value="moveis">Móveis</option>
            <option value="medicamentos">Medicamentos</option>
            <option value="automotivo">Automotivo</option>
            <option value="outros">Outros</option>
          </select>
        </div>
 
        <div class="campo">
          <label>Unidade de medida <span style="color: red;">*</span></label>
          <input 
            type="text" 
            placeholder="Ex: kg, l, unidade, etc" 
            id="unidade-produto"
            maxlength="20"
            required
          />
        </div>
 
        <div class="campo">
          <label>Quantidade em estoque <span style="color: red;">*</span></label>
          <input 
            type="number" 
            placeholder="Digite a quantidade" 
            id="quantidade-produto"
            min="1"
            step="1"
            required
          />
          <small style="color: #999;">Mínimo: 1</small>
        </div>
 
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
          <div class="campo">
            <label>Valor de custo <span style="color: red;">*</span></label>
            <input 
              type="text" 
              placeholder="0,00" 
              id="valorCusto-produto"
              pattern="[0-9]+([,\.][0-9]{1,2})?"
              required
              class="input-valor"
            />
            <small style="color: #999;">Ex: 10,50 ou 10.50</small>
          </div>
 
          <div class="campo">
            <label>Valor de venda <span style="color: red;">*</span></label>
            <input 
              type="text" 
              placeholder="0,00" 
              id="valorVenda-produto"
              pattern="[0-9]+([,\.][0-9]{1,2})?"
              required
              class="input-valor"
            />
            <small style="color: #999;">Ex: 15,50 ou 15.50</small>
          </div>
        </div>
 
        <div class="campo">
          <label>Descrição <span style="color: red;">*</span></label>
          <textarea 
            placeholder="Descrição do produto (mínimo 10 caracteres)" 
            id="descricao-produto"
            minlength="10"
            maxlength="500"
            rows="4"
            required
          ></textarea>
          <small style="color: #999;">Caracteres: <span id="char-count">0</span>/500</small>
        </div>
 
        <div class="campo">
          <label>Status</label>
          <select id="status-produto">
            <option value="ativo">Ativo</option>
            <option value="inativo">Inativo</option>
          </select>
        </div>
 
        <div id="erro-validacao" style="
          display: none;
          background-color: #ffe6e6;
          color: #c0392b;
          padding: 10px;
          border-radius: 5px;
          margin-bottom: 15px;
          border-left: 4px solid #c0392b;
        "></div>
 
        <div class="botoes">
          <button type="button" id="btn-cadastrarProduto" onclick="cadastrarProduto()" >Cadastrar</button>
          <button type="button" id="voltar-telaProdutoServico" style="cursor: pointer;" onclick="renderizarPagina('usuarioLayout')">Voltar</button>
        </div>
      </form>
    </div>
    `
}