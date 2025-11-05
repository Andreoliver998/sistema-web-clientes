import streamlit as st, pandas as pd
from lib.sheets import read_df, append_row, generate_monthly_key
from lib.utils import buscar_cep, format_phone_br, parse_brl, to_date_str
import gspread
st.title("➕ Nova Venda")
df = read_df()

with st.form("cad"):
    produtor = st.text_input("Produtor")
    produto = st.text_input("Produto")
    plano = st.text_input("Plano")

    comprador = st.text_input("Comprador")
    email = st.text_input("Email")
    tel = st.text_input("Telefone")

    col1,col2 = st.columns(2)
    cep = col1.text_input("CEP")
    if col2.form_submit_button("Buscar CEP"):
        st.session_state["cep"] = buscar_cep(cep)

    cepd = st.session_state.get("cep",{})
    end = st.text_input("Endereço", cepd.get("Endereço",""))
    num = st.text_input("Número")
    comp = st.text_input("Complemento")
    bairro = st.text_input("Bairro", cepd.get("Bairro",""))
    cidade = st.text_input("Cidade", cepd.get("Cidade",""))
    estado = st.text_input("Estado", cepd.get("Estado",""))

    doc = st.text_input("CPF/CNPJ")
    parc = st.text_input("Parcelamento")
    pag = st.text_input("Forma de pagamento")
    status = st.selectbox("Status",["Pago","Pendente","Cancelado","Aguardando Pagamento","Chargeback"])

    v = st.text_input("Valor (150,00)")
    vp = st.text_input("Valor Pago (ex.: 0,00)")
    dv = st.date_input("Data Venda")
    dp = st.date_input("Data Pagamento", disabled=status!="Pago")

    frete = st.text_input("Tipo de Frete")
    rast = st.text_input("Código de Rastreio")

    ok = st.form_submit_button("Salvar")

if ok:
    chave = generate_monthly_key(df, to_date_str(dv))
    append_row({
        "Chave": chave,"Produtor":produtor,"Produto":produto,"Plano":plano,
        "Comprador":comprador,"E-mail":email,"Telefone":format_phone_br(tel),"CEP":cep,
        "Endereço":end,"Número":num,"Complemento":comp,"Bairro":bairro,"Cidade":cidade,"Estado":estado,
        "Documento":doc,"Parcelamento":parc,"Pagamento":pag,"Status":status,
        "Valor":f"{parse_brl(v):.2f}".replace(".",","),"Valor Pago":f"{parse_brl(vp):.2f}".replace(".",","),
        "Data Venda": to_date_str(dv),"Data Pagamento":to_date_str(dp) if status=="Pago" else "",
        "Tipo do Frete":frete,"Código de Rastreio":rast
    })
    st.success(f"✅ Venda cadastrada! Chave: {chave}")
