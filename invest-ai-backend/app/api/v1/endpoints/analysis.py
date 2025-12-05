from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.transaction import Transaction
from app.models.analysis import AIAnalysis
from app.services.market_data_service import MarketDataService
from app.services.ai_service import AIAnalystService
from app.services.email_service import EmailService

router = APIRouter()

@router.post("/generate")
def generate_portfolio_analysis(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # 1. Calculate Portfolio
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()
    
    portfolio_map = {}
    for t in transactions:
        ticker = t.asset.ticker
        if ticker not in portfolio_map:
            portfolio_map[ticker] = {
                "ticker": ticker,
                "category": t.asset.category,
                "qty": 0.0
            }
        if t.type == "BUY":
            portfolio_map[ticker]["qty"] += t.quantity
        elif t.type == "SELL":
            portfolio_map[ticker]["qty"] -= t.quantity
            
    portfolio_data = []
    for ticker, data in portfolio_map.items():
        if data["qty"] > 0:
            current_price = MarketDataService.get_price(ticker)
            value = data["qty"] * current_price
            portfolio_data.append({
                "ticker": ticker,
                "category": data["category"],
                "value": value,
                # Allocation is calculated in AI service or here.
                # AI service calculates it based on total, so we can just pass value.
            })
            
    if not portfolio_data:
         # Depending on logic, empty portfolio might still want analysis? 
         # But AI service prompt assumes assets.
         raise HTTPException(status_code=400, detail="Portfolio is empty or has no assets.")

    # 2. Generate AI Analysis
    ai_service = AIAnalystService()
    analysis_text = ai_service.generate_analysis(portfolio_data)

    # 3. Save to DB
    analysis = AIAnalysis(user_id=current_user.id, content=analysis_text)
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # 4. Email
    EmailService.send_email(current_user.email, "Sua Análise de Portfólio - Invest-AI", analysis_text)

    return {"content": analysis_text}
