from auction import Auction,classify
def test_auction():
 assert classify(Auction('600519.SH',1,103,100,1),100)=='STRONG_OPEN'
 assert classify(Auction('600519.SH',1,97,100,-1),100)=='WEAK_OPEN'
