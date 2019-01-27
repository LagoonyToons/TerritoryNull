
import pygame as pg
from options import *
import random
class Asteroid(pg.sprite.Sprite):
    def __init__(self, size, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load("meteor.png"), (size, size))
        self.x, self.y = (x, y)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = random.randint(2, 6)
    def update(self, player):
        if self.y >= SCREEN_Y:
            self.kill()
        else:
            self.y += self.speed
            self.rect.y +=  self.speed
           # print(piece.position)
        if self.rect.colliderect(player.top_piece.rect) or self.rect.colliderect(player.bot_piece.rect) or self.rect.colliderect(player.mid_piece.rect):
            player.hp -= 1
            print(player.hp)
            self.kill()

class Fuel(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load('fuel.png'), (80, 80))
        self.x, self.y = (x, y)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = random.randint(3, 6)
    def update(self, player):
        if self.y >= SCREEN_Y:
            self.kill()
        else:
            self.y += self.speed
            self.rect.y = self.y
        if self.rect.colliderect(player.top_piece.rect) or self.rect.colliderect(player.bot_piece.rect) or self.rect.colliderect(player.mid_piece.rect):
            player.fuel += 500
            if player.fuel > player.maxFuel:
                player.fuel = player.maxFuel
            self.kill()