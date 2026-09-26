import pandas as pd

def by_regime(trades):
    if not trades:return []
    df=pd.DataFrame(trades); df['pnl']=0.0
    buys=df[df.side=='buy'].set_index('date').price
    for i,r in df[df.side=='sell'].iterrows():
        prior=df[(df.side=='buy')&(df.date<=r.date)]
        if not prior.empty: df.loc[i,'pnl']=(r.price-prior.iloc[-1].price)*r.shares-r.fee
    return df.groupby('regime',dropna=False).agg(trades=('side','count'),pnl=('pnl','sum')).reset_index().to_dict('records')
