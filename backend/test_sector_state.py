from sector_state import SectorPulse,score
def test_strong():assert score(SectorPulse(2,.7,1.3,True))['state']=='STRONG'
