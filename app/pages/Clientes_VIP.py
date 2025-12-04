import streamlit as st
import pandas as pd
from lib.sheets import read_df
import gspread
st.set_page_config(
    page_title="Clientes VIP",
    page_icon="👑",
    layout="wide"
)
st.title("💎 Clientes VIP — Ranking & Ticket Médio")

df = read_df()

if df.empty:
    st.info("Nenhuma venda encontrada ainda.")
    st.stop()

# Conversão segura do Valor Pago (BRL -> float)
def to_float(v):
    try:
        v = str(v).replace("R","").replace("$","").replace(".","").replace(",",".")
        return float(v)
    except:
        return 0.0

df["Valor Pago Num"] = df["Valor Pago"].apply(to_float)

# Agrupamento
ranking = (
    df.groupby("Comprador")
    .agg(
        Total_Compras=("Comprador", "count"),
        Valor_Total=("Valor Pago Num", "sum"),
        Ticket_Medio=("Valor Pago Num", "mean")
    )
    .sort_values("Valor_Total", ascending=False)
)

ranking["Valor_Total"] = ranking["Valor_Total"].apply(lambda x: f"R$ {x:,.2f}")
ranking["Ticket_Medio"] = ranking["Ticket_Medio"].apply(lambda x: f"R$ {x:,.2f}")

st.subheader("🏆 Ranking de Clientes")
st.dataframe(ranking, use_container_width=True)

# Melhor cliente
melhor = ranking.iloc[0]
st.success(f"""
### 👑 Melhor Cliente Atual
**Cliente:** {ranking.index[0]}  
**Compras:** {melhor['Total_Compras']}  
**Total gasto:** {melhor['Valor_Total']}  
**Ticket médio:** {melhor['Ticket_Medio']}  
""")
