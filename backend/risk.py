from dataclasses import dataclass
@dataclass
class RiskGate:
    regime:str; allow_new:bool; max_position:float; chase_limit:float

def gate(regime):
    values={'冰点':(True,.2,.1),'修复':(True,.5,.3),'主升':(True,.8,.5),'高潮':(False,.5,.1),'分歧':(False,.3,.05),'分歧/退潮':(False,.2,0),'退潮':(False,.2,0),'极端退潮':(False,0,0)}
    x=values.get(regime,(False,0,0));return RiskGate(regime,x[0],x[1],x[2]).__dict__
