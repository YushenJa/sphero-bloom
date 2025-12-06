import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI

from core.robot import BloomBot
from assets import FRAMES 

def show_gallery(bot):
    print("Galerie starten...")
    for frame_name in FRAMES.keys():
        print(f"📺 Показываю: {frame_name}")
        bot.display_frame(frame_name)
    print("Galerie fertiggestellt.")

def main():
    print("📡 Suche nach Sphero Bolt...")
    toy = scanner.find_toy()
    
    if not toy:
        print("Roboter nicht gefunden!")
        return

    print(f"Verbunden mit {toy.name}")
    
    with SpheroEduAPI(toy) as droid:
        bot = BloomBot(droid)
        
        show_gallery(bot)

if __name__ == "__main__":
    main()