import streamlit as st
import pandas as pd
from datetime import date

from database.eventos_db import (
    listar_eventos,
    cadastrar_evento,
    atualizar_evento,
    excluir_evento
)


def tela_eventos():

    st.title("📅 Gestão de Eventos")

    abas = st.tabs([
        "📋 Listar",
        "➕ Cadastrar",
        "✏️ Editar",
        "🗑️ Excluir"
    ])

    # =========================
    # LISTAR
    # =========================
    with abas[0]:

        st.subheader("📋 Eventos cadastrados")

        df = listar_eventos()

        if df.empty:
            st.info("Nenhum evento cadastrado.")
        else:
            st.dataframe(df, use_container_width=True)

    # =========================
    # CADASTRAR
    # =========================
    with abas[1]:

        st.subheader("➕ Cadastrar Evento")

        with st.form("form_cadastrar_evento"):

            nome = st.text_input("Nome do Evento")
            cidade = st.text_input("Cidade")
            estado = st.text_input("Estado", max_chars=2)
            local_evento = st.text_input("Local do Evento")

            col1, col2 = st.columns(2)

            with col1:
                data_inicio = st.date_input("Data de Início", value=date.today())

            with col2:
                data_fim = st.date_input("Data de Fim", value=date.today())

            descricao = st.text_area("Descrição")
            ativo = st.checkbox("Evento ativo", value=True)

            salvar = st.form_submit_button("Salvar Evento")

            if salvar:

                if not nome.strip():
                    st.error("Informe o nome do evento.")
                else:
                    sucesso = cadastrar_evento(
                        nome,
                        cidade,
                        estado.upper(),
                        local_evento,
                        data_inicio,
                        data_fim,
                        descricao,
                        ativo
                    )

                    if sucesso:
                        st.success("Evento cadastrado com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao cadastrar evento.")

    # =========================
    # EDITAR
    # =========================
    with abas[2]:

        st.subheader("✏️ Editar Evento")

        df = listar_eventos()

        if df.empty:
            st.info("Nenhum evento cadastrado para editar.")
        else:
            evento_id = st.selectbox(
                "Selecione o evento",
                df["id"].tolist(),
                format_func=lambda x: df.loc[df["id"] == x, "nome"].values[0]
            )

            evento = df[df["id"] == evento_id].iloc[0]

            with st.form("form_editar_evento"):

                nome = st.text_input("Nome do Evento", value=evento["nome"])
                cidade = st.text_input("Cidade", value=evento["cidade"] or "")
                estado = st.text_input("Estado", value=evento["estado"] or "", max_chars=2)
                local_evento = st.text_input("Local do Evento", value=evento["local_evento"] or "")

                col1, col2 = st.columns(2)

                data_inicio_valor = pd.to_datetime(evento["data_inicio"]).date() if pd.notna(evento["data_inicio"]) else date.today()
                data_fim_valor = pd.to_datetime(evento["data_fim"]).date() if pd.notna(evento["data_fim"]) else date.today()

                with col1:
                    data_inicio = st.date_input("Data de Início", value=data_inicio_valor)

                with col2:
                    data_fim = st.date_input("Data de Fim", value=data_fim_valor)

                descricao = st.text_area("Descrição", value=evento["descricao"] or "")
                ativo = st.checkbox("Evento ativo", value=bool(evento["ativo"]))

                salvar = st.form_submit_button("Salvar Alterações")

                if salvar:

                    if not nome.strip():
                        st.error("Informe o nome do evento.")
                    else:
                        sucesso = atualizar_evento(
                            evento_id,
                            nome,
                            cidade,
                            estado.upper(),
                            local_evento,
                            data_inicio,
                            data_fim,
                            descricao,
                            ativo
                        )

                        if sucesso:
                            st.success("Evento atualizado com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao atualizar evento.")

    # =========================
    # EXCLUIR
    # =========================
    with abas[3]:

        st.subheader("🗑️ Excluir Evento")

        df = listar_eventos()

        if df.empty:
            st.info("Nenhum evento cadastrado para excluir.")
        else:
            evento_id = st.selectbox(
                "Selecione o evento para excluir",
                df["id"].tolist(),
                format_func=lambda x: df.loc[df["id"] == x, "nome"].values[0],
                key="excluir_evento"
            )

            evento = df[df["id"] == evento_id].iloc[0]

            st.warning(f"Você está prestes a excluir: {evento['nome']}")

            confirmar = st.checkbox("Confirmo que desejo excluir este evento")

            if st.button("Excluir Evento"):

                if not confirmar:
                    st.error("Marque a confirmação antes de excluir.")
                else:
                    sucesso = excluir_evento(evento_id)

                    if sucesso:
                        st.success("Evento excluído com sucesso!")
                        st.rerun()
                    else:
                        st.error("Erro ao excluir evento.")