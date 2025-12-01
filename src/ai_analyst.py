import google.generativeai as genai
import logging
import json
from config.settings import Settings

logger = logging.getLogger(__name__)

class AIAnalyst:
    def __init__(self):
        self.api_key = Settings.GEMINI_API_KEY
        self.models_to_try = ['gemini-2.5-pro', 'gemini-2.0-flash']
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            logger.warning("GEMINI_API_KEY not set. AI Analysis will be skipped.")

    def _log_available_models(self):
        """Helper to log available models for debugging."""
        try:
            logger.info("Listing available Gemini models for this API key:")
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    logger.info(f" - {m.name}")
        except Exception as e:
            logger.warning(f"Could not list models: {e}")

    def generate_ai_analysis(self, portfolio_df, total_value, indicators):
        if not self.api_key:
            return "Análise de IA indisponível (Chave API não configurada)."

        # Prepare Data for AI
        portfolio_summary = portfolio_df.to_dict(orient='records')
        
        # Create a simplified summary to save tokens and focus attention
        # Create a simplified summary to save tokens and focus attention
        summary_text = f"Valor Total: R$ {total_value:,.2f}\n"
        summary_text += f"Indicadores: Selic {indicators.get('selic_meta')}% | CDI {indicators.get('cdi')}% | PTAX {indicators.get('ptax_venda')}\n"
        summary_text += "Ativos:\n"
        for item in portfolio_summary:
            pl_pct = item.get('profit_loss_pct', 0.0)
            pl_val = item.get('profit_loss_val', 0.0)
            summary_text += f"- {item['ticker']} ({item['category']}): R$ {item['value_brl']:.2f} ({item['allocation']:.1f}%) | L/P: {pl_pct:.2f}% (R$ {pl_val:.2f})\n"

        system_prompt = """
        Você é um consultor Wealth Management de alta performance. Analise a carteira com base nos dados fornecidos:

        Rentabilidade Real: Compare o preço atual com o preço médio (PM). Quais ativos estão carregando a carteira e quais estão drenando?
        
        Rebalanceamento Inteligente: Considerando o aporte de R$ 250,00, não sugira apenas comprar o que está "para trás", mas valide se o ativo não perdeu seus fundamentos (ex: HCTR11 caiu muito, vale a pena aportar ou é uma faca caindo?).
        
        Consistência: Aponte se a concentração em um único ativo (ex: BBAS3) aumentou ou diminuiu em relação à diversificação ideal.
        
        Regras:
        1. Seja direto e executivo.
        2. Use os dados de L/P (Lucro/Prejuízo) fornecidos para embasar sua análise.
        3. Não invente dados.
        """

        full_prompt = f"{system_prompt}\n\nDados da Carteira:\n{summary_text}"

        for model_name in self.models_to_try:
            try:
                logger.info(f"Attempting AI analysis with model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(full_prompt)
                return response.text
            except Exception as e:
                logger.error(f"Error generating analysis with {model_name}: {e}")
                
                # Log available models to help user debug 404s
                self._log_available_models()
                
                if model_name == self.models_to_try[-1]:
                    # If this was the last model, return a friendly error
                    logger.error("All AI models failed.")
                    return "Análise de IA temporariamente indisponível. Verifique os logs para detalhes dos modelos acessíveis."
                else:
                    logger.info("Switching to fallback model...")
                    continue
