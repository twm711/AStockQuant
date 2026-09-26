import pandas as pd
from minute_features import add_vwap_features
def test_vwap():
 d=pd.DataFrame({'symbol':['A','A'],'ts':[1,2],'high':[11,12],'low':[9,10],'close':[10,11],'amount':[100,110],'volume':[10,10]})
 x=add_vwap_features(d); assert round(x.vwap.iloc[-1],2)==10.5
