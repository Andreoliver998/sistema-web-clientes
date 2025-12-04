import streamlit as st
import pandas as pd
from lib.sheets import read_df
from io import BytesIO

# ================= CONFIG =================
st.set_page_config(page_title="CRM - Clientes", layout="wide")

if "cliente_sel" not in st.session_state:
    st.session_state.cliente_sel = None

# ================ CSS MODERNO ================
st.markdown("""
<style>
body, .main, .block-container {background:#0f1117;}
.card {
    background:#161b22;
    padding:18px; 
    border-radius:12px; 
    border:1px solid #2d323c;
    margin-bottom:10px;
}
.lbl {color:#8b949e; font-size:13px;}
.val {color:white; font-weight:600; font-size:15px;}
.bigvalue {font-size:26px; color:white; font-weight:700;}
</style>
""", unsafe_allow_html=True)

# ================ LOAD DATA =================
df = read_df().dropna(how="all")

if df.empty:
    st.info("Nenhum cliente registrado.")
    st.stop()

df = df.copy()

# Normalização
df["Telefone"] = df["Telefone"].astype(str)
df["Documento"] = df["Documento"].astype(str)
df["Telefone_Limp"] = df["Telefone"].str.replace(r'\D+', '', regex=True)
df["Documento_Limp"] = df["Documento"].str.replace(r'\D+', '', regex=True)

# ================ SIDEBAR FILTERS =================
with st.sidebar:
    st.title("🔍 Filtrar")
    busca = st.text_input("Nome / Email / Telefone / CPF")
    status = st.selectbox("Status", ["(Todos)"] + sorted(df["Status"].dropna().unique().tolist()))

    if st.button("Limpar Filtros"):
        st.session_state.clear()
        st.rerun()

# Filter logic
df_f = df.copy()

if busca:
    t = busca.lower()
    df_f = df_f[
        df_f["Comprador"].str.lower().str.contains(t, na=False) |
        df_f["E-mail"].str.lower().str.contains(t, na=False) |
        df_f["Telefone_Limp"].str.contains(t, na=False) |
        df_f["Documento_Limp"].str.contains(t, na=False)
    ]

if status != "(Todos)":
    df_f = df_f[df_f["Status"] == status]

# Metrics
total = len(df)
filtrados = len(df_f)
valor_pago = pd.to_numeric(df_f["Valor Pago"].astype(str).str.replace(",", "."), errors="coerce").sum()

# ================ HEADER CARDS =================
col1, col2, col3 = st.columns(3)
col1.markdown(f"<div class='card'><div class='lbl'>Clientes Filtrados</div><div class='bigvalue'>{filtrados}</div></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='card'><div class='lbl'>Total Registros</div><div class='bigvalue'>{total}</div></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='card'><div class='lbl'>Total em Pagamentos</div><div class='bigvalue'>R$ {valor_pago:,.2f}</div></div>", unsafe_allow_html=True)

# ================ TABLE =================
st.subheader("📄 Registros")

st.dataframe(df_f, use_container_width=True, height=350)

# ================ SELECT CLIENT =================
st.subheader("👤 Ficha do Cliente")

chaves = df_f["Chave"].astype(str).tolist()
if not chaves:
    st.warning("Nenhum cliente encontrado com esses filtros.")
    st.stop()

if st.session_state.cliente_sel not in chaves:
    st.session_state.cliente_sel = chaves[0]

sel = st.selectbox("Selecione", options=chaves, index=chaves.index(st.session_state.cliente_sel))

if sel != st.session_state.cliente_sel:
    st.session_state.cliente_sel = sel
    st.rerun()

cliente = df_f[df_f["Chave"] == sel].iloc[0]

# ================ CLIENT CARD =================
st.markdown("### 🧾 Dados do Cliente")
cols = st.columns(2)

info = {
    "Nome": cliente["Comprador"],
    "E-mail": cliente["E-mail"],
    "Telefone": cliente["Telefone"],
    "Documento": cliente["Documento"],
    "Produtor": cliente["Produtor"],
    "Produto": cliente["Produto"],
    "Plano": cliente["Plano"],
    "Pagamento": cliente["Pagamento"],
    "Status": cliente["Status"],
    "Valor": cliente["Valor"],
    "Valor Pago": cliente["Valor Pago"],
    "Data de Venda": cliente["Data Venda"],
    "Data Pagamento": cliente["Data Pagamento"],
    "Frete": cliente["Tipo do Frete"],
    "Rastreio": cliente["Código de Rastreio"]
    
}

i = 0
for k, v in info.items():
    col = cols[i % 2]
    col.markdown(f"<div class='card'><div class='lbl'>{k}</div><div class='val'>{v}</div></div>", unsafe_allow_html=True)
    i += 1

with st.expander("📍 Endereço"):
    st.write(f"**CEP:** {cliente['CEP']}")
    st.write(f"**Endereço:** {cliente['Endereço']}, {cliente['Número']}")
    st.write(f"**Complemento:** {cliente['Complemento']}")
    st.write(f"**Bairro:** {cliente['Bairro']}")
    st.write(f"**Cidade:** {cliente['Cidade']} - {cliente['Estado']}")


# WhatsApp Button
phone = cliente["Telefone_Limp"]
st.link_button("💬 WhatsApp", f"https://wa.me/{phone}?text=Olá%20{cliente['Comprador']},%20tudo%20bem?")
