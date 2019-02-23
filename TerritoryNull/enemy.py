import pygame as pg
from options import *
import random


class Asteroid():
    def __init__(self, x, y, image):
        self.image = image
        self.x, self.y = (x, y)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = random.randint(3, 8)
    def update(self, player, enemies, speedMultiplier, bulletList):
        if self.y >= SCREEN_Y:
            enemies.remove(self)
        else:
            self.y += self.speed*speedMultiplier
            self.rect.y = self.y
        # print(piece.position)
        if self.rect.colliderect(player.top_piece.rect) or self.rect.colliderect(player.bot_piece.rect) or self.rect.colliderect(player.mid_piece.rect):
            player.hp -= 1
            print(player.hp)
            enemies.remove(self)
        for bullet in bulletList:
            if self.rect.colliderect(bullet.rect):
                if bullet.name == "laser":
                    try:
                        enemies.remove(self)
                    except:
                        pass
                else:
                    try:
                        enemies.remove(self)
                    except:
                        pass
                    try:
                        bulletList.remove(bullet)
                    except:
                        pass


class Fuel():
    def __init__(self, x, y, image):
        self.image = image
        self.x, self.y = (x, y)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = random.randint(3, 6)

    def update(self, player, enemies, speedMultiplier, bulletList):
        if self.y >= SCREEN_Y:
            enemies.remove(self)
        else:
            self.y += self.speed*speedMultiplier
            self.rect.y = self.y
        if self.rect.colliderect(player.top_piece.rect) or self.rect.colliderect(player.bot_piece.rect) or self.rect.colliderect(player.mid_piece.rect):
            player.fuel += 500
            if player.fuel > player.maxFuel:
                player.fuel = player.maxFuel
            enemies.remove(self)

class Heal():
    def __init__(self, x, y, image):
        self.image = image
        self.x, self.y = (x, y)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = random.randint(4, 8)

    def update(self, player, enemies, speedMultiplier, bulletList):
        if self.y >= SCREEN_Y:
            enemies.remove(self)
        else:
            self.y += self.speed*speedMultiplier
            self.rect.y = self.y
        if self.rect.colliderect(player.top_piece.rect) or self.rect.colliderect(player.bot_piece.rect) or self.rect.colliderect(player.mid_piece.rect):
            player.hp += 1
            enemies.remove(self)


class GravityField(pg.sprite.Sprite):
    def __init__(self):
        self.size = 80
        self.size2 = 200
        pg.sprite.Sprite.__init__(self)
        self.imageCenter = pg.transform.scale(pg.image.load('image/gravitycenter.png'), (self.size, self.size))
        self.imageSurround = pg.transform.scale(pg.image.load('image/gravityfield.png'), (self.size2, self.size2))
        self.side = random.randint(0,1)
        if self.side == 0:
            self.x, self.y = (random.randint(0, 150), random.randint(200, SCREEN_Y-250))
            self.pull = -3
        elif self.side == 1:
            self.x, self.y = (random.randint(SCREEN_X-190,SCREEN_X-40), random.randint(200, SCREEN_Y-250))
            self.pull = 3
        self.x2 = self.x - (self.size2-self.size)/2
        self.y2 = self.y - (self.size2-self.size)/2
        self.rect = self.imageCenter.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.lifeCount = 0
        self.invulnerableFrames = 0

    def update(self, enemies, player):
        self.lifeCount += 1
        self.invulnerableFrames += 1
        if self.lifeCount >= 360:
            self.kill()
        for enemy in enemies:
            enemy.x += self.pull
            enemy.rect.x = enemy.x
            enemy.y -= 2
            enemy.rect.y = enemy.y
            if enemy.x <= 0:
                enemy.x = SCREEN_X -100
                enemy.rect.x = enemy.x
            if enemy.x >= SCREEN_X-50:
                enemy.x = 50
                enemy.rect.x = enemy.x
        if player.top_piece.x + self.pull*2 + 80 <= SCREEN_X and player.top_piece.x + self.pull*2 >= 0:
            player.top_piece.x += self.pull*2/3
            player.bot_piece.x += self.pull*2/3
            player.mid_piece.x += self.pull*2/3

            player.top_piece.rect.x = player.top_piece.x
            player.bot_piece.rect.x = player.bot_piece.x
            player.mid_piece.rect.x = player.mid_piece.x
        if self.rect.colliderect(player.top_piece.rect) or self.rect.colliderect(player.bot_piece.rect) or self.rect.colliderect(player.mid_piece.rect):
            if self.invulnerableFrames >= 60:
                player.hp -= 1
                self.kill()
