import re
import hashlib
from datetime import datetime

from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime
)
from sqlalchemy.orm import declarative_base, sessionmaker



engine = create_engine("sqlite:///cpr.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# ─────────────────────────────────────────────
#  Modelos ORM
# ─────────────────────────────────────────────
class Cliente(Base):
    __tablename__ = "clientes"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    nome          = Column(String(150), nullable=False)
    cpf           = Column(String(11),  nullable=False, unique=True)
    nascimento    = Column(String(10),  nullable=False)   # DD/MM/AAAA
    senha_hash    = Column(String(64),  nullable=False)
    email         = Column(String(100), nullable=False)
    telefone      = Column(String(11),  nullable=False)
    cep           = Column(String(9),   nullable=False)
    estado        = Column(String(2),   nullable=False)
    cidade        = Column(String(100), nullable=False)
    bairro        = Column(String(100), nullable=False)
    rua           = Column(String(150), nullable=False)
    cadastrado_em = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Cliente id={self.id} nome='{self.nome}' cpf='{self.cpf}'>"


class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    nome          = Column(String(150), nullable=False)
    cnpj          = Column(String(14),  nullable=False, unique=True)
    email         = Column(String(100), nullable=False)
    telefone      = Column(String(11),  nullable=False)
    cadastrado_em = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Fornecedor id={self.id} nome='{self.nome}' cnpj='{self.cnpj}'>"


# Cria as tabelas se não existirem
Base.metadata.create_all(engine)


# ─────────────────────────────────────────────
#  Utilitários de validação
# ─────────────────────────────────────────────
def _hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def _so_digitos(valor: str) -> str:
    return re.sub(r"\D", "", valor)


def _validar_cpf(cpf: str) -> bool:
    cpf = _so_digitos(cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * (i + 1 - j) for j in range(i))
        if (soma * 10 % 11) % 10 != int(cpf[i]):
            return False
    return True


def _validar_cnpj(cnpj: str) -> bool:
    cnpj = _so_digitos(cnpj)
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1
    for i, pesos in enumerate([pesos1, pesos2]):
        soma = sum(int(cnpj[j]) * pesos[j] for j in range(len(pesos)))
        resto = soma % 11
        digito = 0 if resto < 2 else 11 - resto
        if digito != int(cnpj[12 + i]):
            return False
    return True


def _validar_data(data: str) -> bool:
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def _validar_email(email: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email))


def _validar_telefone(tel: str) -> bool:
    return len(_so_digitos(tel)) in (10, 11)


def _validar_cep(cep: str) -> bool:
    return bool(re.match(r"^\d{5}-?\d{3}$", cep))


# ─────────────────────────────────────────────
#  Utilitários de entrada
# ─────────────────────────────────────────────
def _input_validado(prompt: str, validar_fn, msg_erro: str) -> str:
    while True:
        valor = input(prompt).strip()
        if validar_fn(valor):
            return valor
        print(f"  ✗ {msg_erro}")


def _input_nao_vazio(prompt: str) -> str:
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        print("  ✗ Campo obrigatório.")


# ─────────────────────────────────────────────
#  Utilitários de formatação
# ─────────────────────────────────────────────
def _fmt_cpf(cpf: str) -> str:
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}" if len(cpf) == 11 else cpf


def _fmt_cnpj(cnpj: str) -> str:
    return (f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
            if len(cnpj) == 14 else cnpj)


def _fmt_tel(tel: str) -> str:
    if len(tel) == 11:
        return f"({tel[:2]}) {tel[2:7]}-{tel[7:]}"
    if len(tel) == 10:
        return f"({tel[:2]}) {tel[2:6]}-{tel[6:]}"
    return tel


# ─────────────────────────────────────────────
#  CADASTRO DE CLIENTE
# ─────────────────────────────────────────────


def cadastrar_cliente() -> None:
    print("\n" + "═" * 50)
    print("  CADASTRO DE CLIENTE")
    print("═" * 50)

    session = Session()
    try:
        nome = _input_nao_vazio("Nome completo............: ")

        cpf = _so_digitos(_input_validado(
            "CPF (somente números)....: ",
            _validar_cpf,
            "CPF inválido. Informe 11 dígitos válidos."
        ))
        if session.query(Cliente).filter_by(cpf=cpf).first():
            print("  ✗ CPF já cadastrado!")
            return

        nascimento = _input_validado(
            "Data de nascimento (DD/MM/AAAA): ",
            _validar_data,
            "Data inválida. Use DD/MM/AAAA."
        )

        while True:
            senha = input("Senha (mín. 6 caracteres): ").strip()
            if len(senha) >= 6:
                break
            print("  ✗ A senha deve ter pelo menos 6 caracteres.")

        email = _input_validado(
            "E-mail...................: ",
            _validar_email,
            "E-mail inválido."
        )

        telefone = _so_digitos(_input_validado(
            "Telefone pessoal.........: ",
            _validar_telefone,
            "Telefone inválido. Informe DDD + número."
        ))

        cep = _input_validado(
            "CEP (XXXXX-XXX)..........: ",
            _validar_cep,
            "CEP inválido."
        )

        estado = _input_nao_vazio("Estado (UF)..............: ").upper()[:2]
        cidade = _input_nao_vazio("Cidade...................: ")
        bairro = _input_nao_vazio("Bairro...................: ")
        rua    = _input_nao_vazio("Rua......................: ")

        cliente = Cliente(
            nome=nome,
            cpf=cpf,
            nascimento=nascimento,
            senha_hash=_hash_senha(senha),
            email=email,
            telefone=telefone,
            cep=cep,
            estado=estado,
            cidade=cidade,
            bairro=bairro,
            rua=rua,
        )
        session.add(cliente)
        session.commit()
        print(f"\n  ✔ Cliente cadastrado com sucesso! (ID: {cliente.id})")

    except Exception as e:
        session.rollback()
        print(f"  ✗ Erro ao cadastrar cliente: {e}")
    finally:
        session.close()


# ─────────────────────────────────────────────
#  CADASTRO DE FORNECEDOR
# ─────────────────────────────────────────────
def cadastrar_fornecedor() -> None:
    print("\n" + "═" * 50)
    print("  CADASTRO DE FORNECEDOR")
    print("═" * 50)

    session = Session()
    try:
        nome = _input_nao_vazio("Nome oficial.............: ")

        cnpj = _so_digitos(_input_validado(
            "CNPJ (somente números)...: ",
            _validar_cnpj,
            "CNPJ inválido. Informe 14 dígitos válidos."
        ))
        if session.query(Fornecedor).filter_by(cnpj=cnpj).first():
            print("  ✗ CNPJ já cadastrado!")
            return

        email = _input_validado(
            "E-mail...................: ",
            _validar_email,
            "E-mail inválido."
        )

        telefone = _so_digitos(_input_validado(
            "Telefone.................: ",
            _validar_telefone,
            "Telefone inválido. Informe DDD + número."
        ))

        fornecedor = Fornecedor(
            nome=nome,
            cnpj=cnpj,
            email=email,
            telefone=telefone,
        )
        session.add(fornecedor)
        session.commit()
        print(f"\n  ✔ Fornecedor cadastrado com sucesso! (ID: {fornecedor.id})")

    except Exception as e:
        session.rollback()
        print(f"  ✗ Erro: {e}")
    finally:
        session.close()




# ─────────────────────────────────────────────
#  LISTAGENS
# ─────────────────────────────────────────────
def listar_clientes() -> None:
    session = Session()
    try:
        clientes = session.query(Cliente).order_by(Cliente.nome).all()
        print("\n" + "═" * 50)
        print(f"  CLIENTES CADASTRADOS ({len(clientes)})")
        print("═" * 50)
        if not clientes:
            print("  Nenhum cliente cadastrado.")
            return
        for c in clientes:
            dt = c.cadastrado_em.strftime("%d/%m/%Y %H:%M") if c.cadastrado_em else "-"
            print(f"\n  [ID {c.id}] {c.nome}")
            print(f"      CPF      : {_fmt_cpf(c.cpf)}")
            print(f"      Nasc.    : {c.nascimento}")
            print(f"      E-mail   : {c.email}")
            print(f"      Telefone : {_fmt_tel(c.telefone)}")
            print(f"      Endereço : {c.rua}, {c.bairro} — {c.cidade}/{c.estado}")
            print(f"      CEP      : {c.cep}")
            print(f"      Cadastro : {dt}")
    finally:
        session.close()


def listar_fornecedores() -> None:
    session = Session()
    try:
        fornecedores = session.query(Fornecedor).order_by(Fornecedor.nome).all()
        print("\n" + "═" * 50)
        print(f"  FORNECEDORES CADASTRADOS ({len(fornecedores)})")
        print("═" * 50)
        if not fornecedores:
            print("  Nenhum fornecedor cadastrado.")
            return
        for f in fornecedores:
            dt = f.cadastrado_em.strftime("%d/%m/%Y %H:%M") if f.cadastrado_em else "-"
            print(f"\n  [ID {f.id}] {f.nome}")
            print(f"      CNPJ     : {_fmt_cnpj(f.cnpj)}")
            print(f"      E-mail   : {f.email}")
            print(f"      Telefone : {_fmt_tel(f.telefone)}")
            print(f"      Cadastro : {dt}")
    finally:
        session.close()


# ─────────────────────────────────────────────
#  BUSCA
# ─────────────────────────────────────────────
def buscar_cliente() -> None:
    termo = input("\nBuscar cliente (nome ou CPF): ").strip()
    session = Session()
    try:
        digitos = _so_digitos(termo)
        resultados = (
            session.query(Cliente)
            .filter(
                Cliente.nome.ilike(f"%{termo}%") |
                Cliente.cpf.contains(digitos)
            )
            .all()
        )
        if not resultados:
            print("  Nenhum cliente encontrado.")
            return
        for c in resultados:
            print(f"\n  ✔ [ID {c.id}] {c.nome} | CPF: {_fmt_cpf(c.cpf)} | {c.email}")
    finally:
        session.close()


def buscar_fornecedor() -> None:
    termo = input("\nBuscar fornecedor (nome ou CNPJ): ").strip()
    session = Session()
    try:
        digitos = _so_digitos(termo)
        resultados = (
            session.query(Fornecedor)
            .filter(
                Fornecedor.nome.ilike(f"%{termo}%") |
                Fornecedor.cnpj.contains(digitos)
            )
            .all()
        )
        if not resultados:
            print("  Nenhum fornecedor encontrado.")
            return
        for f in resultados:
            print(f"\n  ✔ [ID {f.id}] {f.nome} | CNPJ: {_fmt_cnpj(f.cnpj)} | {f.email}")
    finally:
        session.close()


# ─────────────────────────────────────────────
#  EXCLUSÃO
# ─────────────────────────────────────────────
def excluir_cliente() -> None:
    try:
        id_ = int(input("\nID do cliente a excluir: ").strip())
    except ValueError:
        print("  ✗ ID inválido.")
        return
    session = Session()
    try:
        cliente = session.get(Cliente, id_)
        if not cliente:
            print("  ✗ Cliente não encontrado.")
            return
        confirma = input(f"  Excluir '{cliente.nome}'? (s/N): ").strip().lower()
        if confirma == "s":
            session.delete(cliente)
            session.commit()
            print("  ✔ Cliente excluído.")
        else:
            print("  Operação cancelada.")
    except Exception as e:
        session.rollback()
        print(f"  ✗ Erro: {e}")
    finally:
        session.close()


def excluir_fornecedor() -> None:
    try:
        id_ = int(input("\nID do fornecedor a excluir: ").strip())
    except ValueError:
        print("  ✗ ID inválido.")
        return
    session = Session()
    try:
        fornecedor = session.get(Fornecedor, id_)
        if not fornecedor:
            print("  ✗ Fornecedor não encontrado.")
            return
        confirma = input(f"  Excluir '{fornecedor.nome}'? (s/N): ").strip().lower()
        if confirma == "s":
            session.delete(fornecedor)
            session.commit()
            print("  ✔ Fornecedor excluído.")
        else:
            print("  Operação cancelada.")
    except Exception as e:
        session.rollback()
        print(f"  ✗ Erro: {e}")
    finally:
        session.close()


# ─────────────────────────────────────────────
#  MENU PRINCIPAL
# ─────────────────────────────────────────────
def menu() -> None:
    opcoes = {
        "1": ("Cadastrar Cliente",       cadastrar_cliente),
        "2": ("Cadastrar Fornecedor",    cadastrar_fornecedor),
        "3": ("Listar Clientes",         listar_clientes),
        "4": ("Listar Fornecedores",     listar_fornecedores),
        "5": ("Buscar Cliente",          buscar_cliente),
        "6": ("Buscar Fornecedor",       buscar_fornecedor),
        "7": ("Excluir Cliente",         excluir_cliente),
        "8": ("Excluir Fornecedor",      excluir_fornecedor),
        "0": ("Sair",                    None),
    }

    while True:
        print("\n" + "╔" + "═" * 48 + "╗")
        print("║   SISTEMA CPR — Contas a Pagar e Receber      ║")
        print("║   Banco: SQLite via SQLAlchemy ORM            ║")
        print("╠" + "═" * 48 + "╣")
        for k, (desc, _) in opcoes.items():
            print(f"║   [{k}] {desc:<42}║")
        print("╚" + "═" * 48 + "╝")

        escolha = input("  Opção: ").strip()
        if escolha == "0":
            print("\n  Encerrando o sistema CPR. Até logo!\n")
            break
        if escolha in opcoes:
            opcoes[escolha][1]()
        else:
            print("  ✗ Opção inválida.")


# ─────────────────────────────────────────────
#  Ponto de entrada
# ─────────────────────────────────────────────
if __name__ == "__main__":
    menu()