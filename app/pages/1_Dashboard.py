import streamlit as st
import pandas as pd
import plotly.express as px
from lib.sheets import read_df
from lib.utils import parse_brl, format_brl
import gspread
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)
# ==== GLOBAL STYLE ====
def css():
    st.markdown("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    .main {
        background-color: #0e1117;
    }

    .metric-card {
        background: #161b22;
        padding: 18px;
        border-radius: 10px;
        border: 1px solid #30363d;
        text-align:center;
        margin-bottom: 12px;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.15);
    }
    .metric-title {
        font-size:14px;
        color:#8b949e;
    }
    .metric-number {
        font-size:26px;
        font-weight:700;
        color:white;
    }

    .stDataFrame {
        border-radius: 10px !important;
    }

    .stButton>button {
        background: #238636 !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
    }

    .stTextInput>div>div>input, .stSelectbox, .stDateInput {
        border-radius: 8px !important;
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        padding: 8px !important;
    }

    </style>
    """, unsafe_allow_html=True)

css()  # aplica estilo global

# ========================== DASHBOARD ==========================

st.title("📊 Dashboard — Vendas e Faturamento")

df = read_df()

if df.empty:
    st.warning("Nenhuma venda cadastrada ainda.")
    st.stop()

df["Valor_float"] = df["Valor"].apply(parse_brl)
df["ValorPago_float"] = df["Valor Pago"].apply(parse_brl)

# ==== KPI CARDS ====
total_vendas = len(df)
faturamento = df["Valor_float"].sum()
recebido = df["ValorPago_float"].sum()
pendente = faturamento - recebido

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='metric-card'><div class='metric-title'>Vendas</div><div class='metric-number'>{total_vendas}</div></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-card'><div class='metric-title'>Faturamento</div><div class='metric-number'>{format_brl(faturamento)}</div></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-card'><div class='metric-title'>Recebido</div><div class='metric-number'>{format_brl(recebido)}</div></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-card'><div class='metric-title'>Pendente</div><div class='metric-number'>{format_brl(pendente)}</div></div>", unsafe_allow_html=True)

st.write(" ")

# ==== GRÁFICO POR STATUS ====
if "Status" in df.columns:
    fig_status = px.bar(
        df.groupby("Status").size().reset_index(name="Vendas"),
        x="Status",
        y="Vendas",
        title="Vendas por Status",
        text="Vendas"
    )
    fig_status.update_layout(template="plotly_dark")
    st.plotly_chart(fig_status, use_container_width=True)

# ==== GRÁFICO POR MÊS ====
if "Data Venda" in df.columns and df["Data Venda"].notna().any():
    df["DataVendaTS"] = pd.to_datetime(df["Data Venda"], errors="coerce")
    monthly = df.dropna(subset=["DataVendaTS"]).copy()

    if not monthly.empty:
        monthly["Mes"] = monthly["DataVendaTS"].dt.to_period("M").dt.to_timestamp()
        grp = monthly.groupby("Mes")["Valor_float"].sum().reset_index()

        fig_mes = px.line(
            grp, x="Mes", y="Valor_float",
            title="Faturamento por Mês",
            markers=True
        )
        fig_mes.update_layout(template="plotly_dark")
        st.plotly_chart(fig_mes, use_container_width=True)
