
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração
API_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(page_title="Invest-AI", page_icon="📈", layout="wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load CSS
try:
    local_css("frontend/styles.css")
except FileNotFoundError:
    pass # Should be in frontend folder relative to run command, usually project root if running streamlit run frontend/app.py

# --- Funções de API ---
def login(email, password):
    try:
        response = requests.post(f"{API_URL}/auth/access-token", data={"username": email, "password": password})
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def signup(email, password, full_name):
    """Realiza cadastro de usuário"""
    try:
        payload = {"email": email, "password": password, "full_name": full_name}
        response = requests.post(f"{API_URL}/auth/signup", json=payload)
        
        if response.status_code == 200:
            return True, "Cadastro realizado com sucesso! Faça login."
        else:
            detail = response.json().get('detail', 'Erro desconhecido')
            return False, f"Erro: {detail}"
    except Exception as e:
        return False, f"Erro de conexão: {e}"

def get_portfolio(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{API_URL}/portfolio/portfolio", headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            st.error("Sessão expirada. Faça login novamente.")
            st.session_state.token = None
            st.rerun()
        return []
    except:
        return []

def create_transaction_flow(token, ticker, category, type_, qty, price):
    headers = {"Authorization": f"Bearer {token}"}
    
    asset_id = None
    asset_data = {"ticker": ticker.upper(), "category": category, "name": ticker.upper()}
    resp_asset = requests.post(f"{API_URL}/portfolio/assets", json=asset_data, headers=headers)
    
    if resp_asset.status_code == 200:
        asset_id = resp_asset.json()['id']
    elif resp_asset.status_code == 400:
        st.warning(f"Ativo {ticker} já existe. Tentando continuar...")
        # Fallback assumption (Since we can't search ID easily yet without filter endpoint)
        # However, for this step, user said "Assuma que o usuário vai cadastrar" or "Tente criar"
        return False, "Ativo já existe (backend precisa de ajuste para retornar ID ou buscar). Tente outro ou peça ajuste."
    else:
        return False, f"Erro ao cadastrar ativo: {resp_asset.text}"

    if not asset_id:
        return False, "ID do ativo não encontrado."

    tx_data = {
        "asset_id": asset_id,
        "type": type_,
        "quantity": qty,
        "price": price
    }
    resp_tx = requests.post(f"{API_URL}/portfolio/transactions", json=tx_data, headers=headers)
    
    if resp_tx.status_code == 200:
        return True, "Transação salva com sucesso!"
    else:
        return False, f"Erro na transação: {resp_tx.text}"

def generate_analysis(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.post(f"{API_URL}/analysis/generate", headers=headers)
        if response.status_code == 200:
            return True, response.json().get('content', '')
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

# --- Interface ---

if 'token' not in st.session_state:
    st.session_state.token = None

if not st.session_state.token:
    # TELA DE LOGIN / CADASTRO
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🔐 Invest-AI")
        
        tab_login, tab_signup = st.tabs(["Entrar", "Cadastrar"])
        
        with tab_login:
            with st.container():
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Senha", type="password", key="login_pass")
                if st.button("Entrar", type="primary"):
                    data = login(email, password)
                    if data:
                        st.session_state.token = data['access_token']
                        st.rerun()
                    else:
                        st.error("Credenciais inválidas")
        
        with tab_signup:
            with st.container():
                new_email = st.text_input("Email", key="signup_email")
                new_pass = st.text_input("Senha", type="password", key="signup_pass")
                new_name = st.text_input("Nome Completo", key="signup_name")
                
                if st.button("Criar Conta"):
                    if new_email and new_pass:
                        success, msg = signup(new_email, new_pass, new_name)
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)
                    else:
                        st.warning("Preencha os campos obrigatórios.")
else:
    # ÁREA LOGADA
    with st.sidebar:
        st.title("Invest-AI 2.0")
        st.write("Gestor de Investimentos")
        if st.button("Sair"):
            st.session_state.token = None
            st.rerun()

    tab1, tab2 = st.tabs(["📊 Dashboard", "➕ Nova Transação"])

    with tab1:
        st.header("Visão Geral")
        data = get_portfolio(st.session_state.token)
        
        if not data:
            st.info("Nenhum ativo encontrado. Cadastre na aba ao lado.")
        else:
            df = pd.DataFrame(data)
            df['Valor Atual'] = df['total_quantity'] * df['average_price'] # Simplificado
            
            # --- Cards de Métricas ---
            total = df['Valor Atual'].sum()
            count_assets = len(df)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Patrimônio Total</div>
                    <div class="metric-value">R$ {total:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total de Ativos</div>
                    <div class="metric-value">{count_assets}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # --- Gráficos e Tabelas ---
            col_chart, col_table = st.columns([1, 2])
            
            with col_chart:
                st.subheader("Alocação por Ativo")
                if not df.empty:
                    # Gráfico de Rosca com Plotly
                    fig = px.pie(df, values='Valor Atual', names='ticker', hole=0.4, 
                                 template='plotly_dark', color_discrete_sequence=px.colors.sequential.RdBu)
                    fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
                    st.plotly_chart(fig, use_container_width=True)
            
            with col_table:
                st.subheader("Detalhamento")
                st.dataframe(
                    df[['ticker', 'total_quantity', 'average_price', 'Valor Atual']],
                    column_config={
                        "ticker": "Ativo",
                        "total_quantity": "Qtd",
                        "average_price": st.column_config.NumberColumn("Preço Médio", format="R$ %.2f"),
                        "Valor Atual": st.column_config.NumberColumn("Valor Total", format="R$ %.2f"),
                    },
                    use_container_width=True,
                    hide_index=True
                )
            
            st.divider()
            st.subheader("🤖 Análise de IA")
            if st.button("Gerar Nova Análise"):
                with st.spinner("A IA está analisando seu portfólio... Isso pode levar alguns segundos."):
                    success, result = generate_analysis(st.session_state.token)
                    if success:
                        st.success("Análise gerada e enviada para seu email!")
                        st.markdown(result)
                    else:
                        st.error(f"Erro ao gerar análise: {result}")

    with tab2:
        st.header("Cadastrar Operação")
        st.markdown('<div class="metric-card">Preencha os dados da operação abaixo</div>', unsafe_allow_html=True)
        
        with st.form("nova_operacao"):
            col_a, col_b = st.columns(2)
            with col_a:
                ticker = st.text_input("Ticker (ex: AAPL, PETR4)", help="O código do ativo").upper()
                category = st.selectbox("Categoria", ["Ações BR", "FIIs", "Stocks", "Cripto", "Renda Fixa"])
            with col_b:
                op_type = st.selectbox("Tipo", ["BUY", "SELL"])
                date_op = st.date_input("Data", datetime.now())
            
            col_c, col_d = st.columns(2)
            with col_c:
                qty = st.number_input("Quantidade", min_value=0.01, step=1.0)
            with col_d:
                price = st.number_input("Preço Unitário (R$)", min_value=0.01, step=0.10)
                
            submit = st.form_submit_button("Salvar Transação")
            
            if submit:
                if ticker and qty > 0 and price > 0:
                    cat_map = {"Ações BR": "BR_STOCKS", "FIIs": "FIIS", "Stocks": "US_STOCKS", "Cripto": "CRYPTO"}
                    cat_api = cat_map.get(category, "OUTROS")
                    
                    success, msg = create_transaction_flow(
                        st.session_state.token, ticker, cat_api, op_type, qty, price
                    )
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
                else:
                    st.warning("Preencha todos os campos obrigatórios.")
