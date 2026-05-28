servicos = [
    # ─── Banco do Brasil ────────────────────────────────────────────────────────
    {"nome_do_servico": "Conta Corrente Empresarial",         "prestador_do_servico_fornecedor": "00000000000191", "prestador_do_servico_usuario": None, "descricao_do_servico": "Conta corrente para PJ com gestão de fluxo de caixa e internet banking",                              "valor_do_servico": 89.90,     "categoria_do_servico": "Serviços Bancários"},
    {"nome_do_servico": "Crédito Rural BB",                   "prestador_do_servico_fornecedor": "00000000000191", "prestador_do_servico_usuario": None, "descricao_do_servico": "Financiamento para atividades agropecuárias com taxas subsidiadas do governo",                         "valor_do_servico": 0.0,       "categoria_do_servico": "Crédito"},

    # ─── Petrobras ──────────────────────────────────────────────────────────────
    {"nome_do_servico": "Fornecimento de GNL Industrial",     "prestador_do_servico_fornecedor": "33000167000101", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fornecimento de gás natural liquefeito para indústrias com contrato de longo prazo",                  "valor_do_servico": 12500.0,   "categoria_do_servico": "Energia"},
    {"nome_do_servico": "Lubrificantes Industriais Petrobras","prestador_do_servico_fornecedor": "33000167000101", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fornecimento de lubrificantes especializados para máquinas e equipamentos industriais",              "valor_do_servico": 3800.0,    "categoria_do_servico": "Energia"},

    # ─── Eletrobras ─────────────────────────────────────────────────────────────
    {"nome_do_servico": "Energia Elétrica em Alta Tensão",    "prestador_do_servico_fornecedor": "00001180000126", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fornecimento de energia em alta tensão para grandes consumidores industriais",                          "valor_do_servico": 45000.0,   "categoria_do_servico": "Energia Elétrica"},
    {"nome_do_servico": "Consultoria em Eficiência Energética","prestador_do_servico_fornecedor": "00001180000126","prestador_do_servico_usuario": None, "descricao_do_servico": "Análise, diagnóstico e otimização do consumo energético empresarial",                                  "valor_do_servico": 8500.0,    "categoria_do_servico": "Consultoria"},

    # ─── Energisa MT ────────────────────────────────────────────────────────────
    {"nome_do_servico": "Distribuição de Energia Elétrica MT","prestador_do_servico_fornecedor": "03467321000199", "prestador_do_servico_usuario": None, "descricao_do_servico": "Serviço de distribuição de energia elétrica no Mato Grosso para consumidores rurais e urbanos",      "valor_do_servico": 2300.0,    "categoria_do_servico": "Energia Elétrica"},

    # ─── RGE Sul ────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Distribuição de Energia Elétrica RS","prestador_do_servico_fornecedor": "02016440000162", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fornecimento e distribuição de energia elétrica no Rio Grande do Sul",                                 "valor_do_servico": 1950.0,    "categoria_do_servico": "Energia Elétrica"},

    # ─── CPFL Energia ───────────────────────────────────────────────────────────
    {"nome_do_servico": "Geração de Energia Solar CPFL",      "prestador_do_servico_fornecedor": "02429144000193", "prestador_do_servico_usuario": None, "descricao_do_servico": "Projeto, instalação e operação de usina fotovoltaica para empresas e indústrias",                     "valor_do_servico": 120000.0,  "categoria_do_servico": "Energia Solar"},
    {"nome_do_servico": "Manutenção de Infraestrutura Elétrica","prestador_do_servico_fornecedor": "02429144000193","prestador_do_servico_usuario": None,"descricao_do_servico": "Manutenção preventiva e corretiva de redes de distribuição e infraestrutura elétrica",              "valor_do_servico": 7500.0,    "categoria_do_servico": "Manutenção"},

    # ─── Energisa S/A ───────────────────────────────────────────────────────────
    {"nome_do_servico": "Conexão de Unidade Consumidora",     "prestador_do_servico_fornecedor": "00864214000106", "prestador_do_servico_usuario": None, "descricao_do_servico": "Serviço de ligação e conexão de nova unidade à rede de distribuição de energia",                     "valor_do_servico": 3200.0,    "categoria_do_servico": "Energia Elétrica"},

    # ─── CEMIG ──────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Mercado Livre de Energia CEMIG",     "prestador_do_servico_fornecedor": "17155730000164", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fornecimento de energia elétrica no mercado livre para grandes consumidores em MG",                   "valor_do_servico": 38000.0,   "categoria_do_servico": "Energia Elétrica"},
    {"nome_do_servico": "Vistoria de Instalações Elétricas",  "prestador_do_servico_fornecedor": "17155730000164", "prestador_do_servico_usuario": None, "descricao_do_servico": "Inspeção técnica e laudo de instalações elétricas prediais e industriais",                           "valor_do_servico": 1200.0,    "categoria_do_servico": "Inspeção"},

    # ─── COPEL ──────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Fornecimento de Energia Elétrica PR","prestador_do_servico_fornecedor": "76483817000120", "prestador_do_servico_usuario": None, "descricao_do_servico": "Distribuição de energia elétrica no Paraná para consumidores residenciais e industriais",            "valor_do_servico": 2700.0,    "categoria_do_servico": "Energia Elétrica"},

    # ─── SABESP ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Fornecimento de Água Industrial",    "prestador_do_servico_fornecedor": "43776517000180", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fornecimento de água tratada para uso industrial no estado de São Paulo",                            "valor_do_servico": 5600.0,    "categoria_do_servico": "Saneamento"},
    {"nome_do_servico": "Coleta e Tratamento de Esgoto",      "prestador_do_servico_fornecedor": "43776517000180", "prestador_do_servico_usuario": None, "descricao_do_servico": "Serviço de coleta, transporte e tratamento de esgoto sanitário para empresas",                      "valor_do_servico": 3200.0,    "categoria_do_servico": "Saneamento"},

    # ─── AES Tietê ──────────────────────────────────────────────────────────────
    {"nome_do_servico": "Comercialização de Energia Hidrelétrica","prestador_do_servico_fornecedor": "04128563000110","prestador_do_servico_usuario": None,"descricao_do_servico": "Comercialização de energia de origem hidrelétrica no mercado livre para empresas",              "valor_do_servico": 28000.0,   "categoria_do_servico": "Energia Elétrica"},

    # ─── COSAN ──────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Distribuição de Combustíveis a Granel","prestador_do_servico_fornecedor": "50746577000115","prestador_do_servico_usuario": None,"descricao_do_servico": "Fornecimento e logística de combustíveis para frotas empresariais e postos revendedores",           "valor_do_servico": 95000.0,   "categoria_do_servico": "Combustíveis"},

    # ─── Raízen ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Biocombustível Corporativo Raízen",  "prestador_do_servico_fornecedor": "08070508000178", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fornecimento de etanol e biocombustíveis para empresas com gestão de frota",                        "valor_do_servico": 42000.0,   "categoria_do_servico": "Combustíveis"},
    {"nome_do_servico": "Bioeletricidade para Indústrias",    "prestador_do_servico_fornecedor": "08070508000178", "prestador_do_servico_usuario": None, "descricao_do_servico": "Geração e fornecimento de bioeletricidade a partir do bagaço de cana-de-açúcar",                   "valor_do_servico": 18500.0,   "categoria_do_servico": "Energia"},

    # ─── Ultrapar ───────────────────────────────────────────────────────────────
    {"nome_do_servico": "Distribuição de GLP Industrial",     "prestador_do_servico_fornecedor": "33256439000139", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fornecimento e distribuição de GLP para uso industrial, comercial e residencial",                   "valor_do_servico": 15000.0,   "categoria_do_servico": "Combustíveis"},

    # ─── Vale ───────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Logística Ferroviária de Cargas Vale","prestador_do_servico_fornecedor": "33592510000154","prestador_do_servico_usuario": None,"descricao_do_servico": "Transporte de cargas pesadas por modal ferroviário nas malhas da Vale",                             "valor_do_servico": 75000.0,   "categoria_do_servico": "Logística Ferroviária"},
    {"nome_do_servico": "Fornecimento de Minério de Ferro",   "prestador_do_servico_fornecedor": "33592510000154", "prestador_do_servico_usuario": None, "descricao_do_servico": "Extração, beneficiamento e entrega de minério de ferro com 65% de pureza",                         "valor_do_servico": 320000.0,  "categoria_do_servico": "Mineração"},

    # ─── Gerdau ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Processamento de Sucata Metálica",   "prestador_do_servico_fornecedor": "33611500000119", "prestador_do_servico_usuario": None, "descricao_do_servico": "Coleta, triagem e reciclagem de sucata metálica industrial",                                         "valor_do_servico": 28000.0,   "categoria_do_servico": "Reciclagem"},
    {"nome_do_servico": "Corte e Dobra de Aço Estrutural",    "prestador_do_servico_fornecedor": "33611500000119", "prestador_do_servico_usuario": None, "descricao_do_servico": "Serviço de corte e dobra de barras de aço para construção civil sob medida",                       "valor_do_servico": 12500.0,   "categoria_do_servico": "Aço e Metais"},

    # ─── CSN ────────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Fornecimento de Aço Plano CSN",      "prestador_do_servico_fornecedor": "33042730000104", "prestador_do_servico_usuario": None, "descricao_do_servico": "Laminação e entrega de aço plano para indústria automotiva e de eletrodomésticos",                  "valor_do_servico": 145000.0,  "categoria_do_servico": "Aço e Metais"},

    # ─── Usiminas ───────────────────────────────────────────────────────────────
    {"nome_do_servico": "Serviço de Galvanização Usiminas",   "prestador_do_servico_fornecedor": "60894730000105", "prestador_do_servico_usuario": None, "descricao_do_servico": "Galvanização de chapas e estruturas metálicas para proteção contra corrosão",                      "valor_do_servico": 35000.0,   "categoria_do_servico": "Aço e Metais"},
    {"nome_do_servico": "Consultoria Metalúrgica",            "prestador_do_servico_fornecedor": "60894730000105", "prestador_do_servico_usuario": None, "descricao_do_servico": "Análise e especificação técnica de materiais metálicos para projetos industriais",                  "valor_do_servico": 9800.0,    "categoria_do_servico": "Consultoria"},

    # ─── Braskem ────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Fornecimento de Resinas Termoplásticas","prestador_do_servico_fornecedor": "42150391000170","prestador_do_servico_usuario": None,"descricao_do_servico": "Fornecimento de polipropileno e polietileno para indústria plástica e embalagens",              "valor_do_servico": 85000.0,   "categoria_do_servico": "Petroquímica"},

    # ─── Suzano ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Fornecimento de Celulose Suzano",    "prestador_do_servico_fornecedor": "16404287000155", "prestador_do_servico_usuario": None, "descricao_do_servico": "Celulose branqueada de eucalipto para produção de papel, tecido e embalagens sustentáveis",        "valor_do_servico": 95000.0,   "categoria_do_servico": "Papel e Celulose"},
    {"nome_do_servico": "Consultoria em Gestão Florestal",    "prestador_do_servico_fornecedor": "16404287000155", "prestador_do_servico_usuario": None, "descricao_do_servico": "Planejamento e manejo sustentável de áreas de reflorestamento de eucalipto",                       "valor_do_servico": 22000.0,   "categoria_do_servico": "Consultoria Ambiental"},

    # ─── Itaú Unibanco ──────────────────────────────────────────────────────────
    {"nome_do_servico": "Gestão de Folha de Pagamento Itaú",  "prestador_do_servico_fornecedor": "60701190000104", "prestador_do_servico_usuario": None, "descricao_do_servico": "Processamento e pagamento automatizado de folha salarial empresarial",                              "valor_do_servico": 450.0,     "categoria_do_servico": "Serviços Bancários"},
    {"nome_do_servico": "Câmbio Corporativo Itaú",            "prestador_do_servico_fornecedor": "60701190000104", "prestador_do_servico_usuario": None, "descricao_do_servico": "Operações de câmbio para importação e exportação corporativa com hedge cambial",                   "valor_do_servico": 1200.0,    "categoria_do_servico": "Câmbio"},

    # ─── Bradesco ───────────────────────────────────────────────────────────────
    {"nome_do_servico": "Seguros Empresariais Bradesco",      "prestador_do_servico_fornecedor": "60746948000112", "prestador_do_servico_usuario": None, "descricao_do_servico": "Pacote de seguros para empresas com cobertura de patrimônio e responsabilidade civil",              "valor_do_servico": 3500.0,    "categoria_do_servico": "Seguros"},
    {"nome_do_servico": "Antecipação de Recebíveis Bradesco", "prestador_do_servico_fornecedor": "60746948000112", "prestador_do_servico_usuario": None, "descricao_do_servico": "Desconto de duplicatas e antecipação de recebíveis para capital de giro",                          "valor_do_servico": 0.0,       "categoria_do_servico": "Crédito"},

    # ─── Caixa Econômica Federal ────────────────────────────────────────────────
    {"nome_do_servico": "Financiamento Habitacional MCMV",    "prestador_do_servico_fornecedor": "00360305000104", "prestador_do_servico_usuario": None, "descricao_do_servico": "Financiamento imobiliário pelo programa Minha Casa Minha Vida com taxas subsidiadas",               "valor_do_servico": 0.0,       "categoria_do_servico": "Crédito Imobiliário"},
    {"nome_do_servico": "Gestão do FGTS Empresarial",         "prestador_do_servico_fornecedor": "00360305000104", "prestador_do_servico_usuario": None, "descricao_do_servico": "Processamento e gestão de recolhimento do FGTS dos funcionários da empresa",                        "valor_do_servico": 120.0,     "categoria_do_servico": "Serviços Bancários"},

    # ─── Santander ──────────────────────────────────────────────────────────────
    {"nome_do_servico": "Maquininha POS Santander",           "prestador_do_servico_fornecedor": "90400888000142", "prestador_do_servico_usuario": None, "descricao_do_servico": "Terminal de pagamento com chip e NFC para estabelecimentos comerciais com tarifas competitivas",    "valor_do_servico": 89.0,      "categoria_do_servico": "Pagamentos"},
    {"nome_do_servico": "Crédito para Capital de Giro",       "prestador_do_servico_fornecedor": "90400888000142", "prestador_do_servico_usuario": None, "descricao_do_servico": "Linha de crédito empresarial para capital de giro e investimento com prazo flexível",              "valor_do_servico": 0.0,       "categoria_do_servico": "Crédito"},

    # ─── BTG Pactual ────────────────────────────────────────────────────────────
    {"nome_do_servico": "Gestão de Patrimônio BTG",           "prestador_do_servico_fornecedor": "30306294000145", "prestador_do_servico_usuario": None, "descricao_do_servico": "Gestão de investimentos e patrimônio para empresas e pessoas físicas de alta renda",                "valor_do_servico": 5000.0,    "categoria_do_servico": "Gestão de Patrimônio"},
    {"nome_do_servico": "Investment Banking BTG",             "prestador_do_servico_fornecedor": "30306294000145", "prestador_do_servico_usuario": None, "descricao_do_servico": "Assessoria em fusões, aquisições e emissão de debêntures e CRIs",                                  "valor_do_servico": 0.0,       "categoria_do_servico": "Banco de Investimento"},

    # ─── XP Investimentos ───────────────────────────────────────────────────────
    {"nome_do_servico": "Corretagem de Valores XP",           "prestador_do_servico_fornecedor": "02332886000104", "prestador_do_servico_usuario": None, "descricao_do_servico": "Intermediação na compra e venda de ações, fundos e renda fixa na B3",                              "valor_do_servico": 0.0,       "categoria_do_servico": "Investimentos"},
    {"nome_do_servico": "Previdência Privada XP",             "prestador_do_servico_fornecedor": "02332886000104", "prestador_do_servico_usuario": None, "descricao_do_servico": "PGBL e VGBL com gestão ativa e passiva para planejamento de aposentadoria",                        "valor_do_servico": 500.0,     "categoria_do_servico": "Previdência"},

    # ─── Nubank ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Conta Digital PJ Nubank",            "prestador_do_servico_fornecedor": "18236120000158", "prestador_do_servico_usuario": None, "descricao_do_servico": "Conta digital para pessoas jurídicas sem tarifas mensais com rendimento automático",               "valor_do_servico": 0.0,       "categoria_do_servico": "Serviços Bancários"},
    {"nome_do_servico": "Cartão Corporativo Nubank",          "prestador_do_servico_fornecedor": "18236120000158", "prestador_do_servico_usuario": None, "descricao_do_servico": "Cartão de crédito corporativo com gestão de despesas em tempo real pelo app",                      "valor_do_servico": 49.0,      "categoria_do_servico": "Pagamentos"},

    # ─── B3 ─────────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Custódia de Valores Mobiliários",    "prestador_do_servico_fornecedor": "09346601000125", "prestador_do_servico_usuario": None, "descricao_do_servico": "Guarda e administração centralizada de títulos e valores mobiliários",                              "valor_do_servico": 1500.0,    "categoria_do_servico": "Mercado de Capitais"},
    {"nome_do_servico": "Liquidação de Operações B3",         "prestador_do_servico_fornecedor": "09346601000125", "prestador_do_servico_usuario": None, "descricao_do_servico": "Compensação e liquidação de operações no mercado financeiro e de capitais",                        "valor_do_servico": 850.0,     "categoria_do_servico": "Mercado de Capitais"},

    # ─── Porto Seguro ───────────────────────────────────────────────────────────
    {"nome_do_servico": "Seguro Auto Porto Seguro",           "prestador_do_servico_fornecedor": "61198164000160", "prestador_do_servico_usuario": None, "descricao_do_servico": "Seguro completo para veículos com cobertura de colisão, roubo e assistência 24h",                  "valor_do_servico": 2800.0,    "categoria_do_servico": "Seguros"},
    {"nome_do_servico": "Seguro Residencial Porto Seguro",    "prestador_do_servico_fornecedor": "61198164000160", "prestador_do_servico_usuario": None, "descricao_do_servico": "Proteção residencial completa contra incêndio, roubo e danos elétricos",                           "valor_do_servico": 890.0,     "categoria_do_servico": "Seguros"},

    # ─── SulAmérica ─────────────────────────────────────────────────────────────
    {"nome_do_servico": "Plano de Saúde Empresarial SulAmérica","prestador_do_servico_fornecedor": "29978814000187","prestador_do_servico_usuario": None,"descricao_do_servico": "Plano de saúde coletivo empresarial com rede credenciada nacional e cobertura odontológica",     "valor_do_servico": 650.0,     "categoria_do_servico": "Saúde"},

    # ─── Ambev ──────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Fornecimento de Bebidas para Eventos","prestador_do_servico_fornecedor": "07526557000100","prestador_do_servico_usuario": None,"descricao_do_servico": "Fornecimento de bebidas em larga escala para eventos corporativos e festivais",                  "valor_do_servico": 18500.0,   "categoria_do_servico": "Bebidas"},
    {"nome_do_servico": "Locação de Chopeiras Ambev",         "prestador_do_servico_fornecedor": "07526557000100", "prestador_do_servico_usuario": None, "descricao_do_servico": "Locação, instalação e manutenção de chopeiras para bares e restaurantes parceiros",              "valor_do_servico": 350.0,     "categoria_do_servico": "Equipamentos"},

    # ─── JBS ────────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Proteína Animal para Food Service",  "prestador_do_servico_fornecedor": "02916265000160", "prestador_do_servico_usuario": None, "descricao_do_servico": "Cortes bovinos, suínos e aves para restaurantes, hotéis e hospitais com entrega refrigerada",     "valor_do_servico": 45000.0,   "categoria_do_servico": "Alimentos"},

    # ─── BRF ────────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Sadia/Perdigão para Food Service",   "prestador_do_servico_fornecedor": "01838723000127", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fornecimento de alimentos processados e congelados para cozinhas industriais e hospitais",        "valor_do_servico": 28000.0,   "categoria_do_servico": "Alimentos"},

    # ─── Marfrig ────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Exportação de Cortes Bovinos Marfrig","prestador_do_servico_fornecedor": "03853896000140","prestador_do_servico_usuario": None,"descricao_do_servico": "Processamento e exportação de cortes bovinos para mercados internacionais com rastreabilidade", "valor_do_servico": 380000.0,  "categoria_do_servico": "Alimentos"},

    # ─── M. Dias Branco ─────────────────────────────────────────────────────────
    {"nome_do_servico": "Massas e Biscoitos para Varejo",     "prestador_do_servico_fornecedor": "07206816000115", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fornecimento de massas, biscoitos e farinha para distribuidoras e redes de supermercados",        "valor_do_servico": 32000.0,   "categoria_do_servico": "Alimentos"},

    # ─── Camil ──────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Grãos Embalados para Supermercados", "prestador_do_servico_fornecedor": "64904295000103", "prestador_do_servico_usuario": None, "descricao_do_servico": "Distribuição de arroz, feijão e outros grãos embalados para redes varejistas",                    "valor_do_servico": 25000.0,   "categoria_do_servico": "Alimentos"},

    # ─── Magazine Luiza ─────────────────────────────────────────────────────────
    {"nome_do_servico": "Marketplace Magazine Luiza",         "prestador_do_servico_fornecedor": "47960950000121", "prestador_do_servico_usuario": None, "descricao_do_servico": "Plataforma de vendas online para lojistas com logística, pagamentos e publicidade integrados",    "valor_do_servico": 0.0,       "categoria_do_servico": "E-commerce"},
    {"nome_do_servico": "Magalu Ads",                         "prestador_do_servico_fornecedor": "47960950000121", "prestador_do_servico_usuario": None, "descricao_do_servico": "Serviço de publicidade e mídia paga dentro da plataforma Magazine Luiza para fornecedores",      "valor_do_servico": 1500.0,    "categoria_do_servico": "Publicidade"},

    # ─── Americanas ─────────────────────────────────────────────────────────────
    {"nome_do_servico": "Fulfillment Americanas",             "prestador_do_servico_fornecedor": "00776574000156", "prestador_do_servico_usuario": None, "descricao_do_servico": "Serviço de armazenagem e fulfillment para vendedores do marketplace Americanas",                  "valor_do_servico": 2200.0,    "categoria_do_servico": "Logística"},

    # ─── Grupo Pão de Açúcar ────────────────────────────────────────────────────
    {"nome_do_servico": "Espaço Promocional GPA",             "prestador_do_servico_fornecedor": "47508411000156", "prestador_do_servico_usuario": None, "descricao_do_servico": "Aluguel de espaço em gôndolas e pontos extras nas lojas do Grupo Pão de Açúcar",                  "valor_do_servico": 4500.0,    "categoria_do_servico": "Varejo"},

    # ─── Carrefour ──────────────────────────────────────────────────────────────
    {"nome_do_servico": "Cadastro de Fornecedores Carrefour", "prestador_do_servico_fornecedor": "45543915000181", "prestador_do_servico_usuario": None, "descricao_do_servico": "Processo de homologação e cadastramento de produtos para as lojas da rede Carrefour Brasil",      "valor_do_servico": 0.0,       "categoria_do_servico": "Varejo"},
    {"nome_do_servico": "Publicidade In-Store Carrefour",     "prestador_do_servico_fornecedor": "45543915000181", "prestador_do_servico_usuario": None, "descricao_do_servico": "Mídia dentro das lojas Carrefour: totens, TVs, displays e materiais de PDV",                      "valor_do_servico": 8900.0,    "categoria_do_servico": "Publicidade"},

    # ─── eBazar - Mercado Livre ─────────────────────────────────────────────────
    {"nome_do_servico": "Mercado Envios Full",                "prestador_do_servico_fornecedor": "03007331000141", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fulfillment do Mercado Livre com armazenagem nos CDs e envio automático ao comprador",            "valor_do_servico": 0.0,       "categoria_do_servico": "Logística"},
    {"nome_do_servico": "Mercado Pago Para Empresas",         "prestador_do_servico_fornecedor": "03007331000141", "prestador_do_servico_usuario": None, "descricao_do_servico": "Solução de pagamentos com maquininha, link de pagamento e checkout para e-commerce",             "valor_do_servico": 99.0,      "categoria_do_servico": "Pagamentos"},

    # ─── Raia Drogasil ──────────────────────────────────────────────────────────
    {"nome_do_servico": "Farmácia Corporativa RD",            "prestador_do_servico_fornecedor": "61585865000151", "prestador_do_servico_usuario": None, "descricao_do_servico": "Programa de benefício farmacêutico para funcionários com desconto na rede Raia e Drogasil",      "valor_do_servico": 250.0,     "categoria_do_servico": "Saúde"},

    # ─── Lojas Renner ───────────────────────────────────────────────────────────
    {"nome_do_servico": "Uniforme Corporativo Renner",        "prestador_do_servico_fornecedor": "92754738000162", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fornecimento de uniformes e fardamentos corporativos para empresas via cartão Renner",            "valor_do_servico": 0.0,       "categoria_do_servico": "Varejo"},

    # ─── Arezzo ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Franquia Arezzo",                    "prestador_do_servico_fornecedor": "16590234000176", "prestador_do_servico_usuario": None, "descricao_do_servico": "Modelo de franquia para abertura de loja da marca Arezzo com treinamento e suporte completo",     "valor_do_servico": 120000.0,  "categoria_do_servico": "Franquia"},

    # ─── Embraer ────────────────────────────────────────────────────────────────
    {"nome_do_servico": "MRO de Aeronaves Embraer",           "prestador_do_servico_fornecedor": "07689002000189", "prestador_do_servico_usuario": None, "descricao_do_servico": "Manutenção, reparo e revisão (MRO) de aeronaves comerciais e executivas Embraer",                "valor_do_servico": 480000.0,  "categoria_do_servico": "Aviação"},
    {"nome_do_servico": "Treinamento de Pilotos Embraer",     "prestador_do_servico_fornecedor": "07689002000189", "prestador_do_servico_usuario": None, "descricao_do_servico": "Capacitação e habilitação de pilotos em simuladores full-flight de aeronaves Embraer",           "valor_do_servico": 35000.0,   "categoria_do_servico": "Treinamento"},

    # ─── WEG ────────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Manutenção de Motores Elétricos WEG","prestador_do_servico_fornecedor": "84429695000111","prestador_do_servico_usuario": None,"descricao_do_servico": "Reparo, rebobinagem e manutenção preventiva de motores elétricos industriais WEG",              "valor_do_servico": 8500.0,    "categoria_do_servico": "Manutenção Industrial"},
    {"nome_do_servico": "Automação Industrial WEG",           "prestador_do_servico_fornecedor": "84429695000111", "prestador_do_servico_usuario": None, "descricao_do_servico": "Projeto e implantação de sistemas de automação com inversores de frequência e CLPs WEG",       "valor_do_servico": 45000.0,   "categoria_do_servico": "Automação"},

    # ─── TOTVS ──────────────────────────────────────────────────────────────────
    {"nome_do_servico": "ERP TOTVS Protheus",                 "prestador_do_servico_fornecedor": "53113791000122", "prestador_do_servico_usuario": None, "descricao_do_servico": "Licença e implantação do sistema ERP Protheus para gestão empresarial integrada",                "valor_do_servico": 15000.0,   "categoria_do_servico": "Software"},
    {"nome_do_servico": "Suporte Técnico TOTVS",              "prestador_do_servico_fornecedor": "53113791000122", "prestador_do_servico_usuario": None, "descricao_do_servico": "Atendimento técnico mensal para sistemas TOTVS com SLA de resposta garantido",                  "valor_do_servico": 3200.0,    "categoria_do_servico": "Suporte TI"},

    # ─── Telefônica / Vivo ──────────────────────────────────────────────────────
    {"nome_do_servico": "Internet Fibra Empresarial Vivo",    "prestador_do_servico_fornecedor": "02558157000162", "prestador_do_servico_usuario": None, "descricao_do_servico": "Conexão de internet por fibra óptica dedicada com SLA de uptime e IP fixo",                      "valor_do_servico": 1800.0,    "categoria_do_servico": "Telecomunicações"},
    {"nome_do_servico": "PABX em Nuvem Vivo",                 "prestador_do_servico_fornecedor": "02558157000162", "prestador_do_servico_usuario": None, "descricao_do_servico": "Telefonia empresarial em nuvem com ramais virtuais, URA e gravação de chamadas",               "valor_do_servico": 950.0,     "categoria_do_servico": "Telecomunicações"},

    # ─── TIM ────────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Plano Corporativo TIM",              "prestador_do_servico_fornecedor": "02421421000111", "prestador_do_servico_usuario": None, "descricao_do_servico": "Plano de telefonia móvel corporativo com dados ilimitados para frotas de funcionários",          "valor_do_servico": 89.0,      "categoria_do_servico": "Telecomunicações"},

    # ─── Claro ──────────────────────────────────────────────────────────────────
    {"nome_do_servico": "IoT Corporativo Claro",              "prestador_do_servico_fornecedor": "40432544000147", "prestador_do_servico_usuario": None, "descricao_do_servico": "Conectividade IoT para rastreamento de ativos, telemetria e monitoramento remoto de frota",     "valor_do_servico": 2500.0,    "categoria_do_servico": "Telecomunicações"},
    {"nome_do_servico": "Cloud Empresarial Claro",            "prestador_do_servico_fornecedor": "40432544000147", "prestador_do_servico_usuario": None, "descricao_do_servico": "Computação em nuvem, backup automático e hospedagem gerenciada para empresas",                  "valor_do_servico": 4200.0,    "categoria_do_servico": "Cloud"},

    # ─── Oi ─────────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Banda Larga Empresarial Oi",         "prestador_do_servico_fornecedor": "76535764000143", "prestador_do_servico_usuario": None, "descricao_do_servico": "Internet banda larga para pequenas empresas com suporte técnico incluso e roteador gerenciado",  "valor_do_servico": 350.0,     "categoria_do_servico": "Telecomunicações"},

    # ─── Positivo ───────────────────────────────────────────────────────────────
    {"nome_do_servico": "Computadores Corporativos Positivo", "prestador_do_servico_fornecedor": "81243735000148", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fornecimento de notebooks e desktops para empresas com garantia on-site estendida",             "valor_do_servico": 3200.0,    "categoria_do_servico": "Tecnologia"},
    {"nome_do_servico": "Suporte de TI Positivo",             "prestador_do_servico_fornecedor": "81243735000148", "prestador_do_servico_usuario": None, "descricao_do_servico": "Manutenção preventiva e corretiva de equipamentos de informática com contrato anual",           "valor_do_servico": 1500.0,    "categoria_do_servico": "Suporte TI"},

    # ─── Hapvida ────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Plano de Saúde Coletivo Hapvida",    "prestador_do_servico_fornecedor": "63554067000198", "prestador_do_servico_usuario": None, "descricao_do_servico": "Plano empresarial com hospitais e clínicas próprias no Nordeste e interior do Brasil",          "valor_do_servico": 420.0,     "categoria_do_servico": "Saúde"},
    {"nome_do_servico": "Telemedicina Hapvida",               "prestador_do_servico_fornecedor": "63554067000198", "prestador_do_servico_usuario": None, "descricao_do_servico": "Consultas médicas online para beneficiários com acesso 24h pelo aplicativo Hapvida",           "valor_do_servico": 80.0,      "categoria_do_servico": "Saúde Digital"},

    # ─── Hypera ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Medicamentos para Hospitais Hypera", "prestador_do_servico_fornecedor": "02932074000191", "prestador_do_servico_usuario": None, "descricao_do_servico": "Distribuição de medicamentos de referência para hospitais, clínicas e farmácias",               "valor_do_servico": 75000.0,   "categoria_do_servico": "Farmacêutico"},

    # ─── Fleury ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Exames Laboratoriais Corporativos",  "prestador_do_servico_fornecedor": "60840055000131", "prestador_do_servico_usuario": None, "descricao_do_servico": "Programa de exames periódicos para funcionários com coleta on-site e resultado digital",        "valor_do_servico": 280.0,     "categoria_do_servico": "Diagnóstico"},
    {"nome_do_servico": "Medicina Ocupacional Fleury",        "prestador_do_servico_fornecedor": "60840055000131", "prestador_do_servico_usuario": None, "descricao_do_servico": "Exames admissionais, periódicos e demissionais com emissão de ASO e relatórios PCMSO",         "valor_do_servico": 190.0,     "categoria_do_servico": "Saúde Ocupacional"},

    # ─── OdontoPrev ─────────────────────────────────────────────────────────────
    {"nome_do_servico": "Plano Odontológico Empresarial",     "prestador_do_servico_fornecedor": "58119199000151", "prestador_do_servico_usuario": None, "descricao_do_servico": "Benefício odontológico com cobertura de consultas, limpeza, restaurações e emergências",       "valor_do_servico": 89.0,      "categoria_do_servico": "Saúde"},

    # ─── Cogna ──────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Educação Corporativa Cogna",         "prestador_do_servico_fornecedor": "02800026000140", "prestador_do_servico_usuario": None, "descricao_do_servico": "Capacitação e treinamento corporativo com cursos presenciais e EAD para equipes",               "valor_do_servico": 1200.0,    "categoria_do_servico": "Educação"},
    {"nome_do_servico": "Plataforma EAD Cogna",               "prestador_do_servico_fornecedor": "02800026000140", "prestador_do_servico_usuario": None, "descricao_do_servico": "Licença de LMS educacional para universidades corporativas e instituições de ensino",          "valor_do_servico": 8500.0,    "categoria_do_servico": "EdTech"},

    # ─── Yduqs / Estácio ────────────────────────────────────────────────────────
    {"nome_do_servico": "Graduação EAD Estácio",              "prestador_do_servico_fornecedor": "08807432000110", "prestador_do_servico_usuario": None, "descricao_do_servico": "Graduação a distância em diversas áreas com tutoria online e material didático digital",        "valor_do_servico": 650.0,     "categoria_do_servico": "Educação"},

    # ─── Rumo ───────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Transporte Ferroviário de Grãos",    "prestador_do_servico_fornecedor": "02387241000160", "prestador_do_servico_usuario": None, "descricao_do_servico": "Transporte de grãos do Centro-Oeste ao porto de Santos por malha ferroviária Rumo",            "valor_do_servico": 120000.0,  "categoria_do_servico": "Logística Ferroviária"},

    # ─── Motiva ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Concessão de Rodovias Motiva",       "prestador_do_servico_fornecedor": "02846056000197", "prestador_do_servico_usuario": None, "descricao_do_servico": "Operação e manutenção de rodovias concedidas com pedágios e serviços de assistência ao usuário","valor_do_servico": 0.0,       "categoria_do_servico": "Infraestrutura"},

    # ─── EcoRodovias ────────────────────────────────────────────────────────────
    {"nome_do_servico": "Pedágio Eletrônico EcoRodovias",     "prestador_do_servico_fornecedor": "04149454000180", "prestador_do_servico_usuario": None, "descricao_do_servico": "Sistema de pedágio automático para frotas com fatura mensal consolidada por CNPJ",             "valor_do_servico": 450.0,     "categoria_do_servico": "Infraestrutura"},
    {"nome_do_servico": "Transporte de Cargas Especiais",     "prestador_do_servico_fornecedor": "04149454000180", "prestador_do_servico_usuario": None, "descricao_do_servico": "Coordenação logística para transporte de cargas indivisíveis e perigosas em rodovias",         "valor_do_servico": 18000.0,   "categoria_do_servico": "Logística"},

    # ─── JSL ────────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Transporte Rodoviário de Cargas JSL","prestador_do_servico_fornecedor": "52548435000179","prestador_do_servico_usuario": None,"descricao_do_servico": "Transporte de cargas fracionadas e lotação em todo o território nacional",                    "valor_do_servico": 35000.0,   "categoria_do_servico": "Logística"},

    # ─── Movida ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Aluguel de Frota Movida",            "prestador_do_servico_fornecedor": "21314559000166", "prestador_do_servico_usuario": None, "descricao_do_servico": "Locação de frota para empresas com gestão integrada, telemetria e manutenção inclusa",         "valor_do_servico": 1800.0,    "categoria_do_servico": "Locação de Veículos"},

    # ─── Localiza ───────────────────────────────────────────────────────────────
    {"nome_do_servico": "Gestão de Frotas Localiza",          "prestador_do_servico_fornecedor": "16670085000155", "prestador_do_servico_usuario": None, "descricao_do_servico": "Terceirização completa de frota corporativa com rastreamento GPS e relatórios gerenciais",      "valor_do_servico": 2500.0,    "categoria_do_servico": "Locação de Veículos"},
    {"nome_do_servico": "Aluguel Avulso de Veículos Localiza","prestador_do_servico_fornecedor": "16670085000155","prestador_do_servico_usuario": None,"descricao_do_servico": "Locação diária ou semanal de veículos para viagens corporativas em todo o Brasil",            "valor_do_servico": 220.0,     "categoria_do_servico": "Locação de Veículos"},

    # ─── Cyrela ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Incorporação Imobiliária Cyrela",    "prestador_do_servico_fornecedor": "73178600000118", "prestador_do_servico_usuario": None, "descricao_do_servico": "Desenvolvimento e venda de empreendimentos residenciais de alto padrão em SP",                 "valor_do_servico": 0.0,       "categoria_do_servico": "Construção Civil"},

    # ─── MRV ────────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Unidades Habitacionais MRV",         "prestador_do_servico_fornecedor": "08343492000120", "prestador_do_servico_usuario": None, "descricao_do_servico": "Construção e venda de unidades habitacionais populares com financiamento FGTS e MCMV",          "valor_do_servico": 0.0,       "categoria_do_servico": "Construção Civil"},

    # ─── EZ Tec ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Incorporação Residencial EZ Tec",    "prestador_do_servico_fornecedor": "08312229000173", "prestador_do_servico_usuario": None, "descricao_do_servico": "Lançamento e venda de apartamentos de médio e alto padrão na Grande São Paulo",               "valor_do_servico": 0.0,       "categoria_do_servico": "Construção Civil"},

    # ─── Construtora Tenda ──────────────────────────────────────────────────────
    {"nome_do_servico": "Habitação Popular Tenda",            "prestador_do_servico_fornecedor": "71476527000135", "prestador_do_servico_usuario": None, "descricao_do_servico": "Empreendimentos habitacionais populares dentro do programa Minha Casa Minha Vida",              "valor_do_servico": 0.0,       "categoria_do_servico": "Construção Civil"},

    # ─── Klabin ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Embalagens de Papelão Klabin",       "prestador_do_servico_fornecedor": "89637490000145", "prestador_do_servico_usuario": None, "descricao_do_servico": "Embalagens personalizadas de papelão ondulado e caixas para indústrias e e-commerce",          "valor_do_servico": 42000.0,   "categoria_do_servico": "Embalagens"},
    {"nome_do_servico": "Papel Kraft Industrial Klabin",      "prestador_do_servico_fornecedor": "89637490000145", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fornecimento de papel kraft em bobinas para uso industrial e confecção de embalagens",         "valor_do_servico": 28000.0,   "categoria_do_servico": "Papel e Celulose"},

    # ─── Natura ─────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Amenidades Natura para Hospedagem",  "prestador_do_servico_fornecedor": "71673990000177", "prestador_do_servico_usuario": None, "descricao_do_servico": "Linha de amenidades Natura para hotéis e pousadas com produtos 100% sustentáveis",             "valor_do_servico": 8500.0,    "categoria_do_servico": "Cosméticos"},
    {"nome_do_servico": "Bem-Estar Corporativo Natura",       "prestador_do_servico_fornecedor": "71673990000177", "prestador_do_servico_usuario": None, "descricao_do_servico": "Programa de bem-estar para empresas com kits de produtos de cuidado pessoal Natura",          "valor_do_servico": 3200.0,    "categoria_do_servico": "Bem-Estar"},

    # ─── GOL ────────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Passagens Corporativas GOL",         "prestador_do_servico_fornecedor": "06164253000187", "prestador_do_servico_usuario": None, "descricao_do_servico": "Programa de tarifas corporativas GOL com gestão centralizada de viagens aéreas",               "valor_do_servico": 980.0,     "categoria_do_servico": "Aviação"},
    {"nome_do_servico": "GOL Cargo",                          "prestador_do_servico_fornecedor": "06164253000187", "prestador_do_servico_usuario": None, "descricao_do_servico": "Serviço de carga aérea expressa em todo o Brasil via malha de voos da GOL",                   "valor_do_servico": 4500.0,    "categoria_do_servico": "Logística Aérea"},

    # ─── Azul ───────────────────────────────────────────────────────────────────
    {"nome_do_servico": "Azul Empresas",                      "prestador_do_servico_fornecedor": "09305994000129", "prestador_do_servico_usuario": None, "descricao_do_servico": "Tarifas especiais para empresas com acesso a destinos regionais exclusivos da malha Azul",     "valor_do_servico": 850.0,     "categoria_do_servico": "Aviação"},
    {"nome_do_servico": "Azul Cargo Express",                 "prestador_do_servico_fornecedor": "09305994000129", "prestador_do_servico_usuario": None, "descricao_do_servico": "Entrega expressa de encomendas por modal aéreo com rastreamento online em tempo real",        "valor_do_servico": 3800.0,    "categoria_do_servico": "Logística Aérea"},

    # ─── Iguatemi ───────────────────────────────────────────────────────────────
    {"nome_do_servico": "Locação Comercial Iguatemi",         "prestador_do_servico_fornecedor": "51218147000193", "prestador_do_servico_usuario": None, "descricao_do_servico": "Aluguel de lojas e quiosques em shopping centers premium da rede Iguatemi",                    "valor_do_servico": 25000.0,   "categoria_do_servico": "Imóveis Comerciais"},

    # ─── Marcopolo ──────────────────────────────────────────────────────────────
    {"nome_do_servico": "Manutenção de Ônibus Marcopolo",     "prestador_do_servico_fornecedor": "88611835000129", "prestador_do_servico_usuario": None, "descricao_do_servico": "Revisão, reparo e fornecimento de peças originais para carrocerias de ônibus Marcopolo",       "valor_do_servico": 22000.0,   "categoria_do_servico": "Transporte"},
    {"nome_do_servico": "Ônibus Especiais Sob Encomenda",     "prestador_do_servico_fornecedor": "88611835000129", "prestador_do_servico_usuario": None, "descricao_do_servico": "Fabricação de ônibus rodoviários e urbanos com especificações customizadas pelo cliente",      "valor_do_servico": 580000.0,  "categoria_do_servico": "Transporte"},
]

# Total de serviços
print(f"Total de serviços cadastrados: {len(servicos)}")

# Verificar quantos CNPJs únicos foram cobertos
cnpjs_cobertos = {s["prestador_do_servico_fornecedor"] for s in servicos}
print(f"CNPJs de fornecedores cobertos: {len(cnpjs_cobertos)}")