#.\venv\Scripts\activate
import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
import spherov2.commands.sensor as sensor_mod
from controller.controller import RoutineController


def ignore_collision_packet(listener, packet):
    pass

sensor_mod.__collision_detected_notify_helper = ignore_collision_packet

from core.robot import BloomBot
from assets import FRAMES

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
        
        controller = RoutineController(bot)
        controller.start_morning()   # or start_morning()

if __name__ == "__main__":
    main()