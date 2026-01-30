import streamlit as st
import gspread
from datetime import datetime

# =============================
# CONFIGURAÇÃO GOOGLE SHEETS
# =============================
gc = gspread.service_account_from_dict(
    st.secrets["google_credentials"]
)

PLANILHA = gc.open("Banco de dados")

ABA_USUARIOS = "USUARIOS"
ABA_FORM_1 = "FORMULÁRIO 1"

# =============================
# SESSION STATE (OBRIGATÓRIO)
# =============================
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"

if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

if "tipo_usuario" not in st.session_state:
    st.session_state["tipo_usuario"] = None

if "formulario_atual" not in st.session_state:
    st.session_state["formulario_atual"] = None

# =============================
# FUNÇÕES AUXILIARES
# =============================
def get_data_hoje():
    return datetime.now().strftime("%d/%m/%Y")


def ler_usuarios():
    aba = PLANILHA.worksheet(ABA_USUARIOS)
    dados = aba.get_all_records()
    return dados


def autenticar(login, senha):
    usuarios = ler_usuarios()
    for u in usuarios:
        if u["login"].strip().lower() == login.strip().lower() and str(u["senha"]) == str(senha):
            return u
    return None


def verificar_resposta_existente(cliente):
    aba = PLANILHA.worksheet(ABA_FORM_1)
    dados = aba.get_all_records()
    for linha in dados:
        if linha.get("Cliente") == cliente:
            return linha
    return None


def salvar_resposta_form1(resposta, editar=False):
    aba = PLANILHA.worksheet(ABA_FORM_1)

    CAMPOS = list(resposta.keys())

    if aba.row_count == 0 or aba.row_values(1) == []:
        aba.append_row(CAMPOS)

    dados = aba.get_all_records()

    if editar:
        for i, linha in enumerate(dados, start=2):
            if linha["Cliente"] == resposta["Cliente"]:
                aba.update(f"A{i}:{chr(64+len(CAMPOS))}{i}", [list(resposta.values())])
                return
    else:
        aba.append_row(list(resposta.values()))


# =============================
# TELAS
# =============================
def tela_login():
    st.title("Login")

    login = st.text_input("Login")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        user = autenticar(login, senha)
        if user:
            st.session_state["logado"] = True
            st.session_state["usuario"] = user["login"]
            st.session_state["tipo_usuario"] = user["tipo"]
            st.session_state["pagina"] = "home"
            st.rerun()
        else:
            st.error("Login ou senha inválidos")


def tela_home():
    st.title("Painel")

    st.write(f"Usuário: **{st.session_state['usuario']}**")

    if st.session_state["tipo_usuario"] == "cliente":
        if st.button("Formulário 1"):
            st.session_state["formulario_atual"] = "F1"
            st.session_state["pagina"] = "formulario"
            st.rerun()

    if st.button("Sair"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


def tela_formulario_f1():
    st.title("FORMULÁRIO 1")

    cliente = st.session_state["usuario"]
    resposta_existente = verificar_resposta_existente(cliente)

    editar = False
    if resposta_existente:
        st.warning("Você já respondeu este formulário.")
        editar = st.button("Editar respostas")

    if resposta_existente and not editar:
        st.info("Clique em **Editar respostas** para alterar.")
        return

    # =============================
    # CAMPOS DO FORMULÁRIO
    # =============================
    st.subheader("Dados Gerais")

    idade = st.number_input(
        "Idade",
        min_value=0,
        value=resposta_existente["Idade"] if resposta_existente else 0
    )

    humor = st.selectbox(
        "Como está se sentindo hoje?",
        ["", "Bem", "Normal", "Mal"],
        index=0 if not resposta_existente else ["", "Bem", "Normal", "Mal"].index(resposta_existente["Humor"])
    )

    raiva = st.radio(
        "Sente raiva de alguém?",
        ["Não", "Sim"],
        index=0 if not resposta_existente else ["Não", "Sim"].index(resposta_existente["Raiva"])
    )

    quem_raiva = ""
    if raiva == "Sim":
        quem_raiva = st.text_input(
            "De quem?",
            value=resposta_existente["Quem_raiva"] if resposta_existente else ""
        )

    # =============================
    # ENVIO
    # =============================
    if st.button("Enviar"):
        resposta = {
            "Cliente": cliente,
            "Data": get_data_hoje(),
            "Idade": idade,
            "Humor": humor,
            "Raiva": raiva,
            "Quem_raiva": quem_raiva
        }

        salvar_resposta_form1(resposta, editar=bool(resposta_existente))
        st.success("Resposta salva com sucesso!")
        st.session_state["pagina"] = "home"
        st.rerun()


# =============================
# ROTEAMENTO
# =============================
if not st.session_state["logado"]:
    tela_login()

elif st.session_state["pagina"] == "home":
    tela_home()

elif st.session_state["pagina"] == "formulario":
    if st.session_state.get("formulario_atual") == "F1":
        tela_formulario_f1()
