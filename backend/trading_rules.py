from dataclasses import dataclass
@dataclass
class Instrument:
    symbol:str; prev_close:float; limit_pct:float|None=None; st:bool=False; suspended:bool=False; buyable:bool=True; sellable:bool=True

def default_limit_pct(symbol:str,st=False):
    if st:return .05
    code=symbol.split('.')[0]
    if code.startswith(('300','301','688','689')): return .20
    if code.startswith(('430','8','92')): return .30
    return .10

def limit_prices(i:Instrument):
    pct=i.limit_pct if i.limit_pct is not None else default_limit_pct(i.symbol,i.st)
    return round(i.prev_close*(1-pct),2),round(i.prev_close*(1+pct),2)
def can_buy(i:Instrument,price:float):
    _,hi=limit_prices(i); return i.buyable and not i.suspended and price < hi-1e-9
def can_sell(i:Instrument,price:float):
    lo,_=limit_prices(i); return i.sellable and not i.suspended and price > lo+1e-9
def round_lot(cash,price): return max(0,int(cash//price//100)*100)
