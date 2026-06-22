import streamlit as st
import base64
import os

from database.usuarios_db import validar_login


# =========================
# FUNDO DA TELA
# =========================
def set_bg():

    img_path = "assets/fundo.jpeg"

    if not os.path.exists(img_path):
        return

    with open(img_path, "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
        <style>

        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: 520px auto;
            background-position: 28% center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-color: #f5f5f5;
        }}

        html, body {{
            overflow: hidden;
        }}

        h1, h2, h3, .stTitle {{
            color: white !important;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }}

        .block-container {{
            background-color: rgba(0, 0, 0, 0.58);
            padding: 2rem;
            border-radius: 15px;
            max-width: 420px;
            margin-left: 58%;
            margin-right: auto;
            margin-top: 8%;
        }}

        .stTextInput > div > div > input {{
            background-color: rgba(255,255,255,0.95);
            color: black;
            border-radius: 8px;
            padding: 8px;
        }}

        label {{
            color: white !important;
            font-weight: bold;
        }}

        div.stButton > button {{
            width: 100%;
            border-radius: 8px;
            background-color: #2E86C1;
            color: white;
            font-weight: bold;
        }}

        div.stButton > button:hover {{
            background-color: #1B4F72;
            color: white;
        }}

        </style>
    """, unsafe_allow_html=True)


# =========================
# TELA DE LOGIN
# =========================
def tela_login():

    set_bg()

    st.title("Acesso ao Sistema")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        user = validar_login(usuario, senha)

        if user:
            st.success(f"Bem-vindo, {user[1]}!")

            st.session_state["logado"] = True
            st.session_state["usuario"] = user[1]
            st.session_state["perfil"] = user[4]

            st.rerun()

        else:
            st.error("Usuário ou senha inválidos")