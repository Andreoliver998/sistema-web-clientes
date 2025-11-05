\
import re
import requests
import pandas as pd

def format_phone_br(phone: str) -> str:
    if not phone:
        return ""
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    if len(digits) == 10:
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    return phone

def parse_brl(value: str) -> float:
    if value is None:
        return 0.0
    s = str(value).strip()
    if not s:
        return 0.0
    s = s.replace("R$", "").replace(" ", "")
    s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0

def format_brl(n: float) -> str:
    try:
        return f"R$ {n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return f"R$ {n}"

def buscar_cep(cep: str) -> dict:
    if not cep:
        return {}
    digits = re.sub(r"\D", "", cep)
    if len(digits) != 8:
        return {}
    url = f"https://viacep.com.br/ws/{digits}/json/"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            if data.get("erro"):
                return {}
            return {
                "Endereço": data.get("logradouro", ""),
                "Bairro": data.get("bairro", ""),
                "Cidade": data.get("localidade", ""),
                "Estado": data.get("uf", ""),
            }
    except requests.RequestException:
        pass
    return {}

def to_date_str(dt) -> str:
    if dt is None or dt == "":
        return ""
    if isinstance(dt, (pd.Timestamp, )):
        return str(dt.date())
    if hasattr(dt, "strftime"):
        return dt.strftime("%Y-%m-%d")
    return str(dt)
