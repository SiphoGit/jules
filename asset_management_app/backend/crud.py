from sqlalchemy.orm import Session
from . import models, database # database.py contains DbClient, DbAsset, DbPortfolio, PortfolioAssetAssociation

# Client CRUD Operations
def get_client(db: Session, client_id: int):
    return db.query(database.DbClient).filter(database.DbClient.id == client_id).first()

def get_client_by_email(db: Session, email: str):
    return db.query(database.DbClient).filter(database.DbClient.email == email).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.DbClient).offset(skip).limit(limit).all()

def create_client(db: Session, client: models.ClientCreate):
    db_client = database.DbClient(
        email=client.email,
        first_name=client.first_name,
        last_name=client.last_name,
        risk_profile=client.risk_profile
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, client_id: int, client_update: models.ClientCreate):
    db_client = get_client(db, client_id)
    if db_client:
        db_client.first_name = client_update.first_name
        db_client.last_name = client_update.last_name
        db_client.email = client_update.email
        db_client.risk_profile = client_update.risk_profile
        db.commit()
        db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    db_client = get_client(db, client_id)
    if db_client:
        db.delete(db_client)
        db.commit()
    return db_client

# Asset CRUD Operations
def get_asset(db: Session, asset_id: int):
    return db.query(database.DbAsset).filter(database.DbAsset.id == asset_id).first()

def get_asset_by_ticker(db: Session, ticker_symbol: str):
    return db.query(database.DbAsset).filter(database.DbAsset.ticker_symbol == ticker_symbol).first()

def get_assets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(database.DbAsset).offset(skip).limit(limit).all()

def create_asset(db: Session, asset: models.AssetCreate):
    db_asset = database.DbAsset(**asset.dict())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

# Portfolio CRUD Operations
def get_portfolio(db: Session, portfolio_id: int):
    return db.query(database.DbPortfolio).filter(database.DbPortfolio.id == portfolio_id).first()

def get_portfolios_by_client(db: Session, client_id: int, skip: int = 0, limit: int = 10):
    return db.query(database.DbPortfolio).filter(database.DbPortfolio.client_id == client_id).offset(skip).limit(limit).all()

def create_client_portfolio(db: Session, portfolio: models.PortfolioCreate, client_id: int):
    db_portfolio = database.DbPortfolio(name=portfolio.name, client_id=client_id)
    db.add(db_portfolio)
    db.commit()
    # Now handle assets
    for p_asset in portfolio.assets:
        # Check if asset exists
        db_asset_check = get_asset(db, p_asset.asset_id)
        if not db_asset_check:
            # Or raise an error, for now skipping if asset not found
            print(f"Asset with id {p_asset.asset_id} not found. Skipping.")
            continue

        association = database.PortfolioAssetAssociation(
            portfolio_id=db_portfolio.id,
            asset_id=p_asset.asset_id,
            quantity=p_asset.quantity
        )
        db.add(association)

    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

def update_portfolio_assets(db: Session, portfolio_id: int, portfolio_update: models.PortfolioCreate):
    db_portfolio = get_portfolio(db, portfolio_id)
    if not db_portfolio:
        return None

    # Clear existing asset associations for this portfolio
    db.query(database.PortfolioAssetAssociation).filter(
        database.PortfolioAssetAssociation.portfolio_id == portfolio_id
    ).delete()

    # Add new asset associations
    for p_asset in portfolio_update.assets:
        db_asset_check = get_asset(db, p_asset.asset_id)
        if not db_asset_check:
            print(f"Asset with id {p_asset.asset_id} not found. Skipping.")
            continue
        association = database.PortfolioAssetAssociation(
            portfolio_id=portfolio_id,
            asset_id=p_asset.asset_id,
            quantity=p_asset.quantity
        )
        db.add(association)

    db_portfolio.name = portfolio_update.name # Update name as well
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio

def get_portfolio_details(db: Session, portfolio_id: int):
    # This function would ideally return the portfolio with its assets and calculated total value.
    # For now, it returns the basic portfolio. Calculation can be added in the schema or service layer.
    db_portfolio = get_portfolio(db, portfolio_id)
    if not db_portfolio:
        return None

    # Fetch associated assets and their quantities
    associations = db.query(database.PortfolioAssetAssociation).filter(
        database.PortfolioAssetAssociation.portfolio_id == portfolio_id
    ).all()

    assets_with_quantity = []
    total_value = 0.0
    for assoc in associations:
        asset_details = get_asset(db, assoc.asset_id)
        if asset_details:
            value = asset_details.current_price * assoc.quantity
            assets_with_quantity.append({
                "asset": models.Asset.from_orm(asset_details),
                "quantity": assoc.quantity,
                "value": value
            })
            total_value += value

    # We need to construct a Pydantic model for the response here.
    # Let's augment the existing models.Portfolio object or create a new one.
    # For now, returning a dict, will refine with Pydantic models in main.py or models.py

    # Create a models.Portfolio object and populate its 'assets' field
    # This requires models.Portfolio.assets to be List[models.Asset] or similar.
    # Current models.Portfolio.assets is List[models.PortfolioAsset] (id and quantity)
    # This means the response shaping will largely happen in the API endpoint.

    # For now, the CRUD returns the DB object, and the endpoint will shape it.
    # Or, we can attach this info to the db_portfolio object if the Pydantic model supports it.
    # Let's assume the endpoint will handle the shaping using this data.

    return {
        "portfolio_id": db_portfolio.id,
        "name": db_portfolio.name,
        "client_id": db_portfolio.client_id,
        "assets_details": assets_with_quantity,
        "total_value": total_value
    }
