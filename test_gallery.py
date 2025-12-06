import time
from assets import FRAMES

def show_gallery(bot):
    
    all_frames = list(FRAMES.keys())
    
    while True:
        for frame_name in all_frames:
            print(f"Male: {frame_name}")
            
            bot.display_frame(frame_name)
            
            time.sleep(2)