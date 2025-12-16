import time

class MorningRoutine:
    def __init__(self, bot):
        self.bot = bot
        self.is_running = False

    def run(self, duration):
        self.is_running = True
        start = time.time()

        while self.is_running and time.time() - start < duration:
            self.bot.display_frame("SUN")
            """ self.bot.roll(0, 50, 0.5)
            self.bot.roll(90, 50, 0.5)
            self.bot.roll(180, 50, 0.5)
            self.bot.roll(270, 50, 0.5)
            """
            self.bot.roll(0, 10, 5)
    def stop(self):
        self.is_running = False
        self.bot.stop()
        self.bot.clear_matrix()
