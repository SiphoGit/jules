from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, database, ai_engine # ai_engine will be used later

# Create database tables
database.create_db_and_tables()

app = FastAPI(
    title="AI Asset Management API",
    description="API for managing financial advisor assets and providing AI-powered recommendations.",
    version="0.1.0"
)

# Dependency to get DB session
def get_db_session():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Endpoints

# Clients
@app.post("/clients/", response_model=models.Client, status_code=201, tags=["Clients"])
def create_new_client(client: models.ClientCreate, db: Session = Depends(get_db_session)):
    db_client = crud.get_client_by_email(db, email=client.email)
    if db_client:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_client(db=db, client=client)

@app.get("/clients/", response_model=List[models.Client], tags=["Clients"])
def read_all_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    clients = crud.get_clients(db, skip=skip, limit=limit)
    return clients

@app.get("/clients/{client_id}", response_model=models.Client, tags=["Clients"])
def read_single_client(client_id: int, db: Session = Depends(get_db_session)):
    db_client = crud.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    # Manually construct portfolio responses to include details
    portfolios_with_details = []
    for p_db in db_client.portfolios:
        p_details_dict = crud.get_portfolio_details(db, p_db.id) # This returns a dict
        if p_details_dict:
             # We need a Pydantic model that matches structure of p_details_dict for response_model
             # For now, let's create a temporary structure or adjust models.Portfolio
             # This highlights a need to refine Portfolio response model
            assets_in_p = [models.PortfolioAsset(asset_id=ad['asset'].id, quantity=ad['quantity']) for ad in p_details_dict.get('assets_details', [])]

            portfolios_with_details.append(models.Portfolio(
                id=p_details_dict['portfolio_id'],
                name=p_details_dict['name'],
                client_id=p_details_dict['client_id'],
                assets=assets_in_p, # This now matches List[PortfolioAsset]
                total_value=p_details_dict['total_value']
            ))
    client_data = models.Client.from_orm(db_client)
    client_data.portfolios = portfolios_with_details
    return client_data


@app.put("/clients/{client_id}", response_model=models.Client, tags=["Clients"])
def update_existing_client(client_id: int, client: models.ClientCreate, db: Session = Depends(get_db_session)):
    db_client = crud.update_client(db, client_id=client_id, client_update=client)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@app.delete("/clients/{client_id}", response_model=models.Client, tags=["Clients"])
def delete_existing_client(client_id: int, db: Session = Depends(get_db_session)):
    db_client = crud.delete_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

# Assets
@app.post("/assets/", response_model=models.Asset, status_code=201, tags=["Assets"])
def create_new_asset(asset: models.AssetCreate, db: Session = Depends(get_db_session)):
    db_asset = crud.get_asset_by_ticker(db, ticker_symbol=asset.ticker_symbol)
    if db_asset:
        raise HTTPException(status_code=400, detail="Asset ticker symbol already exists")
    return crud.create_asset(db=db, asset=asset)

@app.get("/assets/", response_model=List[models.Asset], tags=["Assets"])
def read_all_assets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    assets = crud.get_assets(db, skip=skip, limit=limit)
    return assets

@app.get("/assets/{asset_id}", response_model=models.Asset, tags=["Assets"])
def read_single_asset(asset_id: int, db: Session = Depends(get_db_session)):
    db_asset = crud.get_asset(db, asset_id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return db_asset

# Portfolio class for response model that includes details
class PortfolioDetailsResponse(models.PortfolioBase):
    id: int
    client_id: int
    assets_details: List[models.RecommendedAsset] # Re-using RecommendedAsset for structure
    total_value: float

# Portfolios
# This endpoint creates a new portfolio for a client or updates an existing one (if logic is adapted)
# For simplicity, let's assume one main portfolio is created/updated.
# If a client can have multiple portfolios, this might be POST /clients/{client_id}/portfolios/
# and PUT /portfolios/{portfolio_id}
@app.post("/clients/{client_id}/portfolio", response_model=models.Portfolio, tags=["Portfolios"])
def create_or_update_client_portfolio(client_id: int, portfolio: models.PortfolioCreate, db: Session = Depends(get_db_session)):
    db_client = crud.get_client(db, client_id=client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Check if client already has portfolios. If so, update the first one found? Or allow multiple?
    # Current plan implies one portfolio endpoint. Let's assume we update the first one or create new.
    existing_portfolios = crud.get_portfolios_by_client(db, client_id=client_id, limit=1)
    if existing_portfolios:
        # Update existing portfolio's assets
        updated_portfolio = crud.update_portfolio_assets(db, portfolio_id=existing_portfolios[0].id, portfolio_update=portfolio)
        if not updated_portfolio:
             raise HTTPException(status_code=500, detail="Could not update portfolio") # Should not happen if portfolio exists
        # We need to shape this response to models.Portfolio
        # crud.update_portfolio_assets returns DbPortfolio, so from_orm should work if fields match
        # Let's re-fetch details for consistent response structure
        p_details_dict = crud.get_portfolio_details(db, updated_portfolio.id)
        assets_in_p = [models.PortfolioAsset(asset_id=ad['asset'].id, quantity=ad['quantity']) for ad in p_details_dict.get('assets_details', [])]
        return models.Portfolio(
            id=p_details_dict['portfolio_id'],
            name=p_details_dict['name'],
            client_id=p_details_dict['client_id'],
            assets=assets_in_p,
            total_value=p_details_dict['total_value']
        )

    else:
        # Create new portfolio
        new_portfolio = crud.create_client_portfolio(db=db, portfolio=portfolio, client_id=client_id)
        # crud.create_client_portfolio returns DbPortfolio. We need to shape this.
        p_details_dict = crud.get_portfolio_details(db, new_portfolio.id) # Re-fetch to get details
        assets_in_p = [models.PortfolioAsset(asset_id=ad['asset'].id, quantity=ad['quantity']) for ad in p_details_dict.get('assets_details', [])]
        return models.Portfolio(
            id=p_details_dict['portfolio_id'],
            name=p_details_dict['name'],
            client_id=p_details_dict['client_id'],
            assets=assets_in_p,
            total_value=p_details_dict['total_value']
        )

@app.get("/clients/{client_id}/portfolio", response_model=PortfolioDetailsResponse, tags=["Portfolios"])
def get_client_portfolio_details(client_id: int, db: Session = Depends(get_db_session)):
    db_client = crud.get_client(db, client_id=client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Assuming client has one main portfolio for this endpoint, or we fetch the first one.
    portfolios = crud.get_portfolios_by_client(db, client_id=client_id, limit=1)
    if not portfolios:
        raise HTTPException(status_code=404, detail="Portfolio not found for this client")

    portfolio_details_dict = crud.get_portfolio_details(db, portfolio_id=portfolios[0].id)
    if not portfolio_details_dict:
        raise HTTPException(status_code=404, detail="Portfolio details not found")

    # Adapt portfolio_details_dict to PortfolioDetailsResponse
    # RecommendedAsset has: name, ticker_symbol, asset_type, current_price, suitability_score, rationale
    # crud.get_portfolio_details returns 'assets_details': [{'asset': models.Asset, 'quantity': ..., 'value': ...}]

    assets_resp_details = []
    for ad in portfolio_details_dict.get('assets_details', []):
        asset_obj = ad['asset'] # This is models.Asset
        assets_resp_details.append(models.RecommendedAsset(
            name=asset_obj.name,
            ticker_symbol=asset_obj.ticker_symbol,
            asset_type=asset_obj.asset_type,
            current_price=asset_obj.current_price
            # quantity and value are specific to portfolio, not part of RecommendedAsset model directly
            # This means PortfolioDetailsResponse may need adjustment or we accept this structure.
            # For now, it will only populate common fields.
        ))

    return PortfolioDetailsResponse(
        id=portfolio_details_dict['portfolio_id'],
        name=portfolio_details_dict['name'],
        client_id=portfolio_details_dict['client_id'],
        assets_details=assets_resp_details, # List of RecommendedAsset
        total_value=portfolio_details_dict['total_value']
    )

# AI Recommendations Endpoint
@app.post("/clients/{client_id}/recommendations", response_model=List[models.RecommendedAsset], tags=["AI Engine"])
def get_ai_recommendations_for_client(
    client_id: int,
    request_body: models.RecommendationRequest, # Contains market_trend (client_id from path is already used by RecommendationRequest model)
    db: Session = Depends(get_db_session)
):
    # client_id from path is authoritative. request_body.client_id is ignored if present.
    db_client = crud.get_client(db, client_id=client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    # The RecommendationRequest model has client_id, but we use the path client_id.
    # We also need to ensure the market_trend from the body is used.

    # Option 1: Use all_db_assets (requires them to be created first)
    # all_db_assets_orm = crud.get_assets(db, limit=1000) # Fetch all assets
    # all_db_assets_pydantic = [models.Asset.from_orm(asset) for asset in all_db_assets_orm]
    # recommendations = ai_engine.get_asset_recommendations(
    #     risk_profile=db_client.risk_profile, # Taken from the fetched client
    #     market_trends=request_body.market_trend, # Taken from the request body
    #     all_available_assets=all_db_assets_pydantic
    # )

    # Option 2: Using the mock pool within ai_engine for simplicity as per current ai_engine.py design
    # This is simpler for now as we haven't necessarily populated the DB with many assets.
    recommendations = ai_engine.get_asset_recommendations(
        risk_profile=db_client.risk_profile, # Taken from the fetched client
        market_trends=request_body.market_trend # Taken from the request body
        # all_available_assets parameter is omitted to allow ai_engine to use its MOCK_ASSETS_POOL
    )

    if not recommendations:
        # Return an empty list if no recommendations, or could be a 404.
        # Frontend should handle an empty list gracefully.
        return []

    return recommendations

# Placeholder for Uvicorn runner if main.py is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
