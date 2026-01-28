import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


# ===============================
# CONFIGURAÇÕES
# ===============================

PLANILHA_NOME = "clientes_formulario"

st.set_page_config(page_title="Formulário de Avaliação", page_icon="📝")
st.title("📝 Formulário de Avaliação Pessoal")
st.write("Responda com sinceridade. Não existem respostas certas ou erradas.")


# ===============================
# GOOGLE SHEETS
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
# CABEÇALHO FIXO
# ===============================

CAMPOS = [
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
    "Raiva", "Medo", "Culpa", "Tristeza", "Ansiedade",
    "Ciúme", "Frustração", "Solidão", "Cansaço"
]


# ===============================
# FORMULÁRIO
# ===============================

respostas = {}

with st.form("formulario_avaliacao"):

    st.subheader("🧠 Autopercepção")

    respostas[CAMPOS[0]] = st.text_area(CAMPOS[0])
    respostas[CAMPOS[1]] = st.text_area(CAMPOS[1])
    respostas[CAMPOS[2]] = st.text_area("Se você avaliasse sua atuação na vida, qual papel que mais caberia a você hoje?")

    papel = st.radio("Você se vê mais como:", ["Vítima", "Responsável"])
    respostas[CAMPOS[3]] = papel

    respostas[CAMPOS[4]] = ""
    respostas[CAMPOS[5]] = ""
    respostas[CAMPOS[6]] = ""

    if papel == "Vítima":
        respostas[CAMPOS[4]] = st.text_area(CAMPOS[4])
        respostas[CAMPOS[5]] = st.text_area(CAMPOS[5])
    else:
        respostas[CAMPOS[6]] = st.text_area(CAMPOS[6])


    st.subheader("💔 Relacionamentos")

    respostas[CAMPOS[7]] = st.radio(CAMPOS[7], ["Vitoriosa(o)", "Derrotada(o)"])
    respostas[CAMPOS[8]] = st.radio("Nos relacionamentos e na vida, você prefere ser:", ["Dominante", "Submisso"])
    respostas[CAMPOS[9]] = st.text_area(CAMPOS[9])

    raiva = st.radio(CAMPOS[10], ["Não", "Sim"])
    respostas[CAMPOS[10]] = raiva
    respostas[CAMPOS[11]] = st.text_input(CAMPOS[11]) if raiva == "Sim" else ""


    st.subheader("⚖️ Pressões e Controle")

    pressao = st.radio(CAMPOS[12], ["Não", "Sim"])
    respostas[CAMPOS[12]] = pressao
    respostas[CAMPOS[13]] = st.text_area(CAMPOS[13]) if pressao == "Sim" else ""

    respostas[CAMPOS[14]] = st.radio(CAMPOS[14], ["Sim", "Não"])

    inferior = st.radio(CAMPOS[15], ["Não", "Sim"])
    respostas[CAMPOS[15]] = inferior
    respostas[CAMPOS[16]] = st.text_area(CAMPOS[16]) if inferior == "Sim" else ""


    st.subheader("💭 Emoções")

    for emocao in CAMPOS[17:]:
        respostas[emocao] = st.selectbox(
            emocao,
            ["Não sinto", "Pouca intensidade", "Média intensidade", "Muita intensidade"]
        )

    enviar = st.form_submit_button("Enviar formulário")


# ===============================
# ENVIO
# ===============================

if enviar:

    if not planilha.get_all_values():
        planilha.append_row(CAMPOS)

    planilha.append_row([respostas[campo] for campo in CAMPOS])

    st.success("Formulário enviado com sucesso!")

