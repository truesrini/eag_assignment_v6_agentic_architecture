from pydantic import BaseModel, Field, validator
from typing import Dict, Literal
from decimal import Decimal

class Portfolio(BaseModel):
    equity: Decimal = Field(ge=0)
    fixed_income: Decimal = Field(ge=0)
    real_estate: Decimal = Field(ge=0)
    alternate_investments: Decimal = Field(ge=0)
    cash: Decimal = Field(ge=0)

    @validator('*')
    def validate_amounts(cls, v):
        if v < 0:
            raise ValueError("Investment amounts cannot be negative")
        return v

class RiskProfile(BaseModel):
    risk_level: Literal["High", "Medium", "Low"]

class InvestmentProposal(BaseModel):
    category: Literal["Equity", "Fixed Income", "Real Estate", "Alternate Investments", "Cash"]
    amount: Decimal = Field(ge=0)

    @validator('amount')
    def validate_amount(cls, v):
        if v < 0:
            raise ValueError("Investment amount cannot be negative")
        return v 
