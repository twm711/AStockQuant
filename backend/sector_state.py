from dataclasses import dataclass
@dataclass
class SectorPulse:
    return_pct:float; breadth:float; amount_ratio:float; leader_above_vwap:bool

def score(x:SectorPulse):
 s=0
 if x.return_pct>0:s+=1
 if x.breadth>=.6:s+=1
 if x.amount_ratio>=1.2:s+=1
 if x.leader_above_vwap:s+=1
 return {'score':s,'state':'STRONG' if s>=3 else 'WEAK' if s<=1 else 'MIXED'}
