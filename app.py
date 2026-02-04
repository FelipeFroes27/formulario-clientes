# ===============================
# IMPORTAÇÕES
# ===============================

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import qrcode
from io import BytesIO
import crcmod


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
# FUNÇÃO PIX (PADRÃO BANCO CENTRAL)
# ===============================

def gerar_payload_pix(chave, nome, cidade, valor=None, txid="***"):
    def campo(id, valor):
        return f"{id}{len(valor):02d}{valor}"

    payload = "000201"
    payload += campo("26", campo("00", "BR.GOV.BCB.PIX") + campo("01", chave))
    payload += campo("52", "0000")
    payload += campo("53", "986")

    if valor:
        payload += campo("54", f"{valor:.2f}")

    payload += campo("58", "BR")
    payload += campo("59", nome[:25])
    payload += campo("60", cidade[:15])
    payload += campo("62", campo("05", txid))

    payload += "6304"

    crc16 = crcmod.predefined.mkCrcFun("crc-ccitt-false")
    crc = format(crc16(payload.encode("utf-8")), "04X")

    return payload + crc


# ===============================
# ÁREA DO CLIENTE
# ===============================

st.title("Guerra de estados ⚔️")
st.write("Bem-vindo, Nome")

st.text_input("Qual o seu nome?")
st.radio("Selecione o estado para participar da guerra:", ["SP", "RJ"])


# ===============================
# QR CODE PIX
# ===============================

payload_pix = gerar_payload_pix(
    chave="froesfelipe03@gmail.com",
    nome="GUERRA DE ESTADOS",
    cidade="SAO PAULO",
    valor=10.00,
    txid="GUERRA01"
)

qr = qrcode.make(payload_pix)

buffer = BytesIO()
qr.save(buffer, format="PNG")
buffer.seek(0)

st.image(buffer, caption="Pague com PIX para entrar na guerra ⚔️", width=250)

