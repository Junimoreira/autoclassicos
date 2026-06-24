import streamlit as st
import qrcode
from io import BytesIO

from database.eventos_db import listar_eventos
from database.clubes_db import listar_clubes
from database.inscricao_publica_db import cadastrar_inscricao_publica


def gerar_qrcode(valor):

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(valor)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    return buffer.getvalue()


def tela_inscricao_publica():

    st.title("🚗 Inscrição para Evento")

    if st.session_state.get("inscricao_publica_sucesso"):

        numero = st.session_state.get("numero_inscricao_publica")
        uuid_qrcode = st.session_state.get("uuid_qrcode_publica")

        st.success(
            f"Inscrição realizada com sucesso! Número da inscrição: {numero}"
        )

        if uuid_qrcode:

            st.info(
                f"Código de validação da inscrição: {uuid_qrcode}"
            )

            imagem_qrcode = gerar_qrcode(uuid_qrcode)

            st.image(
                imagem_qrcode,
                caption="QR Code da Inscrição",
                width=250
            )

            st.download_button(
                label="Baixar QR Code",
                data=imagem_qrcode,
                file_name=f"qrcode_inscricao_{numero}.png",
                mime="image/png"
            )

        st.session_state["inscricao_publica_sucesso"] = False
        st.session_state["numero_inscricao_publica"] = None
        st.session_state["uuid_qrcode_publica"] = None

    st.info(
        "Preencha seus dados para participar do evento."
    )

    eventos = listar_eventos()
    clubes = listar_clubes()

    if eventos.empty:
        st.warning(
            "Não há eventos disponíveis para inscrição."
        )
        return

    lista_clubes = [None]

    if not clubes.empty:
        lista_clubes += clubes["id"].tolist()

    with st.form(
        "form_inscricao_publica",
        clear_on_submit=True
    ):

        st.subheader("📅 Evento")

        evento_id = st.selectbox(
            "Evento",
            eventos["id"].tolist(),
            format_func=lambda x:
            eventos.loc[
                eventos["id"] == x,
                "nome"
            ].values[0]
        )

        st.divider()

        st.subheader("👤 Dados do Participante")

        nome = st.text_input("Nome Completo")

        telefone = st.text_input("Telefone")

        email = st.text_input("E-mail")

        cidade = st.text_input("Cidade")

        estado = st.text_input(
            "Estado",
            max_chars=2
        )

        clube_id = st.selectbox(
            "Clube",
            lista_clubes,
            format_func=lambda x:
            "Sem clube"
            if x is None
            else clubes.loc[
                clubes["id"] == x,
                "nome"
            ].values[0]
        )

        primeira_participacao = st.checkbox(
            "Primeira participação no evento?"
        )

        autorizacao_imagem = st.checkbox(
            "Autorizo uso de imagem",
            value=True
        )

        observacoes = st.text_area(
            "Observações"
        )

        st.divider()

        st.subheader("🚗 Dados do Veículo")

        marca = st.text_input("Marca")

        modelo = st.text_input("Modelo")

        ano = st.number_input(
            "Ano",
            min_value=1900,
            max_value=2100,
            value=1980
        )

        cor = st.text_input("Cor")

        placa = st.text_input("Placa")

        categoria = st.selectbox(
            "Categoria",
            [
                "Carro Antigo",
                "Motocicleta",
                "Utilitário",
                "Caminhão",
                "Outro"
            ]
        )

        st.divider()

        st.subheader("📝 Dados da Inscrição")

        quantidade_pessoas = st.number_input(
            "Quantidade de Pessoas",
            min_value=1,
            value=1
        )

        chegada_prevista = st.date_input(
            "Chegada Prevista",
            format="DD/MM/YYYY"
        )

        saida_prevista = st.date_input(
            "Saída Prevista",
            format="DD/MM/YYYY"
        )

        enviar = st.form_submit_button(
            "Enviar Inscrição"
        )

        if enviar:

            if not nome.strip():

                st.error(
                    "Informe seu nome."
                )

            elif not telefone.strip():

                st.error(
                    "Informe seu telefone."
                )

            elif not cidade.strip():

                st.error(
                    "Informe sua cidade."
                )

            elif not estado.strip():

                st.error(
                    "Informe seu estado."
                )

            elif not marca.strip():

                st.error(
                    "Informe a marca do veículo."
                )

            elif not modelo.strip():

                st.error(
                    "Informe o modelo do veículo."
                )

            else:

                sucesso, resultado = cadastrar_inscricao_publica(
                    evento_id=evento_id,
                    nome=nome.strip(),
                    telefone=telefone.strip(),
                    email=email.strip(),
                    cidade=cidade.strip(),
                    estado=estado.strip().upper(),
                    clube_id=clube_id,
                    primeira_participacao=primeira_participacao,
                    autorizacao_imagem=autorizacao_imagem,
                    observacoes_participante=observacoes.strip(),
                    marca=marca.strip(),
                    modelo=modelo.strip(),
                    ano=int(ano),
                    cor=cor.strip(),
                    placa=placa.strip().upper(),
                    categoria=categoria,
                    quantidade_pessoas=int(quantidade_pessoas),
                    chegada_prevista=chegada_prevista,
                    saida_prevista=saida_prevista
                )

                if sucesso:

                    st.session_state["inscricao_publica_sucesso"] = True
                    st.session_state["numero_inscricao_publica"] = resultado.get(
                        "numero_inscricao"
                    )
                    st.session_state["uuid_qrcode_publica"] = resultado.get(
                        "uuid_qrcode"
                    )

                    st.rerun()

                else:

                    st.error(
                        f"Erro ao realizar inscrição: {resultado}"
                    )