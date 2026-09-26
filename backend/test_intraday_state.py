from intraday_state import BarState,classify
def test_reclaim():
 x=BarState(101,100,100,101,110,1,False);assert classify(x)=='VWAP_RECLAIM'
def test_breakout():
 x=BarState(110,100,100,110,120,2,True);assert classify(x)=='BREAKOUT_WITH_VOLUME'
def test_limit():
 x=BarState(10,9,9,10,10,1,True);assert classify(x)=='LIMIT_UP_SEALED'
