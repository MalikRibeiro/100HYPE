
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Asset(Base):
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True)
    name = Column(String)
    
    transactions = relationship("Transaction", back_populates="asset")
