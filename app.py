# ===============================
# IMPORTAÇÕES
# ===============================

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime


# ===============================
# CONFIGURAÇÕES GERAIS
# ===============================

PLANILHA_NOME = "Banco de dados"

st.set_page_config(
    page_title="Sistema de Consultoria",
    page_icon="🧠"
)


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
aba_formularios = planilha.worksheet("FORMULÁRIOS")
aba_acessos = planilha.worksheet("ACESSOS")


# ===============================
# CAMPOS FORMULÁRIO 1
# ===============================

CAMPOS_F1 = [
    "Cliente", "Data",
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
    "Raiva", "Medo", "Culpa", "Tristeza",
    "Ansiedade", "Ciúme", "Frustração",
    "Solidão", "Cansaço"
]


# ===============================
# FUNÇÃO AUXILIAR
# ===============================

def buscar_resposta(aba, usuario):
    registros = aba.get_all_records()
    for i, linha in enumerate(registros, start=2):
        if linha.get("Cliente", "").strip().lower() == usuario:
            return i, linha
    return None, None


# ===============================
# LOGIN
# ===============================

def tela_login():

    st.title("🔐 Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        for u in aba_usuarios.get_all_records():
            if (
                usuario.strip().lower() == str(u.get("usuario", "")).strip().lower()
                and senha.strip() == str(u.get("senha", "")).strip()
            ):
                st.session_state.update({
                    "logado": True,
                    "usuario": usuario.strip().lower(),
                    "tipo": str(u.get("tipo", "")).strip().lower(),
                    "pagina": "home"
                })
                return

        st.error("Usuário ou senha inválidos")


# ===============================
# ÁREA DO CLIENTE
# ===============================

def tela_cliente():

    st.title("👤 Área do Cliente")
    st.write(f"Bem-vindo, **{st.session_state['usuario']}**")

    acessos = aba_acessos.get_all_records()
    formularios = aba_formularios.get_all_records()

    ids_liberados = [
        a.get("formulario_id")
        for a in acessos
        if a.get("usuario", "").strip().lower() == st.session_state["usuario"]
    ]

    liberados = [
        f for f in formularios
        if f.get("id") in ids_liberados
        and f.get("ativo", "").strip().lower() == "sim"
    ]

    st.subheader("📝 Formulários disponíveis")

    if not liberados:
        st.info("Nenhum formulário liberado para você.")
        return

    for f in liberados:
        if st.button(f.get("nome", "Formulário")):
            st.session_state["formulario_atual"] = f.get("id")
            st.session_state["pagina"] = "formulario"


# ===============================
# FORMULÁRIO 1
# ===============================

def tela_formulario_f1():

    aba = planilha.worksheet("FORMULÁRIO 1")

    st.title("📝 Avaliação Pessoal")

    usuario = st.session_state["usuario"]
    linha, dados = buscar_resposta(aba, usuario)

    respostas = {campo: "" for campo in CAMPOS_F1}
    if dados:
        respostas.update(dados)

    respostas["Cliente"] = usuario
    respostas["Data"] = datetime.now().strftime("%d/%m/%Y")

    for campo in CAMPOS_F1[2:]:
        respostas[campo] = st.text_area(campo, respostas.get(campo, ""))

    if st.button("Salvar formulário"):

        if not aba.row_values(1):
            aba.append_row(CAMPOS_F1)

        valores = [respostas[c] for c in CAMPOS_F1]

        if linha:
            aba.update(f"A{linha}:AB{linha}", [valores])
            st.success("Formulário atualizado!")
        else:
            aba.append_row(valores)
            st.success("Formulário enviado!")

        st.session_state["pagina"] = "home"


# ===============================
# NAVEGAÇÃO
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
            if st.session_state.get("formulario_atual") == "F1":
                tela_formulario_f1()
