import winsound
import time

# winsound.PlaySound('../sounds/cow.wav', winsound.SND_FILENAME)  # 播放牛叫
# winsound.PlaySound('SystemExit', winsound.SND_ALIAS) # 叮咚
# winsound.PlaySound('SystemHand', winsound.SND_ALIAS) # 滴咚
# winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS) # 滴呤咚~
# winsound.PlaySound('SystemQuestion', winsound.SND_ALIAS) # 滴呤咚~
winsound.PlaySound('SystemAsterisk', winsound.SND_ALIAS|winsound.SND_LOOP) # 滴呤咚~
# winsound.MessageBeep()
winsound.Beep(500, 150) # freq=37到 32,767之间。duration指定持续的毫秒数
# time.sleep(3)