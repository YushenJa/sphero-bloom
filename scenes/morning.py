import time
from assets import Palette

HAND_THRESHOLD_RATIO = 0.7
HAND_DETECT_TIME = 1.0  #seconds that it has to be covered

class MorningRoutine:
    def __init__(self, bot):
        self.bot = bot
        self.is_running = False
        self.avg_light = None
        self.hand_cover_start = None

    def run(self):
        self.is_running = True
        self.bot.display_frame("SUN")
        self.bot.set_ambient_light(Palette.ORANGE)
        self.bot.play_mp3("little-robot-melody-211849.mp3")


        while self.is_running:
            sensors = self.bot.get_sensor_data()
            current_light = sensors['light']

            if self.avg_light is None:
                self.avg_light = current_light

            ratio = current_light / self.avg_light if self.avg_light > 0 else 1
            hand_detected_now = ratio < HAND_THRESHOLD_RATIO

            # Hand timer
            if hand_detected_now:
                if self.hand_cover_start is None:
                    self.hand_cover_start = time.time()
                elif time.time() - self.hand_cover_start >= HAND_DETECT_TIME:
                    self.handle_off(current_light)
                    break
            else:
                self.hand_cover_start = None

            self.avg_light = (self.avg_light * 0.95) + (current_light * 0.05)

            # movement
            self.bot.roll(0, 30, 1)
            self.bot.roll(90, 30, 1)
            self.bot.roll(180, 30, 1)
            self.bot.roll(270, 30, 1)

            time.sleep(0.1)


    def handle_off(self, current_light):
        print(f"Hand! (Avg: {self.avg_light:.1f} -> Curr: {current_light:.1f})")
        self.bot.stop()
        self.bot.set_ambient_light(Palette.BAD_RED) 
        self.bot.play_mp3("a-magical-discovery-chime-395712.mp3")
        self.calmed_down = True
        self.last_waddle_time = time.time()
        self.bot.display_frame("FLOWER_FULL")
        time.sleep(6) 
        self.bot.off_ambient_light()
        return "FLOWER :)"
    

