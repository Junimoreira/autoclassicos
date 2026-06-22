import streamlit as st

from database.veiculos_db import (
    listar_veiculos,
    cadastrar_veiculo,
    atualizar_veiculo,
    excluir_veiculo
)

from database.participantes_db import listar_participantes


def _opcoes_participantes():
    df = listar_participantes()

    opcoes = {}

    if not df.empty:
        for _, row in df.iterrows():
            opcoes[int(row["id"])] = row["nome"]

    return opcoes


def tela_veiculos():

    st.title("🚗 Gestão de Veículos")

    if st.session_state.get("veiculo_cadastrado"):
        st.success("Veículo cadastrado com sucesso!")
        st.session_state["veiculo_cadastrado"] = False

    abas = st.tabs([
        "📋 Listar",
        "➕ Cadastrar",
        "✏️ Editar",
        "🗑️ Excluir"
    ])

    with abas[0]:

        st.subheader("📋 Veículos cadastrados")

        df = listar_veiculos()

        if df.empty:
            st.info("Nenhum veículo cadastrado.")
        else:
            st.dataframe(df, use_container_width=True)

    with abas[1]:

        st.subheader("➕ Cadastrar Veículo")

        participantes = _opcoes_participantes()

        if not participantes:
            st.warning("Cadastre um participante antes de cadastrar o veículo.")
            return

        with st.form("form_cadastrar_veiculo", clear_on_submit=True):

            participante_id = st.selectbox(
                "Proprietário / Participante",
                list(participantes.keys()),
                format_func=lambda x: participantes[x]
            )

            col1, col2 = st.columns(2)

            with col1:
                marca = st.text_input("Marca")
                modelo = st.text_input("Modelo")
                ano = st.number_input("Ano", min_value=1900, max_value=2100, step=1)

            with col2:
                cor = st.text_input("Cor")
                placa = st.text_input("Placa")
                categoria = st.selectbox(
                    "Categoria",
                    ["Automóvel", "Moto", "Caminhão", "Utilitário", "Outro"]
                )

            foto = st.text_input("Foto/URL da imagem (opcional)")
            descricao = st.text_area("Descrição / Observações")

            salvar = st.form_submit_button("Salvar Veículo")

            if salvar:

                if not marca.strip():
                    st.error("Informe a marca do veículo.")
                elif not modelo.strip():
                    st.error("Informe o modelo do veículo.")
                else:
                    sucesso = cadastrar_veiculo(
                        participante_id,
                        marca.strip(),
                        modelo.strip(),
                        int(ano) if ano else None,
                        cor.strip(),
                        placa.strip().upper(),
                        categoria,
                        foto.strip(),
                        descricao.strip()
                    )

                    if sucesso is True:
                        st.session_state["veiculo_cadastrado"] = True
                        st.rerun()
                    else:
                        st.error(f"Erro ao cadastrar veículo: {sucesso}")

    with abas[2]:

        st.subheader("✏️ Editar Veículo")

        df = listar_veiculos()
        participantes = _opcoes_participantes()

        if df.empty:
            st.info("Nenhum veículo cadastrado para editar.")
        elif not participantes:
            st.warning("Nenhum participante cadastrado.")
        else:
            veiculo_id = st.selectbox(
                "Selecione o veículo",
                df["id"].tolist(),
                format_func=lambda x: f"{df.loc[df['id'] == x, 'marca'].values[0]} {df.loc[df['id'] == x, 'modelo'].values[0]} - {df.loc[df['id'] == x, 'placa'].values[0]}"
            )

            veiculo = df[df["id"] == veiculo_id].iloc[0]

            with st.form("form_editar_veiculo"):

                participante_atual = int(veiculo["participante_id"])

                participante_id = st.selectbox(
                    "Proprietário / Participante",
                    list(participantes.keys()),
                    index=list(participantes.keys()).index(participante_atual)
                    if participante_atual in participantes else 0,
                    format_func=lambda x: participantes[x]
                )

                col1, col2 = st.columns(2)

                with col1:
                    marca = st.text_input("Marca", value=veiculo["marca"] or "")
                    modelo = st.text_input("Modelo", value=veiculo["modelo"] or "")
                    ano = st.number_input(
                        "Ano",
                        min_value=1900,
                        max_value=2100,
                        step=1,
                        value=int(veiculo["ano"]) if veiculo["ano"] else 1900
                    )

                with col2:
                    cor = st.text_input("Cor", value=veiculo["cor"] or "")
                    placa = st.text_input("Placa", value=veiculo["placa"] or "")
                    categoria = st.selectbox(
                        "Categoria",
                        ["Automóvel", "Moto", "Caminhão", "Utilitário", "Outro"],
                        index=["Automóvel", "Moto", "Caminhão", "Utilitário", "Outro"].index(veiculo["categoria"])
                        if veiculo["categoria"] in ["Automóvel", "Moto", "Caminhão", "Utilitário", "Outro"] else 0
                    )

                foto = st.text_input("Foto/URL da imagem (opcional)", value=veiculo["foto"] or "")
                descricao = st.text_area("Descrição / Observações", value=veiculo["descricao"] or "")

                salvar = st.form_submit_button("Salvar Alterações")

                if salvar:

                    if not marca.strip():
                        st.error("Informe a marca do veículo.")
                    elif not modelo.strip():
                        st.error("Informe o modelo do veículo.")
                    else:
                        sucesso = atualizar_veiculo(
                            veiculo_id,
                            participante_id,
                            marca.strip(),
                            modelo.strip(),
                            int(ano) if ano else None,
                            cor.strip(),
                            placa.strip().upper(),
                            categoria,
                            foto.strip(),
                            descricao.strip()
                        )

                        if sucesso is True:
                            st.success("Veículo atualizado com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"Erro ao atualizar veículo: {sucesso}")

    with abas[3]:

        st.subheader("🗑️ Excluir Veículo")

        df = listar_veiculos()

        if df.empty:
            st.info("Nenhum veículo cadastrado para excluir.")
        else:
            veiculo_id = st.selectbox(
                "Selecione o veículo para excluir",
                df["id"].tolist(),
                format_func=lambda x: f"{df.loc[df['id'] == x, 'marca'].values[0]} {df.loc[df['id'] == x, 'modelo'].values[0]} - {df.loc[df['id'] == x, 'placa'].values[0]}",
                key="excluir_veiculo"
            )

            veiculo = df[df["id"] == veiculo_id].iloc[0]

            st.warning(
                f"Você está prestes a excluir: {veiculo['marca']} {veiculo['modelo']} - {veiculo['placa']}"
            )

            confirmar = st.checkbox("Confirmo que desejo excluir este veículo")

            if st.button("Excluir Veículo"):

                if not confirmar:
                    st.error("Marque a confirmação antes de excluir.")
                else:
                    sucesso = excluir_veiculo(veiculo_id)

                    if sucesso is True:
                        st.success("Veículo excluído com sucesso!")
                        st.rerun()
                    else:
                        st.error(f"Erro ao excluir veículo: {sucesso}")