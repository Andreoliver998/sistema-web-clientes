import streamlit as st
from pathlib import Path
import base64

# ========= CONFIG =========
st.set_page_config(page_title="CRM de Vendas", page_icon="🧾", layout="wide")

# ========= CSS PAINEL =========
def css_app():
    st.markdown("""
    <style>
    body { background-color:#0e1117 !important; }
    .center-box {
        background: linear-gradient(90deg, #12151e, #161b22, #12151e);
        padding: 25px; border-radius: 12px; border: 1px solid #2d323b;
        text-align: center; margin-bottom: 40px;
    }
    .title { font-size: 28px; font-weight: 800; color: #ffffff; }
    .subtitle { font-size: 14px; color: #a6a6a6; margin-top: -4px; }
    .logo-section { text-align:center; margin-top: 40px; margin-bottom: 10px; }
    .logo-text { font-size: 22px; font-weight: 700; color: white; margin-top: 10px; }
    .slogan { font-size: 14px; color: #9fa4ad; margin-top: -5px; }
    </style>
    """, unsafe_allow_html=True)

# ========= LOGO PAINEL =========
def exibir_logo_painel():
    # Caminho automático da logo (funciona no PC e no Streamlit Cloud)
    logo_path = Path(__file__).resolve().parent / "assets" / "logo_dashboard.png"

    if logo_path.exists():
        with open(logo_path, "rb") as img:
            base = base64.b64encode(img.read()).decode()
        st.markdown(
            f"""
            <div class='logo-section'>
                <img src="data:image/png;base64,{base}" width="280px">
                <div class='logo-text'>ga-suautoestima.com.br</div>
                <div class='slogan'>Bem-vindo ao seu painel de gestão</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(f"❗ Logo não encontrada no caminho: {logo_path}")

# ========= LOGIN DESATIVADO =========
# Sistema entra direto
st.session_state.logged = True

# ========= PAINEL LIBERADO =========
css_app()

# ========= HEADER DO PAINEL =========
st.markdown("""
<div class='center-box'>
    <div class='title'>📑 Sistema de Controle</div>
    <div class='subtitle'>Sistema conectado, rápido e profissional</div>
</div>
""", unsafe_allow_html=True)

exibir_logo_painel()

# Aqui você coloca o restante do seu painel
#st.write("✅ Sistema carregado com sucesso!")
#st.write("Agora você pode adicionar tabelas, gráficos e páginas aqui.")
