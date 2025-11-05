import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ✅ Escopos mínimos (melhor segurança)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# ✅ Colunas esperadas — SEM criar, apenas valida
COLUMNS = [
    "Chave","Produtor","Produto","Plano","Comprador","E-mail","Telefone","CEP",
    "Endereço","Número","Complemento","Bairro","Cidade","Estado","Documento",
    "Parcelamento","Pagamento","Status","Valor","Valor Pago","Data Venda",
    "Data Pagamento","Tipo do Frete","Código de Rastreio"
]

SHEET_NAME = "clientes"


# ---------------- FUNÇÃO DE CONEXÃO ----------------

@st.cache_resource(show_spinner=False)
def _get_ws():
    """Retorna worksheet existente sem criar nada automaticamente."""

    sa_info = st.secrets.get("google_service_account")
    if not sa_info:
        raise RuntimeError("❌ Credencial 'google_service_account' não encontrada em st.secrets.")

    if "sheets" not in st.secrets or "SHEET_ID" not in st.secrets["sheets"]:
        raise RuntimeError("❌ 'SHEET_ID' não configurado em st.secrets.")

    sheet_id = st.secrets["sheets"]["SHEET_ID"]

    # ✅ Somente leitura — boa prática & evita criação acidental
    creds = Credentials.from_service_account_info(sa_info, scopes=[
        "https://www.googleapis.com/auth/spreadsheets"
    ])

    client = gspread.authorize(creds)
    sh = client.open_by_key(sheet_id)

    # ✅ Não cria worksheet automaticamente — exige que exista
    try:
        ws = sh.worksheet(SHEET_NAME)
    except gspread.exceptions.WorksheetNotFound:
        raise RuntimeError(
            f"❌ Aba '{SHEET_NAME}' não existe.\n"
            f"📌 Vá no Google Sheets e crie manualmente.\n"
            f"📎 Coloque exatamente estes cabeçalhos na primeira linha:\n\n{', '.join(COLUMNS)}"
        )

    # ✅ Validação do cabeçalho — sem reescrever, só alerta
    header = ws.row_values(1)
    if header != COLUMNS:
        raise RuntimeError(
            "⚠️ Cabeçalho da planilha não corresponde aos campos esperados.\n"
            "Corrija no Google Sheets.\n\n"
            f"Esperado:\n{', '.join(COLUMNS)}\n\n"
            f"Encontrado:\n{', '.join(header)}"
        )

    return ws


# ---------------- LEITURA DE DADOS ----------------

def read_df():
    """Retorna DataFrame com os dados do Google Sheets, sem alterar nada."""
    ws = _get_ws()
    values = ws.get_all_values()

    if not values or len(values) < 2:
        return pd.DataFrame(columns=COLUMNS)

    # ✅ remove colunas duplicadas
    df = pd.DataFrame(values[1:], columns=values[0])
    df = df.loc[:, ~df.columns.duplicated()]
    return df


# ---------------- ESCRITA CONTROLADA ----------------

def append_row(row_dict):
    """Adiciona linha sem criar colunas extras."""
    ws = _get_ws()
    row = [row_dict.get(c, "") for c in COLUMNS]
    ws.append_row(row, table_range="A1")


def update_row(row_index, row_dict):
    """Edita linha sem criar cabeçalhos/células extras."""
    ws = _get_ws()
    row = [row_dict.get(c, "") for c in COLUMNS]
    start_col = "A"
    end_col = chr(ord("A") + len(COLUMNS) - 1)
    cell_range = f"{start_col}{row_index+2}:{end_col}{row_index+2}"
    ws.update(cell_range, [row])


# ---------------- GERADOR DE CHAVE ----------------

def generate_monthly_key(df, date_str):
    """Gera chave única ano-mês-sequencial."""
    try:
        ts = pd.to_datetime(date_str, errors="coerce")
        ym = f"{ts.year:04d}-{ts.month:02d}" if ts is not None else None
    except:
        ym = None

    if not ym:
        now = pd.Timestamp.now(tz="America/Sao_Paulo")
        ym = f"{now.year:04d}-{now.month:02d}"

    existing = df[df["Chave"].str.startswith(ym + "-")]["Chave"]
    seq = max([int(x.split("-")[-1]) for x in existing], default=0) + 1 if not existing.empty else 1

    return f"{ym}-{seq:04d}"
