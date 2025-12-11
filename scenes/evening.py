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

    def handle_snooze(self):
        print("15 Sekunden SNOOZE")
        self.bot.stop()
        self.bot.display_frame("EYES_OPEN")
        self.bot.off_ambient_light()

        try:
            self.bot.droid.play_sound("collision")
        except: pass

        # Stille-Timer (jetzt 20 Sekunden, später 900)
        self.snooze_until = time.time() + 20
        time.sleep(20)
        self.bot.display_frame("ZZZ")
        self.bot.set_ambient_light(Palette.CENTER_ORANGE)
        

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

            # 1. Überprüfung des Ladezustands            
            if sensors['is_charging']:
                return "GO_TO_SLEEP"

            # 2. Beruhigung mit der Hand (wenn es dunkel ist und ...)            
            if (sensors['light'] < config.LIGHT_THRESHOLD_LOW) and (sensors['shake'] > 1.0):
                continue
            else:
                self.calmed_down = False

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