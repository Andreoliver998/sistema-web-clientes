\
from narwhals import col
import streamlit as st
import pandas as pd
from lib.sheets import read_df, append_row, generate_monthly_key
from lib.utils import buscar_cep, format_phone_br, parse_brl, to_date_str
import gspread
st.title("➕ Cadastrar Nova Venda")

STATUS_OPTS = ["Pago","Pendente","Cancelado","Aguardando Pagamento","Chargeback"]

with st.form("cadastro"):
    colp1, colp2, colp3, colp4 = st.columns(4)
    chave = colp1.text_input("Chave")
    produtor = colp2.text_input("Produtor")
    produto = colp3.text_input("Produto")
    plano = colp4. text_input("Plano")

    comprador = st.text_input("Comprador")
    email = st.text_input("E-mail")
    telefone = st.text_input("Telefone (autoformata)")

    col_cep1, col_cep2 = st.columns([1,1])
    cep = col_cep1.text_input("CEP (8 dígitos)")
    if col_cep2.form_submit_button("Buscar CEP"):
        st.session_state["_cep_fill"] = buscar_cep(cep)

    cep_data = st.session_state.get("_cep_fill", {})

    endereco = st.text_input("Endereço", value=cep_data.get("Endereço",""))
    numero = st.text_input("Número")
    complemento = st.text_input("Complemento")
    bairro = st.text_input("Bairro", value=cep_data.get("Bairro",""))
    colc1, colc2 = st.columns(2)
    cidade = colc1.text_input("Cidade", value=cep_data.get("Cidade",""))
    estado = colc2.text_input("Estado", value=cep_data.get("Estado",""))

    documento = st.text_input("Documento (CPF/CNPJ)")
    parcelamento = st.text_input("Parcelamento (ex.: 1/12)")
    pagamento = st.text_input("Forma de Pagamento (PIX, Cartão, Boleto...)")
    status = st.selectbox("Status", STATUS_OPTS, index=1)

    colv1, colv2 = st.columns(2)
    valor = colv1.text_input("Valor (ex.: 150,00)")
    valor_pago = colv2.text_input("Valor Pago (ex.: 0,00)")

    coldt1, coldt2 = st.columns(2)
    data_venda = coldt1.date_input("Data Venda", value=pd.Timestamp.now(tz="America/Sao_Paulo").date())
    data_pag = coldt2.date_input("Data Pagamento", value=None, disabled=(status!="Pago"))

    colf1, colf2 = st.columns(2)
    tipo_frete = colf1.text_input("Tipo do Frete")
    codigo_rastreio = colf2.text_input("Código de Rastreio")

    submitted = st.form_submit_button("Salvar Venda")

if submitted:
    df = read_df()
    chave = generate_monthly_key(df, to_date_str(data_venda))

    row = {
        "Chave": chave,
        "Produtor": produtor.strip(),
        "Produto": produto.strip(),
        "Plano": plano.strip(),
        "Comprador": comprador.strip(),
        "E-mail": email.strip(),
        "Telefone": format_phone_br(telefone),
        "CEP": str(cep).strip(),
        "Endereço": endereco.strip(),
        "Número": numero.strip(),
        "Complemento": complemento.strip(),
        "Bairro": bairro.strip(),
        "Cidade": cidade.strip(),
        "Estado": estado.strip(),
        "Documento": documento.strip(),
        "Parcelamento": parcelamento.strip(),
        "Pagamento": pagamento.strip(),
        "Status": status,
        "Valor": f"{parse_brl(valor):.2f}".replace(".", ","),
        "Valor Pago": f"{parse_brl(valor_pago):.2f}".replace(".", ","),
        "Data Venda": to_date_str(data_venda),
        "Data Pagamento": to_date_str(data_pag) if status=="Pago" else "",
        "Tipo do Frete": tipo_frete.strip(),
        "Código de Rastreio": codigo_rastreio.strip(),
    }
    append_row(row)
    st.success(f"Venda cadastrada! Chave: {chave}")
    if "_cep_fill" in st.session_state:
        del st.session_state["_cep_fill"]
