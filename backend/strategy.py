from dataclasses import dataclass
try:
    from .risk import gate as _risk_gate
except ImportError:
    from risk import gate as _risk_gate
@dataclass
class Gate:
    regime:str
    max_position:float
    allow_new:bool

def gate_for(regime:str)->Gate:
    r=_risk_gate(regime)
    return Gate(regime,r['max_position'],r['allow_new'])
def signal(*,close,sma20,rsi,rel_volume,above_vwap,regime):
    gate=gate_for(regime)
    reasons=[]; score=0
    if close>sma20: score+=1;reasons.append('价格在SMA20上方')
    if 45<=rsi<=75: score+=1;reasons.append('RSI处于趋势区间')
    if rel_volume>=1.2: score+=1;reasons.append('相对成交量放大')
    if above_vwap: score+=1;reasons.append('分时在VWAP上方')
    if score>=3 and gate.allow_new: action='buy'
    elif score<=1: action='sell'
    else: action='hold'
    return {'action':action,'score':score,'max_position':gate.max_position,'reasons':reasons,'regime':regime}
