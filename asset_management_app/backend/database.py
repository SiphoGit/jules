from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .models import RiskProfile # Importing our Pydantic enum

DATABASE_URL = "sqlite:///./asset_management.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False} # check_same_thread is needed only for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Association table for Portfolio and Asset (Many-to-Many)
class PortfolioAssetAssociation(Base):
    __tablename__ = "portfolio_asset_association"
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), primary_key=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    quantity = Column(Float, nullable=False)

    asset = relationship("DbAsset") # Relationship to DbAsset

class DbClient(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    risk_profile = Column(SQLAlchemyEnum(RiskProfile), default=RiskProfile.medium)

    portfolios = relationship("DbPortfolio", back_populates="owner")

class DbAsset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    ticker_symbol = Column(String, unique=True, index=True)
    asset_type = Column(String)
    current_price = Column(Float)

    # portfolios attribute for the many-to-many relationship will be defined via PortfolioAssetAssociation
    # This allows accessing portfolios this asset is part of, if needed.
    # portfolios = relationship("DbPortfolio", secondary="portfolio_asset_association", back_populates="assets_in_portfolio")


class DbPortfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Default Portfolio")
    client_id = Column(Integer, ForeignKey("clients.id"))

    owner = relationship("DbClient", back_populates="portfolios")
    # assets_in_portfolio is a list of DbAsset objects linked via PortfolioAssetAssociation
    assets_in_portfolio = relationship("DbAsset", secondary="portfolio_asset_association", viewonly=True) # viewonly because quantity is in association
    # If we want to access the association table directly to get quantity:
    asset_associations = relationship("PortfolioAssetAssociation")


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
