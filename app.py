# ===============================
# IMPORTAÇÕES
# ===============================

import streamlit as st                       # framework do app
import gspread                               # Google Sheets
from google.oauth2.service_account import Credentials
from datetime import datetime                # data atual


# ===============================
# CONFIGURAÇÕES GERAIS
# ===============================

PLANILHA_NOME = "Banco de dados"              # nome da planilha no Google Sheets

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
aba_formularios = planilha.worksheet("FORMULARIOS")
aba_acessos = planilha.worksheet("ACESSOS")


# ===============================
# CAMPOS DO FORMULÁRIO 1
# ===============================

CAMPOS_F1 = [
    "Cliente",
    "Data",
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
# FUNÇÃO AUXILIAR
# BUSCA RESPOSTA EXISTENTE
# ===============================

def buscar_resposta(aba, usuario):
    """
    Procura se o cliente já respondeu o formulário.
    Retorna:
    - número da linha (int)
    - dicionário com respostas
    """
    registros = aba.get_all_records()

    for i, linha in enumerate(registros, start=2):
        if linha.get("Cliente", "").strip().lower() == usuario:
            return i, linha

    return None, None


# ===============================
# TELA DE LOGIN
# ===============================

def tela_login():

    st.title("🔐 Login")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        usuarios = aba_usuarios.get_all_records()

        for u in usuarios:

            if (
                usuario.strip().lower() == str(u["usuario"]).strip().lower()
                and senha.strip() == str(u["senha"]).strip()
            ):
                st.session_state["logado"] = True
                st.session_state["usuario"] = usuario.strip().lower()
                st.session_state["tipo"] = str(u["tipo"]).strip().lower()
                st.session_state["pagina"] = "home"
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

    # filtra formulários liberados para o cliente
    liberados = [
        f for f in formularios
        if f["id"] in [
            a["formulario_id"] for a in acessos
            if a["usuario"].strip().lower() == st.session_state["usuario"]
        ]
        and f["ativo"].lower() == "sim"
    ]

    st.subheader("📝 Formulários disponíveis")

    for f in liberados:
        if st.button(f["nome"]):
            st.session_state["formulario_atual"] = f["id"]
            st.session_state["pagina"] = "formulario"


# ===============================
# FORMULÁRIO 1 (COM EDIÇÃO)
# ===============================

def tela_formulario_f1():

    aba = planilha.worksheet("FORMULÁRIO 1")

    st.title("📝 Avaliação Pessoal")

    usuario = st.session_state["usuario"]

    # verifica se já existe resposta
    linha, dados = buscar_resposta(aba, usuario)

    respostas = {campo: "" for campo in CAMPOS_F1}

    if dados:
        for campo in CAMPOS_F1:
            respostas[campo] = dados.get(campo, "")

    respostas["Cliente"] = usuario
    respostas["Data"] = datetime.now().strftime("%d/%m/%Y")

    respostas[CAMPOS_F1[2]] = st.text_area(CAMPOS_F1[2], respostas[CAMPOS_F1[2]])
    respostas[CAMPOS_F1[3]] = st.text_area(CAMPOS_F1[3], respostas[CAMPOS_F1[3]])
    respostas[CAMPOS_F1[4]] = st.text_area(CAMPOS_F1[4], respostas[CAMPOS_F1[4]])

    papel = st.radio(
        CAMPOS_F1[5],
        ["Vítima", "Responsável"],
        index=0 if respostas[CAMPOS_F1[5]] == "Vítima" else 1
    )
    respostas[CAMPOS_F1[5]] = papel

    if papel == "Vítima":
        respostas[CAMPOS_F1[6]] = st.text_area(CAMPOS_F1[6], respostas[CAMPOS_F1[6]])
        respostas[CAMPOS_F1[7]] = st.text_area(CAMPOS_F1[7], respostas[CAMPOS_F1[7]])
    else:
        respostas[CAMPOS_F1[8]] = st.text_area(CAMPOS_F1[8], respostas[CAMPOS_F1[8]])

    for emocao in CAMPOS_F1[19:]:
        respostas[emocao] = st.selectbox(
            emocao,
            ["Não sinto", "Pouca intensidade", "Média intensidade", "Muita intensidade"],
            index=[
                "Não sinto",
                "Pouca intensidade",
                "Média intensidade",
                "Muita intensidade"
            ].index(respostas.get(emocao, "Não sinto"))
        )

    if st.button("Salvar formulário"):

        if not aba.row_values(1):
            aba.append_row(CAMPOS_F1)

        valores = [respostas[campo] for campo in CAMPOS_F1]

        if linha:
            aba.update(f"A{linha}:AA{linha}", [valores])
            st.success("Respostas atualizadas com sucesso!")
        else:
            aba.append_row(valores)
            st.success("Formulário enviado com sucesso!")

        st.session_state["pagina"] = "home"


# ===============================
# PAINEL DO CONSULTOR
# ===============================

def tela_mestre():
    st.title("🧠 Painel do Consultor")
    st.write("Em breve: gestão de clientes e formulários")


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

            if st.session_state["formulario_atual"] == "F1":
                tela_formulario_f1()

    elif st.session_state["tipo"] == "mestre":
        tela_mestre()
