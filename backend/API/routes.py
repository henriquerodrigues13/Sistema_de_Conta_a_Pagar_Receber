from fastapi import APIRouter, Depends, HTTPException, Query, Response
from backend.models.database import get_session
from starlette.responses import JSONResponse
from backend.API.criptografia import *
from backend.API.validações import *
from backend.models.engine import *
from sqlalchemy.orm import Session
from sqlalchemy import select, func, update
from typing import Annotated

from backend.models.engine import reponse_servicos

router = APIRouter(tags=["cadastro e login"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post(path='/login', response_model=reponsa_usuario,
             responses={404: {'description': 'Usuario nao encontrado'},
                        401: {'description': 'Senha incorreta'}})
async def login(usuario_login: login_usuario, session: SessionDep) -> reponsa_usuario:

    if (usuario_existe := session.execute(
        select(usuarios).where(usuarios.email == usuario_login.email)
    ).scalar_one_or_none()):
        if verificar_senha(senha=usuario_login.senha, hash_salvo=usuario_existe.senha):
            return reponsa_usuario.model_validate(usuario_existe)
        raise HTTPException(status_code=401, detail="Senha incorreta")
    raise HTTPException(status_code=404, detail='Usuario nao encontrado')

@router.post('/cadastro_usuario', response_model=reponsa_usuario,
             responses={409: {'description': 'Usuario ja existe'},
                        401: {'description': 'Email invalido'}})
async def cadastro_usuario(cadastro_do_usuario: cadastro_usuario, session: SessionDep) -> HTTPException | reponsa_usuario:
    if not (isEmail_valido:=validacao_email(email=cadastro_do_usuario.email)):
        raise HTTPException(status_code=401, detail='Email invalido')

    if (usario_ja_existe := session.execute(
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

    return reponsa_usuario.model_validate(novo_usuario)

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
        .where(produtos.proprietario_usuario == usuario_email,
               produtos.produto_deletado == False)
        .limit(pages_size)
        .offset(offset)
    ).scalars().all()

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

        return JSONResponse(content={'mensagem' : f'o produto: {nome_do_produto} foi atualizado'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="Produto não encontrado.")

@router.delete("/delete_produto/{usuario_email}/{nome_do_produto}", response_model=delete_produto,
               responses={404: {"description": "Produto não encontrado."}})
async def deletar_produto(usuario_email: EmailStr,
                          nome_do_produto: str,
                          session: SessionDep) -> JSONResponse | HTTPException:
    if produto := (session.execute(update(produtos).where(produtos.proprietario_usuario == usuario_email,
                                                          produtos.nome_do_produto == nome_do_produto)
                                                          .values(status_do_produto='indisponivel', produto_deletado=True))):

        session.commit()

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
        .where(servicos.prestador_do_servico_usuario == usuario_email,
               servicos.servico_deletado == False)
        .limit(pages_size)
        .offset(offset)
    ).scalars().all()

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
        return JSONResponse(content={'mensagem' : f'o servico : {nome_do_servico} foi atualizado'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="Serviço não encontrado.")

@router.delete("/delete_servico/{usuario_email}/{nome_do_servico}", response_model=delete_servico,
               responses={404: {"description": "Serviço não encontrado."}})
async def deletar_servico(usuario_email: EmailStr,
                          nome_do_servico: str,
                          session: SessionDep) -> JSONResponse | HTTPException:
    if produto := (session.execute(update(servicos).where(servicos.prestador_do_servico_usuario == usuario_email,
                                                          servicos.nome_do_servico == nome_do_servico)
                                                          .values(servico_deletado=True))):

        session.commit()

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
        .where(vendas.vendedor_email == usuario_email,
               vendas.venda_deletado == False)
        .limit(pages_size)
        .offset(offset)
    ).scalars().all()

    return [reponse_venda.model_validate(venda) for venda in vendas_reponse]

@router.patch("/update_venda/{usuario_email}/{nome_do_servico_ou_produto}", response_model=patch_servico,
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
        return JSONResponse(content={'mensagem' : f'o servico : {nome_do_servico} foi atualizado'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="Serviço não encontrado.")

@router.delete("/delete_venda/{usuario_email}/{nome_do_servico}", response_model=delete_servico,
               responses={404: {"description": "Serviço não encontrado."}})
async def deletar_venda(usuario_email: EmailStr,
                          nome_do_servico: str,
                          session: SessionDep) -> JSONResponse | HTTPException:
    if produto := (session.execute(update(servicos).where(servicos.prestador_do_servico_usuario == usuario_email,
                                                          servicos.nome_do_servico == nome_do_servico)
                                                          .values(servico_deletado=True))):

        session.commit()

        return JSONResponse(content={'mensagem' : f'o servico: {nome_do_servico} foi deletado'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="Serviço não encontrado.")