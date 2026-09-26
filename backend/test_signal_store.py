from strategy import signal
def test_signal_shape():
 x=signal(close=11,sma20=10,rsi=60,rel_volume=2,above_vwap=True,regime='主升');assert {'action','score','reasons'}<=set(x)
