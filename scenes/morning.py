import time
from assets import Palette

class MorningRoutine:
    def __init__(self, bot):
        self.bot = bot
        self.is_running = False
    
    def run(self, duration):
        self.is_running = True
        start = time.time()

        while self.is_running and time.time() - start < duration:
            self.bot.set_ambient_light(Palette.ORANGE)
            self.bot.display_frame("SUN")
            #Combines heading(0-360°), speed(-255-255), and duration (sec).
            for _ in range(3):
                self.bot.roll(0, 50, 0.5) #(heading: int, speed: int, duration: float)
                self.bot.roll(90, 50, 0.5)
                self.bot.roll(180, 50, 0.5)
                self.bot.roll(270, 50, 0.5)
            
    def stop(self):
        self.is_running = False
        self.bot.stop()
        self.bot.clear_matrix()
