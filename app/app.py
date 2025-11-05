import streamlit as st
from pathlib import Path
import base64

# ========= CONFIG =========
st.set_page_config(page_title="CRM de Vendas", page_icon="🧾", layout="wide")

# ========= CSS TELA LOGIN =========
def css_login_mode():
    st.markdown("""
    <style>
    [data-testid="stSidebar"], header, footer { display: none !important; }
    body { background-color: #0e1117 !important; }
    .center-login {
        display:flex; flex-direction:column; justify-content:center; align-items:center;
        height:10vh; text-align:center;
    }
    .login-box {
        background:#161b22; padding:35px; border-radius:12px; width:350px;
        border:1px solid #2d323b; box-shadow:0px 0px 12px rgba(0,0,0,0.45);
    }
    .login-title { font-size:22px; font-weight:700; color:white; margin-bottom:5px; }
    .login-sub { font-size:14px; color:#9fa4ad; margin-bottom:20px; }
    </style>
    """, unsafe_allow_html=True)

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

# ========= LOGO LOGIN =========
def exibir_logo(path="assets/logo.png", width=200):
    try:
        with open(path, "rb") as img:
            base = base64.b64encode(img.read()).decode()
        st.markdown(f"<img src='data:image/png;base64,{base}' width='{width}px' style='margin-bottom:20px;'>",
                    unsafe_allow_html=True)
    except:
        st.warning("assets/logo.png")

# ========= LOGO PAINEL =========
def exibir_logo_painel():
    try:
        with open("assets/logo_dashboard.png", "rb") as img:
            base = base64.b64encode(img.read()).decode()
        st.markdown(
            f"""
            <div class='logo-section'>
                <img src="data:image/png;base64,{base}" width="280px">
                <div class='logo-text'>ga-suautoestima.com.br</div>
                <div class='slogan'>Bem-vindo ao seu painel de gestão</div>
            </div>
            """, unsafe_allow_html=True
        )
    except:
        st.warning("📎 Adicione: assets/logo_dashboard.png")

# ========= LOGIN =========
def tela_login():
    css_login_mode()
    st.markdown('<div class="center-login">', unsafe_allow_html=True)

   # exibir_logo(220)
    st.markdown("""
        <div class='login-box'>
            <div class='login-title'>Acesso ao Sistema</div>
            <div class='login-sub'>Digite suas credenciais</div>
    """, unsafe_allow_html=True)

    user = st.text_input("Usuário")
    pwd = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if user == st.secrets["auth"]["username"] and pwd == st.secrets["auth"]["password"]:
            st.session_state.logged = True
            st.rerun()
        else:
            st.error("❌ Usuário ou senha inválidos")

    st.markdown("</div></div>", unsafe_allow_html=True)

# ========= CONTROLE DE SESSÃO =========
if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    tela_login()
    st.stop()

# ========= PAINEL LIBERADO =========
css_app()

#st.sidebar.success("✅ Login confirmado — acesso liberado")
if st.sidebar.button("Sair"):
    st.session_state.logged = False
    st.rerun()

# ========= HEADER DO PAINEL =========
st.markdown("""
<div class='center-box'>
    <div class='title'>📑 Sistema de Controle</div>
    <div class='subtitle'>Sistema conectado, rápido e profissional</div>
</div>
""", unsafe_allow_html=True)

exibir_logo_painel()
