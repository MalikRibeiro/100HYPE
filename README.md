````markdown
# 🤖 Invest-AI 2.0  
### Seu Gestor de Portfólio Inteligente na Nuvem

O **Invest-AI 2.0** é um sistema autônomo de análise e gestão de portfólio que combina **automação financeira**, **dados em tempo real** e **Inteligência Artificial (Google Gemini)** para produzir **relatórios diários ricos**, contextualizados e acionáveis.

Tudo roda **100% na nuvem via GitHub Actions**, lendo sua carteira diretamente de uma **Google Sheet** — sem configurações manuais, sem editar arquivos locais.

---

## 🚀 Principais Recursos

### 📊 Gestão via Google Sheets  
Altere sua carteira editando uma planilha simples. O robô lê tudo automaticamente a cada execução.

### 🧠 IA Analyst (Gemini Pro)  
Uma IA configurada como **gestor CFA** analisa sua carteira diariamente, avalia fundamentos, contextualiza quedas, identifica riscos e dá diagnósticos que evitam decisões impulsivas.

### 🗞️ Contexto de Mercado  
Coleta automática das principais notícias do dia (Ibovespa, dólar, política, macro) para enriquecer a análise.

### 📈 Dados em Tempo Real  
- Cotações e indicadores via **Yahoo Finance**  
- Selic, CDI e PTAX via **Banco Central**

### 💰 Sugestão de Aporte  
Algoritmo que define **exatamente onde aportar** (ex: R$ 250,00) para manter o portfólio alinhado às metas de alocação.

### 📧 Relatório Diário  
Enviado por e-mail em HTML contendo:  
- Patrimônio, variação e resumo do dia  
- Gráfico de alocação  
- Análise completa da IA  
- Tabela de rebalanceamento para aportes

### ☁️ Automação Total  
Executa sozinho nos dias úteis às **13:00 (BRT)** via GitHub Actions, salvando histórico automaticamente.

---

## 🛠️ Estrutura da Planilha (Google Sheets)

Crie uma planilha com a seguinte estrutura **na primeira aba**:

| Ticker      | Quantidade | Categoria    | Meta |
|-------------|------------|--------------|------|
| BBAS3.SA    | 100        | BR_STOCKS    | 10% |
| HCTR11.SA   | 50         | FIIS         | 5%  |
| IVVB11.SA   | 20         | ETFS         | 15% |
| AAPL        | 5          | US_STOCKS    | 5%  |
| O           | 10         | US_REITS     | 5%  |
| USDT-USD    | 50.5       | CRYPTO       | 2%  |
| RDB-NUBANK  | 2150.55    | RENDA_FIXA   | 35% |

### ⚠️ Regras importantes

- **Categorias permitidas:**  
  `BR_STOCKS`, `FIIS`, `ETFS`, `US_STOCKS`, `US_REITS`, `CRYPTO`, `RENDA_FIXA`
- **Renda Fixa:** usar `RDB-NUBANK`; quantidade = valor financeiro total.  
- **Cripto:** use tickers em USD (ex: `BTC-USD`, `ETH-USD`).
- **Publicação da planilha:**  
  - Arquivo → Compartilhar → **Publicar na Web**  
  - Escolha formato **CSV**  
  - Cole o link no arquivo: `config/settings.py` → variável `SHEET_CSV_URL`

---

## ⚙️ Instalação Local

### Pré-requisitos
- Python 3.12+
- Conta Google (Sheets + API Gemini)
- Gmail com **senha de app** (para envio de relatórios)

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/Invest-AI.git
cd Invest-AI
pip install -r requirements.txt
````

### 2. Criar o `.env`

```
EMAIL_SENDER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_app_google
EMAIL_RECEIVER=email_destino@gmail.com
GEMINI_API_KEY=sua_chave_api_google_ai_studio
LOG_LEVEL=INFO
```

### 3. Executar localmente

```bash
python main.py
```

O sistema irá baixar a planilha, coletar dados, analisar com IA e enviar o relatório completo.

---

## 🤖 Automação via GitHub Actions

O projeto já inclui um workflow configurado.

1. Faça **Fork** ou envie este projeto ao seu GitHub.
2. Vá em: **Settings → Secrets and variables → Actions**
3. Adicione estes secrets:

* `EMAIL_SENDER`
* `EMAIL_PASSWORD`
* `EMAIL_RECEIVER`
* `GEMINI_API_KEY`

O workflow `daily_report.yml` roda:
🕒 **Seg–Sex às 16:00 UTC (13:00 no Brasil)**

O histórico é salvo automaticamente em:

```
data/history.json
```

---

## 📂 Estrutura do Projeto

```
.
├── main.py                      # Ponto de entrada do sistema
├── config/
│   └── settings.py              # Configurações gerais + URL da planilha
├── src/
│   ├── sheets_manager.py        # Leitura e tratamento do Google Sheets
│   ├── data_collector.py        # Yahoo Finance + BCB
│   ├── ai_analyst.py            # Prompts e chamadas ao Gemini
│   ├── news_collector.py        # Notícias financeiras do dia
│   ├── portfolio.py             # Cálculos e rebalanceamento
│   ├── report_generator.py      # HTML, Markdown e gráficos
│   └── notifier.py              # Envio dos e-mails
├── data/
│   └── history.json             # Histórico de patrimônio
└── .github/
    └── workflows/
        └── daily_report.yml     # Execução na nuvem
```

---

## 🛡️ Segurança e Privacidade

* **Nunca** inclua o `.env` no GitHub.
* A planilha publicada como CSV é acessível apenas por quem possui o link.
* Evite inserir informações sensíveis — apenas tickers e quantidades.

---

## 🧩 Desenvolvido com

**Python**, automação, análise fundamentalista e uma pitada generosa de 🤖 IA.

---

```
```
