from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.portfolio import PortfolioPosition

class PortfolioService:
    @staticmethod
    def calculate_portfolio(user_id: int, db: Session) -> List[PortfolioPosition]:
        """
        Calculates the current portfolio position for a given user.
        Groups transactions by ticker, sums quantities, and calculates average price.
        """
        transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
        
        portfolio: Dict[str, Dict] = {}

        for t in transactions:
            ticker = t.asset.ticker
            if ticker not in portfolio:
                portfolio[ticker] = {"qty": 0.0, "total_cost": 0.0}
            
            if t.type == "BUY":
                portfolio[ticker]["qty"] += t.quantity
                # For simplified avg price, we track total cost of BUYs
                portfolio[ticker]["total_cost"] += (t.quantity * t.price)
            elif t.type == "SELL":
                portfolio[ticker]["qty"] -= t.quantity
                # We don't reduce total_cost here for the "Avg Buy Price" calculation 
                # as requested significantly often in simple portfolio managers.
                # However, to be more accurate for "Position Cost", we should reduce it.
                # But sticking to the logic extracted from the endpoint:
                # "Get purely BUYs to calculate true average BUY price"
                pass

        results = []
        for ticker, data in portfolio.items():
            # Recalculate Avg Price based on ALL Buys (Weighted Average Price)
            # This follows the logic previously in the endpoint.
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
