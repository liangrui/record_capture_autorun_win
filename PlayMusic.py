import threading
import winsound


class PalySound(threading.Thread):
    def __init__(self):
        print("初始化...")
        threading.Thread.__init__(self)
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        self.play_sound()

    def play_sound(self, sound='./sounds/3.wav'):
        while self._running:
            winsound.PlaySound(sound, winsound.SND_ALIAS)
