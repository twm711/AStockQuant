from dataclasses import dataclass
@dataclass
class Fill:
    side:str; price:float; shares:int; fee:float

def sellable_shares(bought_today:int, held:int)->int:
    return max(0,held-bought_today)
def executable(side:str, *, suspended=False, at_limit_up=False, at_limit_down=False):
    if suspended:return False
    if side=='buy' and at_limit_up:return False
    if side=='sell' and at_limit_down:return False
    return True
