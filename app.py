import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# CONFIGURAÇÕES DA PÁGINA
st.set_page_config(page_title="Cadastro de Clientes", page_icon="📝")
st.title("📝 Formulário de Cadastro")
st.write("Preencha os dados abaixo:")

# AUTENTICAÇÃO GOOGLE
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(
    st.secrets["google_credentials"],
    scopes=scope
)

client = gspread.authorize(creds)

# ABRIR PLANILHA
planilha = client.open("clientes_formulario").sheet1

# FORMULÁRIO
with st.form("form_cliente"):
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    email = st.text_input("Email")

    enviar = st.form_submit_button("Enviar")

# AO ENVIAR
if enviar:
    if nome == "" or email == "":
        st.error("Preencha todos os campos obrigatórios.")
    else:
        planilha.append_row([nome, idade, email])
        st.success("Dados enviados com sucesso!")
