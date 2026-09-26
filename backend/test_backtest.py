import pandas as pd
from backtest import run

def test_roundtrip():
 d=pd.DataFrame({'date':pd.date_range('2025-01-01',periods=3),'close':[10,12,11],'signal':[1,0,-1]})
 x=run(d); assert x['metrics']['final_equity']>0
