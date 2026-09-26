import pandas as pd

def trade_metrics(trades):
    if not trades:return {'win_rate':0,'profit_factor':0,'avg_hold_days':0,'max_loss_streak':0}
    buys=[x for x in trades if x['side']=='buy']; sells=[x for x in trades if x['side']=='sell']; pnls=[]; holds=[]
    for sell in sells:
        prior=[x for x in buys if x['date']<=sell['date']]
        if prior:
            buy=prior[-1];pnls.append((sell['price']-buy['price'])*sell['shares']-sell['fee']-buy['fee'])
            try:holds.append((pd.Timestamp(sell['date'])-pd.Timestamp(buy['date'])).days)
            except Exception:holds.append(0)
    wins=[p for p in pnls if p>0]; losses=[p for p in pnls if p<0]; streak=best=0
    for p in pnls:
        streak=streak+1 if p<0 else 0;best=max(best,streak)
    return {'win_rate':round(len(wins)/len(pnls),4) if pnls else 0,'profit_factor':round(sum(wins)/abs(sum(losses)),4) if losses else None,'avg_hold_days':round(sum(holds)/len(holds),2) if holds else 0,'max_loss_streak':best}
