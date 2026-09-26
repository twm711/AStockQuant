from trading_rules import *
def test_st_limit(): assert limit_prices(Instrument('000001.SZ',10,st=True))==(9.5,10.5)
def test_board_limits():
 assert limit_prices(Instrument('300750.SZ',100))==(80,120)
 assert limit_prices(Instrument('688001.SH',100))==(80,120)
 assert limit_prices(Instrument('430001.BJ',100))==(70,130)
def test_lot(): assert round_lot(1234,10)==100
