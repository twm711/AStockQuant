from ladder import build_ladder
def test_ladder():
 x=build_ladder([{'symbol':'a','board_height':1},{'symbol':'b','board_height':2,'promoted':True},{'symbol':'c','board_height':3,'is_broken':True}])
 assert x['max_height']==2 and x['promotion_rate']==1.0
