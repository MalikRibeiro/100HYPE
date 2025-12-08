import google.generativeai as genai
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIAnalystService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.models_to_try = ['gemini-2.5-pro', 'gemini-2.0-flash', 'gemini-pro']
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            logger.warning("GEMINI_API_KEY not set. AI Analysis will be skipped.")

    def generate_analysis(self, portfolio_data: list) -> str:
        """
        Generates AI analysis for the given portfolio data.
        portfolio_data: List of dictionaries containing asset info. 
        Example item: {'ticker': 'AAPL', 'category': 'US_STOCKS', 'value': 1000.0, ...}
        """
        if not self.api_key:
            return "Análise de IA indisponível (Chave API não configurada)."

        # Calculate total value and prepare summary
        total_value = sum(item.get('value', 0) for item in portfolio_data)
        
        # Note: In a real scenario, we would fetch these from MarketDataService
        news_summary = "Notícias de mercado indisponíveis no momento."
        indicators = {"selic_meta": "N/A", "cdi": "N/A", "ptax_venda": "N/A"}

        summary_text = f"Valor Total: R$ {total_value:,.2f}\n"
        summary_text += f"Indicadores: Selic {indicators['selic_meta']} | CDI {indicators['cdi']} | PTAX {indicators['ptax_venda']}\n"
        summary_text += "Ativos:\n"
        
        for item in portfolio_data:
            ticker = item.get('ticker', 'N/A')
            category = item.get('category', 'N/A')
            value = item.get('value', 0.0)
            allocation = (value / total_value * 100) if total_value > 0 else 0
            
            # Additional fields if available (PL, ROE etc might not be in the passed list yet, logic depends on endpoint)
            # Assuming basic data for now
            summary_text += f"- {ticker} ({category}): R$ {value:.2f} ({allocation:.1f}%)\n"

        system_prompt = """
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

        full_prompt = system_prompt.format(news_summary=news_summary, summary_text=summary_text)

        for model_name in self.models_to_try:
            try:
                logger.info(f"Attempting AI analysis with model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(full_prompt)
                return response.text
            except Exception as e:
                logger.error(f"Error generating analysis with {model_name}: {e}")
                if model_name == self.models_to_try[-1]:
                    return "Não foi possível gerar a análise no momento."
                continue
