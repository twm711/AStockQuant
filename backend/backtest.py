"""Leakage-safe baseline event backtester with A-share execution guards."""
from dataclasses import dataclass
import pandas as pd
try:
    from .trading_rules import round_lot
    from .backtest_rules import executable, sellable_shares
    from .risk import gate
except ImportError:
    from trading_rules import round_lot
    from backtest_rules import executable, sellable_shares
    from risk import gate
@dataclass
class BacktestConfig:
    initial_cash:float=1_000_000; fee_rate:float=.0003; stamp_tax:float=.0005; slippage:float=.0005; max_position:float=.95

def run(df:pd.DataFrame,cfg=BacktestConfig()):
    required={'date','close','signal'}
    if not required<=set(df): raise ValueError(f'missing columns: {required-set(df)}')
    cash=cfg.initial_cash; shares=0; bought_today=0; last_day=None; rows=[]; trades=[]
    for _,r in df.sort_values('date').iterrows():
        day=str(r.date)[:10]
        if day!=last_day: bought_today=0;last_day=day
        px=float(r.close); side='buy' if r.signal>0 else 'sell' if r.signal<0 else ''
        regime=str(r.get('regime',''))
        regime_cap=gate(regime)['max_position'] if regime else 1.0
        if side=='buy' and regime and not gate(regime)['allow_new']: side=''
        suspended=bool(r.get('suspended',False)); at_up=bool(r.get('at_limit_up',False)); at_down=bool(r.get('at_limit_down',False))
        if side=='buy' and shares==0 and executable(side,suspended=suspended,at_limit_up=at_up,at_limit_down=at_down):
            budget=cash*min(cfg.max_position,regime_cap); qty=round_lot(budget,px*(1+cfg.slippage)); cost=qty*px*(1+cfg.slippage); fee=cost*cfg.fee_rate; cash-=cost+fee;shares+=qty;bought_today+=qty;trades.append({'date':r.date,'side':'buy','price':px,'shares':qty,'fee':fee,'regime':regime})
        elif side=='sell' and shares>0 and executable(side,suspended=suspended,at_limit_up=at_up,at_limit_down=at_down):
            qty=sellable_shares(bought_today,shares); proceeds=qty*px*(1-cfg.slippage); fee=proceeds*(cfg.fee_rate+cfg.stamp_tax); cash+=proceeds-fee;shares-=qty;trades.append({'date':r.date,'side':'sell','price':px,'shares':qty,'fee':fee,'regime':regime})
        rows.append({'date':r.date,'cash':cash,'shares':shares,'equity':cash+shares*px})
    curve=pd.DataFrame(rows)
    if curve.empty:return {'metrics':{},'curve':curve,'trades':trades}
    dd=curve.equity/curve.equity.cummax()-1
    return {'metrics':{'total_return':round(float(curve.equity.iloc[-1]/cfg.initial_cash-1),6),'max_drawdown':round(float(dd.min()),6),'final_equity':round(float(curve.equity.iloc[-1]),2),'trade_count':len(trades)},'curve':curve,'trades':trades}
