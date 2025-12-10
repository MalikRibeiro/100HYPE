import google.generativeai as genai
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIAnalystService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = None

        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Dynamically select a supported model
            try:
                available_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # Priority 1: Flash models (Better for free tier/latency)
                flash_model = next((m for m in available_models if 'flash' in m.name.lower()), None)
                
                # Priority 2: Pro models
                pro_model = next((m for m in available_models if 'pro' in m.name.lower()), None)
                
                # Selection Logic
                selected_model = flash_model or pro_model or (available_models[0] if available_models else None)

                if selected_model:
                    self.model = genai.GenerativeModel(selected_model.name)
                    logger.info(f"Selected AI Model: {selected_model.name}")
            except Exception as e:
                 logger.error(f"Error listing models: {e}")
        else:
            logger.warning("GEMINI_API_KEY not set. AI Analysis will be skipped.")

    def generate_analysis(self, portfolio_data: list, language: str = 'pt') -> str:
        """
        Generates AI analysis for the given portfolio data.
        portfolio_data: List of dictionaries containing asset info. 
        language: 'pt' or 'en'
        """
        if not self.api_key:
            return "AI Analysis unavailable (API Key not set)." if language == 'en' else "Análise de IA indisponível (Chave API não configurada)."

        # Calculate total value and prepare summary
        total_value = sum(item.get('value', 0) for item in portfolio_data)
        
        # Note: In a real scenario, we would fetch these from MarketDataService
        news_summary = "Notícias de mercado indisponíveis no momento." if language == 'pt' else "Market news unavailable at the moment."
        indicators = {"selic_meta": "N/A", "cdi": "N/A", "ptax_venda": "N/A"}

        summary_text = f"Total Value: R$ {total_value:,.2f}\n" if language == 'en' else f"Valor Total: R$ {total_value:,.2f}\n"
        summary_text += f"Indices: Selic {indicators['selic_meta']} | CDI {indicators['cdi']} | PTAX {indicators['ptax_venda']}\n"
        summary_text += "Assets:\n" if language == 'en' else "Ativos:\n"
        
        for item in portfolio_data:
            ticker = item.get('ticker', 'N/A')
            category = item.get('category', 'N/A')
            value = item.get('value', 0.0)
            allocation = (value / total_value * 100) if total_value > 0 else 0
            
            summary_text += f"- {ticker} ({category}): R$ {value:.2f} ({allocation:.1f}%)\n"

        PROMPT_PT = """
        Você é um **Gestor de Portfólio Sênior (CFA)** e Arquiteto de Investimentos. 
        Sua missão é analisar a carteira do cliente com profundidade, usando dados fundamentalistas e o contexto de mercado atual.

        **CONTEXTO DE MERCADO:**
        {news_summary}

        **DIRETRIZES DE ANÁLISE:**
        1.  **Contexto Macro:** Explique brevemente como o cenário atual impacta a carteira.
        2.  **Análise da Carteira:** Avalie a diversificação e riscos.
        3.  **REGRA DE OURO (RENDA FIXA):**
            - Se a categoria 'RENDA_FIXA' estiver alta, considere como reserva de oportunidade.
            - Não sugira venda de Renda Fixa sem necessidade de liquidez.
        4.  **Tom de Voz:** Executivo, direto, sofisticado.

        **DADOS DA CARTEIRA:**
        {summary_text}
        """

        PROMPT_EN = """
        You are a **Senior Portfolio Manager (CFA)** and Investment Architect.
        Your mission is to deeply analyze the client's portfolio using fundamental data and current market context.

        **MARKET CONTEXT:**
        {news_summary}

        **ANALYSIS GUIDELINES:**
        1.  **Macro Context:** Briefly explain how the current scenario impacts the portfolio.
        2.  **Portfolio Analysis:** Evaluate diversification and risks.
        3.  **GOLDEN RULE (FIXED INCOME):**
            - If 'RENDA_FIXA' (Fixed Income) is high, consider it an opportunity reserve.
            - Do not suggest selling Fixed Income unless liquidity is needed.
        4.  **Tone:** Executive, direct, sophisticated.

        **PORTFOLIO DATA:**
        {summary_text}
        """

        selected_prompt = PROMPT_EN if language == 'en' else PROMPT_PT
        full_prompt = selected_prompt.format(news_summary=news_summary, summary_text=summary_text)

        if not self.model:
             return "AI Model not available." if language == 'en' else "Modelo de IA não disponível."

        try:
             response = self.model.generate_content(full_prompt)
             return response.text
        except Exception as e:
             logger.error(f"Error generating analysis: {e}")
             if "429" in str(e):
                 return "AI Quota exceeded. Please wait 1 minute." if language == 'en' else "Cota de IA excedida. Por favor, aguarde 1 minuto e tente novamente."
             return "Unable to generate analysis at the moment." if language == 'en' else "Não foi possível gerar a análise no momento."
