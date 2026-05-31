from datetime import datetime
from decimal import Decimal
from pynfe.entidades.emitente import Emitente
from pynfe.entidades.cliente import Cliente
from pynfe.entidades.notafiscal import NotaFiscal
from pynfe.entidades.fonte_dados import _fonte_dados
#from pynfe.serializacao.xml import SerializacaoXML
#from pynfe.assinatura.certificado import AssinaturaA1
#from pynfe.comunicacao.cliente_ws import ClienteNFe
from backend.models.tabelas import request_nota_fiscal


def emitir_NotaFiscal(dados: request_nota_fiscal, numero_da_nota: int):
    fonte = _fonte_dados()

    emitente = Emitente()
    emitente._fonte_dados = fonte
    emitente.razao_social = dados.emitente_razao_social
    emitente.cnpj = dados.emitente_cnpj
    emitente.inscricao_estadual = dados.emitente_inscricao_estadual
    emitente.inscricao_municipal = dados.emitente_inscricao_municipal
    emitente.codigo_municipio = dados.emitente_codigo_municipio
    emitente.municipio = dados.emitente_municipio
    emitente.uf = dados.emitente_uf
    emitente.cep = dados.emitente_cep
    emitente.logradouro = dados.emitente_logradouro
    emitente.bairro = dados.emitente_bairro
    emitente.pais = dados.emitente_pais
    emitente.codigo_pais = "1058"
    emitente.regime_tributario = dados.emitente_regime_tributario

    cliente = Cliente()
    cliente._fonte_dados = fonte
    cliente.razao_social = dados.cliente_nome_razao_social
    cliente.cpf = dados.cliente_cpf_cnj
    cliente.inscricao_estadual = dados.cliente_inscricao_estadual
    cliente.logradouro = dados.cliente_logradouro
    cliente.bairro = dados.cliente_bairro
    cliente.municipio = dados.cliente_municipio
    cliente.codigo_municipio = dados.cliente_codigo_municipal
    cliente.uf = dados.cliente_uf
    cliente.cep = dados.cliente_cep
    cliente.pais = dados.cliente_pais
    cliente.codigo_pais = "1058"
    cliente.indicador_ie = dados.cliente_indicador_ie

    nota = NotaFiscal()
    nota._fonte_dados = fonte
    nota.emitente = emitente
    nota.cliente = cliente
    nota.numero = numero_da_nota
    nota.serie = numero_da_nota
    nota.tipo_documento = 1
    nota.natureza_operacao = "VENDA DE MERCADORIA"
    nota.forma_emissao = 1
    nota.finalidade_emissao = 1
    nota.tipo_impressao = 1
    nota.tipo_ambiente = 2
    nota.local_destino = 1
    nota.indicador_destino = 1
    nota.data_emissao = datetime.now()
    nota.data_saida_entrada = datetime.now()
    nota.municipio_ocorrencia = dados.emitente_municipio
    nota.uf_ocorrencia = dados.emitente_uf
    nota.codigo_municipio =dados.emitente_codigo_municipal
    nota.forma_pagamento = dados.nota_forma_de_pagamento
    nota.modalidade_frete = dados.nota_modalidade_frete
    nota.informacoes_adicionais = dados.nota_informacoes_adicionais

    valor_total_bruto = dados.produto_quantidade * dados.produto_valor_unitario
    valor_icms = valor_total_bruto * dados.produto_aliquoya_icms

    nota.adicionar_produto_servico(
        codigo= dados.produto_codigo,
        descricao=dados.descricao,
        ncm=dados.produto_ncm,
        cest=dados.produto_cest,
        cfop=dados.produto_cfop,
        unidade_comercial=dados.produto_unidade_comercial,
        quantidade_comercial=dados.produto_quantidade,
        valor_unitario_comercial=dados.produto_valor_unitario_comercial,
        valor_total_bruto= valor_total_bruto,
        unidade_tributavel=dados.produto_unidade_comercial,
        quantidade_tributavel=dados.produto_quantidade,
        valor_unitario_tributavel=dados.produto_valor_unitario_comercial,
        ean="SEM GTIN" or dados.produto_ean,
        ean_tributavel="SEM GTIN" or dados.produto_ean,
        indicador_total=1,
        origem_produto=0,
        modalidade_bc_icms=3,
        aliquota_icms=dados.produto_aliquota_icms,
        valor_icms= valor_icms,
        cst_pis="07",
        aliquota_pis=dados.produto_aliquota_pis,
        valor_pis=Decimal("0.00"),
        cst_cofins="07",
        aliquota_cofins=dados.produto_aliquota_cofins,
        valor_cofins=Decimal("0.00"),
    )


#serializador = SerializacaoXML(fonte, homologacao=True)
#xml = serializador.exportar()

#assinatura = AssinaturaA1()
#xml_assinado = assinatura.assinar(xml)

#cliente_ws = ClienteNFe(
#    uf           = "PA",
#    homologacao  = True,
#   certificado  = assinatura,
#)
