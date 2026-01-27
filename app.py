import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Cadastro de Clientes", page_icon="📝")

st.title("📝 Formulário de Cadastro")
st.write("Preencha os dados abaixo:")

# Formulário
with st.form("form_cliente"):
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    email = st.text_input("Email")

    enviar = st.form_submit_button("Enviar")

# Quando clicar em enviar
if enviar:
    if nome == "" or email == "":
        st.error("Preencha todos os campos obrigatórios.")
    else:
        dados = {
            "Nome": [nome],
            "Idade": [idade],
            "Email": [email]
        }

        df_novo = pd.DataFrame(dados)

        arquivo = "clientes.xlsx"

        # Se o arquivo já existir, adiciona nova linha
        if os.path.exists(arquivo):
            df_existente = pd.read_excel(arquivo)
            df_final = pd.concat([df_existente, df_novo], ignore_index=True)
        else:
            df_final = df_novo

        df_final.to_excel(arquivo, index=False)

        st.success("Dados salvos com sucesso!")
