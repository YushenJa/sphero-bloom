import math
import time
from spherov2.types import Color
import os
import pygame
from spherov2 import scanner


from assets import FRAMES, get_color_from_char

class BloomBot:
    def __init__(self, droid):

        self.droid = droid
        self.current_frame = None 
        self.last_print_time = 0

        try:
            self.droid.set_stabilization(True)
        except:
            pass

        try:
            pygame.mixer.init()
            print("🔊 Audio System: Online")
        except Exception as e:
            print(f"⚠️ Audio Error: {e}")



    def play_mp3(self, filename):
        try:
            
            sound_path = os.path.join("sound", filename)
            
            if os.path.exists(sound_path):
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play()
            else:
                print(f"⚠️ Sound file not found: {sound_path}")
        except Exception as e:
            print(f"⚠️ Play Error: {e}")



    def display_frame(self, frame_name):

        if self.current_frame == frame_name: return

        print(f" [Display] Image: {frame_name}")
        frame_data = FRAMES.get(frame_name, FRAMES.get("LOADING"))

        try:
            for y in range(8):
                for x in range(8):
                    char = frame_data[y][x]
                    color = get_color_from_char(char)
                    self.droid.set_matrix_pixel(x, y, color)
                    time.sleep(0.015) 
            self.current_frame = frame_name
        except Exception as e:
            print(f" Frame error: {e}")

    def set_ambient_light(self, color):
        self.droid.set_back_led(color)
        self.droid.set_front_led(color)

    def off_ambient_light(self):
        self.droid.set_back_led(Color(0, 0, 0))
        self.droid.set_front_led(Color(0, 0, 0))




    def get_sensor_data(self):
        data = {"light": 0, "is_charging": False, "shake": 0}

        try:
            lux = self.droid.get_luminosity()
            if lux and 'ambient_light' in lux: data["light"] = lux['ambient_light']
        except: pass
        
        # Mikro-Pause für Bluetooth
        time.sleep(0.02)

        try:
            gyro = self.droid.get_gyroscope()
            accel = self.droid.get_acceleration()
            shake_score = 0
            
            if gyro:
                gx, gy, gz = abs(gyro.get('x',0)), abs(gyro.get('y',0)), abs(gyro.get('z',0))
                shake_score += (gx + gy + gz) / 20.0

            if accel:
                ax, ay, az = accel.get('x',0), accel.get('y',0), accel.get('z',0)
                g_force = math.sqrt(ax**2 + ay**2 + az**2)
                shake_score += abs(g_force - 1.0) * 10 

            data["shake"] = shake_score

           
            if time.time() - self.last_print_time > 0.5:
                print(f"SENSOR: {shake_score:.2f} | Light: {data['light']}")
                self.last_print_time = time.time()

        except: pass

        return data

    def wait_for_interaction(self, duration, threshold):

        start_time = time.time()
        while time.time() - start_time < duration:
            data = self.get_sensor_data()
            if data["shake"] > threshold:
                return True

            time.sleep(0.05)
        return False

    def waddle(self, shake_threshold):

        try:
            self.droid.set_back_led(Color(255, 140, 0))
            self.droid.set_front_led(Color(255, 140, 0))
            print(" SPIN ")
            self.droid.spin(360, 3) 
            if self.wait_for_interaction(0.3, shake_threshold): 
                self.stop()
                return True
            
            self.off_ambient_light()
            return False
            
        except Exception as e:
            print(f"Waddle error: {e}")
            self.stop()
            return False

    def stop(self):
        try: self.droid.roll(0, 0, 0)
        except: pass


    def is_charging(self):
        try:
            self.droid.roll(0, 10, 0.5)

            gyro = self.droid.get_gyroscope()
            accel = self.droid.get_acceleration()
            shake_score = 0
            
            if gyro:
                gx, gy, gz = abs(gyro.get('x',0)), abs(gyro.get('y',0)), abs(gyro.get('z',0))
                shake_score += (gx + gy + gz) / 20.0

            if accel:
                ax, ay, az = accel.get('x',0), accel.get('y',0), accel.get('z',0)
                g_force = math.sqrt(ax**2 + ay**2 + az**2)
                shake_score += abs(g_force - 1.0) * 10 

            print (shake_score)



            return shake_score < 0.25
        except:
            return False
        
