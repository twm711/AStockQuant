from dataclasses import dataclass
@dataclass
class DayMetrics:
    limit_up:int; limit_down:int; broken_rate:float; max_height:int; promotion_rate:float; breadth:float; turnover_ratio:float

def classify(m:DayMetrics, prev:str|None=None):
    if m.limit_down>=max(30,m.limit_up*1.5) or m.breadth<.25:return '极端退潮'
    if m.limit_up<=15 and m.broken_rate>=.4:return '冰点'
    if prev in ('冰点','极端退潮') and m.limit_up>15 and m.broken_rate<.35:return '修复'
    if m.limit_up>=60 and m.broken_rate<.2 and m.promotion_rate>=.35:return '高潮'
    if m.max_height>=5 and m.promotion_rate>=.3 and m.breadth>=.55:return '主升'
    if m.broken_rate>=.4 or m.promotion_rate<.2:return '退潮'
    return '分歧'

def transition(previous,current):
    if not previous:return 'INIT'
    if previous==current:return 'HOLD'
    return f'{previous}->{current}'
