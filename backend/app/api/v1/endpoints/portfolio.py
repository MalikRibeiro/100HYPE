
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
        return asset

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
    from app.services.portfolio_service import PortfolioService
    return PortfolioService.calculate_portfolio(current_user.id, db)
