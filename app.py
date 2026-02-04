# ===============================
# IMPORTAÇÕES
# ===============================

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import qrcode
from pixqrcode import Payload
from io import BytesIO


# ===============================
# CONFIGURAÇÕES GERAIS
# ===============================

PLANILHA_NOME = "Guerra de estados"

st.set_page_config(
    page_title="Guerra de estados",
    page_icon="⚔️"
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

aba_usuarios = planilha.worksheet("Estados")


# ===============================
# ÁREA DO CLIENTE
# ===============================

st.title("Guerra de estados ⚔️")
st.write("Bem-vindo, Nome")

st.text_input("Qual o seu nome?")
st.radio(
    "Selecione o estado para participar da guerra:",
    ["SP", "RJ"]
)


# ===============================
# QR CODE PIX
# ===============================

pix = Payload(
    pixkey="froesfelipe03@gmail.com",   # CHAVE PIX
    merchant_name="GUERRA DE ESTADOS",
    merchant_city="SAO PAULO",
    amount=10.00,                      # remova essa linha se quiser valor livre
    txid="GUERRA01"
)

payload_pix = pix.payload()

qr = qrcode.make(payload_pix)

buffer = BytesIO()
qr.save(buffer, format="PNG")
buffer.seek(0)

st.image(buffer, caption="Pague com PIX para entrar na guerra ⚔️", width=250)

