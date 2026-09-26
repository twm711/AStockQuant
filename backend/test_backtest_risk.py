import pandas as pd
from backtest import run
def test_regime_caps_new_position():
 d=pd.DataFrame({'date':['2026-01-01'],'close':[10.0],'signal':[1],'regime':['冰点']})
 x=run(d); assert x['curve'].iloc[0].shares <= 20000
