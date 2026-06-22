import streamlit as st

from database.clubes_db import (
    listar_clubes,
    cadastrar_clube,
    atualizar_clube,
    excluir_clube
)


def tela_clubes():

    st.title("🏁 Gestão de Clubes")

    if st.session_state.get("clube_cadastrado"):
        st.success("Clube cadastrado com sucesso!")
        st.session_state["clube_cadastrado"] = False

    abas = st.tabs([
        "📋 Listar",
        "➕ Cadastrar",
        "✏️ Editar",
        "🗑️ Excluir"
    ])

    with abas[0]:

        st.subheader("📋 Clubes cadastrados")

        df = listar_clubes()

        if df.empty:
            st.info("Nenhum clube cadastrado.")
        else:
            st.dataframe(df, use_container_width=True)

    with abas[1]:

        st.subheader("➕ Cadastrar Clube")

        with st.form("form_cadastrar_clube", clear_on_submit=True):

            nome = st.text_input("Nome do Clube")
            cidade = st.text_input("Cidade")
            estado = st.text_input("Estado", max_chars=2)
            instagram = st.text_input("Instagram")

            salvar = st.form_submit_button("Salvar Clube")

            if salvar:

                if not nome.strip():
                    st.error("Informe o nome do clube.")
                else:
                    sucesso = cadastrar_clube(
                        nome.strip(),
                        cidade.strip(),
                        estado.strip().upper(),
                        instagram.strip()
                    )

                    if sucesso is True:
                        st.session_state["clube_cadastrado"] = True
                        st.rerun()
                    else:
                        st.error(f"Erro ao cadastrar clube: {sucesso}")

    with abas[2]:

        st.subheader("✏️ Editar Clube")

        df = listar_clubes()

        if df.empty:
            st.info("Nenhum clube cadastrado para editar.")
        else:
            clube_id = st.selectbox(
                "Selecione o clube",
                df["id"].tolist(),
                format_func=lambda x: df.loc[df["id"] == x, "nome"].values[0]
            )

            clube = df[df["id"] == clube_id].iloc[0]

            with st.form("form_editar_clube"):

                nome = st.text_input("Nome do Clube", value=clube["nome"])
                cidade = st.text_input("Cidade", value=clube["cidade"] or "")
                estado = st.text_input("Estado", value=clube["estado"] or "", max_chars=2)
                instagram = st.text_input("Instagram", value=clube["instagram"] or "")

                salvar = st.form_submit_button("Salvar Alterações")

                if salvar:

                    if not nome.strip():
                        st.error("Informe o nome do clube.")
                    else:
                        sucesso = atualizar_clube(
                            clube_id,
                            nome.strip(),
                            cidade.strip(),
                            estado.strip().upper(),
                            instagram.strip()
                        )

                        if sucesso is True:
                            st.success("Clube atualizado com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"Erro ao atualizar clube: {sucesso}")

    with abas[3]:

        st.subheader("🗑️ Excluir Clube")

        df = listar_clubes()

        if df.empty:
            st.info("Nenhum clube cadastrado para excluir.")
        else:
            clube_id = st.selectbox(
                "Selecione o clube para excluir",
                df["id"].tolist(),
                format_func=lambda x: df.loc[df["id"] == x, "nome"].values[0],
                key="excluir_clube"
            )

            clube = df[df["id"] == clube_id].iloc[0]

            st.warning(f"Você está prestes a excluir: {clube['nome']}")

            confirmar = st.checkbox("Confirmo que desejo excluir este clube")

            if st.button("Excluir Clube"):

                if not confirmar:
                    st.error("Marque a confirmação antes de excluir.")
                else:
                    sucesso = excluir_clube(clube_id)

                    if sucesso is True:
                        st.success("Clube excluído com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro ao excluir clube: {sucesso}")