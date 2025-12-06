import time
from spherov2.types import Color

from assets import FRAMES, get_color_from_char

class BloomBot:
    def __init__(self, droid):

        self.droid = droid
        self.current_frame = None 

    def display_frame(self, frame_name):

        if self.current_frame == frame_name:
            return

        print(f" [Display] male: {frame_name}")
        
        frame_data = FRAMES.get(frame_name, FRAMES["LOADING"])

        for y in range(8):
            for x in range(8):
                char = frame_data[y][x]
                color = get_color_from_char(char)
                self.droid.set_matrix_pixel(x, y, color)
        
        self.current_frame = frame_name