import math
import time
from spherov2.types import Color
from assets import Palette
from assets import FRAMES, get_color_from_char

class BloomBot:
    def __init__(self, droid):

        self.droid = droid
        self.current_frame = None 
        self.last_print_time = 0
        self.frame_animations = {}
        self.register_all_frames()

        
        try:
            self.droid.set_stabilization(True)
        except:
            pass

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
            pwr = str(self.droid.get_power_state())
            if "Charging" in pwr or "Charged" in pwr: data["is_charging"] = True
        except: pass

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
    
    def roll(self, heading, speed, duration):
        self.droid.roll(heading, speed, duration)

    def stop(self, heading=None):
        self.droid.stop_roll(heading)
    
    def clear_matrix(self):
        self.droid.clear_matrix()

    def register_all_frames(self):
        animation_id = 0
        
        # Max 16 colors
        palette = [
            Palette.OFF,           # 0
            Palette.YELLOW,        # 1
            Palette.WHITE,         # 2
            Palette.STEM_GREEN,    # 3
            Palette.PETAL_PINK,    # 4
            Palette.ORANGE,        # 5
            Palette.LOADING_BLUE,  # 6
            Palette.BAD_RED,       # 7
        ]
        
        char_to_index = {
            '.': 0,  # OFF
            'Y': 1,  # YELLOW
            'W': 2,  # WHITE
            'G': 3,  # STEM_GREEN
            'P': 4,  # PETAL_PINK
            'O': 5,  # ORANGE
            'B': 6,  # LOADING_BLUE
            'R': 7,  # BAD_RED
        }
        
        for frame_name, frame_data in FRAMES.items():
            # Convert strings to indexe's matrix  
            frame_matrix = []
            for row_str in frame_data:
                row = [char_to_index[char] for char in row_str]
                frame_matrix.append(row)
            
            # Register animation
            self.droid.register_matrix_animation(
                frames=[frame_matrix],
                palette=palette,
                fps=1,
                transition=False
            )
            
            self.frame_animations[frame_name] = animation_id
            animation_id += 1
        
        print(f" [BloomBot] {len(self.frame_animations)} frames registered")
    

    def display_frame(self, frame_name):
        if self.current_frame == frame_name:
            return
        
        if frame_name not in self.frame_animations:
            print(f" [Display] Frame '{frame_name}' nicht gefunden")
            frame_name = "LOADING"  # fallback
        
        print(f" [Display] Image: {frame_name}")
        
        animation_id = self.frame_animations[frame_name]
        self.droid.clear_matrix()
        self.droid.play_matrix_animation(animation_id, loop=False)
        
        self.current_frame = frame_name
    
        """ def display_frame(self, frame_name):

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
            print(f" Frame error: {e}") """