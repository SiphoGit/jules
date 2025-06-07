from typing import List, Optional
from .models import RiskProfile, MarketTrend, RecommendedAsset, Asset # Asset is needed for fetching all assets

# This is a very basic placeholder for the AI engine.
# In a real application, this would involve more complex logic, data analysis,
# and potentially machine learning models.

# Mock database of available assets for recommendation purposes
# In a real scenario, this would come from the database (crud.get_assets)
MOCK_ASSETS_POOL = [
    models.Asset(id=101, name="SafeCorp Bonds", ticker_symbol="SCB", asset_type="Bond", current_price=100.0),
    models.Asset(id=102, name="SteadyGrowth Equity", ticker_symbol="SGE", asset_type="Stock", current_price=150.0),
    models.Asset(id=103, name="HighYield REIT", ticker_symbol="HYR", asset_type="REIT", current_price=75.0),
    models.Asset(id=104, name="Tech Innovators Fund", ticker_symbol="TIF", asset_type="ETF", current_price=200.0),
    models.Asset(id=105, name="Emerging Markets Debt", ticker_symbol="EMD", asset_type="Bond", current_price=90.0),
    models.Asset(id=106, name="Blue Chip Dividend Stock", ticker_symbol="BCDS", asset_type="Stock", current_price=120.0),
]

def get_asset_recommendations(
    risk_profile: RiskProfile,
    market_trends: MarketTrend,
    # db: Session, # In a real version, you'd pass the DB session to fetch assets
    all_available_assets: Optional[List[Asset]] = None # Pass available assets
) -> List[RecommendedAsset]:

    recommendations: List[RecommendedAsset] = []

    # If no specific assets are passed, use the mock pool
    # In a real app, you'd query from db using crud.get_assets(db, limit=some_large_number)
    assets_to_consider = all_available_assets if all_available_assets else MOCK_ASSETS_POOL

    for asset in assets_to_consider:
        suitability_score = 0.5  # Default score
        rationale = "General recommendation."

        # Rule-based logic based on risk profile
        if risk_profile == RiskProfile.low:
            if asset.asset_type == "Bond":
                suitability_score = 0.8
                rationale = "Bonds are generally lower risk."
            elif asset.asset_type == "Stock" and asset.name == "Blue Chip Dividend Stock":
                suitability_score = 0.65
                rationale = "Blue chip stocks can be part of a low-risk portfolio."
            elif asset.asset_type == "Stock":
                suitability_score = 0.3
                rationale = "Stocks are generally higher risk."

        elif risk_profile == RiskProfile.medium:
            if asset.asset_type == "ETF" or asset.asset_type == "Stock":
                suitability_score = 0.7
                rationale = "ETFs and diversified stocks fit a medium risk profile."
            elif asset.asset_type == "REIT":
                suitability_score = 0.6
                rationale = "Real estate can offer diversification."
            elif asset.asset_type == "Bond" and asset.name == "Emerging Markets Debt":
                suitability_score = 0.55
                rationale = "Emerging market debt offers higher yield with moderate risk."


        elif risk_profile == RiskProfile.high:
            if asset.asset_type == "Stock" or asset.asset_type == "ETF":
                suitability_score = 0.8
                rationale = "Equities form the core of a high-risk portfolio."
            if asset.ticker_symbol == "TIF": # Tech Innovators Fund
                 suitability_score = 0.85
                 rationale = "Tech funds can offer high growth, suitable for high risk tolerance."
            elif asset.asset_type == "REIT":
                suitability_score = 0.7
                rationale = "REITs can provide good returns."

        # Rule-based logic based on market trends (very simplified)
        if market_trends == MarketTrend.bullish:
            if asset.asset_type == "Stock" or asset.asset_type == "ETF":
                suitability_score = min(1.0, suitability_score + 0.1) # Increase score in bullish market
                rationale += " Positive outlook in bullish market."
        elif market_trends == MarketTrend.bearish:
            if asset.asset_type == "Bond":
                suitability_score = min(1.0, suitability_score + 0.1) # Bonds might be favored
                rationale += " Potential safe haven in bearish market."
            elif asset.asset_type == "Stock":
                 suitability_score = max(0.0, suitability_score - 0.1)
                 rationale += " Caution for stocks in bearish market."

        # Only recommend if score is above a certain threshold
        if suitability_score > 0.5:
            recommendations.append(
                models.RecommendedAsset(
                    name=asset.name,
                    ticker_symbol=asset.ticker_symbol,
                    asset_type=asset.asset_type,
                    current_price=asset.current_price,
                    suitability_score=round(suitability_score, 2),
                    rationale=rationale
                )
            )

    # Sort by suitability score descending
    recommendations.sort(key=lambda x: x.suitability_score, reverse=True)
    return recommendations[:5] # Return top 5 recommendations
