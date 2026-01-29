# Importa a biblioteca Streamlit para criar a interface web
import streamlit as st

# Importa a biblioteca gspread para acessar o Google Sheets
import gspread

# Importa a classe Credentials para autenticação com o Google
from google.oauth2.service_account import Credentials


# ===============================
# CONFIGURAÇÕES GERAIS DO SITE
# ===============================

# Define o título da aba do navegador e o ícone do site
st.set_page_config(page_title="Sistema de Consultoria", page_icon="🧠")

# Define o título principal da página
st.title("🔐 Login do Sistema")

# Texto explicativo para o usuário
st.write("Digite seu usuário e senha para acessar o sistema.")


# ===============================
# CONEXÃO COM O GOOGLE SHEETS
# ===============================

# Define os escopos de permissão que o app terá no Google
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Cria as credenciais usando os dados salvos no st.secrets
creds = Credentials.from_service_account_info(
    st.secrets["google_credentials"],
    scopes=scope
)

# Autoriza o acesso ao Google Sheets
client = gspread.authorize(creds)

# Abre a planilha principal do sistema
planilha = client.open("clientes_formulario")

# Acessa a aba USUARIOS
aba_usuarios = planilha.worksheet("USUARIOS")


# ===============================
# CAMPOS DE LOGIN
# ===============================

# Cria um campo de texto para o usuário digitar o login
usuario_digitado = st.text_input("Usuário")

# Cria um campo de senha (oculta os caracteres)
senha_digitada = st.text_input("Senha", type="password")


# ===============================
# BOTÃO DE LOGIN
# ===============================

# Cria um botão para o usuário tentar entrar no sistema
if st.button("Entrar"):

    # Busca todos os usuários cadastrados na aba USUARIOS
    usuarios = aba_usuarios.get_all_records()
    st.write(usuarios)

    # Variável para controlar se o login foi encontrado
    usuario_valido = None

    # Percorre cada usuário cadastrado
    for u in usuarios:

        # Verifica se o usuário e a senha digitados conferem
        if u["usuario"] == usuario_digitado and u["senha"] == senha_digitada:
            usuario_valido = u
            break

    # Se encontrou um usuário válido
    if usuario_valido:

        # Salva o id do usuário na sessão
        st.session_state["id_usuario"] = usuario_valido["id_usuario"]

        # Salva o tipo de usuário (cliente ou master)
        st.session_state["tipo"] = usuario_valido["tipo"]

        # Salva o nome do usuário
        st.session_state["usuario"] = usuario_valido["usuario"]

        # Mensagem de sucesso
        st.success("Login realizado com sucesso!")

        # Se for consultor (master)
        if usuario_valido["tipo"] == "master":
            st.switch_page("pages/master_dashboard.py")

        # Se for cliente
        else:
            st.switch_page("pages/cliente_dashboard.py")

    # Caso usuário ou senha estejam incorretos
    else:
        st.error("Usuário ou senha inválidos.")
