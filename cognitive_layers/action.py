from typing import Dict, List
from models.data_models import Portfolio, RiskProfile, InvestmentProposal
from utils.llm_config import get_llm_model, generate_response

class ActionLayer:
    def __init__(self):
        self.model = get_llm_model()
        self.response_templates = {
            "portfolio_analysis": """
            You are an investment advisor assistant. Analyze the following portfolio information and provide recommendations:

            Current Portfolio Deviations:
            {deviations}

            Investment Recommendation:
            {recommendation}

            Please provide a clear, professional analysis that:
            1. Summarizes the current portfolio status
            2. Explains any significant deviations from the target allocation
            3. Provides specific recommendations for the proposed investment
            4. Suggests next steps for the investor

            Use a friendly but professional tone and format the response clearly.
            """,
            "error": """
            You are an investment advisor assistant. An error has occurred:
            {message}

            Please explain the error to the user in a clear, professional manner and provide guidance on how to proceed.
            Include specific steps they should take to resolve the issue.
            """
        }

    def format_portfolio_analysis(self, deviations: List[Dict[str, str]], 
                                recommendation: str) -> str:
        """Format the portfolio analysis results using LLM"""
        deviation_text = "\n".join([
            f"- {d['category']} is {d['status']} by {d['difference']}"
            for d in deviations
        ]) if deviations else "Portfolio is well-balanced within tolerance levels."

        prompt = self.response_templates["portfolio_analysis"].format(
            deviations=deviation_text,
            recommendation=recommendation
        )
        
        return generate_response(self.model, prompt)

    def format_error(self, message: str) -> str:
        """Format error messages using LLM"""
        prompt = self.response_templates["error"].format(message=message)
        return generate_response(self.model, prompt) 
