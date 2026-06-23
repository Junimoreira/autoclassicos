import streamlit as st
from database.dashboard_db import buscar_resumo_dashboard


def card(titulo, valor, icone):

    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #FFFFFF 0%, #F4F7FB 100%);
            border-left: 6px solid #D4AF37;
            border-radius: 14px;
            padding: 22px;
            box-shadow: 0 4px 14px rgba(13, 44, 84, 0.16);
            min-height: 130px;
        ">
            <div style="
                font-size: 16px;
                color: #0D2C54;
                font-weight: 700;
                margin-bottom: 8px;
            ">
                {icone} {titulo}
            </div>
            <div style="
                font-size: 38px;
                color: #1E5AA8;
                font-weight: 900;
            ">
                {valor}
            </div>
        </div>
    """, unsafe_allow_html=True)


def tela_dashboard():

    st.title("📊 Dashboard")

    resumo = buscar_resumo_dashboard()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        card("Eventos", resumo["eventos"], "📅")

    with col2:
        card("Clubes", resumo["clubes"], "🏁")

    with col3:
        card("Participantes", resumo["participantes"], "👤")

    with col4:
        card("Veículos", resumo["veiculos"], "🚗")

    st.divider()

    st.subheader("🚗 AutoClássicos")
    st.info("Sistema de gestão de encontros de carros antigos.")