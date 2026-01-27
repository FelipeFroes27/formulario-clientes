# ===============================
# IMPORTAÇÃO DAS BIBLIOTECAS
# ===============================

import streamlit as st
# Streamlit é responsável por criar o site, formulários, textos e botões

import gspread
# gspread permite acessar e escrever dados no Google Sheets

from google.oauth2.service_account import Credentials
# Classe usada para autenticar com o Google usando a conta de serviço (JSON)


# ===============================
# CONFIGURAÇÕES DA PÁGINA
# ===============================

# Define o título da aba do navegador e o ícone do site
st.set_page_config(page_title="Cadastro de Clientes", page_icon="📝")

# Título principal exibido no site
st.title("📝 Formulário de Cadastro")

# Texto explicativo abaixo do título
st.write("Preencha os dados abaixo:")


# ===============================
# AUTENTICAÇÃO COM O GOOGLE
# ===============================

# Define as permissões que o app terá no Google
# - Ler e escrever planilhas
# - Acessar o Google Drive
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Cria as credenciais usando o JSON salvo no Secrets do Streamlit
# st.secrets["google_credentials"] é o bloco que você colou no Streamlit Cloud
creds = Credentials.from_service_account_info(
    st.secrets["google_credentials"],
    scopes=scope
)

# Autoriza o cliente do gspread usando as credenciais
client = gspread.authorize(creds)


# ===============================
# ABERTURA DA PLANILHA
# ===============================

# Abre a planilha chamada "clientes_formulario"
# sheet1 indica a primeira aba da planilha
planilha = client.open("clientes_formulario").sheet1


# ===============================
# FORMULÁRIO DO SITE
# ===============================

# Cria um formulário no Streamlit
# O conteúdo só é enviado quando o botão "Enviar" for clicado
with st.form("form_cliente"):

    # Campo de texto para o nome do cliente
    nome = st.text_input("Nome")
    empresa = st.text_input("Empresa")

    # Campo numérico para idade
    # Aceita valores entre 0 e 120
    idade = st.number_input(
        "Idade",
        min_value=0,
        max_value=120,
        step=1
    )

    # Campo de texto para email
    email = st.text_input("Email")

    # Botão de envio do formulário
    enviar = st.form_submit_button("Enviar")


# ===============================
# AÇÃO AO ENVIAR O FORMULÁRIO
# ===============================

# Esse bloco só roda quando o botão "Enviar" for clicado
if enviar:

    # Validação simples: nome e email não podem estar vazios
    if nome == "" or email == "":
        st.error("Preencha todos os campos obrigatórios.")

    else:
        # Adiciona uma nova linha na planilha
        # Cada valor vai para uma coluna
        planilha.append_row([nome, idade, email, empresa])

        # Mensagem de sucesso exibida no site
        st.success("Dados enviados com sucesso!")
