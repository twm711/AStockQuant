from dataclasses import dataclass
@dataclass
class Auction:
    symbol:str; ts_ms:int; indicative_price:float; matched_volume:float; imbalance:float

def classify(a:Auction, prev_close:float):
    gap=(a.indicative_price/prev_close-1) if prev_close else 0
    if gap>=.03 and a.imbalance>=0: return 'STRONG_OPEN'
    if gap<=-.03 and a.imbalance<0: return 'WEAK_OPEN'
    if abs(gap)<.01: return 'NEUTRAL_OPEN'
    return 'DIVERGENT_OPEN'
