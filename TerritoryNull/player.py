import pygame as pg
from options import *
import sys

class Player():
    def __init__(self, playerList, soundEffects):
        self.hp = playerList[0][0] + playerList[1][0] + playerList[2][0]
        self.speed = self.storedSpeed = playerList[0][2] + playerList[1][2] + playerList[2][2]
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
        self.passive = playerList[5][1]
        self.abilityTimer2 = [0]
        self.timeStopTimer = 0
        self.shrinkTimer = 0
        if self.ability2 == "mine":
            self.mineCount = 2
        else:
            self.mineCount = 0
        self.exploding = False
        self.firing = False
        if self.ability2 == "exploding" or self.ability2 == "laserFire":
            self.explodyBar = 1200
        else:
            self.explodyBar = 0
        self.invincibilityFrames = 20
        self.invincibility = 0
        self.timeStopCounter = 0
        self.timeStopIncreaseToCooldown = 0
        self.energyRecoveryRate = 4

        self.abilityDelay = playerList[3][2]
        self.abilityDelay2 = playerList[4][2]

        self.soundEffects = soundEffects

        self.passiveStateMachine()


    def update(self, speedMultiplier):
        if self.explodyBar < 1200 and self.ability2 == "explosion":
            self.explodyBar += self.energyRecoveryRate*speedMultiplier
        if self.explodyBar < 1200 and self.ability2 == "laserFire":
            self.explodyBar += self.energyRecoveryRate*speedMultiplier
        if self.exploding == True and self.explodyBar > 0:
            self.explodyBar -= 11*speedMultiplier
        if self.firing == True and self.explodyBar > 0:
            self.explodyBar -= 11*speedMultiplier
            #print(self.explodyBar)
        if self.timeStopIncreaseToCooldown > 0:
            self.timeStopCounter -= 1*speedMultiplier
            if self.timeStopCounter <= 0:
                self.timeStopIncreaseToCooldown -= 5
                self.timeStopCounter = 40
        if self.invincibility > 0:
            self.invincibility -= 1*speedMultiplier
        elif not self.exploding:
            self.speed = self.storedSpeed
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
        if self.ability2 == "mine" and self.mineCount < 3 and self.abilityTimer2[0] <= 0:
            self.mineCount += 1
            self.abilityTimer2[0] = self.abilityDelay2
        return self.isDead()

    def isDead(self):
        if self.hp <= 0:
            return True
        return False
    def passiveStateMachine(self):
        if self.passive == "bHealth":
            self.hp += 3
        elif self.passive == "bSpeed":
            self.speed += 3
        elif self.passive == "bFuel":
            self.maxFuel += 2000
            self.fuel += 2000
        elif self.passive == "bIFrames":
            self.invincibilityFrames *= 2
        elif self.passive == "dACooldown":
            self.abilityDelay *= .8
            self.abilityDelay = round(self.abilityDelay)
        elif self.passive == "dGCooldown":
            if self.ability2 != "explosion":
                self.abilityDelay2 *= .875
                self.abilityDelay2 = round(self.abilityDelay2)
            self.energyRecoveryRate *= 1.25
        elif self.passive == "bScore":
            pass


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
        # elif ability == "explosion":
        #     self.explodeFire(abilityTimer, args[1])
        elif ability == "bullet":
            self.bulletFire(abilityTimer, args[1])
        elif ability == "shotgun":
            self.shotgunFire(abilityTimer, args[1], args[4])
        elif ability == "tracker":
            self.trackerFire(abilityTimer, args[1], args[2], args[3])
        elif ability == "mine":
            self.mineFire(abilityTimer, args[1])

    def heal(self, abilityTimer):
        if abilityTimer == 1:
            if self.fuel >= 1000 and self.abilityTimer[0] <= 0:
                self.fuel -= 1000
                self.abilityTimer[0] = self.abilityDelay
                self.hp += 1
        elif abilityTimer == 2:
            if self.fuel >= 1000 and self.abilityTimer2[0] <= 0:
                self.fuel -= 1000
                self.abilityTimer2[0] = self.abilityDelay2
                self.hp += 1

    def timeStop(self, abilityTimer):
        if abilityTimer == 1:
            if self.abilityTimer[0] <= 0:
                self.timeStopIncreaseToCooldown += 40
                self.abilityTimer[0] = self.abilityDelay+self.timeStopIncreaseToCooldown
                self.timeStopTimer = 60
                pg.mixer.Channel(5).play(self.soundEffects[0])

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
                self.invincibility = 140
                self.fuel += 500
                self.abilityTimer[0] = self.abilityDelay

    def deathBoost(self, abilityTimer, score):
        score[0] += 250000
        self.hp -= self.hp

    def laserFire(self, abilityTimer, bulletList):
        if abilityTimer == 1:
            if self.abilityTimer[0] <= 0:
                bulletList.append(
                    Laser(self.ability2Image, self.top_piece.x,
                          self.top_piece.y))
                self.abilityTimer[0] = self.abilityDelay
        elif abilityTimer == 2:
            if self.abilityTimer2[0] <= 0:
                bulletList.append(
                    Laser(self.ability2Image, self.top_piece.x,
                          self.top_piece.y))
                self.abilityTimer2[0] = self.abilityDelay2
    # def explodeFire(self, abilityTimer, bulletList):
    #     if abilityTimer == 2:
    #         if self.fuel >= 200 and self.abilityTimer2[0] <= 0:
    #             bulletList.append(
    #                 Explode(self.ability2Image, self.top_piece.x,
    #                       self.top_piece.y))
    #             self.fuel -= 100
    #             self.abilityTimer2[0] = self.abilityDelay2
    def bulletFire(self, abilityTimer, bulletList):
        if self.abilityTimer2[0] <= 0:
            bulletList.append(
                Bullet(self.ability2Image, self.top_piece.x, self.top_piece.y))
            self.abilityTimer2[0] = self.abilityDelay2
            self.abilityTimer[0] -= 6
            if self.abilityTimer[0] < 0:
                self.abilityTimer[0] = 0

    def mineFire(self, abilityTimer, bulletList):
        if self.mineCount > 0:
            bulletList.append(
                Mine(self.ability2Image, self.top_piece.x, self.top_piece.y))
            self.mineCount -= 1
            #self.abilityTimer2[0] = self.abilityDelay2

    def shotgunFire(self, abilityTimer, bulletList, bulletImages):
        speed = 10
        if self.abilityTimer2[0] <= 0:
            bulletList.append(
                Shotgun(bulletImages[3], self.top_piece.x, self.top_piece.y, round(-speed/2), speed))
            bulletList.append(
                Shotgun(bulletImages[0], self.top_piece.x, self.top_piece.y, 0, speed))
            bulletList.append(
                Shotgun(bulletImages[1], self.top_piece.x, self.top_piece.y, round(speed/2), speed))
            bulletList.append(
                Shotgun(bulletImages[2], self.top_piece.x, self.top_piece.y, round(speed/3), round(speed-2)))
            bulletList.append(
                Shotgun(bulletImages[4], self.top_piece.x, self.top_piece.y, round(-speed/3), round(speed-2)))
            self.abilityTimer2[0] = self.abilityDelay2

    def trackerFire(self, abilityTimer, bulletList, enemyList, difficulty):
        if self.abilityTimer2[0] <= 0:
            bulletList.append(
                Tracker(self.ability2Image, self.top_piece.x-70, self.top_piece.y-40, enemyList))
            bulletList.append(
                Tracker(self.ability2Image, self.top_piece.x, self.top_piece.y-40, enemyList))
            if self.passive == "dGCooldown":
                self.abilityTimer2[0] = round(self.abilityDelay2-(difficulty*(.8)*1.5))
            else:
                 self.abilityTimer2[0] = round(self.abilityDelay2-(difficulty*1.5))


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
        self.rect = pg.Rect(self.x - self.x_size / 2 + 24,
                                   self.y-500, self.x_size, 500)

    def update(self, player, bulletList, multiplier):
        self.x = player.x
        self.y = player.y
        self.rect = pg.Rect(self.x - self.x_size / 2 + 24,
                                   self.y-500, self.x_size, 500)
    def draw(self, screen):
        pg.draw.rect(screen, pg.Color("red"), self.rect)


class Explode:
    def __init__(self, image, x, y):
        self.name = "laser"
        self.x = x
        self.y = y
        self.y_size = 0
        self.x_size = 5
        #self.count = 120
        self.rect = pg.Rect(self.x+15, self.y-35, self.x_size,
                            self.y+80)

    def update(self, player, bulletList, multiplier):
        self.x = player.x+24
        self.y = player.y+60
        if self.x_size < 120:
            self.x_size += 8*multiplier
        #self.x_size += 4
        #self.count -= 1 * multiplier
        self.rect = pg.Rect(self.x-self.x_size, self.y-self.x_size, self.x_size*2, self.x_size*2)
        #if self.count <= 0:
            #bulletList.remove(self)
        # for enemy in enemies:
        #     if self.rect.colliderect(enemy.rect):
        #         enemies.remove(enemy)
        #         print("hello world")

    def draw(self, screen):
        #pg.draw.rect(screen, pg.Color("blue"), self.rect)
        pg.draw.circle(screen, pg.Color("red"), (round(self.x), round(self.y)), round(self.x_size), 5)
        pg.draw.circle(screen, pg.Color("lightBlue"), (round(self.x), round(self.y)), round(self.x_size-2))



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
        self.y -= round(13*multiplier)
        self.rect.y = self.y
        if self.rect.y <= -30:
            bulletList.remove(self)
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Tracker:
    def __init__(self, image, x, y, enemyList):
        self.name = "bullet"
        self.image = image
        self.x = x
        self.y = y
        #print(x, y)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 16
        self.target = [0,0]
        self.currentLowest = 9999
        for enemy in enemyList:
            self.xDifference = abs(enemy.rect.centerx-self.x)
            self.yDifference = abs(enemy.rect.centery - self.y)
            self.totalDifference = self.xDifference+self.yDifference
            if self.totalDifference < self.currentLowest and not enemy.tracked:
                self.currentLowest = self.totalDifference
                self.target = enemy.coordinates
                enemy.tracked = True
                try:
                    storedenemy.tracked = False
                except:
                    pass
                storedenemy = enemy
        self.lifeTime = 120

    def update(self, player, bulletList, multiplier):
        self.lifeTime -= 1
        if self.target:
            self.xDifference = self.x - self.target[0]
            self.yDifference = self.y - self.target[1]
            self.ratio = self.speed/(abs(self.xDifference) + abs(self.yDifference))
            self.xSpeed = round(self.xDifference*self.ratio)
            self.ySpeed = round(self.yDifference * self.ratio)
            #print(self.xSpeed, self.ySpeed)
            # print(self.target)
            # self.x = player.x
            self.y -= round(self.ySpeed*multiplier)
            self.rect.y = self.y
            self.x -= round(self.xSpeed * multiplier)
            self.rect.x = self.x
        if self.y <= 0 or self.y > SCREEN_Y or self.x <= 0 or self.x > SCREEN_X or self.lifeTime < 0:
            bulletList.remove(self)

    def draw(self, screen):
        #try:
        pg.draw.circle(screen, pg.Color("green"), (round(self.x), round(self.y)), round(self.rect.width/2))
        #pg.draw.circle(self.screen, pg.Color("white"), (round(SCREEN_X/3), SCREEN_Y - 80), 30, 1)
    #except:
    #print(self.x, self.y)


class Shotgun:
    def __init__(self, image, x, y, x_speed, y_speed):
        self.name = "shotgun"
        self.image = image
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.lifeSpan = 35

    def update(self, player, bulletList, multiplier):
        self.lifeSpan -= 1*multiplier
        # self.x = player.x
        self.y -= round(self.y_speed * multiplier)
        self.rect.y = self.y
        self.x -= round(self.x_speed * multiplier)
        self.rect.x = self.x
        if self.rect.y <= 0 or self.rect.x <= 0 or self.rect.x >= SCREEN_X or self.rect.y >= SCREEN_Y or self.lifeSpan <= 0:
            bulletList.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


class Mine:
    def __init__(self, image, x, y):
        self.name = "mine"
        self.exploding = False
        self.image = image
        self.x = x
        self.y = y
        self.yVel = 14
        self.yVelDecayRate = .5
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timeTillBoom = 200
        self.x_size = 5
        self.boomTime = 26

    def update(self, player, bulletList, multiplier):
        if self.yVel > 0:
            self.y -= self.yVel
            self.yVel -= self.yVelDecayRate
            self.rect = pg.Rect(self.x-self.x_size, self.y -
                                self.x_size, self.x_size*2, self.x_size*2)
        if self.timeTillBoom > 0:
            self.timeTillBoom -= 1
            if self.timeTillBoom <= 0:
                self.exploding = True
                self.name = "laser"
        else:
            # print("bol")
            self.rect = pg.Rect(self.x-self.x_size, self.y -
                                self.x_size, self.x_size*2, self.x_size*2)
            self.boomTime -= 1
            self.x_size += 4
        # self.x = player.x
       # self.y -= round(5 * multiplier)
        #self.rect.y = self.y
        if self.boomTime < 0:
            bulletList.remove(self)

    def draw(self, screen):
        if not self.exploding:
            screen.blit(self.image, (self.x, self.y))
        else:
            pg.draw.circle(screen, pg.Color("red"), (round(
                self.x), round(self.y)), round(self.x_size-2))
