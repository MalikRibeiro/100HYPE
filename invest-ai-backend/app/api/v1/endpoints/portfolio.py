
from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.asset import Asset
from app.models.transaction import Transaction
from app.schemas.portfolio import (
    AssetCreate,
    AssetResponse,
    TransactionCreate,
    TransactionResponse,
    PortfolioPosition,
)

router = APIRouter()

@router.post("/assets", response_model=AssetResponse)
def create_asset(
    asset_in: AssetCreate,
    db: Session = Depends(deps.get_db),
    # current_user: User = Depends(deps.get_current_user) # Optional: admin only?
):
    asset = db.query(Asset).filter(Asset.ticker == asset_in.ticker).first()
    if asset:
        raise HTTPException(status_code=400, detail="Asset already exists")
    asset = Asset(
        ticker=asset_in.ticker,
        category=asset_in.category,
        name=asset_in.name
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(
    transaction_in: TransactionCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Verify asset exists
    asset = db.query(Asset).filter(Asset.id == transaction_in.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    transaction = Transaction(
        user_id=current_user.id,
        asset_id=transaction_in.asset_id,
        type=transaction_in.type.upper(),
        quantity=transaction_in.quantity,
        price=transaction_in.price
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

@router.get("/portfolio", response_model=List[PortfolioPosition])
def read_portfolio(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Simply grouping transactions to calculate holdings
    # This logic mimics the request: sum buys - sum sells, avg price approximation
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()
    
    portfolio: Dict[str, Dict] = {}

    for t in transactions:
        ticker = t.asset.ticker
        if ticker not in portfolio:
            portfolio[ticker] = {"qty": 0.0, "total_cost": 0.0}
        
        if t.type == "BUY":
            portfolio[ticker]["qty"] += t.quantity
            portfolio[ticker]["total_cost"] += (t.quantity * t.price)
        elif t.type == "SELL":
            portfolio[ticker]["qty"] -= t.quantity
            # Logic for reducing cost basis on sell is complex (FIFO/LIFO/Avg). 
            # For simple "average price" display, we often track avg cost of current holdings.
            # Simplified approach: reduce total_cost proportionally or ignore for simple "avg price of BUYs".
            # The prompt asked for: "Ticker, Quantidade Total, Preço Médio".
            # Usually users want Avg Price of *open* position.
            # Let's simple implementation: total_cost only increases on BUY.
            # Avg Price = total_cost / total_bought_qty? Or current_qty?
            # Let's stick to: Avg Price = (Sum(Buy Qty * Buy Price) / Sum(Buy Qty)) -> Position Cost.
            pass

    results = []
    for ticker, data in portfolio.items():
        # Get purely BUYs to calculate true average BUY price
        buys = [t for t in transactions if t.asset.ticker == ticker and t.type == "BUY"]
        total_bought = sum(t.quantity for t in buys)
        total_cost = sum(t.quantity * t.price for t in buys)
        
        avg_price = (total_cost / total_bought) if total_bought > 0 else 0.0
        
        if data["qty"] > 0: # Only show assets with positive balance
            results.append(PortfolioPosition(
                ticker=ticker,
                total_quantity=data["qty"],
                average_price=avg_price
            ))
            
    return results
