from fastapi import APIRouter, Depends, HTTPException, Query, Response, BackgroundTasks
from backend.models.banco_dados_inicia import cria_sessao_banco_de_dados
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from backend.API.emitir_NFe import emitir_NotaFiscal
from build.lib.backend.logs import setup_logger
from starlette.responses import JSONResponse
from sqlalchemy import select, func, update
from backend.API.criptografia import *
from backend.API.validações import *
from backend.models.tabelas import *
from sqlalchemy.orm import Session
from backend.API.gerador import *
from typing import Annotated


BRASILIA = timezone(timedelta(hours=-3))

logger = setup_logger('rotas')

conf = ConnectionConfig(
    MAIL_USERNAME="henriquefnaf2680@gmail.com",
    MAIL_PASSWORD="tuqq rxpr rxyy jome",
    MAIL_FROM="henriquefnaf2680@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

fast_mail = FastMail(conf)

router = APIRouter(tags=["cadastro e login"])
SessionDep = Annotated[Session, Depends(cria_sessao_banco_de_dados)]

def model_to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

def formatar_brl(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return str(v)


@router.post(path='/login', response_model=reponsa_usuario,
             responses={404: {'description': 'Usuario nao encontrado'},
                        401: {'description': 'Senha incorreta'}})
async def login(usuario_login: login_usuario, session: SessionDep) -> reponsa_usuario:

    if (usuario_existe := session.execute(
        select(usuarios).where(usuarios.email == usuario_login.email)
    ).scalar_one_or_none()):
        if verificar_senha(senha=usuario_login.senha, hash_salvo=usuario_existe.senha):
            logger.info(f'O usuario {usuario_existe.nome_completo} com o email {usuario_existe.email} entrou no sistema')
            return reponsa_usuario.model_validate(usuario_existe)
        raise HTTPException(status_code=401, detail="Senha incorreta")
    raise HTTPException(status_code=404, detail='Usuario nao encontrado')

@router.post('/cadastro_usuario', response_model=reponsa_usuario,
             responses={409: {'description': 'Usuario ja existe'},
                        401: {'description': 'Email invalido'}})
async def cadastro_usuario(cadastro_do_usuario: cadastro_usuario, session: SessionDep) -> HTTPException | reponsa_usuario:
    if not (isEmail_valido:=validacao_email(email=cadastro_do_usuario.email)):
        raise HTTPException(status_code=401, detail='Email invalido')

    if (usuario_ja_existe := session.execute(
            select(usuarios).where(usuarios.email == cadastro_do_usuario.email))
            .scalar_one_or_none()):
        raise HTTPException(status_code=409, detail='Usuario ja existe')
    senha_HASH = senha_hash(senha=cadastro_do_usuario.senha)

    novo_usuario = usuarios(
        nome_completo = cadastro_do_usuario.nome_completo,
        senha = senha_HASH,
        email = cadastro_do_usuario.email,
        numero_telefone = cadastro_do_usuario.numero_telefone,
        cep = cadastro_do_usuario.cep,
        estado = cadastro_do_usuario.estado,
        cidade = cadastro_do_usuario.cidade,
        bairro = cadastro_do_usuario.bairro,
        logradouro = cadastro_do_usuario.logradouro,
    )

    session.add(novo_usuario)
    session.commit()
    session.refresh(novo_usuario)

    logger.info(f'O usuario {cadastro_do_usuario.nome_completo} com o email {cadastro_do_usuario.email} se cadastrou no sistema')
    return reponsa_usuario.model_validate(novo_usuario)

@router.post('/recuperacao_senha', response_model=request_recuperacao_senha)
async def recuperacao_senha(usuario: request_recuperacao_senha,
                            session: SessionDep,
                            background_tasks: BackgroundTasks) -> HTTPException | JSONResponse:
    if usuario_existe := session.execute(select(usuarios).where(usuarios.email == usuario.email)).scalar_one_or_none():

        usuario = usuario_existe

        token = gerador_de_token()
        usuario.token_reset_senha = token
        usuario.expiracao_do_token = limite_de_expiracao_token()

        session.commit()
        session.refresh(usuario)

        message = MessageSchema(
            subject="Recuperação de senha",
            recipients = [usuario.email],
            body=f"Seu token: {token}",
            subtype="plain"
        )

        background_tasks.add_task(fast_mail.send_message, message)

        logger.info(f'O email {usuario.email} pediu para recupera senha')
        return JSONResponse(status_code=201, content={'message': 'Email para recuperação de senha, enviado'})
    raise HTTPException(status_code=404, detail='Usuario não encontrado')

@router.post('/reset_senha', response_model=request_reset_senha)
async def recuperacao_senha(reset: request_reset_senha,
                            session: SessionDep) -> HTTPException | JSONResponse:

    if usuario := session.execute(select(usuarios).where(usuarios.token_reset_senha == reset.token)).scalar_one_or_none():
        if usuario.expiracao_do_token.replace(tzinfo=BRASILIA) > datetime.now(BRASILIA):
            session.execute(update(usuarios).where(usuarios.token_reset_senha == reset.token).
                            values(senha=senha_hash(reset.senha)))
            session.commit()
            logger.info(f'O usuario de email {usuario.email} alterou a sua senha')
            return JSONResponse(status_code=200, content={'message': 'Senha atualizada'})
        raise HTTPException(status_code=400, detail='Token expirado')
    raise HTTPException(status_code=404, detail='Token não encontrado')

@router.post('/cadastro_produtos', response_model=request_produtos,
             responses={404: {'description': 'Usuario nao existe'},
                        409: {'description': 'produto ja existe'}})
async def cadastro_produtos(cadastro_produto: request_produtos,
                            session: SessionDep
                            ) -> JSONResponse | HTTPException:
    if not (email_nao_existe := session.execute(
            select(usuarios).where(usuarios.email == cadastro_produto.proprietario_usuario))
            .scalar_one_or_none()):
        raise HTTPException(status_code=404, detail='Usuario nao existe')

    if (produto_ja_existe := session.execute(
            select(produtos).where(produtos.proprietario_usuario == cadastro_produto.proprietario_usuario,
                                   produtos.nome_do_produto == cadastro_produto.nome_do_produto ))
            .scalar_one_or_none()):
        raise HTTPException(status_code=409, detail='produto ja existe')

    novo_produto = produtos(
        nome_do_produto = cadastro_produto.nome_do_produto,
        proprietario_usuario =  cadastro_produto.proprietario_usuario,
        unidade_de_medida = cadastro_produto.unidade_de_medida,
        quantidade_em_estoque = cadastro_produto.quantidade_em_estoque,
        categoria_do_produto = cadastro_produto.categoria_do_produto,
        valor_de_custo = cadastro_produto.valor_de_custo,
        valor_final = cadastro_produto.valor_final,
        descricao_do_produto = cadastro_produto.descricao_do_produto,
    )

    session.add(novo_produto)
    session.commit()
    session.refresh(novo_produto)

    logger.info(
        f'O usuario com o email {cadastro_produto.proprietario_usuario} cadastrou o produto {cadastro_produto.nome_do_produto} no sistema')
    return JSONResponse(content={'mensagem' : f'O produto {cadastro_produto.nome_do_produto} com sucesso'},
                        media_type= 'text/plain')

@router.get('/get_produtos_usuario/{usuario_email}', response_model=list[reponse_produtos_usuario])
async def get_produtos_usuario(
        usuario_email: EmailStr,
        session: SessionDep,
        response: Response,
        page: int = Query(1, ge= 1),
        ) -> list[reponse_produtos_usuario]:

    pages_size = 10

    total = session.scalar(
        select(func.count())
        .select_from(produtos)
        .where(produtos.proprietario_usuario == usuario_email))

    total_pages = (total + pages_size - 1) // pages_size

    if page > total_pages and total_pages > 0:
        page = total_pages

    offset = (page - 1) * pages_size

    response.headers["X-Total-Pages"] = str(total_pages)
    response.headers["X-Total-Items"] = str(total)

    produtos_reponse = session.execute(
        select(produtos)
        .where(produtos.proprietario_usuario == usuario_email)
        .limit(pages_size)
        .offset(offset)
    ).scalars().all()

    logger.info(
        f'O usuario com o email {usuario_email} requisitou um get dos seu produtos')
    return [reponse_produtos_usuario.model_validate(produto) for produto in produtos_reponse]

@router.patch("/update_produto/{usuario_email}/{nome_do_produto}", response_model=patch_produto,
              responses={404: {"description": "produto não encontrado."},
                         400: {"description": "Nenhum dado válido enviado para atualização."}})
async def atualizar_produto(usuario_email: EmailStr, nome_do_produto: str,
                            produto_update: patch_produto, session: SessionDep) -> JSONResponse:
    update_data = produto_update.model_dump(exclude_unset=True, exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado válido enviado para atualização.")

    if produto := session.scalar(select(produtos).where(produtos.proprietario_usuario == usuario_email,
                                                    produtos.nome_do_produto == nome_do_produto)):
        for key, value in update_data.items():
            setattr(produto, key, value)

        session.commit()

        logger.info(
            f'O usuario com o email {usuario_email} alterou o produto {produto.nome_do_produto} no sistema')
        return JSONResponse(content={'mensagem' : f'o produto: {nome_do_produto} foi atualizado'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="Produto não encontrado.")

@router.delete("/delete_produto/{usuario_email}/{nome_do_produto}", response_model=delete_produto,
               responses={404: {"description": "Produto não encontrado."}})
async def deletar_produto(usuario_email: EmailStr,
                          nome_do_produto: str,
                          session: SessionDep) -> JSONResponse | HTTPException:
    if produto := (session.execute(select(produtos).where(produtos.proprietario_usuario == usuario_email,
                                                          produtos.nome_do_produto == nome_do_produto))).scalar_one_or_none():
        session.delete(produto)
        session.commit()
        logger.info(f'O usuario com o email {usuario_email} deletou o produto {produto.nome_do_produto} no sistema')
        return JSONResponse(content={'mensagem' : f'o produto {nome_do_produto} foi deletado'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="Produto não encontrado.")

@router.get('/get_fornecedor', response_model=list[reponse_fornecedor])
async def get_fornecedor(
        session: SessionDep,
        response: Response,
        page: int = Query(1, ge= 1),
        ) -> list[reponse_fornecedor]:

    pages_size = 10

    total_fornecedores = session.scalar(select(func.count()).select_from(fornecedores))

    total_pages = (total_fornecedores + pages_size - 1) // pages_size

    if page > total_pages and total_pages > 0:
        page = total_pages

    offset = (page - 1) * pages_size

    response.headers["X-Total-Pages"] = str(total_pages)
    response.headers["X-Total-Items"] = str(total_fornecedores)

    fornecedores_reponse = session.execute(
        select(fornecedores).limit(pages_size).offset(offset)
    ).scalars().all()

    return [reponse_fornecedor.model_validate(forncedor) for forncedor in fornecedores_reponse]

@router.get('/get_produtos_fornecedor/{cnpj}', response_model=list[reponse_produtos_fornecedor])
async def get_produtos_fornecedor(
        fornecedor_cnpj: str,
        session: SessionDep,
        response: Response,
        page: int = Query(1, ge= 1),
        ) -> list[reponse_produtos_fornecedor]:

    pages_size = 10

    total = session.scalar(
        select(func.count())
        .select_from(produtos)
        .where(produtos.proprietario_fornecedor == fornecedor_cnpj))

    total_pages = (total + pages_size - 1) // pages_size

    if page > total_pages and total_pages > 0:
        page = total_pages

    offset = (page - 1) * pages_size

    response.headers["X-Total-Pages"] = str(total_pages)
    response.headers["X-Total-Items"] = str(total)

    produtos_reponse = session.execute(
        select(produtos)
        .where(produtos.proprietario_fornecedor == fornecedor_cnpj)
        .limit(pages_size)
        .offset(offset)
    ).scalars().all()

    return [reponse_produtos_fornecedor.model_validate(produto) for produto in produtos_reponse]

@router.post('/cadastro_servico', response_model=request_servico,
             responses={404: {'description': 'Usuario nao existe'},
                        409: {'description': 'serviço ja existe'}})
async def cadastro_servico(cadastro_do_servico: request_servico,
                            session: SessionDep
                            ) -> JSONResponse | HTTPException:
    if not (email_nao_existe := session.execute(
            select(usuarios).where(usuarios.email == cadastro_do_servico.prestador_do_servico_usuario))
            .scalar_one_or_none()):
        raise HTTPException(status_code=404, detail='Usuario nao existe')

    if (produto_ja_existe := session.execute(
            select(servicos).where(servicos.prestador_do_servico_usuario == cadastro_do_servico.prestador_do_servico_usuario,
                                   servicos.nome_do_servico == cadastro_do_servico.nome_do_servico))
            .scalar_one_or_none()):
        raise HTTPException(status_code=409, detail='serviço ja existe')

    novo_servico = servicos(
        nome_do_servico = cadastro_do_servico.nome_do_servico,
        prestador_do_servico_usuario = cadastro_do_servico.prestador_do_servico_usuario,
        descricao_do_servico = cadastro_do_servico.descricao_do_servico,
        valor_do_servico = cadastro_do_servico.valor_do_servico,
        categoria_do_servico = cadastro_do_servico.categoria_do_servico
    )

    session.add(novo_servico)
    session.commit()
    session.refresh(novo_servico)

    logger.info(
        f'O usuario com o email {email_nao_existe.email} cadastrou o serviço {cadastro_do_servico.nome_do_servico} no sistema')
    return JSONResponse(content={'mensagem' : f'O servico: {cadastro_do_servico.nome_do_servico} foi cadastro com sucesso'},
                        media_type= 'text/plain')

@router.get('/get_servico_usuario/{usuario_email}', response_model=list[reponse_servicos])
async def get_servico_usuario(
        usuario_email: EmailStr,
        session: SessionDep,
        response: Response,
        page: int = Query(1, ge= 1),
        ) -> list[reponse_servicos]:

    pages_size = 10

    total = session.scalar(
        select(func.count())
        .select_from(servicos)
        .where(servicos.prestador_do_servico_usuario == usuario_email))

    total_pages = (total + pages_size - 1) // pages_size

    if page > total_pages and total_pages > 0:
        page = total_pages

    offset = (page - 1) * pages_size

    response.headers["X-Total-Pages"] = str(total_pages)
    response.headers["X-Total-Items"] = str(total)

    servico_reponse = session.execute(
        select(servicos)
        .where(servicos.prestador_do_servico_usuario == usuario_email)
        .limit(pages_size)
        .offset(offset)
    ).scalars().all()

    logger.info(
        f'O usuario com o email {usuario_email} requisitou uma vizualização dos serviços no sistema')
    return [reponse_servicos.model_validate(servico) for servico in servico_reponse]

@router.patch("/update_servico/{usuario_email}/{nome_do_servico}", response_model=patch_servico,
              responses={404: {"description": "serviço não encontrado."},
                         400: {"description": "Nenhum dado válido enviado para atualização."}})
async def atualizar_servico(usuario_email: EmailStr, nome_do_servico: str,
                            servico_update: patch_servico, session: SessionDep) -> JSONResponse:
    update_data = servico_update.model_dump(exclude_unset=True, exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado válido enviado para atualização.")

    if servico := session.execute(select(servicos).where(servicos.prestador_do_servico_usuario == usuario_email,
                                                    servicos.nome_do_servico == nome_do_servico)).scalar_one_or_none():
        for key, value in update_data.items():
            setattr(servico, key, value)

        session.commit()
        session.refresh(servico)
        logger.info(
            f'O usuario com o email {usuario_email} atualizou o serviço {nome_do_servico} no sistema')
        return JSONResponse(content={'mensagem' : f'o servico : {nome_do_servico} foi atualizado'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="Serviço não encontrado.")

@router.delete("/delete_servico/{usuario_email}/{nome_do_servico}", response_model=delete_servico,
               responses={404: {"description": "Serviço não encontrado."}})
async def deletar_servico(usuario_email: EmailStr,
                          nome_do_servico: str,
                          session: SessionDep) -> JSONResponse | HTTPException:
    if servico := (session.execute(select(servicos).where(servicos.prestador_do_servico_usuario == usuario_email,
                                                          servicos.nome_do_servico == nome_do_servico))).scalar_one_or_none():

        session.delete(servico)
        session.commit()

        logger.info(
            f'O usuario com o email {usuario_email} deletou o serviço {nome_do_servico} no sistema')
        return JSONResponse(content={'mensagem' : f'o servico: {nome_do_servico} foi deletado'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="Serviço não encontrado.")

@router.get('/get_servicos_fornecedor/{cnpj}', response_model=list[reponse_servicos_fornecedor])
async def get_servicos_fornecedor(
        fornecedor_cnpj: str,
        session: SessionDep,
        response: Response,
        page: int = Query(1, ge= 1),
        ) -> list[reponse_servicos_fornecedor]:

    pages_size = 10

    total = session.scalar(
        select(func.count())
        .select_from(servicos)
        .where(servicos.prestador_do_servico_fornecedor == fornecedor_cnpj))

    total_pages = (total + pages_size - 1) // pages_size

    if page > total_pages and total_pages > 0:
        page = total_pages

    offset = (page - 1) * pages_size

    response.headers["X-Total-Pages"] = str(total_pages)
    response.headers["X-Total-Items"] = str(total)

    servicos_reponse = session.execute(
        select(servicos)
        .where(servicos.prestador_do_servico_fornecedor == fornecedor_cnpj)
        .limit(pages_size)
        .offset(offset)
    ).scalars().all()

    return [reponse_servicos_fornecedor.model_validate(servico) for servico in servicos_reponse]

@router.post('/cadastro_venda_servico', response_model=request_venda_servico,
             responses={404: {'description': 'Vendedor nao encontrado'}})
async def cadastro_venda_servico(cadastro_da_venda: request_venda_servico,
                            session: SessionDep) -> JSONResponse | HTTPException:
    comprador_email = None
    cpf = None
    if not (vendedor_existe := session.execute(
            select(usuarios).where(usuarios.email == cadastro_da_venda.vendedor_email))
            .scalar_one_or_none()):
        raise HTTPException(status_code=404, detail='Vendedor nao encontrado')

    if not (servico := session.execute(
            select(servicos).where(servicos.prestador_do_servico_usuario == cadastro_da_venda.vendedor_email,
                                   servicos.nome_do_servico == cadastro_da_venda.nome_do_servico))
            .scalar_one_or_none()):
        raise HTTPException(status_code=404, detail='serviço nao encontrado')

    data_request = cadastro_da_venda.model_dump(exclude_unset=True)

    if 'comprador_email' in data_request:
        if not (comprador_existe := session.execute(
                select(usuarios).where(usuarios.email == cadastro_da_venda.comprador_email))
                .scalar_one_or_none()):
            raise HTTPException(status_code=404, detail='Comprador nao encontrado')
        comprador_email = data_request['comprador_email']

    if 'comprador_cpf' in data_request:
        cpf = validacao_cpf(normalizada(dado= data_request['comprador_cpf']))
        if not cpf:
            raise HTTPException(status_code=401, detail='Cpf invalido')
        cpf = data_request['comprador_cpf']

    nova_venda = vendas(
        nome_do_servico = cadastro_da_venda.nome_do_servico,
        vendedor_email = cadastro_da_venda.vendedor_email,
        comprador_email = comprador_email,
        comprador_cpf = cpf,
        descricao_da_venda = cadastro_da_venda.descricao_da_venda,
        valor_da_venda = cadastro_da_venda.valor_da_venda,
        forma_de_pagamento = cadastro_da_venda.forma_de_pagamento,
        porcentagem_do_desconto = cadastro_da_venda.porcentagem_do_desconto,
        valor_final = cadastro_da_venda.valor_final
    )

    session.add(nova_venda)
    session.commit()
    session.refresh(nova_venda)

    logger.info(
        f'O usuario com o email {cadastro_da_venda.vendedor_email} adicinou uma venda do serviço {cadastro_da_venda.nome_do_servico} no sistema')
    return JSONResponse(content={'mensagem' : f'A venda do serviço: {cadastro_da_venda.nome_do_servico} foi cadastrada com sucesso'},
                        media_type= 'text/plain')

@router.post('/cadastro_venda_produto', response_model=request_venda_produto,
             responses={404: {'description': 'Usuario nao existe'},
                        409: {'description': 'Email invalido'}})
async def cadastro_venda_produto(cadastro_da_venda: request_venda_produto,
                            session: SessionDep
                            ) -> JSONResponse | HTTPException:
    comprador_email = None
    cpf = None
    if not (vendedor_existe := session.execute(
            select(usuarios).where(usuarios.email == cadastro_da_venda.vendedor_email))
            .scalar_one_or_none()):
        raise HTTPException(status_code=404, detail='Vendedor nao encontrado')

    if not (produto := session.execute(
            select(produtos).where(produtos.proprietario_usuario == cadastro_da_venda.vendedor_email,
                                   produtos.nome_do_produto == cadastro_da_venda.nome_do_produto))
            .scalar_one_or_none()):
        raise HTTPException(status_code=404, detail='produto nao encontrado')

    data_request = cadastro_da_venda.model_dump(exclude_unset=True)

    if 'comprador_email' in data_request:
        if not (comprador_existe := session.execute(
                select(usuarios).where(usuarios.email == cadastro_da_venda.comprador_email))
                .scalar_one_or_none()):
            raise HTTPException(status_code=404, detail='Comprador nao encontrado')
        comprador_email = data_request['comprador_email']

    if 'comprador_cpf' in data_request:
        cpf = validacao_cpf(normalizada(dado=data_request['comprador_cpf']))
        if not cpf:
            raise HTTPException(status_code=401, detail='Cpf invalido')
        cpf = data_request['comprador_cpf']

    nova_venda = vendas(
        nome_do_produto=cadastro_da_venda.nome_do_produto,
        vendedor_email=cadastro_da_venda.vendedor_email,
        comprador_email=comprador_email,
        comprador_cpf=cpf,
        descricao_da_venda=cadastro_da_venda.descricao_da_venda,
        quantidade= cadastro_da_venda.quantidade,
        valor_da_venda=cadastro_da_venda.valor_da_venda,
        forma_de_pagamento=cadastro_da_venda.forma_de_pagamento,
        porcentagem_do_desconto=cadastro_da_venda.porcentagem_do_desconto,
        valor_final=cadastro_da_venda.valor_final
    )

    session.add(nova_venda)
    session.commit()
    session.refresh(nova_venda)

    logger.info(
        f'O usuario com o email {cadastro_da_venda.vendedor_email} adicinou uma venda do produto {cadastro_da_venda.nome_do_produto} no sistema')
    return JSONResponse(
        content={'mensagem': f'A venda do produto: {cadastro_da_venda.nome_do_produto} foi cadastrada com sucesso'},
        media_type='text/plain')

@router.get('/get_vendas/{usuario_email}', response_model=list[reponse_venda])
async def get_vendas(
        usuario_email: EmailStr,
        session: SessionDep,
        response: Response,
        page: int = Query(1, ge= 1),
        ) -> list[reponse_venda]:

    pages_size = 10

    total = session.scalar(
        select(func.count())
        .select_from(vendas)
        .where(vendas.vendedor_email == usuario_email))

    total_pages = (total + pages_size - 1) // pages_size

    if page > total_pages and total_pages > 0:
        page = total_pages

    offset = (page - 1) * pages_size

    response.headers["X-Total-Pages"] = str(total_pages)
    response.headers["X-Total-Items"] = str(total)

    vendas_reponse = session.execute(
        select(vendas)
        .where(vendas.vendedor_email == usuario_email)
        .limit(pages_size)
        .offset(offset)
    ).scalars().all()

    logger.info(f'O usuario com o email {usuario_email} requisitou a vizualização das vendas no sistema')
    return [reponse_venda.model_validate(venda) for venda in vendas_reponse]

@router.patch("/update_venda/{usuario_email}/{identificador}", response_model=patch_venda,
              responses={404: {"description": "venda não encontrado."},
                         400: {"description": "Nenhum dado válido enviado para atualização."}})
async def atualizar_venda(usuario_email: EmailStr, identificador: str,
                            venda_update: patch_venda, session: SessionDep) -> JSONResponse:
    update_data = venda_update.model_dump(exclude_unset=True, exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado válido enviado para atualização.")

    if venda := session.execute(select(vendas).where(vendas.vendedor_email == usuario_email,
                                                    vendas.identificador == identificador)).scalar_one_or_none():
        for key, value in update_data.items():
            setattr(venda, key, value)

        session.commit()
        session.refresh(venda)
        return JSONResponse(content={'mensagem' : f'A venda foi atualizado'}, media_type= 'text/plain')
    logger.info(f'O usuario com o email {usuario_email} atualiza a venda com identificador {identificador} no sistema')
    raise HTTPException(status_code=404, detail="Serviço não encontrado.")

@router.delete("/delete_venda/{usuario_email}/{identificador}", response_model=delete_venda,
               responses={404: {"description": "Venda não encontrado."}})
async def deletar_venda(usuario_email: EmailStr,
                          identificador: str,
                          session: SessionDep) -> JSONResponse | HTTPException:
    if venda := (session.execute(select(vendas).where( vendas.vendedor_email== usuario_email,
                                                          vendas.identificador == identificador))).scalar_one_or_none():

        session.delete(venda)
        session.commit()

        logger.info(
            f'O usuario com o email {usuario_email} deletou a venda com identificador {identificador} no sistema')
        return JSONResponse(content={'mensagem' : f'A venda foi deletado'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="A venda não encontrado.")

@router.post('/cadastro_nota_fiscal', response_model=request_nota_fiscal)
async def cadastro_nota_fiscal(cadastro_da_nota_fiscal: request_nota_fiscal,
                            session: SessionDep) -> JSONResponse | HTTPException:

    if not (usuario_existe := session.execute(select(usuarios).where(usuarios.email == cadastro_da_nota_fiscal.usuario_email)).scalar_one_or_none()):
        if 0 ==(maior_numero := session.scalar(select(func.max(nota_fiscal.numero_da_nota))
                                                       .where(nota_fiscal.usuario_email == cadastro_da_nota_fiscal.usuario_email)) or 0):
            #emitir_NotaFiscal(dados=cadastro_da_nota_fiscal.model_dump(exclude_unset=True), numero_da_nota= 1)
            nova_nota = nota_fiscal(
                usuario_email = cadastro_da_nota_fiscal.usuario_email,
                numero_da_nota = 1
            )
            session.commit()
            session.refresh(nova_nota)
            logger.info(
                f'O usuario com o email {cadastro_da_nota_fiscal.usuario_email} requisitou uma nota fiscal no sistema')
            return JSONResponse(content={'mensage': 'nota emitida'}, media_type= 'text/plain')
        else:
            #emitir_NotaFiscal(dados=cadastro_da_nota_fiscal.model_dump(exclude_unset=True), numero_da_nota= cadastro_da_nota_fiscal.numero_da_nota + 1)
            nova_nota = nota_fiscal(
                usuario_email=cadastro_da_nota_fiscal.usuario_email,
                numero_da_nota= maior_numero.numero_da_nota + 1
            )
            session.commit()
            session.refresh(nova_nota)
            logger.info(
                f'O usuario com o email {cadastro_da_nota_fiscal.usuario_email} requisitou uma nota fiscal no sistema')
            return JSONResponse(content={'mensage': 'nota emitida'}, media_type='text/plain')

    raise HTTPException(status_code=404, detail="Usuario não encontrado")

@router.post('/cadastro_receita', response_model=request_receita,
             responses={404: {'description': 'Usuario nao existe'},
                        409: {'description': 'Email invalido'}})
async def cadastro_receita(cadastro_de_receita: request_receita,
                            session: SessionDep
                            ) -> JSONResponse | HTTPException:
    pagador = None
    if not (recebedor_existe := session.execute(
            select(usuarios).where(usuarios.email == cadastro_de_receita.recebedor_email))
            .scalar_one_or_none()):
        raise HTTPException(status_code=404, detail='Vendedor nao encontrado')

    data_request = cadastro_de_receita.model_dump(exclude_unset=True)

    if 'pagador_email' in data_request:
        if not (pagador_email := session.execute(
                select(usuarios).where(usuarios.email == cadastro_de_receita.pagador_email))
                .scalar_one_or_none()):
            raise HTTPException(status_code=404, detail='Comprador nao encontrado')
        pagador = data_request['pagador_email']


    nova_receita = receitas(
        recebedor_email= cadastro_de_receita.recebedor_email,
        pagador_email= pagador,
        tipo_da_receita= cadastro_de_receita.tipo_da_receita,
        data_da_receita= cadastro_de_receita.data_da_receita,
        valor_da_receita= cadastro_de_receita.valor_da_receita,
        forma_de_pagamento= cadastro_de_receita.forma_de_pagamento,
        observacao= cadastro_de_receita.observacao,
        documento_anexado= cadastro_de_receita.documento_anexado,
    )

    session.add(nova_receita)
    session.commit()
    session.refresh(nova_receita)

    logger.info(
        f'O usuario com o email {cadastro_de_receita.recebedor_email} adicionou uma receita no sistema')
    return JSONResponse(
        content={'mensagem': f'A receita foi cadastrada com sucesso'},
        media_type='text/plain')

@router.get('/get_receitas/{usuario_email}', response_model=list[reponse_receita])
async def get_receitas(
        usuario_email: EmailStr,
        session: SessionDep,
        response: Response,
        page: int = Query(1, ge= 1),
        ) -> list[reponse_receita]:

    pages_size = 10

    total = session.scalar(
        select(func.count())
        .select_from(receitas)
        .where(receitas.recebedor_email == usuario_email))

    total_pages = (total + pages_size - 1) // pages_size

    if page > total_pages and total_pages > 0:
        page = total_pages

    offset = (page - 1) * pages_size

    response.headers["X-Total-Pages"] = str(total_pages)
    response.headers["X-Total-Items"] = str(total)

    receitas_reponse = session.execute(
        select(receitas)
        .where(receitas.recebedor_email == usuario_email)
        .limit(pages_size)
        .offset(offset)
    ).scalars().all()

    logger.info(
        f'O usuario com o email {usuario_email} requisitou a vizualização das receitas no sistema')
    return [reponse_receita.model_validate(receita) for receita in receitas_reponse]

@router.patch("/update_receita/{usuario_email}/{identificador}", response_model=patch_receita,
              responses={404: {"description": "A receita não encontrado."},
                         400: {"description": "Nenhum dado válido enviado para atualização."}})
async def atualizar_receita(usuario_email: EmailStr, identificador: str,
                            receita_update: patch_receita, session: SessionDep) -> JSONResponse:
    update_data = receita_update.model_dump(exclude_unset=True, exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado válido enviado para atualização.")

    if receita := session.execute(select(receitas).where(receitas.recebedor_email == usuario_email,
                                                    receitas.identificador == identificador)).scalar_one_or_none():
        for key, value in update_data.items():
            setattr(receita, key, value)

        session.commit()
        session.refresh(receita)

        logger.info(
            f'O usuario com o email {usuario_email} atualizou a receita com identificador: {identificador} no sistema')
        return JSONResponse(content={'mensagem' : f'A receita foi atualizado'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="A receita não encontrado.")

@router.delete("/delete_receita/{usuario_email}/{identificador}", response_model=delete_receita,
               responses={404: {"description": "receita não encontrado."}})
async def deletar_receita(usuario_email: EmailStr,
                          identificador: str,
                          session: SessionDep) -> JSONResponse | HTTPException:
    if receita := (session.execute(select(receitas).where( receitas.recebedor_email == usuario_email,
                                                          receitas.identificador == identificador))).scalar_one_or_none():

        session.delete(receita)
        session.commit()

        logger.info(
            f'O usuario com o email {usuario_email} deletou a receita com identificador: {identificador} no sistema')
        return JSONResponse(content={'mensagem' : f'A receita foi deletado'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="A receita não encontrado.")

@router.post('/cadastro_despesa', response_model=request_despesa)
async def cadastro_despesa(cadastro_de_despesa: request_despesa,
                            session: SessionDep
                            ) -> JSONResponse | HTTPException:
    recebedor = None
    if not (pagador_existe := session.execute(
            select(usuarios).where(usuarios.email == cadastro_de_despesa.pagador_email))
            .scalar_one_or_none()):
        raise HTTPException(status_code=404, detail='Pagador não encontrado')

    data_request = cadastro_de_despesa.model_dump(exclude_unset=True)

    if 'recebedor_email' in data_request:
        if not (recebedor_email := session.execute(
                select(usuarios).where(usuarios.email == cadastro_de_despesa.recebedor_email))
                .scalar_one_or_none()):
            raise HTTPException(status_code=404, detail='Recebedor não encontrado')
        recebedor = data_request['recebedor_email']


    nova_despesa = despesas(
        pagador_email= cadastro_de_despesa.pagador_email,
        recebedor_email= recebedor,
        tipo_da_despesa= cadastro_de_despesa.tipo_da_despesa,
        descricao_da_despesa= cadastro_de_despesa.descricao_da_despesa,
        valor_total_da_despesa= cadastro_de_despesa.valor_total_da_despesa,
        forma_de_pagamento= cadastro_de_despesa.forma_de_pagamento,
        valor_por_unidade= cadastro_de_despesa.valor_por_unidade,
        documento_anexado= cadastro_de_despesa.documento_anexado,
        valor_de_revenda= cadastro_de_despesa.valor_de_revenda,
    )

    session.add(nova_despesa)
    session.commit()
    session.refresh(nova_despesa)

    logger.info(
        f'O usuario com o email {cadastro_de_despesa.pagador_email} adicionou uma despesas no sistema')
    return JSONResponse(
        content={'mensagem': f'A receita foi cadastrada com sucesso'},
        media_type='text/plain')

@router.get('/get_despesas/{usuario_email}', response_model=list[reponse_despesa])
async def get_despesa(
        usuario_email: EmailStr,
        session: SessionDep,
        response: Response,
        page: int = Query(1, ge= 1),
        ) -> list[reponse_despesa]:

    pages_size = 10

    total = session.scalar(
        select(func.count())
        .select_from(despesas)
        .where(despesas.pagador_email == usuario_email))

    total_pages = (total + pages_size - 1) // pages_size

    if page > total_pages and total_pages > 0:
        page = total_pages

    offset = (page - 1) * pages_size

    response.headers["X-Total-Pages"] = str(total_pages)
    response.headers["X-Total-Items"] = str(total)

    despesas_reponse = session.execute(
        select(despesas)
        .where(despesas.pagador_email == usuario_email)
        .limit(pages_size)
        .offset(offset)
    ).scalars().all()

    logger.info(
        f'O usuario com o email {usuario_email} requisitou a vizualização das despesas no sistema')
    return [reponse_despesa.model_validate(despensa) for despensa in despesas_reponse]

@router.patch("/update_despesa/{usuario_email}/{identificador}", response_model=patch_despesa,
              responses={404: {"description": "A despesa não encontrado."},
                         400: {"description": "Nenhum dado válido enviado para atualização."}})
async def atualizar_despesa(usuario_email: EmailStr, identificador: str,
                            despensa_update: patch_despesa, session: SessionDep) -> JSONResponse:
    update_data = despensa_update.model_dump(exclude_unset=True, exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado válido enviado para atualização.")

    if despesa := session.execute(select(despesas).where(despesas.pagador_email == usuario_email,
                                                   despesas.identificador == identificador)).scalar_one_or_none():
        for key, value in update_data.items():
            setattr(despesa, key, value)

        session.commit()
        session.refresh(despesa)

        logger.info(
            f'O usuario com o email {usuario_email} atualizou a despesa com identificador: {identificador} no sistema')
        return JSONResponse(content={'mensagem' : f'A despesa foi atualizado'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="A despesa não encontrado.")

@router.delete("/delete_despesa/{usuario_email}/{identificador}", response_model=delete_receita,
               responses={404: {"description": "A despesa não encontrado."}})
async def deletar_despesa(usuario_email: EmailStr,
                          identificador: str,
                          session: SessionDep) -> JSONResponse | HTTPException:
    if despesa := (session.execute(select(despesas).where( despesas.pagador_email == usuario_email,
                                                          despesas.identificador == identificador))).scalar_one_or_none():

        session.delete(despesa)
        session.commit()

        logger.info(
            f'O usuario com o email {usuario_email} deletou a despesa com identificador: {identificador} no sistema')
        return JSONResponse(content={'mensagem' : f'A despesa foi deletada'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="A despesa não encontrado.")

@router.get('/relatorio/{formato}/{email}', response_model=None, responses={
    200: {"content": {
        "application/pdf": {},
        "application/xml": {},
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}
    }}
})
async def get_relatorio(formato: formato_arquivo, email: str, session: SessionDep):

    usuario = session.execute(
        select(usuarios).where(usuarios.email == email)
    ).scalar_one_or_none()
    if not usuario:
        raise HTTPException(status_code=404, detail='Usuário não encontrado.')

    lista_receitas = session.execute(
        select(receitas).where(receitas.recebedor_email == email)
    ).scalars().all()

    lista_despesas = session.execute(
        select(despesas).where(despesas.pagador_email == email)
    ).scalars().all()

    lista_vendas = session.execute(
        select(vendas).where(vendas.vendedor_email == email)
    ).scalars().all()

    lista_produtos = session.execute(
        select(produtos).where(produtos.proprietario_usuario == email)
    ).scalars().all()

    lista_servicos = session.execute(
        select(servicos).where(servicos.prestador_do_servico_usuario == email)
    ).scalars().all()

    lista_receitas = [model_to_dict(r) for r in lista_receitas]
    lista_despesas = [model_to_dict(d) for d in lista_despesas]
    lista_vendas = [model_to_dict(v) for v in lista_vendas]
    lista_produtos = [model_to_dict(p) for p in lista_produtos]
    lista_servicos = [model_to_dict(s) for s in lista_servicos]
    total_rec = sum(r["valor_da_receita"] for r in lista_receitas)
    total_desp = sum(d["valor_total_da_despesa"] for d in lista_despesas)
    saldo = total_rec - total_desp

    dados = {
        "tipo_relatorio": "Relatório Completo",
        "nome_sistema": "Sistema CPR",
        "periodo_inicio": "",
        "periodo_fim": "",
        "data_geracao": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "usuario_nome": usuario.nome_completo,
        "usuario_email": usuario.email,
        "usuario_telefone": usuario.numero_telefone,
        "usuario_cidade": usuario.cidade,
        "usuario_estado": usuario.estado,
        "receitas": lista_receitas,
        "despesas": lista_despesas,
        "vendas": lista_vendas,
        "produtos": lista_produtos,
        "servicos": lista_servicos,
        "total_receitas": formatar_brl(total_rec),
        "qtd_receitas": len(lista_receitas),
        "total_despesas": formatar_brl(total_desp),
        "qtd_despesas": len(lista_despesas),
        "saldo_periodo":  formatar_brl(saldo),
        "status_saldo":   "positivo" if saldo >= 0 else "negativo",
        "observacoes": "",
        "total_inconsistencias": "0",
        "inconsistencias": [],
    }

    if formato == formato_arquivo.xml:
        logger.info(f'O usuario com o email {email} requisitou um relatorio em xml das suas despesas e receitas')
        return gerar_xml(dados)
    elif formato == formato_arquivo.xls:
        logger.info(f'O usuario com o email {email} requisitou um relatorio em xls das suas despesas e receitas')
        return gerar_xls(dados)
    elif formato == formato_arquivo.pdf:
        logger.info(f'O usuario com o email {email} requisitou um relatorio em pdf das suas despesas e receitas')
        return gerar_pdf(dados)
    raise HTTPException(status_code=400, detail='tipo de formato não aceito no sistema')
