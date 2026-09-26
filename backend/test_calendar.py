from datetime import date
from trading_calendar import can_trade,next_trade_date

def test_weekend():
 assert not can_trade(date(2026,9,26),set())
 assert next_trade_date(date(2026,9,25),set())==date(2026,9,28)
