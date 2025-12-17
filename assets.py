from spherov2.types import Color

# --- 1. FARBPALETTE ---
class Palette:
    OFF = Color(0, 0, 0)
    WHITE = Color(255, 255, 255)
    YELLOW = Color(255, 200, 0)
    STEM_GREEN = Color(0, 150, 0)
    PETAL_PINK = Color(255, 20, 147)
    ORANGE = Color(255, 50, 0)
    LOADING_BLUE = Color(0, 0, 255)
    BAD_RED = Color(255, 0, 0)

# --- 2. BILDERGALERIE ---
# Legende:
# . = Dunkelheit
# Y = Gelb (Sleepy)
# G = Grün (Stem)
# P = Rosa (Petal)
# O = Orange (Center)
# W = Weiß
# R = Rot
# B = Blue

FRAMES = {
    # Animation „Zzz“ (Schlaf)
    "ZZZ": [
        "........",
        "....YYYY",
        ".....Y..",
        "YYYY..Y.",
        ".Y..YYYY",
        "..Y.....",
        "YYYY....",
        "........",
    ],

    # Augen (Müdigkeit)
    "EYES_OPEN": [
        "........",
        "........",
        "........",
        "WWW..WWW",
        "W.W..W.W",
        "........",
        "........",
        "........",
    ],
    
    #Snooze
    "CLOCK": [
    "..WWWW..",
    ".W....W.",
    "W......W",
    "WBBB...W",
    "W...B..W",
    ".W...BW.",
    "..WWWW..",
    "........",
    ],

    # Geschlossene Augen (Schläft)
    "EYES_CLOSED": [
        "........",
        "........",
        "........",
        "WWW..WWW",
        "W.W..W.W",
        "........",
        "........",
        "........",
    ],

    # Blume Stufe 0: Keimling (Anfang des Zyklus)
    "FLOWER_BUD0": [
        "....G...",
        "....G...",
        "....G...",
        "...G.G..",
        "........",
        "........",
        "........",
        "........",
    ],

    "SUN": [
        "Y..YY..Y",
        ".Y.OO.Y.",
        "..OYYO..",
        "YOYYYYOY",
        "YOYYYYOY",
        "..OYYO..",
        ".Y.OO.Y.",
        "Y..YY..Y",
    ],

    # Blume Stufe 1: Keimling (Schlechter Schlaf)
    "FLOWER_BUD1": [
        "....G...",
        "....G...",
        "....G...",
        "...GGG..",
        "..G.G...",
        "........",
        "........",
        "........",
    ],

    # Blume Stufe 2: Halb geöffnet (Mittlerer Schlaf)
    "FLOWER_HALB": [
        "....G...",
        "....G...",
        "....G...",
        "...GGG..",
        "..G.G...",
        "...PPP..",
        "....P...",
        "........",
    ],


    # Blume Stufe 3: Vollblüte (Guter Schlaf)
    "FLOWER_FULL": [
        "....G...",
        "....G...",
        "....G...",
        "...GGG..",
        "..G.G...",
        "...PPP..",
        "..PPOPP.",
        "...PPP..",
    ],

    
    # Download-Symbol (Datensynchronisierung)
    "LOADING": [
        "........",
        "..B..B..",
        ".B....B.",
        ".B....B.",
        "..B..B..",
        "........",
        "........",
        "........",
    ]
}

def get_color_from_char(char):
    if char == 'Y': return Palette.YELLOW
    if char == 'W': return Palette.WHITE
    if char == 'G': return Palette.STEM_GREEN
    if char == 'P': return Palette.PETAL_PINK
    if char == 'O': return Palette.ORANGE
    if char == 'B': return Palette.LOADING_BLUE
    if char == 'R': return Palette.BAD_RED
    return Palette.OFF