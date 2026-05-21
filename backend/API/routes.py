from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from backend.models.database import get_session
from backend.API.criptografia import *
from backend.API.validações import *
from backend.models.engine import *
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import select
from typing import Annotated


router = APIRouter(tags=["cadastro e login"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post(path='/login_cliente', response_model=clienteResponse,
             responses={404: {'description': 'Usuario nao encontrado'}})
async def login_cliente(cliente_login: clienteLOGIN, session: SessionDep) -> clienteResponse:
    cpf = normalizadacao_cpf_cnpj(cpf_cnpj=cliente_login.cpf)
    cpf_HASH = cpf_cnpj_hash(cpf_cnpj=cpf)

    cliente_valido = session.execute(
        select(cliente).where(cliente.cpf == cpf_HASH)
    ).scalar_one_or_none()

    if cliente_valido:
        if verificar_senha(senha=cliente_login.senha, hash_salvo=cliente_valido.senha):
            return clienteResponse.model_validate(cliente_valido)
        raise HTTPException(status_code=401, detail="Senha incorreta")
    raise HTTPException(status_code=404, detail='Usuario nao encontrado')


@router.post('/cliente', response_model=clientePOST)
async def cadastro_cliente(cliente_cadastro: clientePOST, session: SessionDep) -> HTTPException | clientePOST:
    cpf = normalizadacao_cpf_cnpj(cpf_cnpj=cliente_cadastro.cpf)
    cliente_valido = validacao_cpf(cpf=cpf,
                                     nome_completo=cliente_cadastro.nome,
                                     data_nascimento=cliente_cadastro.data_nascimento)

    if cliente_valido != 200:
        raise HTTPException(status_code=400, detail='Erro na validação do CPF')

    cpf_HASH = cpf_cnpj_hash(cpf_cnpj=cpf)
    senha_HASH = senha_hash(senha=cliente_cadastro.senha)

    cliente_existe = session.execute(
        select(cliente).where(cliente.cpf == cpf_HASH)
    ).scalar_one_or_none()

    if cliente_existe is not None:
        raise HTTPException(status_code=409, detail='Usuario ja existe no banco de dados')

    cliente_novo = cliente(
        nome=cliente_cadastro.nome,
        cpf=cpf_HASH,
        data_nascimento=cliente_cadastro.data_nascimento,
        senha=senha_HASH,
        email=cliente_cadastro.email,
        numero_telefone_pessoal=cliente_cadastro.numero_telefone_pessoal,
        cep=cliente_cadastro.cep,
        estado=cliente_cadastro.estado,
        cidade=cliente_cadastro.cidade,
        bairro=cliente_cadastro.bairro,
        logradouro=cliente_cadastro.logradouro,
    )

    session.add(cliente_novo)
    session.commit()
    session.refresh(cliente_novo)

    return clientePOST.model_validate(cliente_novo)


@router.post(path='/login_fornecedor', response_model=fornecedorResponde,
             responses={404: {'description': 'Usuario nao encontrado'},
                        401: {'description': 'Senha incorreta'}
                        })
async def login_fornecedor(fornecedor_login: fornecedorLOGIN, session: SessionDep) -> fornecedorResponde:
    cnpj = normalizadacao_cpf_cnpj(cpf_cnpj=fornecedor_login.cnpj)
    cnpj_HASH = cpf_cnpj_hash(cpf_cnpj=cnpj)

    fornecedor_valido = session.execute(
        select(fornecedor).where(fornecedor.cnpj == cnpj_HASH)
    ).scalar_one_or_none()

    if fornecedor_valido:
        if verificar_senha(senha=fornecedor_login.senha, hash_salvo=fornecedor_valido.senha):
            return fornecedorResponde.model_validate(fornecedor_valido)
        raise HTTPException(status_code=401, detail="Senha incorreta")
    raise HTTPException(status_code=404, detail='Usuario nao encontrado')


@router.post('/fornecedor', response_model=fornecedorPOST)
async def cadastro_fornecedor(fornecedor_cadastro: fornecedorREQUEST,
                              session: SessionDep) -> fornecedorPOST | HTTPException:
    cnpj = normalizadacao_cpf_cnpj(cpf_cnpj=fornecedor_cadastro.cnpj)
    fornecedor_dados = validacao_cnpj(cnpj=cnpj,
                                      nome_oficial_empresa=fornecedor_cadastro.nome_oficial_empresa)

    if isinstance(fornecedor_dados, int):
        raise HTTPException(status_code=400, detail='Erro na validação do CNPJ')

    cnpj_HASH = cpf_cnpj_hash(cpf_cnpj=cnpj)
    senha_HASH = senha_hash(senha=fornecedor_cadastro.senha)

    fornecedor_existe = session.execute(
        select(fornecedor).where(fornecedor.cnpj == cnpj_HASH)
    ).scalar_one_or_none()

    if fornecedor_existe is not None:
        raise HTTPException(status_code=409, detail='Usuario ja existe no banco de dados')

    fornecedor_novo = fornecedor(
        cnpj=cnpj_HASH,
        senha=senha_HASH,
        nome_oficial_empresa=fornecedor_dados['nome_oficial_empresa'],
        nome_cormecial_empresa=fornecedor_dados['nome_cormecial_empresa'],
        situacao_cadastral=fornecedor_dados['situacao_cadastral'],
        data_abertura=fornecedor_dados['data_abertura'],
        natureza_juridica=fornecedor_dados['natureza_juridica'],
        cnae=fornecedor_dados['cnae'],
        capital_social=fornecedor_dados['capital_social'],
        porte_empresa=fornecedor_dados['porte_empresa'],
        email=fornecedor_cadastro.email,
        numero_telefone_empresa=fornecedor_cadastro.numero_telefone_empresa,
        cep=fornecedor_dados['cep'],
        uf=fornecedor_dados['uf'],
        cidade=fornecedor_dados['cidade'],
        bairro=fornecedor_dados['bairro'],
        logradouro=fornecedor_dados['logradouro'],
    )

    session.add(fornecedor_novo)
    session.commit()
    session.refresh(fornecedor_novo)

    return fornecedorPOST.model_validate(fornecedor_novo)

@router.post('/produto_servico', response_model=produto_servico_Response)
async def cadastro_produto_servico(produto_servico_cadastro: produto_servico_REQUEST,
                                   session: SessionDep) -> produto_servico_Response | HTTPException:
    cpf_cnpj = normalizadacao_cpf_cnpj(cpf_cnpj=produto_servico_cadastro.cpf_cnpj)
    if len(cpf_cnpj) == 11:
        cpf_HASH = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj)
    else:
        cnpj_HASH = cpf_cnpj_hash(cpf_cnpj=cpf_cnpj)

    imcs = lambda x: x * 0.18
    valor_com_imcs = float(imcs(produto_servico_cadastro.valor_final_de_venda))
    margem = (lambda x,y, z: x - (y + z) )
    marga_de_lucro = float(margem(produto_servico_cadastro.valor_final_de_venda,
                            produto_servico_cadastro.valor_custo_de_venda,
                            valor_com_imcs))

    novo_uuid =  uuid4()
    if len(cpf_cnpj) == 11:
        produto_servico_novo = produto_servico(
            produto_servico_uuid = novo_uuid,
            classificacao_produto_servico = produto_servico_cadastro.classificacao_produto_servico,
            nome_produto_servico = produto_servico_cadastro.identidicado_produto_servico,
            cpf_vendendor = cpf_HASH,
            detalhes = produto_servico_cadastro.detalhes_produto_servico,
            data_do_cadastro = datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d'),
            valor_custo = produto_servico_cadastro.valor_custo_de_venda,
            ICMS = "18%",
            valor_com_IMCS = valor_com_imcs,
            valor_final_de_venda= produto_servico_cadastro.valor_final_de_venda,
            margem_de_lucro = marga_de_lucro,
        )
    else:
        produto_servico_novo = produto_servico(
            produto_servico_uuid=novo_uuid,
            classificacao_produto_servico=produto_servico_cadastro.classificacao_produto_servico,
            nome_produto_servico=produto_servico_cadastro.identidicado_produto_servico,
            cnpj_vendendor=cnpj_HASH,
            detalhes=produto_servico_cadastro.detalhes_produto_servico,
            data_do_cadastro=datetime.strptime(datetime.today().strftime('%Y-%m-%d'), '%Y-%m-%d'),
            valor_custo=produto_servico_cadastro.valor_custo_de_venda,
            ICMS="18%",
            valor_com_IMCS=valor_com_imcs,
            valor_final_de_venda=produto_servico_cadastro.valor_final_de_venda,
            margem_de_lucro=marga_de_lucro,
        )

    session.add(produto_servico_novo)
    session.commit()
    session.refresh(produto_servico_novo)

    return produto_servico_Response.model_validate(produto_servico_novo)

@router.post('/vendas', response_model=vendas_RESPONSE)
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
    pass