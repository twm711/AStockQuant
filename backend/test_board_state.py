from board_state import LimitState,classify
def test_broken():assert classify(LimitState(9.8,10,True,.01,2))=='LIMIT_UP_BROKEN'
def test_reseal():assert classify(LimitState(10,10,False,.03,2))=='LIMIT_UP_RESEALED'
def test_stable():assert classify(LimitState(10,10,True,.04,1))=='LIMIT_UP_STABLE'
