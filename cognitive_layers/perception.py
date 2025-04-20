from typing import Dict, Optional
from decimal import Decimal
from models.data_models import Portfolio, RiskProfile, InvestmentProposal
from utils.llm_config import get_llm_model, generate_response

class PerceptionLayer:
    def __init__(self):
        self.model = get_llm_model()
        self.input_prompts = {
            "portfolio": """
            You are an investment advisor assistant. Ask the user for their current investment amounts in the following categories:
            - Equity
            - Fixed Income
            - Real Estate
            - Alternate Investments
            - Cash
            
            Format your response as a clear question. After receiving the response, validate that all values are non-negative numbers.
            If any value is invalid, explain the issue and ask for the specific value again.
            """,
            "risk_profile": """
            You are an investment advisor assistant. Ask the user about their risk appetite.
            They must choose one of these options: High, Medium, or Low.
            
            Explain what each risk level means:
            - High: Aggressive growth strategy with higher volatility
            - Medium: Balanced approach with moderate risk and returns
            - Low: Conservative approach focusing on capital preservation
            
            Format your response as a clear question with the options and explanations.
            Validate that the response matches one of the allowed values exactly.
            """,
            "investment_proposal": """
            You are an investment advisor assistant. Ask the user about their proposed investment with these two questions:
            1. Which category they want to invest in (must be one of: Equity, Fixed Income, Real Estate, Alternate Investments, or Cash)
            2. How much they want to invest (must be a positive number)
            
            Format your response as clear questions.
            Validate that:
            - The category matches one of the allowed options exactly
            - The amount is a positive number
            
            If any input is invalid, explain why and ask for the specific input again.
            """
        }

    def _validate_number(self, value: str) -> Optional[Decimal]:
        """Validate and convert string to Decimal"""
        try:
            amount = Decimal(value.strip())
            if amount < 0:
                return None
            return amount
        except:
            return None

    async def gather_portfolio_info(self) -> Optional[Portfolio]:
        """Gather and validate portfolio information using LLM"""
        try:
            # Initial prompt to user
            response = generate_response(self.model, self.input_prompts["portfolio"])
            print("\nInvestment Advisor:", response)
            
            # Get user input for each category
            categories = ["equity", "fixed_income", "real_estate", "alternate_investments", "cash"]
            values = {}
            
            for category in categories:
                while True:
                    value = input(f"\nEnter amount for {category.replace('_', ' ').title()}: ")
                    amount = self._validate_number(value)
                    
                    if amount is not None:
                        values[category] = amount
                        break
                    else:
                        print(f"Invalid amount. Please enter a non-negative number for {category}.")
            
            return Portfolio(**values)
        except Exception as e:
            print(f"Error gathering portfolio information: {e}")
            return None

    async def gather_risk_profile(self) -> Optional[RiskProfile]:
        """Gather and validate risk profile information using LLM"""
        try:
            # Initial prompt to user
            response = generate_response(self.model, self.input_prompts["risk_profile"])
            print("\nInvestment Advisor:", response)
            
            while True:
                risk_level = input("\nYour risk appetite (High/Medium/Low): ").strip()
                if risk_level in ["High", "Medium", "Low"]:
                    return RiskProfile(risk_level=risk_level)
                else:
                    print("Invalid risk level. Please choose High, Medium, or Low.")
        except Exception as e:
            print(f"Error gathering risk profile: {e}")
            return None

    async def gather_investment_proposal(self) -> Optional[InvestmentProposal]:
        """Gather and validate investment proposal information using LLM"""
        try:
            # Initial prompt to user
            response = generate_response(self.model, self.input_prompts["investment_proposal"])
            print("\nInvestment Advisor:", response)
            
            valid_categories = ["Equity", "Fixed Income", "Real Estate", "Alternate Investments", "Cash"]
            
            while True:
                category = input("\nInvestment category: ").strip()
                if category not in valid_categories:
                    print(f"Invalid category. Please choose from: {', '.join(valid_categories)}")
                    continue
                
                amount_str = input("Investment amount: ")
                amount = self._validate_number(amount_str)
                if amount is None:
                    print("Invalid amount. Please enter a positive number.")
                    continue
                
                return InvestmentProposal(category=category, amount=amount)
        except Exception as e:
            print(f"Error gathering investment proposal: {e}")
            return None 