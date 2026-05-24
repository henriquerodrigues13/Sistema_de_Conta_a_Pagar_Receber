from fastapi import APIRouter, Depends, HTTPException
from backend.models.database import get_session
from backend.API.criptografia import *
from backend.API.validações import *
from backend.models.engine import *
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated


router = APIRouter(tags=["cadastro e login"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post(path='/login', response_model=reponsa_usuario,
             responses={404: {'description': 'Usuario nao encontrado'}})
async def login(usuario_login: login_usuario, session: SessionDep) -> reponsa_usuario:

    if (usuario_existe := session.execute(
        select(usuario).where(usuario.email == usuario_login.email)
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
            select(usuario).where(usuario.email == cadastro_do_usuario.email))
            .scalar_one_or_none()):
        raise HTTPException(status_code=409, detail='Usuario ja existe')
    senha_HASH = senha_hash(senha=cadastro_do_usuario.senha)

    novo_usuario = usuario(
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

@router.post('/cadastro_fornecedor', response_model=reponse_fornecedor)
async def cadastro_fornecedor(fornecedor_cadastro: cadastro_fornecedor,
                                   session: SessionDep) -> reponse_fornecedor | HTTPException:
    cnpj = normalizada_cnpj(cnpj=fornecedor_cadastro.cnpj)

    if not (cnpj_valido := validacao_cnpj(cnpj=cnpj)):
        raise HTTPException(status_code=400, detail='Cnpj não é valido')

    if(forncedor_ja_existe := session.execute(
            select(fornecedores).where(fornecedores.cnpj == cnpj))
            .scalar_one_or_none()):
        raise HTTPException(status_code=409, detail='Usuario ja existe')

    novo_fornecedor = fornecedores(
        cnpj = cnpj_valido['cnpj'],
        nome_oficial_empresa = cnpj_valido['razao_social'],
        nome_cormecial_empresa = cnpj_valido['nome_fantasia'],
        situacao_cadastral = cnpj_valido['situacao_cadastral'],
        data_abertura = cnpj_valido['data_inicio_atividade'],
        natureza_juridica = cnpj_valido['natureza_juridica'],
        cnae = cnpj_valido['cnae_fiscal'],
        capital_social = cnpj_valido['capital_social'],
        porte_empresa = cnpj_valido['porte'],
        cep = cnpj_valido['cep'],
        uf = cnpj_valido['uf'],
        cidade = cnpj_valido['municipio'],
        bairro = cnpj_valido['bairro'],
        logradouro = cnpj_valido['logradouro'],

    )

    session.add(novo_fornecedor)
    session.commit()
    session.refresh(novo_fornecedor)

    return reponse_fornecedor.model_validate(novo_fornecedor)

'''@router.post('/vendas', response_model=vendas_RESPONSE)
async def cadastro_vendas(vendas_cadastro: vendas_REQUEST,
                                   session: SessionDep) ->vendas_RESPONSE | HTTPException:
    cpf_cnpj_vendendor = normalizadacao_cpf_cnpj(cpf_cnpj=vendas_cadastro.cpf_cnpj_vendendor)
    cpf_cnpj_comprador = normalizadacao_cpf_cnpj(cpf_cnpj=vendas_cadastro.cpf_cnpj_comprador)
    if len(cpf_cnpj_vendendor) == 11:
        cpf_vendendor = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj_vendendor)
        cnpj_vendendor = None
    else:
        cpf_vendendor = None
        cnpj_vendendor = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj_vendendor)

    if len(cpf_cnpj_comprador) == 11:
        cpf_comprador = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj_comprador)
        cnpj_comprador = None
    else:
        cpf_comprador = None
        cnpj_comprador = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj_comprador)

    valor_final = vendas_cadastro.valor_venda * ((100 - vendas_cadastro.porcentagem_desconto)/100)

    vendas_nova = vendas(
        cpf_vendendor = cpf_vendendor,
        cnpj_vendendor = cnpj_vendendor,
        cpf_comprador = cpf_comprador,
        cnpj_comprador = cnpj_comprador,
        forma_pagamento = vendas_cadastro.forma_pagamento,
        valor_venda= vendas_cadastro.valor_venda,
        porcentagem_desconto = vendas_cadastro.porcentagem_desconto,
        valor_final_venda = valor_final,
    )

    session.add(vendas_nova)
    session.commit()
    session.refresh(vendas_nova)

    return vendas_RESPONSE.model_validate(vendas_nova)

@router.post('/despesas', response_model=despesasResponse)
async def cadastro_despeasas(despesas_cadastro: despesasRESQUEST,
                                   session: SessionDep) -> despesasResponse | HTTPException:
    cpf_cnpj_pagador = normalizadacao_cpf_cnpj(cpf_cnpj=despesas_cadastro.cpf_cnpj_pagador)
    cpf_cnpj_recebedor = normalizadacao_cpf_cnpj(cpf_cnpj=despesas_cadastro.cpf_cnpj_recebedor)
    if len(cpf_cnpj_pagador) == 11:
        cpf_pagador = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj_pagador)
        cnpj_pagador = None
    else:
        cpf_pagador = None
        cnpj_pagador = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj_pagador)

    if len(cpf_cnpj_recebedor) == 11:
        cpf_recebedor = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj_recebedor)
        cnpj_recebedor = None
    else:
        cpf_recebedor = None
        cnpj_recebedor = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj_recebedor)

    despesas_nova = despesas(
        cpf_pagado =cpf_pagador,
        cnpj_pagado= cnpj_pagador,
        cpf_recebedor =cpf_recebedor,
        cnpj_recebedor = cnpj_recebedor,
        valor_despesas = despesas_cadastro.valor_despesas,
        data_evento = despesas_cadastro.data_evento,
        tipo_de_despesa = despesas_cadastro.tipo_de_despesa,
    )

    session.add(despesas_nova)
    session.commit()
    session.refresh(despesas_nova)

    return despesasResponse.model_validate(despesas_nova)

@router.post('/receita', response_model=receitas_RESPONSE)
async def cadastro_receitas(receita_cadastro: receitas_REQUEST,
                                   session: SessionDep) -> receitas_RESPONSE | HTTPException:
    cpf_cnpj_recebedor = normalizadacao_cpf_cnpj(cpf_cnpj=receita_cadastro.cpf_cnpj_recebedor)
    cpf_cnpj_pagador = normalizadacao_cpf_cnpj(cpf_cnpj=receita_cadastro.cpf_cnpj_pagado)
    if len(cpf_cnpj_recebedor) == 11:
        cpf_recebedor = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj_recebedor)
        cnpj_recebedor = None
    else:
        cpf_recebedor = None
        cnpj_recebedor = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj_recebedor)

    if len(cpf_cnpj_pagador) == 11:
        cpf_pagador = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj_pagador)
        cnpj_pagador = None
    else:
        cpf_pagador = None
        cnpj_pagador = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj_pagador)

    receita_nova = receita(
        cpf_recebedor =cpf_recebedor,
        cnpj_recebedor= cnpj_recebedor,
        cpf_pagador =cpf_pagador,
        cnpj_pagador = cnpj_pagador,
        valor_receita = receita_cadastro.valor_receita,
        data_evento_receita = receita_cadastro.data_evento_receita,
        origem_receita = receita_cadastro.origem_receita,
    )

    session.add(receita_nova)
    session.commit()
    session.refresh(receita_nova)

    return receitas_RESPONSE.model_validate(receita_nova)

@router.post('gedador_de_relatorio')
async def exportar_pdf(dados_gerador:dados_gerador_relatorio):
    pass'''