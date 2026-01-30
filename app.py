# ===============================
# IMPORTAÇÕES
# ===============================

import streamlit as st  # framework principal do app
import gspread  # biblioteca para Google Sheets
from google.oauth2.service_account import Credentials  # autenticação Google

# ===============================
# CONFIGURAÇÕES GERAIS
# ===============================

PLANILHA_NOME = "Banco de dados"  # nome do arquivo no Google Sheets

st.set_page_config(page_title="Login", page_icon="🔐")  # configura a página
st.title("🔐 Login do Sistema")  # título da tela


# ===============================
# CONEXÃO COM GOOGLE SHEETS
# ===============================

# escopos de acesso ao Google
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# cria credenciais usando secrets do Streamlit
creds = Credentials.from_service_account_info(
    st.secrets["google_credentials"],
    scopes=scope
)

# autoriza o cliente gspread
client = gspread.authorize(creds)

# abre a planilha principal
planilha = client.open(PLANILHA_NOME)

# acessa a aba de usuários
aba_usuarios = planilha.worksheet("USUARIOS")


# ===============================
# CAMPOS DE LOGIN
# ===============================

username = st.text_input("Usuário")  # campo usuário
password = st.text_input("Senha", type="password")  # campo senha


# ===============================
# BOTÃO DE LOGIN
# ===============================

if st.button("Entrar"):

    # lê todos os usuários da aba
    usuarios = aba_usuarios.get_all_records()

    # variável de controle de login
    login_ok = False

    # percorre cada usuário da planilha
    for usuario in usuarios:

        # normaliza usuário da planilha
        usuario_planilha = str(usuario["usuário"]).strip().lower()

        # normaliza senha da planilha
        senha_planilha = str(usuario["senha"]).strip()

        # normaliza tipo do usuário
        tipo_usuario = str(usuario["tipo"]).strip().lower()

        # normaliza dados digitados
        usuario_digitado = username.strip().lower()
        senha_digitada = password.strip()

        # valida usuário e senha
        if usuario_digitado == usuario_planilha and senha_digitada == senha_planilha:
            login_ok = True  # login válido

            # salva dados na sessão
            st.session_state["logado"] = True
            st.session_state["usuario"] = usuario_planilha
            st.session_state["tipo"] = tipo_usuario

            break  # sai do loop ao encontrar usuário válido

    # resultado do login
    if login_ok:
        st.success("Login realizado com sucesso!")
        st.write("Tipo de usuário:", st.session_state["tipo"])
    else:
        st.error("Usuário ou senha inválidos")
