import streamlit as st
import time
from telas.login import tela_login
from telas.usuarios import tela_usuarios
from telas.eventos import tela_eventos
from telas.clubes import tela_clubes

from database.init_db import criar_tabelas

criar_tabelas()
st.set_page_config(page_title="AutoClássicos", layout="wide")


# =========================
# ESTADO INICIAL
# =========================
if "inicializado" not in st.session_state:
    st.session_state["inicializado"] = False

if "logado" not in st.session_state:
    st.session_state["logado"] = False


# =========================
# LOADING SCREEN
# =========================
if not st.session_state["inicializado"]:

    st.markdown("""
        <style>
        .center {
            text-align: center;
            margin-top: 15%;
            font-size: 28px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='center'>🚗 AutoClássicos</div>", unsafe_allow_html=True)
    st.write("Inicializando sistema...")

    progress = st.progress(0)

    for i in range(1, 101):
        time.sleep(0.01)
        progress.progress(i)

    st.session_state["inicializado"] = True
    st.rerun()


# =========================
# SISTEMA NORMAL
# =========================
if not st.session_state["logado"]:
    tela_login()

else:

    st.sidebar.title("AutoClássicos")

    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Usuários", "Eventos", "Clubes", "Sair"]
    )

    if menu == "Sair":
        st.session_state["logado"] = False
        st.rerun()

    elif menu == "Dashboard":
        st.title("Dashboard")

    elif menu == "Usuários":
        tela_usuarios()

    elif menu == "Eventos":
        st.write("Eventos")

    elif menu == "Clubes":
        st.write("Clubes")

   