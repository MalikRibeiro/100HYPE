
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime
from app.db.base import Base

class MarketData(Base):
    ticker = Column(String, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)
