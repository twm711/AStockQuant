from backtest_rules import executable,sellable_shares
def test_t1(): assert sellable_shares(100,300)==200
def test_limit(): assert not executable('buy',at_limit_up=True); assert not executable('sell',at_limit_down=True)
