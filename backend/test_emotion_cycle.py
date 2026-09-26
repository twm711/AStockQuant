from emotion_cycle import *
def test_repair():
 m=DayMetrics(30,5,.2,4,.4,.6,1.1);assert classify(m,'冰点')=='修复'
def test_decay():
 m=DayMetrics(12,35,.6,2,.1,.2,.7);assert classify(m)=='极端退潮'
def test_transition():assert transition('修复','主升')=='修复->主升'
