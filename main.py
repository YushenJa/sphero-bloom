#.\venv\Scripts\activate
import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
import spherov2.commands.sensor as sensor_mod

def ignore_collision_packet(listener, packet):
    pass

sensor_mod.__collision_detected_notify_helper = ignore_collision_packet

from core.robot import BloomBot
from assets import FRAMES
from scenes.evening import EveningRoutine

def show_gallery(bot):
    print("Galerie starten...")
    for frame_name in FRAMES.keys():
        bot.display_frame(frame_name)
    print("Galerie fertiggestellt.")

def main():
    print("Suche nach Sphero Bolt...")
    toy = scanner.find_toy()
    
    if not toy:
        print("Roboter nicht gefunden!")
        return

    print(f"Verbunden mit {toy.name}")
    
    with SpheroEduAPI(toy) as droid:
        bot = BloomBot(droid)
        
        evening_scene = EveningRoutine(bot)
        
        next_step = evening_scene.run()
        
        if next_step == "GO_TO_SLEEP":
            print("...")


if __name__ == "__main__":
    main()