from emotion import EmotionInput, score

def test_emotion_low():
    s,r=score(EmotionInput(.25,3,40,.7,2,.7)); assert s < 0 and r == '冰点'
def test_emotion_high():
    s,r=score(EmotionInput(.8,80,2,.1,8,1.4)); assert s > 15
