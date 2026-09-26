from dataclasses import dataclass

@dataclass
class EmotionInput:
    breadth: float # 0..1, rising stocks ratio
    limit_up: int
    limit_down: int
    broken_board_rate: float # 0..1
    max_height: int
    turnover_ratio: float # relative to 20d average

def score(x: EmotionInput) -> tuple[float,str]:
    # Transparent, deterministic baseline; calibrate with walk-forward later.
    s = 100*(x.breadth-.5) + min(x.limit_up,100)*.25 - min(x.limit_down,50)*.8
    s += (x.max_height-3)*2 - x.broken_board_rate*25 + (x.turnover_ratio-1)*10
    s=max(-100,min(100,s))
    if s < -45: regime='冰点'
    elif s < -10: regime='修复'
    elif s > 50: regime='高潮'
    elif s > 15: regime='主升'
    else: regime='分歧/退潮'
    return round(s,2),regime
