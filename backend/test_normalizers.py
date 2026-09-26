import pytest
from normalizers import snapshots,daily_bars

def test_snapshot_contract():
 x=snapshots({'code':0,'data':{'item':[{'thscode':'600519.SH','last_price':100,'price_change_ratio_pct':2.1}]}})
 assert x[0]['symbol']=='600519.SH' and x[0]['price']==100

def test_history_contract():
 x=daily_bars({'code':0,'data':{'item':[{'date_ms':1,'open_price':1,'high_price':2,'low_price':.5,'close_price':1.5,'volume':10,'turnover':20}]}},'600519.SH','forward')
 assert x[0]['close']==1.5 and x[0]['adjustment']=='forward'

def test_business_error():
 with pytest.raises(ValueError): snapshots({'code':2001,'message':'bad'})
