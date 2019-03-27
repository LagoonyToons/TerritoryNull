import pygame as pg
import sys
from options import *
from menu import *
from LED import *
pg.init()
pg.mixer.init(channels=5)

joystick = pg.joystick.Joystick(0)
joystick.init()

#rangeList = [0,56, 60,70, 75,85, 90,93, 100 ,103]
rangeList = [0,52, 0,0, 0,0, 0,0, 0,0]
strip = Led(rangeList, LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
strip.begin()
strip.state = "default"
strip.update((0,0,0))

#defined in options
# SCREEN_X, SCREEN_Y = (700, 1200)

pg.display.set_caption("Territory Null")
screen = pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.FULLSCREEN)

#screen = pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.FULLSCREEN)
pg.mouse.set_visible(False)
#screen = pg.display.set_mode((SCREEN_X, SCREEN_Y))
# while True:
#     events = pg.event.get()
#     for event in events:
#         if event.type == pg.QUIT:
#             pg.quit()
#             sys.exit()
music = Start()
Menu(screen, music, strip, joystick)
pg.quit()
exit()
#sys.exit()
