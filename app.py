import streamlit as st
import time

from database.init_db import criar_tabelas

from telas.login import tela_login
from telas.usuarios import tela_usuarios
from telas.eventos import tela_eventos
from telas.clubes import tela_clubes
from telas.participantes import tela_participantes
from telas.veiculos import tela_veiculos
from telas.dashboard import tela_dashboard
from telas.inscricoes import tela_inscricoes
from telas.inscricao_publica import tela_inscricao_publica


st.set_page_config(page_title="AutoClássicos", layout="wide")

criar_tabelas()

params = st.query_params

if params.get("pagina") == "inscricao":
    tela_inscricao_publica()
    st.stop()


def aplicar_estilo_sistema():
    st.markdown("""
        <style>

        .stApp {
            background: linear-gradient(135deg, #F4F7FB 0%, #E6EEF8 100%);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0D2C54 0%, #1E5AA8 100%) !important;
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

        label,
        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stNumberInput label,
        .stDateInput label,
        .stCheckbox label {
            color: #0D2C54 !important;
            font-weight: 700 !important;
        }

        .stCheckbox label p {
            color: #0D2C54 !important;
            font-weight: 700 !important;
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

        div[role="radiogroup"] label {
            width: 100% !important;
            min-width: 190px !important;
            background: rgba(255, 255, 255, 0.10) !important;
            border-radius: 12px !important;
            padding: 11px 14px !important;
            margin-bottom: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.14) !important;
            display: flex !important;
            align-items: center !important;
        }

        div[role="radiogroup"] {
            width: 100% !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stRadio"] {
            width: 100% !important;
        }

        div[role="radiogroup"] label > div:first-child {
            display: none !important;
        }

        div[role="radiogroup"] label p {
            font-size: 15px !important;
            font-weight: 800 !important;
            color: #FFFFFF !important;
            margin: 0 !important;
            line-height: 1.2 !important;
        }

        div[role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.22) !important;
        }

        div[role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(90deg, #D4AF37 0%, #C89B2C 100%) !important;
            border: 1px solid #D4AF37 !important;
        }

        div[role="radiogroup"] label:has(input:checked) p {
            color: #0D2C54 !important;
            font-weight: 900 !important;
        }

        [data-testid="collapsedControl"] {
            background-color: #0D2C54 !important;
            border-radius: 8px;
            padding: 4px;
        }

        [data-testid="collapsedControl"] svg {
            color: white !important;
        }

        </style>
    """, unsafe_allow_html=True)


if "inicializado" not in st.session_state:
    st.session_state["inicializado"] = False

if "logado" not in st.session_state:
    st.session_state["logado"] = False


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


if not st.session_state["logado"]:
    tela_login()

else:

    aplicar_estilo_sistema()

    st.sidebar.title("🚗 AutoClássicos")

    menu = st.sidebar.radio(
        "Menu",
        [
            "🏠 Dashboard",
            "👥 Usuários",
            "📅 Eventos",
            "🏁 Clubes",
            "👤 Participantes",
            "🚗 Veículos",
            "📝 Inscrições",
            "🚪 Sair"
        ],
        label_visibility="collapsed"
    )

    if menu == "🚪 Sair":
        st.session_state["logado"] = False
        st.rerun()

    elif menu == "🏠 Dashboard":
        tela_dashboard()

    elif menu == "👥 Usuários":
        tela_usuarios()

    elif menu == "📅 Eventos":
        tela_eventos()

    elif menu == "🏁 Clubes":
        tela_clubes()

    elif menu == "👤 Participantes":
        tela_participantes()

    elif menu == "🚗 Veículos":
        tela_veiculos()

    elif menu == "📝 Inscrições":
        tela_inscricoes()