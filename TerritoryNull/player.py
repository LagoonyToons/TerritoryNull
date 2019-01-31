import pygame as pg
from options import *
import sys

class Player():
    def __init__(self, playerList):
        self.hp = playerList[0][0] + playerList[1][0] + playerList[2][0]
        self.speed = playerList[0][2] + playerList[1][2] + playerList[2][2]
        self.maxFuel = self.fuel = playerList[0][1] + playerList[1][1] + playerList[2][1]
        self.topw, self.toph = (48, 48)
        self.midw, self.midh = (48, 48)
        self.botw, self.both = (36, 24)
        self.midx, self.midy = (SCREEN_X/2, SCREEN_Y/2+self.toph)
        self.botx, self.boty = (SCREEN_X/2+8, SCREEN_Y/2+self.midh+self.toph)
        self.top_piece = rocketPiece(playerList[0][3],0, SCREEN_X/2, SCREEN_Y/2, self.topw, self.toph)
        self.mid_piece = rocketPiece(playerList[1][3], 1, self.midx, self.midy, self.midw, self.midh, self.toph, self.midh)
        self.bot_piece = rocketPiece(playerList[2][3], 2, self.botx, self.boty, self.botw, self.both, self.toph, self.midh)
        self.pieceList = [self.top_piece, self.mid_piece, self.bot_piece]
    def update(self):
        if self.hp <= 0:
            dead = True
            return dead
        else:
            dead = False
            return dead

class rocketPiece(pg.sprite.Sprite):
    def __init__(self, image, position, x, y, sizex, sizey, *args):
        pg.sprite.Sprite.__init__(self)
        self.position = position
        self.rotation = 0
        self.image = pg.transform.scale(image, (sizex, sizey))
        self.sizex = sizex
        self.sizey = sizey
        self.x, self.y = (x, y)
        self.image1 = pg.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        try:
            self.tops = args[0]
            self.mids = args[1]
        except:
            pass

        if self.position == 0:
            self.offset = [0, 48+24]
        elif self.position == 1:
            self.offset = [48, 24]
        elif self.position == 2:
            self.offset = [48*2, 0]

    def update(self, x, y, *args):
        # if x < 1 and self.rotation <= 45 and x != 0:
        #     self.rotation += 2
        # elif x > 1 and self.rotation >= -45 and x != 0:
        #     self.rotation -= 2
        # elif x == 0:
        #     self.rotation *= .9
        # if self.position == "middle" and x > 0:
        #     self.x = args[0]+(self.rotation * .6)
        #     self.y = args[1]+(self.rotation * .4) + self.tops
        # elif self.position == "middle" and self.x < 0:
        #     self.x = args[0]+(self.rotation * .6)
        #     self.y = args[1]+(self.rotation * .4) + self.tops
        # elif self.position == "bottom" and self.x > 0:
        #     self.x = args[0]+(self.rotation * .3)
        #     self.y = args[1]+(self.rotation * .3) +(self.tops+self.mids)
        # elif self.position == "bottom" and self.x < 0:
        #     self.x = args[0]+(self.rotation * .3)
        #     self.y = args[1]+(self.rotation * .3) +(self.tops+self.mids)
           # print(self.rotation)
        self.x += x
        self.rect.x = self.x
        self.y += y
        self.rect.y = self.y 
        if self.x > SCREEN_X-self.sizex or self.x < 0 or self.y > SCREEN_Y-self.sizey-self.offset[1] or self.y < 0+self.offset[0]:
            self.x -= x
            self.rect.x = self.x
            self.y -= y
            self.rect.y = self.y 
        #self.image1 = pg.transform.rotate(self.image, self.rotation)