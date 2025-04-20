import json
from typing import Dict, Optional
from models.data_models import Portfolio, RiskProfile, InvestmentProposal
from decimal import Decimal

class MemoryLayer:
    def __init__(self):
        self.portfolio: Optional[Portfolio] = None
        self.risk_profile: Optional[RiskProfile] = None
        self.investment_proposal: Optional[InvestmentProposal] = None
        self.reference_portfolios: Dict = self._load_reference_portfolios()

    def _load_reference_portfolios(self) -> Dict:
        """Load reference portfolio allocations from config file"""
        try:
            with open('config/portfolio_config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception("Portfolio configuration file not found")

    def store_portfolio(self, portfolio: Portfolio):
        """Store portfolio information"""
        self.portfolio = portfolio

    def store_risk_profile(self, risk_profile: RiskProfile):
        """Store risk profile information"""
        self.risk_profile = risk_profile

    def store_investment_proposal(self, proposal: InvestmentProposal):
        """Store investment proposal information"""
        self.investment_proposal = proposal

    def get_reference_allocation(self) -> Dict:
        """Get reference allocation for stored risk profile"""
        if not self.risk_profile:
            raise ValueError("Risk profile not set")
        return self.reference_portfolios[self.risk_profile.risk_level]

    def is_data_complete(self) -> bool:
        """Check if all required data is present"""
        return all([self.portfolio, self.risk_profile, self.investment_proposal]) 