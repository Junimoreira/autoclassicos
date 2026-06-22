import streamlit as st
import pandas as pd
from database.usuarios_db import (
    listar_usuarios,
    inserir_usuario,
    atualizar_usuario,
    deletar_usuario
)

def tela_usuarios():

    st.title("👤 Gestão de Usuários")

    menu = st.radio("Ação", ["Listar", "Cadastrar", "Editar", "Excluir"])

    # =========================
    # LISTAR
    # =========================
    if menu == "Listar":

        dados = listar_usuarios()

        df = pd.DataFrame(
            dados,
            columns=["ID", "Nome", "Usuário", "Perfil", "Ativo", "Criado em"]
        )

        st.dataframe(df, use_container_width=True)