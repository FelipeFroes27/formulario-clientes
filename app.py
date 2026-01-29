# importa a biblioteca principal do Streamlit para criar a interface web
import streamlit as st

# importa o gspread para acessar o Google Sheets
import gspread

# importa as credenciais de conta de serviço do Google
from google.oauth2.service_account import Credentials

# escreve um texto fixo na tela para confirmar QUAL arquivo está rodando
st.write("ARQUIVO BETA.PY EM EXECUÇÃO")

# define os escopos de acesso ao Google Sheets e Google Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# cria as credenciais usando o JSON salvo no st.secrets
creds = Credentials.from_service_account_info(
    st.secrets["google_credentials"],  # pega as credenciais do secrets
    scopes=SCOPES                       # aplica os escopos definidos acima
)

# autoriza o gspread usando as credenciais criadas
client = gspread.authorize(creds)

# abre a planilha pelo NOME (troque pelo nome exato da sua planilha)
planilha = client.open("NOME_DA_SUA_PLANILHA_AQUI")

# acessa a aba onde estão os usuários (nome da aba)
aba_usuarios = planilha.worksheet("usuarios")

# cria um título na interface
st.title("Login do Sistema")

# cria um campo de texto para o usuário digitar o login
usuario_digitado = st.text_input("Usuário")

# cria um campo de senha (oculta)
senha_digitada = st.text_input("Senha", type="password")

# cria o botão de login
if st.button("Entrar"):
    
    # confirma visualmente que o botão foi clicado
    st.write("BOTÃO FUNCIONOU")

    # escreve um marcador antes de acessar a planilha
    st.write("ANTES DE LER A PLANILHA")

    # lê todos os registros da aba usuarios como lista de dicionários
    usuarios = aba_usuarios.get_all_records()

    # escreve um marcador depois da leitura
    st.write("DEPOIS DE LER A PLANILHA")

    # mostra na tela exatamente o que veio da planilha
    st.write(usuarios)

    # variável para controlar se encontrou o usuário
    usuario_valido = False

    # percorre cada linha (usuário) da planilha
    for u in usuarios:
        
        # verifica se o usuário e senha digitados batem com a planilha
        if u["usuario"] == usuario_digitado and u["senha"] == senha_digitada:
            
            # marca que o usuário é válido
            usuario_valido = True

            # mostra mensagem de sucesso
            st.success(f"Bem-vindo, {u['usuario']}!")

            # mostra o tipo do usuário (cliente ou master)
            st.write("Tipo de usuário:", u["tipo"])

            # interrompe o loop pois já achou o usuário
            break

    # se terminou o loop e não encontrou o usuário
    if not usuario_valido:
        
        # mostra mensagem de erro
        st.error("Usuário ou senha inválidos")
