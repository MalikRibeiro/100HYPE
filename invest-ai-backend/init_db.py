
# init_db.py
from app.db.base import Base
from app.db.session import engine
# Import all models to ensure they are registered with Base.metadata
from app.models.user import User
from app.models.asset import Asset
from app.models.transaction import Transaction
from app.models.market_data import MarketData

def init():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    init()
