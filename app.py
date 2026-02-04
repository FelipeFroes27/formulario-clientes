# ===============================
# IMPORTAÇÕES
# ===============================

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import qrcode
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
st.write(f"Bem-vindo, Nome")

st.text_input("Qual o seu nome?")
st.radio("Selecione o estado para participar da guerra:", ["SP", "RJ"])


# ===============================
# QR CODE
# ===============================

felipe = "froesfelipe03@gmail.com"

qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4
)
qr.add_data(felipe)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

buffer = BytesIO()
img.save(buffer, format="PNG")
buffer.seek(0)

st.image(buffer, caption="QR Code do participante", width=250)

