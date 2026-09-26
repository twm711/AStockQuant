from strategy import signal
def test_gate_blocks_high_chase():
 x=signal(close=11,sma20=10,rsi=60,rel_volume=2,above_vwap=True,regime='高潮');assert x['action']!='buy'
