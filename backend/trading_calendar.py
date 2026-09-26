from datetime import date

def can_trade(trade_date: date, holidays: set[date]) -> bool:
    return trade_date.weekday() < 5 and trade_date not in holidays

def next_trade_date(d: date, holidays: set[date]):
    from datetime import timedelta
    while True:
        d += timedelta(days=1)
        if can_trade(d, holidays): return d
