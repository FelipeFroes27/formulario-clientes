# ===============================
# IMPORTAÇÕES
# ===============================

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials


# ===============================
# CONFIGURAÇÃO DO FORMULÁRIO
# (ESSA PARTE VOCÊ REUTILIZA)
# ===============================

FORM_CONFIG = {
    "titulo": "📝 Formulário de Cadastro",
    "descricao": "Preencha os dados abaixo:",
    "nome_planilha": "clientes_formulario",
    "campos": [
        {"label": "Nome", "tipo": "texto", "obrigatorio": True},
        {"label": "Idade", "tipo": "numero", "obrigatorio": False},
        {"label": "Email", "tipo": "texto", "obrigatorio": True},
    ]
}


# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================

st.set_page_config(
    page_title=FORM_CONFIG["titulo"],
    page_icon="📝"
)

st.title(FORM_CONFIG["titulo"])
st.write(FORM_CONFIG["descricao"])


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


# ===============================
# ABRIR PLANILHA
# ===============================

planilha = client.open(FORM_CONFIG["nome_planilha"]).sheet1


# ===============================
# FORMULÁRIO DINÂMICO
# ===============================

dados_formulario = {}

with st.form("formulario_dinamico"):

    for campo in FORM_CONFIG["campos"]:

        label = campo["label"]
        tipo = campo["tipo"]

        if tipo == "texto":
            valor = st.text_input(label)

        elif tipo == "numero":
            valor = st.number_input(label, step=1)

        dados_formulario[label] = valor

    enviar = st.form_submit_button("Enviar")


# ===============================
# ENVIO DOS DADOS
# ===============================

if enviar:

    # Validação dos campos obrigatórios
    for campo in FORM_CONFIG["campos"]:
        if campo["obrigatorio"]:
            if dados_formulario[campo["label"]] in ["", 0]:
                st.error(f"O campo '{campo['label']}' é obrigatório.")
                st.stop()

    # Salva os dados na planilha (nova linha)
    planilha.append_row(list(dados_formulario.values()))

    st.success("Dados enviados com sucesso!")
