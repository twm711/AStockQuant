"""Leakage-safe TA-Lib adapter. Optional dependency with numpy fallbacks planned."""
import numpy as np

def add_features(df):
    """Add deterministic OHLCV features; input must be sorted by symbol, timestamp."""
    out=df.copy()
    close=out['close'].astype(float)
    out['ret_1']=close.groupby(out['symbol']).pct_change()
    out['sma_20']=close.groupby(out['symbol']).transform(lambda x:x.rolling(20,min_periods=20).mean())
    out['vol_20']=out['ret_1'].groupby(out['symbol']).transform(lambda x:x.rolling(20,min_periods=20).std())
    out['range_atr_proxy']=(out['high']-out['low'])/close.shift(1)
    out['rel_volume']=out['volume']/out.groupby('symbol')['volume'].transform(lambda x:x.rolling(20,min_periods=5).median())
    try:
        import talib
        groups=[]
        for _,g in out.groupby('symbol',sort=False):
            g=g.copy(); h,l,c=g.high.values,g.low.values,g.close.values
            g['rsi_14']=talib.RSI(c,14);g['adx_14']=talib.ADX(h,l,c,14)
            g['atr_14']=talib.ATR(h,l,c,14);g['macd'],g['macd_signal'],_=talib.MACD(c)
            groups.append(g)
        return __import__('pandas').concat(groups).sort_index()
    except ImportError:
        return out
