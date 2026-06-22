import streamlit as st
import time

from database.init_db import criar_tabelas

from telas.login import tela_login
from telas.usuarios import tela_usuarios
from telas.eventos import tela_eventos
from telas.clubes import tela_clubes
from telas.participantes import tela_participantes
from telas.veiculos import tela_veiculos

st.set_page_config(page_title="AutoClássicos", layout="wide")

criar_tabelas()


# =========================
# ESTILO GLOBAL DO SISTEMA
# =========================
def aplicar_estilo_sistema():
    st.markdown("""
        <style>

        .stApp {
            background: linear-gradient(135deg, #F4F7FB 0%, #E6EEF8 100%);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0D2C54 0%, #1E5AA8 100%);
        }

        section[data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #D4AF37 !important;
            font-weight: 800 !important;
        }

        h1, h2, h3 {
            color: #0D2C54 !important;
            font-weight: 800 !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: #FFFFFF;
            border-radius: 10px 10px 0px 0px;
            padding: 10px 18px;
            color: #0D2C54;
            font-weight: 700;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #0D2C54 0%, #1E5AA8 100%) !important;
            color: #FFFFFF !important;
        }

        div.stButton > button {
            border-radius: 10px;
            border: none;
            background: linear-gradient(90deg, #D4AF37 0%, #C89B2C 100%);
            color: #0D2C54;
            font-weight: 800;
            padding: 0.55rem 1rem;
        }

        div.stButton > button:hover {
            background: linear-gradient(90deg, #C89B2C 0%, #B8860B 100%);
            color: #FFFFFF;
        }

        div[data-testid="stDataFrame"] {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 8px;
            box-shadow: 0 3px 12px rgba(13, 44, 84, 0.12);
        }

        .stAlert {
            border-radius: 12px;
        }

        input, textarea {
            border-radius: 8px !important;
        }

        </style>
    """, unsafe_allow_html=True)


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
        .stApp {
            background: linear-gradient(135deg, #0D2C54 0%, #1E5AA8 55%, #D4AF37 100%);
        }

        .center {
            text-align: center;
            margin-top: 10%;
            font-size: 38px;
            font-weight: bold;
            color: #FFFFFF;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.35);
        }

        .loading-subtitle {
            text-align: center;
            color: #FFFFFF;
            font-size: 18px;
            margin-top: 10px;
            margin-bottom: 30px;
            text-shadow: 1px 1px 5px rgba(0,0,0,0.35);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div class='center'>🚗 AutoClássicos</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='loading-subtitle'>Sistema de Gestão de Encontros de Carros Antigos</div>",
        unsafe_allow_html=True
    )

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

    aplicar_estilo_sistema()

    st.sidebar.title("🚗 AutoClássicos")

    menu = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Usuários", "Eventos", "Clubes", "Participantes","Veículos", "Sair"]
    )

    if menu == "Sair":
        st.session_state["logado"] = False
        st.rerun()

    elif menu == "Dashboard":
        st.title("📊 Dashboard")
        st.info("Dashboard em desenvolvimento.")

    elif menu == "Usuários":
        tela_usuarios()

    elif menu == "Eventos":
        tela_eventos()

    elif menu == "Clubes":
        tela_clubes()

    elif menu == "Participantes":
        tela_participantes()

    elif menu == "Veículos":
        tela_veiculos()