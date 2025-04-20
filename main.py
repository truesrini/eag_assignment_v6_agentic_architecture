import asyncio
from dotenv import load_dotenv
from cognitive_layers.perception import PerceptionLayer
from cognitive_layers.memory import MemoryLayer
from cognitive_layers.decision_making import DecisionMakingLayer
from cognitive_layers.action import ActionLayer

# Load environment variables
load_dotenv()

class InvestmentReviewAgent:
    def __init__(self):
        self.perception = PerceptionLayer()
        self.memory = MemoryLayer()
        self.decision = DecisionMakingLayer()
        self.action = ActionLayer()

    async def run(self):
        """Main agent loop"""
        try:
            print("\n=== Investment Portfolio Review Agent ===\n")
            
            # Perception Phase: Gather all required information
            print("Step 1: Current Portfolio Information")
            portfolio = await self.perception.gather_portfolio_info()
            if not portfolio:
                return self.action.format_error("Failed to gather portfolio information")

            print("\nStep 2: Risk Profile Assessment")
            risk_profile = await self.perception.gather_risk_profile()
            if not risk_profile:
                return self.action.format_error("Failed to gather risk profile")

            print("\nStep 3: Investment Proposal")
            investment_proposal = await self.perception.gather_investment_proposal()
            if not investment_proposal:
                return self.action.format_error("Failed to gather investment proposal")

            # Memory Phase: Store and retrieve information
            self.memory.store_portfolio(portfolio)
            self.memory.store_risk_profile(risk_profile)
            self.memory.store_investment_proposal(investment_proposal)
            reference_allocation = self.memory.get_reference_allocation()

            # Decision Phase: Analyze and evaluate
            current_percentages = self.decision.calculate_portfolio_percentages(portfolio)
            deviations = self.decision.analyze_allocation(
                current_percentages, 
                reference_allocation
            )
            improves, recommendation = self.decision.evaluate_proposal(
                portfolio,
                investment_proposal,
                reference_allocation
            )

            # Action Phase: Format and return results
            print("\n=== Analysis Results ===\n")
            return self.action.format_portfolio_analysis(deviations, recommendation)

        except Exception as e:
            return self.action.format_error(str(e))

async def main():
    agent = InvestmentReviewAgent()
    result = await agent.run()
    print(result)

if __name__ == "__main__":
    asyncio.run(main()) 