import time
import config
from assets import Palette

HAND_DETECT_TIME = 1.5  #seconds that it has to be covered

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
        self.bot.play_mp3("roboter-sound-v1_Y3D6Kcvq.mp3")
        self.bot.set_ambient_light(Palette.BAD_RED)
        self.bot.display_frame("CLOCK")
        self.bot.off_ambient_light()

        # Stille-Timer (jetzt 15 Sekunden, später 900)
        self.snooze_until = time.time() + 15
        time.sleep(15)
        self.bot.display_frame("ZZZ")
        self.bot.play_mp3("wake-up-the-robot-84894.mp3")

    #Go to sleep
    def handle_off(self, current_light):
        print(f"Hand! (Avg: {self.avg_light:.1f} -> Curr: {current_light:.1f})")
        
        # 1. Initiale Aktionen (Licht aus, Augen zu, Sound)
        self.bot.stop()
        self.bot.set_ambient_light(Palette.ORANGE)
        self.bot.play_mp3("cute-snoring-robot.mp3")
        self.bot.display_frame("EYES_HALF_CLOSED")
        self.bot.off_ambient_light()

        time.sleep(1)
        
        last_snore_time = time.time()
        SNORE_INTERVAL = 20

        # 2. Die Endlos-Schleife (Die "Falle")
        while True:
            sensors = self.bot.get_sensor_data()
            if sensors['shake'] < 0.15 and self.bot.is_charging():
                self.bot.display_frame("LOADING")
                self.bot.play_mp3("live-chat-353605.mp3")

                time.sleep(3)

                self.bot.play_mp3("off.mp3")
                self.bot.display_frame("EYES_CLOSED")
                print("⚡ Ladestation erkannt! Beende Programm.")
                return


            if time.time() - last_snore_time > SNORE_INTERVAL:
                print("🔊 Schnarchen...")
                self.bot.play_mp3("cute-snoring-robot.mp3")
                last_snore_time = time.time()
                self.bot.display_frame("EYES_HALF_CLOSED")

            time.sleep(1)

    def run(self):
        print("Szene: ABEND aktiviert")
        self.bot.display_frame("ZZZ")
        self.bot.play_mp3("wake-up-the-robot-84894.mp3")
        self.bot.set_ambient_light(Palette.ORANGE)

        while self.is_running:
            current_time = time.time()
            
            if current_time < self.snooze_until:
                time.sleep(0.2)
                continue

            sensors = self.bot.get_sensor_data()
            current_light = sensors['light']

            if self.avg_light is None:
                self.avg_light = current_light

            hand_detected = False

            print (sensors["spin_value1"])
            print (sensors["spin_value3"])
            if sensors["spin_value1"] < -0.9 and sensors["spin_value3"] < 0.15:

                if sensors['shake'] < 10:
                    print("Ausnahmetag")

                    self.bot.off_ambient_light()
                    self.bot.play_mp3("live-chat-353605.mp3")
                    time.sleep(1)
                    self.bot.play_mp3("audio_2026-01-07_22-00-46.mp3")
                    self.bot.display_frame("LOADING")
                    self.bot.stop()
                        
                    time.sleep(3)
                    self.bot.clear_matrix()
                    self.bot.off_ambient_light()
                        
                    return "EXCEPTION_DAY"
            
            # Adaptive hand detection
            ratio = current_light / max(self.avg_light, 1.0)

            #Check both relative and absolute drop
            if (ratio < 0.7 and
                current_light < self.avg_light - 10):

                if not self.hand_is_covering:
                    self.hand_is_covering = True
                    self.hand_cover_start_time = current_time
                else:
                    if current_time - self.hand_cover_start_time >= HAND_DETECT_TIME:
                        hand_detected = True
            else:
                # Light recovered -> reset state
                self.hand_is_covering = False
                self.hand_cover_start_time = None              

            # Update baseline omly if not covered
            if not self.hand_is_covering:
                self.avg_light = (self.avg_light * 0.95) + (current_light * 0.05)

            if hand_detected and (sensors['shake'] < 0.3):
                self.handle_off(current_light)
                return "GO_TO_SLEEP"
   


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