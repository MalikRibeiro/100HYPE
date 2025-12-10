# 🚀 Invest-AI 2.0

> **Seu Gestor de Portfólio Inteligente com IA Generativa**

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green.svg)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)
![Database](https://img.shields.io/badge/Database-PostgreSQL%20(Supabase)-336791.svg)
![AI](https://img.shields.io/badge/AI-Gemini%20Pro-orange.svg)

O **Invest-AI 2.0** é uma plataforma SaaS (Software as a Service) projetada para democratizar a gestão de investimentos. Diferente de planilhas estáticas, o Invest-AI utiliza Inteligência Artificial para analisar sua carteira, entender o contexto macroeconômico e fornecer recomendações personalizadas de rebalanceamento e aporte.

---

## 🏗️ Arquitetura do Sistema

O projeto evoluiu de um script local para uma arquitetura moderna **Cliente-Servidor**:

1.  **Backend (API Restful):**
    * Construído com **FastAPI**.
    * Gerencia usuários, autenticação (JWT) e segurança (Argon2).
    * Conecta com **PostgreSQL (Supabase)** para persistência de dados.
    * Integração com **Google Gemini** para geração de análises financeiras.
    * Sistema de disparo de e-mails automáticos (`EmailService`).

2.  **Frontend (Web Dashboard):**
    * Construído com **Streamlit** para rápida visualização de dados.
    * Consome a API para login, cadastro de ativos e visualização de gráficos interativos (**Plotly**).

---

## ✨ Funcionalidades Atuais

* 🔐 **Autenticação Segura:** Cadastro e Login de usuários com criptografia.
* 📊 **Dashboard Interativo:** Visualização clara do patrimônio, alocação e quantidade de ativos.
* ➕ **Gestão de Carteira:** Cadastro manual de ativos (Ações, FIIs, Stocks, Cripto).
* 🤖 **Analista IA:** Geração de relatórios fundamentalistas e macroeconômicos da sua carteira com um clique.
* 📧 **Notificações:** Envio automático da análise da IA diretamente para o e-mail do usuário.

---

## 🔮 Visão de Futuro (Roadmap)

Estamos trabalhando para transformar o Invest-AI em um ecossistema completo:

* [ ] **App Mobile Nativo (Android/Kotlin):** Um aplicativo dedicado para gestão na palma da mão.
* [ ] **Integração B3/Yahoo Finance:** Atualização automática de preços em tempo real (Workers em background).
* [ ] **Múltiplas Carteiras:** Suporte para diferentes objetivos (Aposentadoria, Viagem, etc).
* [ ] **Modo "Copiloto":** Chat interativo com a IA para tirar dúvidas sobre investimentos específicos.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.12+
* Conta no Supabase (Banco de Dados)
* Chave de API do Google Gemini
* Senha de App do Gmail (para envio de e-mails)

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU_USUARIO/Invest-AI.git](https://github.com/SEU_USUARIO/Invest-AI.git)
    cd Invest-AI
    ```

2.  **Configure o Ambiente:**
    Crie um arquivo `.env` na pasta `invest-ai-backend` com as credenciais:
    ```env
    DATABASE_URL=postgresql://user:pass@host:port/db
    GEMINI_API_KEY=sua_chave_gemini
    EMAIL_SENDER=seu_email@gmail.com
    EMAIL_PASSWORD=sua_senha_de_app
    ```

3.  **Instale as Dependências:**
    ```bash
    cd invest-ai-backend
    pip install -r requirements.txt
    ```

### Execução Automática (Windows)

Basta dar dois cliques no arquivo **`run_app.bat`** na raiz do projeto.
Ele iniciará automaticamente a API e abrirá o Dashboard no seu navegador.

### Execução Manual

**Terminal 1 (Backend):**
```bash
cd invest-ai-backend
uvicorn app.main:app --reload
```

Terminal 2 (Frontend):

```bash

streamlit run frontend/app.py
```
### Execução Automatica (Windows)

```bash
.\run_app.bat
```

### Execução Docker
```bash
docker-compose up --build
```