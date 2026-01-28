import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


# ===============================
# CONFIGURAÇÕES DO FORMULÁRIO
# ===============================

PLANILHA_NOME = "clientes_formulario"


# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================

st.set_page_config(page_title="Formulário de Avaliação", page_icon="📝")
st.title("📝 Formulário de Avaliação Pessoal")
st.write("Responda com sinceridade. Não existem respostas certas ou erradas.")


# ===============================
# AUTENTICAÇÃO GOOGLE
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
planilha = client.open(PLANILHA_NOME).sheet1


# ===============================
# FORMULÁRIO
# ===============================

respostas = {}

with st.form("formulario_avaliacao"):

    # -------- SEÇÃO 1 --------
    st.subheader("🧠 Autopercepção")

    respostas["O que você pensa a seu respeito?"] = st.text_area(
        "O que você pensa a seu respeito?"
    )

    respostas["Como foi o seu primeiro relacionamento amoroso?"] = st.text_area(
        "Como foi o seu primeiro relacionamento amoroso?"
    )

    respostas["Qual papel você exerce na vida hoje?"] = st.text_area(
        "Se você avaliasse sua atuação na vida, qual papel que mais caberia a você hoje?"
    )

    papel = st.radio(
        "Você se vê mais como:",
        ["Vítima", "Responsável"]
    )
    respostas["Vítima ou Responsável?"] = papel

    if papel == "Vítima":
        respostas["Qual o ganho secundário?"] = st.text_area("Qual o ganho secundário?")
        respostas["Em quais situações você desempenha o papel de vítima?"] = st.text_area(
            "Em quais situações você desempenha o papel de vítima?"
        )
        respostas["Em quais situações você desempenha o papel de responsável?"] = ""
    else:
        respostas["Qual o ganho secundário?"] = ""
        respostas["Em quais situações você desempenha o papel de vítima?"] = ""
        respostas["Em quais situações você desempenha o papel de responsável?"] = st.text_area(
            "Em quais situações você desempenha o papel de responsável?"
        )


    # -------- SEÇÃO 2 --------
    st.subheader("💔 Relacionamentos")

    respostas["Se considera vitoriosa(o) ou derrotada(o)?"] = st.radio(
        "Se considera vitoriosa(o) ou derrotada(o)?",
        ["Vitoriosa(o)", "Derrotada(o)"]
    )

    respostas["Perfil nos relacionamentos"] = st.radio(
        "Nos relacionamentos e na vida, você prefere ser:",
        ["Dominante", "Submisso"]
    )

    respostas["Quem é o culpado pelos seus problemas?"] = st.text_area(
        "Quem deve ser punido por problemas que ocorrem com você?"
    )

    raiva = st.radio(
        "Sente raiva ou rancor de alguém?",
        ["Não", "Sim"]
    )
    respostas["Sente raiva ou rancor de alguém?"] = raiva

    if raiva == "Sim":
        respostas["Raiva direcionada a quem?"] = st.text_input("Quem?")
    else:
        respostas["Raiva direcionada a quem?"] = ""


    # -------- SEÇÃO 3 --------
    st.subheader("⚖️ Pressões e Controle")

    pressao = st.radio(
        "Sente-se pressionada(o) na atualidade?",
        ["Não", "Sim"]
    )
    respostas["Sente-se pressionada(o)?"] = pressao

    if pressao == "Sim":
        respostas["De que maneira se sente pressionada(o)?"] = st.text_area("De que maneira?")
    else:
        respostas["De que maneira se sente pressionada(o)?"] = ""

    respostas["Você se acha uma pessoa controladora?"] = st.radio(
        "Você se acha uma pessoa controladora?",
        ["Sim", "Não"]
    )

    inferior = st.radio(
        "Sente-se inferior aos outros?",
        ["Não", "Sim"]
    )
    respostas["Sente-se inferior aos outros?"] = inferior

    if inferior == "Sim":
        respostas["Por que se sente inferior?"] = st.text_area("Por quê?")
    else:
        respostas["Por que se sente inferior?"] = ""


    # -------- SEÇÃO 4 --------
    st.subheader("💭 Emoções")

    EMOCOES = [
        "Raiva", "Medo", "Culpa", "Tristeza", "Ansiedade",
        "Ciúme", "Frustração", "Solidão", "Cansaço"
    ]

    for emocao in EMOCOES:
        respostas[emocao] = st.selectbox(
            emocao,
            ["Não sinto", "Pouca intensidade", "Média intensidade", "Muita intensidade"]
        )

    enviar = st.form_submit_button("Enviar formulário")


# ===============================
# ENVIO PARA GOOGLE SHEETS
# ===============================

if enviar:

    # cria cabeçalho se a planilha estiver vazia
    if not planilha.get_all_values():
        planilha.append_row(list(respostas.keys()))

    # adiciona respostas
    planilha.append_row(list(respostas.values()))

    st.success("Formulário enviado com sucesso!")
