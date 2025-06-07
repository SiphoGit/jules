from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from enum import Enum

class RiskProfile(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class MarketTrend(str, Enum):
    bullish = "bullish"
    bearish = "bearish"
    neutral = "neutral"

class AssetBase(BaseModel):
    name: str
    ticker_symbol: str = Field(..., pattern="^[A-Z]{1,5}$") # Example: AAPL, GOOGL
    asset_type: str # E.g., Stock, Bond, Real Estate
    current_price: float = Field(gt=0)

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: int

    class Config:
        orm_mode = True

class PortfolioAsset(BaseModel): # Asset within a portfolio, including quantity
    asset_id: int
    quantity: float = Field(gt=0)

class PortfolioBase(BaseModel):
    name: str = "Default Portfolio"
    assets: List[PortfolioAsset] = []

class PortfolioCreate(PortfolioBase):
    pass

class Portfolio(PortfolioBase):
    id: int
    client_id: int
    total_value: Optional[float] = 0.0 # Will be calculated

    class Config:
        orm_mode = True

class ClientBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    risk_profile: RiskProfile = RiskProfile.medium

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    portfolios: List[Portfolio] = []

    class Config:
        orm_mode = True

# For AI Recommendations
class RecommendationRequest(BaseModel):
    client_id: int
    market_trend: MarketTrend = MarketTrend.neutral # Default to neutral if not specified

class RecommendedAsset(AssetBase): # Similar to Asset, but for recommendation output
    suitability_score: Optional[float] = Field(None, ge=0, le=1) # 0 to 1
    rationale: Optional[str] = None
