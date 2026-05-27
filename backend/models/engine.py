from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Integer, String, Float, ForeignKey, Boolean
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from uuid import uuid4, UUID


class Base(DeclarativeBase):
    pass

class usuarios(Base):
    __tablename__ = 'usuarios'

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

    produtos_do_usuario : Mapped[list['produtos']] = relationship(
        back_populates='usuario_produtos',
        foreign_keys="[produtos.proprietario_usuario]"
    )

class cadastro_usuario(BaseModel):
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

class fornecedores(Base):
    __tablename__ = 'fornecedores'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cnpj: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    nome_oficial_empresa: Mapped[str] = mapped_column(String(150), index=True)
    nome_cormecial_empresa: Mapped[str | None] = mapped_column(String(150))
    situacao_cadastral: Mapped[str] = mapped_column(String(20))
    data_abertura: Mapped[str] = mapped_column(String(20))
    natureza_juridica: Mapped[str] = mapped_column(String(150))
    cnae: Mapped[str] = mapped_column(String(150)) # Atividade econômica
    capital_social: Mapped[float] = mapped_column(Float)
    porte_empresa: Mapped[str] = mapped_column(String(150))
    cep: Mapped[str] = mapped_column(String(20))
    uf: Mapped[str] = mapped_column(String(20))
    cidade: Mapped[str] = mapped_column(String(100))
    bairro: Mapped[str] = mapped_column(String(100))
    logradouro: Mapped[str] = mapped_column(String(100))

    produtos_do_fornecedor: Mapped[list['produtos']] = relationship(
        back_populates='fornecedor_produtos',
        foreign_keys="[produtos.proprietario_fornecedor]"
    )

class reponse_fornecedor(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cnpj: str
    nome_oficial_empresa: str

class produtos(Base):
    __tablename__ = 'produtos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid_produto: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, unique=True)
    nome_do_produto: Mapped[str] = mapped_column(String(100), index=True)
    proprietario_fornecedor: Mapped[str | None] = mapped_column(String(100), ForeignKey('fornecedores.cnpj'), index= True)
    proprietario_usuario: Mapped[str | None] = mapped_column(String(100), ForeignKey('usuarios.email'), index= True)
    unidade_de_medida: Mapped[str | None] = mapped_column(String(50))
    quantidade_em_estoque: Mapped[int] = mapped_column(Integer)
    categoria_do_produto: Mapped[str] = mapped_column(String(100))
    valor_de_custo: Mapped[float] = mapped_column(Float)
    valor_final: Mapped[float] = mapped_column(Float)
    descricao_do_produto: Mapped[str | None] = mapped_column(String(500))
    status_do_produto: Mapped[str] = mapped_column(String(100), default= 'disponível')
    produto_deletado: Mapped[bool] = mapped_column(Boolean, default= False)

    usuario_produtos : Mapped['usuarios'] = relationship(
        back_populates='produtos_do_usuario',
        foreign_keys=[proprietario_usuario]
    )

    fornecedor_produtos : Mapped['fornecedores'] = relationship(
        back_populates= 'produtos_do_fornecedor',
        foreign_keys=[proprietario_fornecedor]
    )

class request_produtos(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome_do_produto: str
    proprietario_usuario :EmailStr
    unidade_de_medida : str | None
    quantidade_em_estoque : int
    categoria_do_produto: str
    valor_de_custo : float
    valor_final : float
    descricao_do_produto: str | None

class reponse_produtos_usuario(request_produtos):
    model_config = ConfigDict(from_attributes=True)
    status_do_produto: str

class reponse_produtos_fornecedor(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome_do_produto: str
    proprietario_fornecedor: str
    unidade_de_medida: str | None
    quantidade_em_estoque: int
    categoria_do_produto: str
    valor_de_custo: float
    valor_final: float
    descricao_do_produto: str | None
    status_do_produto: str

class delete_produto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nome_do_produto: str
    proprietario_fornecedor: EmailStr

'''class servicos(Base):
    __tablename__ = 'servicos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, unique=True)
    nome_do_servic: Mapped[str] = mapped_column(String(100), index=True)
    prestador_do_servico_usuario: Mapped[str | None] = mapped_column(String(100), ForeignKey('fornecedor.cnpj'), index=True)
    prestador_do_servico_fornecedor: Mapped[str | None] = mapped_column(String(100), ForeignKey('fornecedor.cnpj'),index=True)
    descricao_do_servico: Mapped[str | None] = mapped_column(String(500))
    valor_do_servico: Mapped[float] = mapped_column(Float)
    categoria_do_servico: Mapped[str] = mapped_column(String(100))
    servico_deletado: Mapped[bool] = mapped_column(Boolean)

    usuario_servico : Mapped['usuarios'] = relationship(
        back_populates='servicos_do_usuario',
        foreign_keys=[prestador_do_servico_usuario]
    )

class (BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cpf_cnpj_vendendor: str
    cpf_cnpj_comprador: str
    forma_pagamento: str
    valor_venda: float
    porcentagem_desconto: float


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
