import threading
import winsound
import time

class PalySound(threading.Thread):
    def __init__(self,sound='./sounds/3.wav'):
        print("初始化...")
        threading.Thread.__init__(self)
        self._running = True
        self._sound = sound


    def terminate(self):
        self._running = False

    def run(self):
        self.play_sound()

    def play_sound(self):
        t1 = t2 = time.time()
        while self._running and (t2 - t1) < 10:
            print(t2-t1)
            winsound.PlaySound(self._sound, winsound.SND_ALIAS)
            t2 = time.time()
