from app.db.session import engine
from app.db.base import Base
from app.models.user import User
from app.models.asset import Asset
from app.models.transaction import Transaction
from app.models.analysis import AIAnalysis

def init_db():
    print("Creating all tables in database...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_db()
