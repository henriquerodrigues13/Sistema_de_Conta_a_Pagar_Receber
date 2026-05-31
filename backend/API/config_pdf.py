from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Paragraph, Table, TableStyle, HRFlowable
)

# ── Cores ──────────────────────────────────────────────────────────────────
VERMELHO = colors.HexColor("#C0392B")
VERMELHO_E = colors.HexColor("#a93226")
CINZA_C = colors.HexColor("#ECECEC")
CINZA_E = colors.HexColor("#7F8C8D")
AMARELO = colors.HexColor("#F1C40F")
AMARELO_E = colors.HexColor("#d4ac0d")
BRANCO = colors.white
PRETO = colors.HexColor("#222222")
CINZA_T = colors.HexColor("#333333")


def estilo_cabecalho():
    return ParagraphStyle(
        "cabecalho",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=BRANCO,
        leading=16,
    )


def estilo_cabecalho_sub():
    return ParagraphStyle(
        "cabecalho_sub",
        fontName="Helvetica",
        fontSize=8.5,
        textColor=BRANCO,
        leading=12,
        alignment=TA_RIGHT,
    )


def estilo_secao():
    return ParagraphStyle(
        "secao",
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=VERMELHO,
        leading=16,
        spaceAfter=4,
        spaceBefore=14,
        textTransform="uppercase",
    )


def estilo_normal():
    return ParagraphStyle(
        "normal",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=CINZA_T,
        leading=13,
    )


def estilo_card_label():
    return ParagraphStyle(
        "card_label",
        fontName="Helvetica-Bold",
        fontSize=8.5,
        textColor=CINZA_E,
        alignment=TA_CENTER,
        leading=11,
        spaceAfter=3,
    )


def estilo_card_valor():
    return ParagraphStyle(
        "card_valor",
        fontName="Helvetica-Bold",
        fontSize=13,
        textColor=VERMELHO,
        alignment=TA_CENTER,
        leading=16,
    )


def estilo_card_sub():
    return ParagraphStyle(
        "card_sub",
        fontName="Helvetica",
        fontSize=8,
        textColor=CINZA_E,
        alignment=TA_CENTER,
        leading=10,
    )


def bloco_cabecalho(dados, largura):

    nome = dados.get("nome_sistema", "")
    tipo = f"Tipo: {dados.get('tipo_relatorio', '')}"

    data = [
        [
            Paragraph(nome, estilo_cabecalho()),
            Paragraph(f"{tipo}", estilo_cabecalho_sub()),
        ]
    ]
    t = Table(data, colWidths=[largura * 0.55, largura * 0.45])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERMELHO),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (0, -1), 10),
        ("RIGHTPADDING", (1, 0), (1, -1), 10),
    ]))
    return t


def bloco_identificacao(dados, largura):

    campos = [
        ("Nome Completo", dados.get("usuario_nome", "")),
        ("E-mail", dados.get("usuario_email", "")),
        ("Telefone", dados.get("usuario_telefone", "")),
        ("Cidade", dados.get("usuario_cidade", "")),
        ("Estado", dados.get("usuario_estado", "")),
    ]
    est = estilo_normal()
    est_bold = ParagraphStyle("nb", parent=est, fontName="Helvetica-Bold", textColor=CINZA_T)

    rows = [
        [Paragraph(label, est_bold), Paragraph(str(valor), est)]
        for label, valor in campos
    ]

    t = Table(rows, colWidths=[largura * 0.38, largura * 0.62])
    style = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (0, -1), CINZA_C),
    ]
    for i in range(0, len(rows), 2):
        style.append(("BACKGROUND", (1, i), (1, i), BRANCO))
    for i in range(1, len(rows), 2):
        style.append(("BACKGROUND", (1, i), (1, i), CINZA_C))

    t.setStyle(TableStyle(style))
    return t


def bloco_resumo(dados, largura):
    col = largura / 3

    def card(label, valor, sub):
        return [
            Paragraph(label.upper(), estilo_card_label()),
            Paragraph(str(valor), estilo_card_valor()),
            Paragraph(str(sub), estilo_card_sub()),
        ]

    qtd_rec = dados.get("qtd_receitas", "0")
    qtd_desp = dados.get("qtd_despesas", "0")
    status = dados.get("status_saldo", "")

    data = [[
        card("Receitas", dados.get("total_receitas", ""), f"{qtd_rec} lançamentos"),
        card("Despesas", dados.get("total_despesas", ""), f"{qtd_desp} lançamentos"),
        card("Saldo do Período", dados.get("saldo_periodo", ""), status),
    ]]

    t = Table(data, colWidths=[col, col, col])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CINZA_C),
        ("BOX", (0, 0), (0, 0), 0.5, colors.HexColor("#cccccc")),
        ("BOX", (1, 0), (1, 0), 0.5, colors.HexColor("#cccccc")),
        ("BOX", (2, 0), (2, 0), 0.5, colors.HexColor("#cccccc")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    return t


def tabela_dados(cabecalhos, linhas, totais, largura):
    """Tabela genérica com cabeçalho vermelho, linhas zebradas e rodapé amarelo."""
    est_th = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9,
                            textColor=BRANCO, leading=12)
    est_td = ParagraphStyle("td", fontName="Helvetica", fontSize=9,
                            textColor=CINZA_T, leading=12)
    est_tot = ParagraphStyle("tot", fontName="Helvetica-Bold", fontSize=9,
                             textColor=CINZA_T, leading=12)

    col_w = largura / len(cabecalhos)

    rows = [[Paragraph(h, est_th) for h in cabecalhos]]
    for linha in linhas:
        rows.append([Paragraph(str(c), est_td) for c in linha])
    rows.append([Paragraph(str(c), est_tot) for c in totais])

    t = Table(rows, colWidths=[col_w] * len(cabecalhos))

    style = [
        # Cabeçalho
        ("BACKGROUND", (0, 0), (-1, 0), VERMELHO),
        ("GRID", (0, 0), (-1, 0), 0.5, VERMELHO_E),
        # Rodapé
        ("BACKGROUND", (0, -1), (-1, -1), AMARELO),
        ("GRID", (0, -1), (-1, -1), 0.5, AMARELO_E),
        # Geral
        ("GRID", (0, 1), (-1, -2), 0.5, colors.HexColor("#dddddd")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    # Zebra
    for i in range(1, len(linhas) + 1):
        bg = BRANCO if i % 2 == 1 else CINZA_C
        style.append(("BACKGROUND", (0, i), (-1, i), bg))

    t.setStyle(TableStyle(style))
    return t


def titulo_secao(texto):
    return Paragraph(texto.upper(), estilo_secao())


def linha_secao(largura):
    return HRFlowable(width=largura, thickness=2, color=VERMELHO, spaceAfter=6)
