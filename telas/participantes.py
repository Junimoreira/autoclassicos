import streamlit as st

from database.participantes_db import (
    listar_participantes,
    cadastrar_participante,
    atualizar_participante,
    excluir_participante
)

from database.clubes_db import listar_clubes


def _opcoes_clubes():
    df_clubes = listar_clubes()

    opcoes = {0: "Sem clube"}

    if not df_clubes.empty:
        for _, row in df_clubes.iterrows():
            opcoes[int(row["id"])] = row["nome"]

    return opcoes


def tela_participantes():

    st.title("👤 Gestão de Participantes")

    if st.session_state.get("participante_cadastrado"):
        st.success("Participante cadastrado com sucesso!")
        st.session_state["participante_cadastrado"] = False

    abas = st.tabs([
        "📋 Listar",
        "➕ Cadastrar",
        "✏️ Editar",
        "🗑️ Excluir"
    ])

    with abas[0]:

        st.subheader("📋 Participantes cadastrados")

        df = listar_participantes()

        if df.empty:
            st.info("Nenhum participante cadastrado.")
        else:
            st.dataframe(df, use_container_width=True)

    with abas[1]:

        st.subheader("➕ Cadastrar Participante")

        clubes = _opcoes_clubes()

        with st.form("form_cadastrar_participante", clear_on_submit=True):

            nome = st.text_input("Nome")
            telefone = st.text_input("Telefone")
            email = st.text_input("E-mail")

            col1, col2 = st.columns(2)

            with col1:
                cidade = st.text_input("Cidade")

            with col2:
                estado = st.text_input("Estado", max_chars=2)

            clube_escolhido = st.selectbox(
                "Clube",
                list(clubes.keys()),
                format_func=lambda x: clubes[x]
            )

            primeira_participacao = st.checkbox("Primeira participação no evento?", value=True)
            autorizacao_imagem = st.checkbox("Autoriza uso de imagem?", value=True)

            observacoes = st.text_area("Observações")

            salvar = st.form_submit_button("Salvar Participante")

            if salvar:

                if not nome.strip():
                    st.error("Informe o nome do participante.")
                else:
                    clube_id = None if clube_escolhido == 0 else clube_escolhido

                    sucesso = cadastrar_participante(
                        nome.strip(),
                        telefone.strip(),
                        email.strip(),
                        cidade.strip(),
                        estado.strip().upper(),
                        clube_id,
                        primeira_participacao,
                        autorizacao_imagem,
                        observacoes.strip()
                    )

                    if sucesso is True:
                        st.session_state["participante_cadastrado"] = True
                        st.rerun()
                    else:
                        st.error(f"Erro ao cadastrar participante: {sucesso}")

    with abas[2]:

        st.subheader("✏️ Editar Participante")

        df = listar_participantes()
        clubes = _opcoes_clubes()

        if df.empty:
            st.info("Nenhum participante cadastrado para editar.")
        else:
            participante_id = st.selectbox(
                "Selecione o participante",
                df["id"].tolist(),
                format_func=lambda x: df.loc[df["id"] == x, "nome"].values[0]
            )

            participante = df[df["id"] == participante_id].iloc[0]

            clube_atual = participante["clube_id"]
            clube_atual = 0 if clube_atual is None else int(clube_atual)

            with st.form("form_editar_participante"):

                nome = st.text_input("Nome", value=participante["nome"])
                telefone = st.text_input("Telefone", value=participante["telefone"] or "")
                email = st.text_input("E-mail", value=participante["email"] or "")

                col1, col2 = st.columns(2)

                with col1:
                    cidade = st.text_input("Cidade", value=participante["cidade"] or "")

                with col2:
                    estado = st.text_input("Estado", value=participante["estado"] or "", max_chars=2)

                clube_escolhido = st.selectbox(
                    "Clube",
                    list(clubes.keys()),
                    index=list(clubes.keys()).index(clube_atual) if clube_atual in clubes else 0,
                    format_func=lambda x: clubes[x]
                )

                primeira_participacao = st.checkbox(
                    "Primeira participação no evento?",
                    value=bool(participante["primeira_participacao"])
                )

                autorizacao_imagem = st.checkbox(
                    "Autoriza uso de imagem?",
                    value=bool(participante["autorizacao_imagem"])
                )

                observacoes = st.text_area("Observações", value=participante["observacoes"] or "")

                salvar = st.form_submit_button("Salvar Alterações")

                if salvar:

                    if not nome.strip():
                        st.error("Informe o nome do participante.")
                    else:
                        clube_id = None if clube_escolhido == 0 else clube_escolhido

                        sucesso = atualizar_participante(
                            participante_id,
                            nome.strip(),
                            telefone.strip(),
                            email.strip(),
                            cidade.strip(),
                            estado.strip().upper(),
                            clube_id,
                            primeira_participacao,
                            autorizacao_imagem,
                            observacoes.strip()
                        )

                        if sucesso is True:
                            st.success("Participante atualizado com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"Erro ao atualizar participante: {sucesso}")

    with abas[3]:

        st.subheader("🗑️ Excluir Participante")

        df = listar_participantes()

        if df.empty:
            st.info("Nenhum participante cadastrado para excluir.")
        else:
            participante_id = st.selectbox(
                "Selecione o participante para excluir",
                df["id"].tolist(),
                format_func=lambda x: df.loc[df["id"] == x, "nome"].values[0],
                key="excluir_participante"
            )

            participante = df[df["id"] == participante_id].iloc[0]

            st.warning(f"Você está prestes a excluir: {participante['nome']}")

            confirmar = st.checkbox("Confirmo que desejo excluir este participante")

            if st.button("Excluir Participante"):

                if not confirmar:
                    st.error("Marque a confirmação antes de excluir.")
                else:
                    sucesso = excluir_participante(participante_id)

                    if sucesso is True:
                        st.success("Participante excluído com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro ao excluir participante: {sucesso}")