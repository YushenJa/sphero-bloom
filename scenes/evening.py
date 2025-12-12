import time
import config
from assets import Palette
class EveningRoutine:
    def __init__(self, bot):
        self.bot = bot
        self.is_running = True
        self.last_waddle_time = 0
        self.snooze_until = 0
        self.calmed_down = False

        self.avg_light = None

    #Snooze
    def handle_snooze(self):
        print("15 Sekunden SNOOZE")
        self.bot.stop()
        self.bot.set_ambient_light(Palette.BAD_RED)
        self.bot.display_frame("CLOCK")
        self.bot.off_ambient_light()

        try:
            self.bot.droid.play_sound("collision")
        except: pass

        # Stille-Timer (jetzt 15 Sekunden, später 900)
        self.snooze_until = time.time() + 15
        time.sleep(15)
        self.bot.display_frame("ZZZ")
        self.bot.set_ambient_light(Palette.CENTER_ORANGE)

    #Go to sleep
    def handle_off(self, current_light):
        print(f"Hand! (Avg: {self.avg_light:.1f} -> Curr: {current_light:.1f})")
        self.bot.stop()
        self.bot.set_ambient_light(Palette.BAD_RED) 
        self.calmed_down = True
        self.last_waddle_time = time.time()
        self.bot.display_frame("EYES_CLOSED")
        self.bot.off_ambient_light()
        return "GO_TO_SLEEP"

    def run(self):
        print("Szene: ABEND aktiviert")
        self.bot.display_frame("ZZZ")
        self.bot.set_ambient_light(Palette.CENTER_ORANGE)

        while self.is_running:
            current_time = time.time()
            
            if current_time < self.snooze_until:
                time.sleep(0.2)
                continue

            sensors = self.bot.get_sensor_data()
            current_light = sensors['light']

            if self.avg_light is None:
                self.avg_light = current_light

            # 1. Überprüfung des Ladezustands            
            if sensors['is_charging']:
                return "GO_TO_SLEEP"

            diff = current_light - self.avg_light
            hand_detected = False
            
            # Adaptive hand detection
            if self.avg_light > 5:
                ratio = current_light / self.avg_light

                if ratio < 0.70:   # 30% weniger Licht
                    hand_detected = True

            if hand_detected and (sensors['shake'] < 0.3):
                self.handle_off(current_light)
                return "GO_TO_SLEEP"
                     
            else:
                self.calmed_down = False
                self.avg_light = (self.avg_light * 0.95) + (current_light * 0.05)

            # 3. Überprüfung der Erschütterung (wenn Roboter einfach steht)            
            if sensors['shake'] > config.SHAKE_THRESHOLD:
                self.handle_snooze()
                continue

            # 4. Waddle
            if current_time - self.last_waddle_time > config.WADDLE_INTERVAL_SECONDS:
                

                was_shaken = self.bot.waddle(config.SHAKE_THRESHOLD)
                
                if was_shaken:
                    self.handle_snooze()
                
                self.last_waddle_time = time.time()
            
            time.sleep(0.1)