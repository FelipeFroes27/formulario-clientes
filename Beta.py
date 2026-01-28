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
# CABEÇALHO FIXO (ORDEM GARANTIDA)
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
# FORMULÁRIO
# ===============================

respostas = {}

with st.form("formulario_avaliacao"):

    # -------- SEÇÃO 1 --------
    st.subheader("🧠 Autopercepção")

    respostas[CAMPOS[0]] = st.text_area(CAMPOS[0], key="q1")
    respostas[CAMPOS[1]] = st.text_area(CAMPOS[1], key="q2")
    respostas[CAMPOS[2]] = st.text_area(
        "Se você avaliasse sua atuação na vida, qual papel que mais caberia a você hoje?",
        key="q3"
    )

    papel = st.radio(
        "Você se vê mais como:",
        ["Vítima", "Responsável"],
        key="papel"
    )
    respostas[CAMPOS[3]] = papel

    respostas[CAMPOS[4]] = ""
    respostas[CAMPOS[5]] = ""
    respostas[CAMPOS[6]] = ""

    if papel == "Vítima":
        respostas[CAMPOS[4]] = st.text_area(CAMPOS[4], key="ganho")
        respostas[CAMPOS[5]] = st.text_area(CAMPOS[5], key="vitima")
    else:
        respostas[CAMPOS[6]] = st.text_area(CAMPOS[6], key="responsavel")


    # -------- SEÇÃO 2 --------
    st.subheader("💔 Relacionamentos")

    respostas[CAMPOS[7]] = st.radio(
        CAMPOS[7],
        ["Vitoriosa(o)", "Derrotada(o)"],
        key="vitoria"
    )

    respostas[CAMPOS[8]] = st.radio(
        "Nos relacionamentos e na vida, você prefere ser:",
        ["Dominante", "Submisso"],
        key="perfil"
    )

    respostas[CAMPOS[9]] = st.text_area(CAMPOS[9], key="culpado")

    raiva = st.radio(
        CAMPOS[10],
        ["Não", "Sim"],
        key="raiva"
    )
    respostas[CAMPOS[10]] = raiva
    respostas[CAMPOS[11]] = st.text_input(CAMPOS[11], key="raiva_quem") if raiva == "Sim" else ""


    # -------- SEÇÃO 3 --------
    st.subheader("⚖️ Pressões e Controle")

    pressao = st.radio(
        CAMPOS[12],
        ["Não", "Sim"],
        key="pressao"
    )
    respostas[CAMPOS[12]] = pressao
    respostas[CAMPOS[13]] = st.text_area(CAMPOS[13], key="pressao_txt") if pressao == "Sim" else ""

    respostas[CAMPOS[14]] = st.radio(
        CAMPOS[14],
        ["Sim", "Não"],
        key="controlador"
    )

    inferior = st.radio(
        CAMPOS[15],
        ["Não", "Sim"],
        key="inferior"
    )
    respostas[CAMPOS[15]] = inferior
    respostas[CAMPOS[16]] = st.text_area(CAMPOS[16], key="inferior_txt") if inferior == "Sim" else ""


    # -------- SEÇÃO 4 --------
    st.subheader("💭 Emoções")

    for idx, emocao in enumerate(CAMPOS[17:], start=1):
        respostas[emocao] = st.selectbox(
            emocao,
            ["Não sinto", "Pouca intensidade", "Média intensidade", "Muita intensidade"],
            key=f"emo_{idx}"
        )

    enviar = st.form_submit_button("Enviar formulário")


# ===============================
# ENVIO PARA GOOGLE SHEETS
# ===============================

if enviar:

    # cria cabeçalho se a primeira linha estiver vazia
    if not planilha.row_values(1):
        planilha.append_row(CAMPOS)

    planilha.append_row([respostas[campo] for campo in CAMPOS])

    st.success("Formulário enviado com sucesso!")

