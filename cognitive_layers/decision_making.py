from typing import Dict, Tuple, List
from decimal import Decimal
from models.data_models import Portfolio, InvestmentProposal

class DecisionMakingLayer:
    def __init__(self):
        self.tolerance = 5  # +/- 5% tolerance for portfolio allocation

    def calculate_portfolio_percentages(self, portfolio: Portfolio) -> Dict[str, float]:
        """Calculate current portfolio allocation percentages"""
        total = sum([
            portfolio.equity,
            portfolio.fixed_income,
            portfolio.real_estate,
            portfolio.alternate_investments,
            portfolio.cash
        ])
        
        if total == 0:
            return {
                "Equity": 0,
                "Fixed Income": 0,
                "Real Estate": 0,
                "Alternate Investments": 0,
                "Cash": 0
            }

        return {
            "Equity": float(portfolio.equity * 100 / total),
            "Fixed Income": float(portfolio.fixed_income * 100 / total),
            "Real Estate": float(portfolio.real_estate * 100 / total),
            "Alternate Investments": float(portfolio.alternate_investments * 100 / total),
            "Cash": float(portfolio.cash * 100 / total)
        }

    def analyze_allocation(self, current: Dict[str, float], 
                         reference: Dict[str, float]) -> List[Dict[str, str]]:
        """Analyze portfolio allocation against reference"""
        deviations = []
        for category in current:
            diff = current[category] - reference[category]
            if abs(diff) > self.tolerance:
                status = "over-allocated" if diff > 0 else "under-allocated"
                deviations.append({
                    "category": category,
                    "status": status,
                    "difference": f"{abs(diff):.2f}%"
                })
        return deviations

    def evaluate_proposal(self, portfolio: Portfolio, 
                         proposal: InvestmentProposal,
                         reference: Dict[str, float]) -> Tuple[bool, str]:
        """Evaluate if the investment proposal improves portfolio balance"""
        current_percentages = self.calculate_portfolio_percentages(portfolio)
        
        # Create new portfolio with proposed investment
        new_portfolio = Portfolio(
            equity=portfolio.equity + (proposal.amount if proposal.category == "Equity" else Decimal(0)),
            fixed_income=portfolio.fixed_income + (proposal.amount if proposal.category == "Fixed Income" else Decimal(0)),
            real_estate=portfolio.real_estate + (proposal.amount if proposal.category == "Real Estate" else Decimal(0)),
            alternate_investments=portfolio.alternate_investments + (proposal.amount if proposal.category == "Alternate Investments" else Decimal(0)),
            cash=portfolio.cash + (proposal.amount if proposal.category == "Cash" else Decimal(0))
        )
        
        new_percentages = self.calculate_portfolio_percentages(new_portfolio)
        
        # Calculate if the proposal improves the overall alignment
        current_deviation = sum(abs(current_percentages[k] - reference[k]) for k in reference)
        new_deviation = sum(abs(new_percentages[k] - reference[k]) for k in reference)
        
        improves = new_deviation < current_deviation
        
        return improves, self._generate_recommendation(improves, proposal, current_percentages, new_percentages, reference)

    def _generate_recommendation(self, improves: bool, 
                               proposal: InvestmentProposal,
                               current: Dict[str, float],
                               new: Dict[str, float],
                               reference: Dict[str, float]) -> str:
        """Generate a detailed recommendation message"""
        if improves:
            return (f"The proposed investment of {proposal.amount} in {proposal.category} "
                   f"would improve your portfolio alignment with the target allocation. "
                   f"Current {proposal.category} allocation: {current[proposal.category]:.2f}% "
                   f"New allocation: {new[proposal.category]:.2f}% "
                   f"Target: {reference[proposal.category]}%")
        else:
            return (f"The proposed investment of {proposal.amount} in {proposal.category} "
                   f"would move your portfolio further from the target allocation. "
                   f"Consider investing in other categories that are under-allocated.") 