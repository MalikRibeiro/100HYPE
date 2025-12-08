from unittest.mock import MagicMock
from app.services.portfolio_service import PortfolioService
from app.models.transaction import Transaction
from app.models.asset import Asset
# --- FIX: Importar AIAnalysis para registrar a tabela no SQLAlchemy ---
from app.models.analysis import AIAnalysis 

def test_calculate_portfolio_simple_buy():
    # Setup Mock DB Session
    mock_db = MagicMock()
    
    # Mock Transactions
    # Scenario: User bought 10 AAPL at $150
    mock_asset = Asset(ticker="AAPL", category="US_STOCKS", name="Apple Inc.")
    tx1 = Transaction(user_id=1, asset=mock_asset, type="BUY", quantity=10, price=150.0)
    
    mock_db.query.return_value.filter.return_value.all.return_value = [tx1]
    
    # Act
    results = PortfolioService.calculate_portfolio(user_id=1, db=mock_db)
    
    # Assert
    assert len(results) == 1
    assert results[0].ticker == "AAPL"
    assert results[0].total_quantity == 10.0
    assert results[0].average_price == 150.0

def test_calculate_portfolio_buy_and_sell():
    # Setup Mock DB Session
    mock_db = MagicMock()
    
    # Mock Transactions
    # Scenario: 
    # 1. Bought 10 AAPL at $100
    # 2. Bought 10 AAPL at $200 (Avg Price should be $150)
    # 3. Sold 5 AAPL (Avg Price should remain $150, but Qty becomes 15)
    mock_asset = Asset(ticker="AAPL", category="US_STOCKS", name="Apple Inc.")
    tx1 = Transaction(user_id=1, asset=mock_asset, type="BUY", quantity=10, price=100.0)
    tx2 = Transaction(user_id=1, asset=mock_asset, type="BUY", quantity=10, price=200.0)
    tx3 = Transaction(user_id=1, asset=mock_asset, type="SELL", quantity=5, price=250.0) # Price doesn't matter for Avg Buy Price
    
    mock_db.query.return_value.filter.return_value.all.return_value = [tx1, tx2, tx3]
    
    # Act
    results = PortfolioService.calculate_portfolio(user_id=1, db=mock_db)
    
    # Assert
    assert len(results) == 1
    assert results[0].ticker == "AAPL"
    assert results[0].total_quantity == 15.0 # 10 + 10 - 5
    assert results[0].average_price == 150.0 # (1000 + 2000) / 20 = 150