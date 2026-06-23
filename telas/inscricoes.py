import streamlit as st
import pandas as pd

from database.inscricoes_db import (
    listar_inscricoes,
    cadastrar_inscricao,
    excluir_inscricao
)

from database.eventos_db import listar_eventos
from database.participantes_db import listar_participantes
from database.veiculos_db import listar_veiculos


def tela_inscricoes():

    st.title("📝 Gestão de Inscrições")

    if st.session_state.get("inscricao_cadastrada"):
        st.success("Inscrição cadastrada com sucesso!")
        st.session_state["inscricao_cadastrada"] = False

    abas = st.tabs([
        "📋 Listar",
        "➕ Nova Inscrição",
        "🗑️ Excluir"
    ])

    # ==================================================
    # LISTAR
    # ==================================================
    with abas[0]:

        st.subheader("📋 Inscrições cadastradas")

        df = listar_inscricoes()

        if df.empty:
            st.info("Nenhuma inscrição cadastrada.")
        else:
            st.dataframe(df, use_container_width=True)

    # ==================================================
    # NOVA INSCRIÇÃO
    # ==================================================
    with abas[1]:

        st.subheader("➕ Nova Inscrição")

        eventos = listar_eventos()
        participantes = listar_participantes()
        veiculos = listar_veiculos()

        if eventos.empty:
            st.warning("Cadastre um evento primeiro.")
            return

        if participantes.empty:
            st.warning("Cadastre um participante primeiro.")
            return

        if veiculos.empty:
            st.warning("Cadastre um veículo primeiro.")
            return

        with st.form(
            "form_nova_inscricao",
            clear_on_submit=True
        ):

            evento_id = st.selectbox(
                "Evento",
                eventos["id"].tolist(),
                format_func=lambda x:
                eventos.loc[
                    eventos["id"] == x,
                    "nome"
                ].values[0]
            )

            participante_id = st.selectbox(
                "Participante",
                participantes["id"].tolist(),
                format_func=lambda x:
                participantes.loc[
                    participantes["id"] == x,
                    "nome"
                ].values[0]
            )

            veiculos_participante = veiculos[
                veiculos["participante_id"] == participante_id
            ]

            if veiculos_participante.empty:

                st.warning(
                    "Este participante não possui veículo cadastrado."
                )

                salvar = False

            else:

                veiculo_id = st.selectbox(
                    "Veículo",
                    veiculos_participante["id"].tolist(),
                    format_func=lambda x:
                    f"{veiculos_participante.loc[veiculos_participante['id'] == x, 'marca'].values[0]} "
                    f"{veiculos_participante.loc[veiculos_participante['id'] == x, 'modelo'].values[0]}"
                )

                quantidade_pessoas = st.number_input(
                    "Quantidade de Pessoas",
                    min_value=1,
                    value=1
                )

                chegada_prevista = st.date_input(
                    "Chegada Prevista"
                )

                saida_prevista = st.date_input(
                    "Saída Prevista"
                )

                observacoes = st.text_area(
                    "Observações"
                )

                salvar = st.form_submit_button(
                    "Salvar Inscrição"
                )

                if salvar:

                    sucesso = cadastrar_inscricao(
                        evento_id,
                        participante_id,
                        veiculo_id,
                        quantidade_pessoas,
                        chegada_prevista,
                        saida_prevista,
                        observacoes
                    )

                    if sucesso is True:

                        st.session_state["inscricao_cadastrada"] = True
                        st.rerun()

                    else:

                        st.error(
                            f"Erro ao cadastrar inscrição: {sucesso}"
                        )

    # ==================================================
    # EXCLUIR
    # ==================================================
    with abas[2]:

        st.subheader("🗑️ Excluir Inscrição")

        df = listar_inscricoes()

        if df.empty:

            st.info("Nenhuma inscrição cadastrada.")

        else:

            inscricao_id = st.selectbox(
                "Selecione a inscrição",
                df["id"].tolist(),
                format_func=lambda x:
                f"Inscrição Nº {df.loc[df['id'] == x, 'numero_inscricao'].values[0]}"
            )

            confirmar = st.checkbox(
                "Confirmo a exclusão"
            )

            if st.button("Excluir Inscrição"):

                if not confirmar:

                    st.error(
                        "Marque a confirmação."
                    )

                else:

                    sucesso = excluir_inscricao(
                        inscricao_id
                    )

                    if sucesso is True:

                        st.success(
                            "Inscrição excluída com sucesso!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            f"Erro ao excluir: {sucesso}"
                        )