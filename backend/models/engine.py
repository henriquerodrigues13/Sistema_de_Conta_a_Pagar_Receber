from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Integer, String, Float, ForeignKey
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from uuid import uuid4, UUID


class Base(DeclarativeBase):
    pass

class usuario(Base):
    __tablename__ = 'usuario'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_completo: Mapped[str] = mapped_column(String(150))
    senha: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    numero_telefone: Mapped[str] = mapped_column(String(11))
    cep: Mapped[str] = mapped_column(String(30))
    estado: Mapped[str] = mapped_column(String(30))
    cidade: Mapped[str] = mapped_column(String(100))
    bairro: Mapped[str] = mapped_column(String(100))
    logradouro: Mapped[str] = mapped_column(String(100))

<<<<<<< Updated upstream
class cadastro_usuario(BaseModel):
=======
    produtos_cliente: Mapped[list['produto_servico']] = relationship(back_populates='vendedor_cpf')

    vendas_cliente: Mapped[list['vendas']] = relationship(back_populates='vendas_cpf', foreign_keys='vendas.cpf_vendendor')
    compras_cliente: Mapped[list['vendas']] = relationship(back_populates='compras_cpf', foreign_keys='vendas.cpf_comprador')

    pagamento_cliente: Mapped[list['despesas']] = relationship(back_populates='pagado_cliente', foreign_keys='despesas.pagado_cliente')
    recebedor_cliente: Mapped[list['despesas']] = relationship(back_populates='recebedor_cliente', foreign_keys='despesas.recebedor_cliente')

class clientePOST(BaseModel):
>>>>>>> Stashed changes
    model_config = ConfigDict(from_attributes=True)
    nome_completo: str
    senha: str
    email: EmailStr
    numero_telefone: str
    cep: str
    estado: str
    cidade: str
    bairro: str
    logradouro: str

class login_usuario(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email : EmailStr
    senha : str

class reponsa_usuario(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome_completo: str

'''class produto_servico(Base):
    __tablename__ = 'produto_servico'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
<<<<<<< Updated upstream
=======
    cnpj: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    senha: Mapped[str] = mapped_column(String(150), index=True)
    nome_oficial_empresa: Mapped[str] = mapped_column(String(150))
    nome_cormecial_empresa: Mapped[str] = mapped_column(String(150))
    situacao_cadastral: Mapped[str] = mapped_column(String(20))
    data_abertura: Mapped[str] = mapped_column(String(20))
    natureza_juridica: Mapped[str] = mapped_column(String(150))
    cnae: Mapped[str] = mapped_column(String(150)) # Atividade econômica
    capital_social: Mapped[float] = mapped_column(Float)
    porte_empresa: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(100))
    numero_telefone_empresa: Mapped[str] = mapped_column(String(11))
    cep: Mapped[str] = mapped_column(String(20))
    uf: Mapped[str] = mapped_column(String(2))
    cidade: Mapped[str] = mapped_column(String(100))
    bairro: Mapped[str] = mapped_column(String(100))
    logradouro: Mapped[str] = mapped_column(String(100))

    produtos_fornecedor: Mapped[list['produto_servico']] = relationship(back_populates='vendedor_cnpj')

    vendas_fornecedor: Mapped[list['vendas']] = relationship(back_populates='vendas_cnpj', foreign_keys='vendas.cnpj_vendendor')
    compras_fornecedor: Mapped[list['vendas']] = relationship(back_populates='compras_cnpj', foreign_keys='vendas.cnpj_comprador'



class fornecedorREQUEST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome_oficial_empresa: str
    cnpj: str
    senha: str
    email: str
    numero_telefone_empresa: str


class fornecedorPOST(BaseModel):  # class despesasPOST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cnpj: str
    senha: str
    nome_oficial_empresa: str
    nome_cormecial_empresa: str
    situacao_cadastral: str
    data_abertura: datetime
    natureza_juridica: str
    cnae: str
    capital_social: float
    porte_empresa: str
    email: str
    numero_telefone_empresa: str
    cep: str
    uf: str
    cidade: str
    bairro: str
    logradouro: str


class fornecedorLOGIN(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cnpj: str
    senha: str

class fornecedorResponde(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome_oficial_empresa: str

class produto_servico(Base):
    __tablename__ = 'produto_servico_cliente'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
>>>>>>> Stashed changes
    produto_servico_uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, unique=True)
    classificacao_produto_servico: Mapped[str] = mapped_column(String(50))
    nome_produto_servico: Mapped[str] = mapped_column(String(150), index=True)
    cpf_vendendor: Mapped[str | None] = mapped_column(String(100), ForeignKey('cliente.cpf'), index=True)
    cnpj_vendendor: Mapped[str | None] = mapped_column(String(100), ForeignKey('fornecedor.cnpj'), index=True)
    detalhes: Mapped[str] = mapped_column(String(150), index=True)
    data_do_cadastro: Mapped[str] = mapped_column(String(30))
    valor_custo: Mapped[float] = mapped_column(Float)
    ICMS: Mapped[str] = mapped_column(String(150))
    valor_com_IMCS: Mapped[float] = mapped_column(Float)
    valor_final_de_venda: Mapped[float] = mapped_column(Float)
    margem_de_lucro: Mapped[float] = mapped_column(Float)

    vendedor_cpf: Mapped['cliente | None'] = relationship(back_populates="produtos_cliente")
    vendedor_cnpj: Mapped['fornecedor | None'] = relationship(back_populates="produtos_fornecedor")

class produto_servico_REQUEST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
<<<<<<< Updated upstream
    cpf_cnpj : str
    classificacao_produto_servico: str
    identidicado_produto_servico: str
    detalhes_produto_servico: str
=======
    cpf_vendendor : str | None = None
    cnpj_vendendor : str | None = None
    classificacao: str
    nome: str
    detalhes: str
>>>>>>> Stashed changes
    valor_custo_de_venda: float
    valor_final_de_venda: float

class produto_servico_Response(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome_produto_servico: str
    classificacao_produto_servico: str
    detalhes: str
    data_do_cadastro: str
    valor_custo: float
    ICMS: str
    valor_com_IMCS: float
    valor_final_de_venda: float
    margem_de_lucro: float


class vendas(Base):
<<<<<<< Updated upstream
    __tablename__ = 'vendas'
=======
    __tablename__ = 'vendas_cliente'
>>>>>>> Stashed changes

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, unique=True)
    cpf_vendendor: Mapped[str | None] = mapped_column(String(100), ForeignKey('cliente.cpf'), index=True)
    cnpj_vendendor: Mapped[str | None] = mapped_column(String(100), ForeignKey('fornecedor.cnpj'), index=True)
    cpf_comprador: Mapped[str | None] = mapped_column(String(100), ForeignKey('cliente.cpf'), index=True)
    cnpj_comprador: Mapped[str | None] = mapped_column(String(100), ForeignKey('fornecedor.cnpj'), index=True)
    forma_pagamento: Mapped[str] = mapped_column(String(50))
    valor_venda: Mapped[float] = mapped_column(Float)
    porcentagem_desconto: Mapped[float] = mapped_column(Float, default=0.0)
    valor_final_venda: Mapped[float] = mapped_column(Float)

    vendas_cpf: Mapped['cliente | None'] = relationship(back_populates='vendas_cliente', foreign_keys=[cpf_vendendor])
    vendas_cnpj: Mapped['fornecedor | None'] = relationship(back_populates='vendas_fornecedor', foreign_keys=[cnpj_vendendor])
    compras_cpf: Mapped['cliente | None'] = relationship(back_populates='compras_cliente', foreign_keys=[cpf_comprador])
    compras_cnpj: Mapped['fornecedor | None'] = relationship(back_populates='compras_fornecedor', foreign_keys=[cnpj_comprador])

class vendas_REQUEST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cpf_cnpj_vendendor: str
    cpf_cnpj_comprador: str
    forma_pagamento: str
    valor_venda: float
    porcentagem_desconto: float
<<<<<<< Updated upstream
=======
    valor_final_venda: float
>>>>>>> Stashed changes

class vendas_RESPONSE(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    forma_pagamento: str
    valor_venda: float
    porcentagem_desconto: float
    valor_final_venda: float

class despesas(Base):
    __tablename__ = 'despesas'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, unique=True)
    cpf_pagado: Mapped[str | None] = mapped_column(String(100),ForeignKey('cliente.cpf'), index=True)
    cnpj_pagado: Mapped[str | None] = mapped_column(String(100), ForeignKey('fornecedor.cnpj'), index=True)
    cpf_recebedor: Mapped[str | None] = mapped_column(String(100), ForeignKey('cliente.cpf'), index=True)
    cnpj_recebedor: Mapped[str | None ] = mapped_column(String(100), ForeignKey('fornecedor.cnpj'), index=True)
    valor_despesas: Mapped[float] = mapped_column(Float)
    data_evento: Mapped[str]= mapped_column(String(30))
    tipo_de_despesa: Mapped[str] = mapped_column(String)

    pagado_cliente: Mapped['cliente | None'] = relationship(back_populates='pagamento_de_despesas_cliente', foreign_keys=[cpf_pagado])
    pagado_fornecedor: Mapped['fornecedor | None'] = relationship(back_populates='pagamento_de_despesas_fornecedor', foreign_keys=[cnpj_pagado])
    recebedo_cliente: Mapped['cliente | None'] = relationship(back_populates='recebemento_de_despesas_cliente', foreign_keys=[cpf_recebedor])
    recebedo_fornecedor: Mapped['fornecedor | None'] = relationship(back_populates='recebemento_de_despesas_fornecedor', foreign_keys=[cnpj_recebedor])

    pagado_cliente: Mapped['cliente'] = relationship(back_populates='pagamento_cliente', foreign_keys=[cpf_pagado])
    pagado_fornecedor: Mapped['fornecedor'] = relationship(back_populates='pagamento_fornecedor', foreign_keys=[cnpj_pagado])
    recebedor_cliente: Mapped['cliente'] = relationship(back_populates='recebedor_cliente', foreign_keys=[cpf_recebedor])
    recebedor_fornecedor: Mapped['fornecedor'] = relationship(back_populates='recebedor_fornecedor', foreign_keys=[cnpj_pagado])

class despesasRESQUEST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cpf_cnpj_pagador: str
    cpf_cnpj_recebedor: str
    tipo_de_despesa: str
    valor_despesas: float
    data_evento: str

<<<<<<< Updated upstream
class despesasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    tipo_de_despesa: str
    valor_despesas: float
    data_evento: str

class receita(Base):
    __tablename__ = 'receitas'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, unique=True)
    cpf_recebedor: Mapped[str | None] = mapped_column(String(100), ForeignKey('cliente.cpf'), index=True)
    cnpj_recebedor: Mapped[str | None] = mapped_column(String(100), ForeignKey('fornecedor.cnpj'), index=True)
=======
class despesasRESQUEST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cpf_cnpj_pagador: str
    cpf_cnpj_recebedor: str
    tipo_de_despesas: str
    valor_despesas: float
    data_evento: str

class despesasResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    tipo_de_despesas: str
    valor_despesas: float
    data_evento: float

class receitas(Base):
    _tablename_ = 'receitas_cliente'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, unique=True)
    cpf_recebedor: Mapped[str] = mapped_column(String(100), ForeignKey('cliente.cpf'), index=True)
>>>>>>> Stashed changes
    cpf_pagador: Mapped[str | None] = mapped_column(String(100), ForeignKey('cliente.cpf'), index=True)
    cnpj_pagador: Mapped[str | None] = mapped_column(String(100), ForeignKey('fornecedor.cnpj'), index=True)
    valor_receita: Mapped[float] = mapped_column(Float)
    data_evento_receita: Mapped[str] = mapped_column(String(30))
    origem_receita: Mapped[str] = mapped_column(String)

<<<<<<< Updated upstream
    recebedor_cliente: Mapped['cliente | None'] = relationship(back_populates='recebedor_de_receita_cliente', foreign_keys=[cpf_recebedor])
    recebedor_fornecedor: Mapped['fornecedor | None'] = relationship(back_populates='recebedor_de_receita_fornecedor', foreign_keys=[cnpj_recebedor])
    pagador_cliente: Mapped['cliente | None'] = relationship(back_populates='pagador_de_receita_cliente', foreign_keys=[cpf_pagador])
    pagador_fornecedor: Mapped['fornecedor | None'] = relationship(back_populates='pagador_de_receita_fornecedor', foreign_keys=[cnpj_pagador])

class receitas_REQUEST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cpf_cnpj_recebedor: str
    cpf_cnpj_pagado: str
=======
class receitas_REQUEST(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cpf_recebedor: str
    cpf_pagador: str
    cnpj_pagador: str
>>>>>>> Stashed changes
    valor_receita: float
    data_evento_receita: str
    origem_receita: str

class receitas_RESPONSE(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    valor_receita: float
    data_evento_receita: str
<<<<<<< Updated upstream
    origem_receita: str

class dados_gerador_relatorio(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cpf_cnpj_recebedor: str
    tipo_do_documento: str'''
=======
    origem_receita: str
>>>>>>> Stashed changes
