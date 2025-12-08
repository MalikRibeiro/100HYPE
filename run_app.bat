@echo off
TITLE Invest-AI Launcher
color 0A

echo ========================================================
echo        INITIALIZING INVEST-AI 2.0 ECOSYSTEM
echo ========================================================
echo.

:: 1. Iniciar o Backend (API)
echo [1/2] Iniciando o Backend (FastAPI)...
echo --------------------------------------------------------
start "Invest-AI Backend API" cmd /k "cd invest-ai-backend && uvicorn app.main:app --reload"

:: Pequena pausa para garantir que a API suba antes do frontend tentar conectar
timeout /t 5 /nobreak >nul

:: 2. Iniciar o Frontend (Streamlit)
echo [2/2] Iniciando o Frontend (Streamlit)...
echo --------------------------------------------------------
start "Invest-AI Web Dashboard" cmd /k "streamlit run frontend/app.py"

echo.
echo [SUCESSO] Sistema inicializado!
echo - API Docs: http://127.0.0.1:8000/docs
echo - Dashboard: http://localhost:8501
echo.
echo Pressione qualquer tecla para encerrar este launcher (os servicos continuarao rodando)...
pause >nul