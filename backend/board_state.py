from dataclasses import dataclass
@dataclass
class LimitState:
    close:float; limit_up:float; was_locked:bool; seal_ratio:float; volume_ratio:float

def classify(x:LimitState):
    locked=x.close>=x.limit_up*.999
    if x.was_locked and not locked:return 'LIMIT_UP_BROKEN'
    if not x.was_locked and locked:return 'LIMIT_UP_RESEALED'
    if locked and x.seal_ratio>=.02:return 'LIMIT_UP_STABLE'
    if locked:return 'LIMIT_UP_WEAK'
    return 'NO_LIMIT'
