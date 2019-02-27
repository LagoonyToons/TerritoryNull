import pygame as pg
from options import *
import sys

class Player():
    def __init__(self, playerList, soundEffects):
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

        self.ability = playerList[3][1]
        self.abilityTimer = [0]
        self.abilityImage = playerList[3][0]
        self.ability2Image = pg.transform.scale(playerList[4][0], (20, 20))
        self.ability2 = playerList[4][1]
        self.abilityTimer2 = [0]
        self.timeStopTimer = 0
        self.shrinkTimer = 0

        self.abilityDelay = playerList[3][2]
        self.abilityDelay2 = playerList[4][2]

        self.soundEffects = soundEffects

    def update(self, speedMultiplier):
        if self.shrinkTimer > 0:
            self.shrinkTimer -= 1*speedMultiplier
            if self.shrinkTimer <= 0:
                for x in self.pieceList:
                    x.image = x.imageFull
                    x.rect = x.fullRect
                    x.offset[1] *= .5
        if self.abilityTimer[0] > 0:
            self.abilityTimer[0] -= 1*speedMultiplier
        if self.abilityTimer2[0] > 0:
            self.abilityTimer2[0] -= 1*speedMultiplier
        return self.isDead()

    def isDead(self):
        if self.hp <= 0:
            return True
        return False

    def abilityStateMachine(self, ability, abilityTimer, *args):
        if ability == "heal":
            self.heal(abilityTimer)
        elif ability == "timeStop":
            self.timeStop(abilityTimer)
        elif ability == "shrink":
            self.shrink(abilityTimer)
        elif ability == "transfusion":
            self.transfusion(abilityTimer)
        elif ability == "deathBoost":
            self.deathBoost(abilityTimer, args[0])
        elif ability == "laserFire":
            self.laserFire(abilityTimer, args[1])
        elif ability == "bullet":
            self.bulletFire(abilityTimer, args[1])

    def heal(self, abilityTimer):
        if abilityTimer == 1:
            if self.fuel >= 300 and self.abilityTimer[0] <= 0:
                self.fuel -= 200
                self.abilityTimer[0] = self.abilityDelay
                self.hp += 1
        elif abilityTimer == 2:
            if self.fuel >= 300 and self.abilityTimer2[0] <= 0:
                self.fuel -= 200
                self.abilityTimer2[0] = self.abilityDelay2
                self.hp += 1

    def timeStop(self, abilityTimer):
        if abilityTimer == 1:
            if self.fuel >= 500 and self.abilityTimer[0] <= 0:
                self.fuel -= 500
                self.abilityTimer[0] = self.abilityDelay
                self.timeStopTimer = 120
                pg.mixer.Channel(5).play(self.soundEffects[0])
        elif abilityTimer == 2:
            if self.fuel >= 500 and self.abilityTimer2[0] <= 0:
                self.fuel -= 500
                self.abilityTimer2[0] = self.abilityDelay2
                self.timeStopTimer = 120

    def shrink(self, abilityTimer):
        if abilityTimer == 1:
            if self.abilityTimer[0] <= 0:
                self.abilityTimer[0] = self.abilityDelay
                self.shrinkTimer = 270
                for x in self.pieceList:
                    x.image = x.imageHalf
                    x.rect = x.rectHalf
                    if x.position == 1:
                        x.y -= 24
                    elif x.position == 2:
                        x.y -= 48

        elif abilityTimer == 2:
            if self.abilityTimer2[0] <= 0:
                self.abilityTimer2[0] = self.abilityDelay2
                self.shrinkTimer = 270
                for x in self.pieceList:
                    x.image = x.imageHalf
                    x.rect = x.rectHalf
                    if x.position == 1:
                        x.y -= 24
                    elif x.position == 2:
                        x.y -= 48

    def transfusion(self, abilityTimer):
        if abilityTimer == 1:
            if self.hp > 1 and self.abilityTimer[0] <= 0:
                self.fuel += 500
                self.abilityTimer[0] = self.abilityDelay
                self.hp -= 1
        elif abilityTimer == 2:
            if self.hp > 1 and self.abilityTimer2[0] <= 0:
                self.fuel += 500
                self.abilityTimer2[0] = self.abilityDelay2
                self.hp -= 1

    def deathBoost(self, abilityTimer, score):
        score[0] += 50000
        self.hp -= self.hp

    def laserFire(self, abilityTimer, bulletList):
        if abilityTimer == 1:
            if self.fuel >= 200 and self.abilityTimer[0] <= 0:
                bulletList.append(
                    Laser(self.ability2Image, self.top_piece.x,
                          self.top_piece.y))
                self.abilityTimer[0] = self.abilityDelay
        elif abilityTimer == 2:
            if self.fuel >= 200 and self.abilityTimer2[0] <= 0:
                bulletList.append(
                    Laser(self.ability2Image, self.top_piece.x,
                          self.top_piece.y))
                self.abilityTimer2[0] = self.abilityDelay2

    def bulletFire(self, abilityTimer, bulletList):
        if self.fuel >= 200 and self.abilityTimer2[0] <= 0:
            bulletList.append(
                Bullet(self.ability2Image, self.top_piece.x, self.top_piece.y))
            self.abilityTimer2[0] = self.abilityDelay2



class rocketPiece(pg.sprite.Sprite):
    def __init__(self, image, position, x, y, sizex, sizey, *args):
        pg.sprite.Sprite.__init__(self)
        self.position = position
        self.rotation = 0
        self.image = self.imageFull = pg.transform.scale(image, (sizex, sizey))
        self.sizex = sizex
        self.sizey = sizey
        self.imageHalf = pg.transform.scale(image, (round(sizex/2), round(sizey/2)))
        self.x, self.y = (x, y)
        # self.image1 = pg.transform.rotate(self.image, self.rotation)
        self.rect = self.fullRect = self.image.get_rect()
        self.rectHalf = self.imageHalf.get_rect()
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

class Laser:
    def __init__(self, image, x, y):
        self.name = "laser"
        self.x = x
        self.y = y
        self.y_size = 0
        self.x_size = 5
        self.count = 80
        self.rect = pg.Rect(self.x - self.x_size / 2 + 24,
                                   0, self.x_size, self.y)

    def update(self, player, bulletList, multiplier):
        self.x = player.x
        self.y = player.y
        #self.x_size += 4
        self.count -= 1*multiplier
        self.rect = pg.Rect(self.x-self.x_size/2 + 24, 0, self.x_size, self.y)
        if self.count <= 0:
            bulletList.remove(self)
        # for enemy in enemies:
        #     if self.rect.colliderect(enemy.rect):
        #         enemies.remove(enemy)
        #         print("hello world")

    def draw(self, screen):
        pg.draw.rect(screen, pg.Color("red"), self.rect)


class Bullet:
    def __init__(self,image, x, y):
        self.name = "bullet"
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, player, bulletList, multiplier):
        # self.x = player.x
        self.y -= round(5*multiplier)
        self.rect.y = self.y
        if self.rect.y <= -30:
            bulletList.remove(self)
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))