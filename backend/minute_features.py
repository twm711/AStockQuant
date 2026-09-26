import pandas as pd

def add_vwap_features(df:pd.DataFrame)->pd.DataFrame:
    out=df.sort_values(['symbol','ts']).copy(); out['typical']=(out.high+out.low+out.close)/3
    out['cum_amount']=out.groupby('symbol').amount.cumsum();out['cum_volume']=out.groupby('symbol').volume.cumsum()
    out['vwap']=out.cum_amount/out.cum_volume.replace(0,pd.NA)
    out['above_vwap']=out.close>out.vwap
    out['relative_volume']=out.volume/out.groupby('symbol').volume.transform(lambda x:x.rolling(20,min_periods=5).median())
    return out
