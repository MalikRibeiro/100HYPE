
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

# --- Assets ---
class AssetBase(BaseModel):
    ticker: str
    category: Optional[str] = None
    name: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetResponse(AssetBase):
    id: int

    class Config:
        from_attributes = True

# --- Transactions ---
class TransactionBase(BaseModel):
    asset_id: int
    type: str  # BUY / SELL
    quantity: float
    price: float

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    date: datetime

    class Config:
        from_attributes = True

# --- Portfolio Summary ---
class PortfolioPosition(BaseModel):
    ticker: str
    total_quantity: float
    average_price: float
