# ===============================
# IMPORTAÇÕES
# ===============================

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


# ===============================
# CONFIGURAÇÕES GERAIS
# ===============================

PLANILHA_NOME = "Banco de dados"

st.set_page_config(page_title="Sistema de Consultoria", page_icon="🧠")


# ===============================
# CONEXÃO COM GOOGLE SHEETS
# ===============================

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["google_credentials"],
    scopes=scope
)

client = gspread.authorize(creds)

planilha = client.open(PLANILHA_NOME)

aba_usuarios = planilha.worksheet("USUARIOS")
aba_formulario = planilha.sheet1


# ===============================
# CAMPOS DO FORMULÁRIO
# ===============================

CAMPOS = [
    "Cliente",
    "O que você pensa a seu respeito?",
    "Como foi o seu primeiro relacionamento amoroso?",
    "Qual papel você exerce na vida hoje?",
    "Vítima ou Responsável?",
    "Qual o ganho secundário?",
    "Em quais situações você desempenha o papel de vítima?",
    "Em quais situações você desempenha o papel de responsável?",
    "Se considera vitoriosa(o) ou derrotada(o)?",
    "Perfil nos relacionamentos",
    "Quem é o culpado pelos seus problemas?",
    "Sente raiva ou rancor de alguém?",
    "Raiva direcionada a quem?",
    "Sente-se pressionada(o)?",
    "De que maneira se sente pressionada(o)?",
    "Você se acha uma pessoa controladora?",
    "Sente-se inferior aos outros?",
    "Por que se sente inferior?",
    "Raiva",
    "Medo",
    "Culpa",
    "Tristeza",
    "Ansiedade",
    "Ciúme",
    "Frustração",
    "Solidão",
    "Cansaço"
]


# ===============================
# TELA DE LOGIN (SEU CÓDIGO)
# ===============================

def tela_login():

    st.title("🔐 Login do Sistema")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        usuarios = aba_usuarios.get_all_records()

        for usuario in usuarios:

            usuario_planilha = str(usuario["usuario"]).strip().lower()
            senha_planilha = str(usuario["senha"]).strip()
            tipo_usuario = str(usuario["tipo"]).strip().lower()

            if username.strip().lower() == usuario_planilha and password.strip() == senha_planilha:

                st.session_state["logado"] = True
                st.session_state["usuario"] = usuario_planilha
                st.session_state["tipo"] = tipo_usuario
                st.session_state["pagina"] = "home"
                return

        st.error("Usuário ou senha inválidos")


# ===============================
# ÁREA DO CLIENTE
# ===============================

def tela_cliente():

    st.title("👤 Área do Cliente")
    st.write(f"Bem-vindo, {st.session_state['usuario']}")

    if st.button("📝 Formulário de Avaliação Pessoal"):
        st.session_state["pagina"] = "formulario"


# ===============================
# FORMULÁRIO DE AVALIAÇÃO
# ===============================

def tela_formulario():

    st.title("📝 Formulário de Avaliação Pessoal")
    st.write("Responda com sinceridade. Não existem respostas certas ou erradas.")

    respostas = {campo: "" for campo in CAMPOS}
    respostas["Cliente"] = st.session_state["usuario"]

    respostas[CAMPOS[1]] = st.text_area(CAMPOS[1])
    respostas[CAMPOS[2]] = st.text_area(CAMPOS[2])
    respostas[CAMPOS[3]] = st.text_area("Se você avaliasse sua atuação na vida, qual papel caberia a você hoje?")

    papel = st.radio("Você se vê mais como:", ["Vítima", "Responsável"])
    respostas[CAMPOS[4]] = papel

    if papel == "Vítima":
        respostas[CAMPOS[5]] = st.text_area(CAMPOS[5])
        respostas[CAMPOS[6]] = st.text_area(CAMPOS[6])
    else:
        respostas[CAMPOS[7]] = st.text_area(CAMPOS[7])

    respostas[CAMPOS[8]] = st.radio(CAMPOS[8], ["Vitoriosa(o)", "Derrotada(o)"])
    respostas[CAMPOS[9]] = st.radio("Nos relacionamentos você tende a ser:", ["Dominante", "Submisso"])
    respostas[CAMPOS[10]] = st.text_area(CAMPOS[10])

    raiva = st.radio(CAMPOS[11], ["Não", "Sim"])
    respostas[CAMPOS[11]] = raiva

    if raiva == "Sim":
        respostas[CAMPOS[12]] = st.text_input(CAMPOS[12])

    pressao = st.radio(CAMPOS[13], ["Não", "Sim"])
    respostas[CAMPOS[13]] = pressao

    if pressao == "Sim":
        respostas[CAMPOS[14]] = st.text_area(CAMPOS[14])

    respostas[CAMPOS[15]] = st.radio(CAMPOS[15], ["Sim", "Não"])

    inferior = st.radio(CAMPOS[16], ["Não", "Sim"])
    respostas[CAMPOS[16]] = inferior

    if inferior == "Sim":
        respostas[CAMPOS[17]] = st.text_area(CAMPOS[17])

    for emocao in CAMPOS[18:]:
        respostas[emocao] = st.selectbox(
            emocao,
            ["Não sinto", "Pouca intensidade", "Média intensidade", "Muita intensidade"]
        )

    if st.button("Enviar formulário"):

        if not aba_formulario.row_values(1):
            aba_formulario.append_row(CAMPOS)

        aba_formulario.append_row([respostas[campo] for campo in CAMPOS])

        st.success("Formulário enviado com sucesso!")
        st.session_state["pagina"] = "home"


# ===============================
# PAINEL DO CONSULTOR
# ===============================

def tela_mestre():

    st.title("🧠 Painel do Consultor")
    st.write("Aqui você terá acesso aos clientes e formulários.")


# ===============================
# CONTROLE DE NAVEGAÇÃO
# ===============================

if "logado" not in st.session_state:
    st.session_state["logado"] = False

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"

if not st.session_state["logado"]:
    tela_login()

else:
    if st.session_state["tipo"] == "cliente":

        if st.session_state["pagina"] == "home":
            tela_cliente()

        elif st.session_state["pagina"] == "formulario":
            tela_formulario()

    elif st.session_state["tipo"] == "mestre":
        tela_mestre()
