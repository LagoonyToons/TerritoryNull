import pygame as pg
import sys
from options import *
from menu import *
pg.init()
pg.mixer.init()

#defined in options
#SCREEN_X, SCREEN_Y = (1200, 700)

pg.display.set_caption("Territory Null")
#screen = pg.display.set_mode((SCREEN_X, SCREEN_Y), pg.FULLSCREEN)
#pg.mouse.set_visible(False)
screen = pg.display.set_mode((SCREEN_X, SCREEN_Y))
# while True:
#     events = pg.event.get()
#     for event in events:
#         if event.type == pg.QUIT:
#             pg.quit()
#             sys.exit()
music = Start()
Menu(screen, music)
pg.quit()
sys.exit()