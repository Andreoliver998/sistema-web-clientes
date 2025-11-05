# 🗂️ CRM Pessoal — Streamlit + Google Sheets

Sistema web simples para **consultar, cadastrar, editar e excluir clientes** diretamente de uma **planilha do Google Sheets**, com **Dashboard** em **Plotly**.

## 🚀 Como rodar

1. **Pré‑requisitos**
   - Python 3.10+
   - Conta no Google Cloud e acesso ao Google Sheets

2. **Crie e configure as credenciais**
   - No [Google Cloud Console](https://console.cloud.google.com/):
     - Crie um **Projeto**.
     - Habilite **Google Sheets API** e **Google Drive API**.
     - Crie uma **Service Account** e gere uma **chave JSON**.
   - Crie uma planilha no Google Sheets com o nome de aba **Clientes** (opcional; o app cria se não existir).
   - **Compartilhe** a planilha com o `client_email` da service account **como Editor**.
   - Coloque o JSON da service account em `.streamlit/secrets.toml` (modelo incluso) e defina `SHEET_ID`.

3. **Instale as dependências**
   ```bash
   cd app
   pip install -r ../requirements.txt
   ```

4. **Execute o app**
   ```bash
   streamlit run app.py
   ```

## 🧱 Estrutura
```
app/
  app.py
  pages/
    1_Dashboard.py
    2_Clientes.py
    3_Cadastrar.py
    4_Configuracoes.py
  lib/
    sheets.py
    utils.py
assets/
.streamlit/
  secrets.toml (exemplo)
requirements.txt
```

## 🧩 Colunas padrão
- ID (autonumeração)
- Nome
- Telefone
- Email
- Endereco
- Cidade
- Estado
- CEP
- DataCadastro (preenchida automaticamente)
- Notas

## 🔒 Segurança
- **Não** commit suas credenciais.
- Use `st.secrets` localmente (arquivo `.streamlit/secrets.toml`) e em produção (secrets do provedor).

## ☁️ Deploy (opções)
- **Streamlit Community Cloud**: subir o repositório (GitHub) e colocar os *secrets*.
- **Railway / Render / Fly.io / VM própria**: rodar `streamlit run app.py` e expor a porta.
- **Docker**: crie um `Dockerfile` simples e publique em qualquer host.

## 🛠️ Dica de Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
EXPOSE 8501
CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

Feito para uso pessoal e empresas pequenas.
