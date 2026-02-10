
# init_db.py
import sys
from app.db.base import Base
from app.db.session import engine
# Import all models to ensure they are registered with Base.metadata
from app.models.user import User
from app.models.asset import Asset
from app.models.transaction import Transaction
from app.models.market_data import MarketData

def init():
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
        return 0
    except Exception as e:
        print(f"Error creating tables: {e}")
        return 1

if __name__ == "__main__":
    exit_code = init()
    sys.exit(exit_code)
