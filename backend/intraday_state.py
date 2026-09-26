from dataclasses import dataclass
@dataclass
class BarState:
    close:float; vwap:float; prev_close:float; high:float; limit_up:float; volume_ratio:float; prev_above_vwap:bool

def classify(x:BarState):
    if x.close>=x.limit_up*.999: return 'LIMIT_UP_SEALED'
    above=x.close>x.vwap
    if not x.prev_above_vwap and above: return 'VWAP_RECLAIM'
    if above and x.volume_ratio>=1.5 and x.close>=x.high*.998: return 'BREAKOUT_WITH_VOLUME'
    if x.prev_above_vwap and not above: return 'VWAP_LOSS'
    if x.close>x.prev_close and above: return 'ABOVE_VWAP_TREND'
    return 'RANGE'
