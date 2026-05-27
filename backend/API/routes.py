from fastapi import APIRouter, Depends, HTTPException, Query, Response
from starlette.responses import JSONResponse
from backend.models.database import get_session
from backend.API.criptografia import *
from backend.API.validações import *
from backend.models.engine import *
from sqlalchemy.orm import Session
from sqlalchemy import select, func, update
from typing import Annotated

from backend.models.engine import reponse_fornecedor

router = APIRouter(tags=["cadastro e login"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post(path='/login', response_model=reponsa_usuario,
             responses={404: {'description': 'Usuario nao encontrado'}})
async def login(usuario_login: login_usuario, session: SessionDep) -> reponsa_usuario:

    if (usuario_existe := session.execute(
        select(usuarios).where(usuarios.email == usuario_login.email)
    ).scalar_one_or_none()):
        if verificar_senha(senha=usuario_login.senha, hash_salvo=usuario_existe.senha):
            return reponsa_usuario.model_validate(usuario_existe)
        raise HTTPException(status_code=401, detail="Senha incorreta")
    raise HTTPException(status_code=404, detail='Usuario nao encontrado')

@router.post('/cadastro_usuario', response_model=reponsa_usuario)
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

@router.post('/cadastro_produtos', response_model=request_produtos)
async def cadastro_produtos(cadastro_produto: request_produtos,
                            session: SessionDep
                            ) -> JSONResponse | HTTPException:
    if not (email_nao_existe := session.execute(
            select(usuarios).where(usuarios.email == cadastro_produto.proprietario_usuario))
            .scalar_one_or_none()):
        raise HTTPException(status_code=404, detail='Usuario nao existe')


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

    return JSONResponse(content={'mensagem' : 'cadastrado com sucesso'}, media_type= 'text/plain')

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

    return [reponse_produtos_usuario.model_validate(produto) for produto in produtos_reponse]

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


@router.patch("/update_produto/{usuario_email}/{nome_do_produto}", response_model=patch_produto,
              responses={404: {"description": "produto não encontrado."},
                         400: {"description": "Nenhum dado válido enviado para atualização."}})
async def atualizar_produto(usuario_email: EmailStr, nome_do_produto: str,
                            produto_update: patch_produto, session: SessionDep) -> JSONResponse:
    update_data = produto_update.model_dump(exclude_unset=True, exclude_none=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado válido enviado para atualização.")

    if livro := session.scalar(select(produtos).where(produtos.proprietario_usuario == usuario_email,
                                                    produtos.nome_do_produto == nome_do_produto)):
        for key, value in update_data.items():
            setattr(livro, key, value)

        session.commit()
        session.refresh(livro)

        return JSONResponse(content={'mensagem' : f'o produto foi atualizado'}, media_type= 'text/plain')

    raise HTTPException(status_code=404, detail="Livro não encontrado.")

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

