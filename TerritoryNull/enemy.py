import pygame as pg
from options import *
import random


class Asteroid():
    def __init__(self, x, y, image):
        self.type = "enemy"
        self.tracked = False
        self.image = image
        self.coordinates = [x, y]
        self.rect = self.image.get_rect()
        self.rect.x = self.coordinates[0]
        self.rect.y = self.coordinates[1]
        self.speed = random.randint(3, 8)
    def update(self, player, enemies, speedMultiplier, bulletList, score):
        if self.coordinates[1] >= SCREEN_Y:
            enemies.remove(self)
        else:
            self.coordinates[1] += self.speed*speedMultiplier
            self.rect.y = self.coordinates[1]
        # print(piece.position)
        if self.rect.colliderect(player.top_piece.rect) or self.rect.colliderect(player.bot_piece.rect) or self.rect.colliderect(player.mid_piece.rect):
            if player.invincibility <= 0:
                player.hp -= 1
                player.invincibility = player.invincibilityFrames
                if player.passive == "bIFrames":
                    player.speed += 4
            #print(player.hp)
            enemies.remove(self)
        for bullet in bulletList:
            if self.rect.colliderect(bullet.rect):
                if bullet.name == "laser":
                    try:
                        enemies.remove(self)
                    except:
                        pass
                elif bullet.name == "mine":
                    bullet.timeTillBoom = 1
                else:
                    try:
                        enemies.remove(self)
                    except:
                        pass
                    try:
                        bulletList.remove(bullet)
                    except:
                        pass
                score[0] += 500

    def draw(self, screen):
        screen.blit(self.image, (self.coordinates[0], self.coordinates[1]))


class Fuel():
    def __init__(self, x, y, image):
        self.type = "upgrade"
        self.image = image
        self.tracked = False
        self.coordinates = [x, y]
        self.rect = self.image.get_rect()
        self.rect.x = self.coordinates[0]
        self.rect.y = self.coordinates[1]
        self.speed = random.randint(3, 6)

    def update(self, player, enemies, speedMultiplier, bulletList, score):
        for bullet in bulletList:
            if self.rect.colliderect(bullet.rect):
                if bullet.name == "bullet" or bullet.name == "shotgun":
                    try:
                        player.fuel += 500
                        if player.fuel > player.maxFuel:
                            player.fuel = player.maxFuel
                        bulletList.remove(bullet)
                        enemies.remove(self)
                    except:
                        pass
        if self.coordinates[1] >= SCREEN_Y:
            enemies.remove(self)
        else:
            self.coordinates[1] += self.speed*speedMultiplier
            self.rect.y = self.coordinates[1]
        if self.rect.colliderect(player.top_piece.rect) or self.rect.colliderect(player.bot_piece.rect) or self.rect.colliderect(player.mid_piece.rect):
            player.fuel += 500
            if player.fuel > player.maxFuel:
                player.fuel = player.maxFuel
            try:
                enemies.remove(self)
            except:
                pass

    def draw(self, screen):
        screen.blit(self.image, (self.coordinates[0], self.coordinates[1]))

class Heal():
    def __init__(self, x, y, image):
        self.type = "upgrade"
        self.tracked = False
        self.image = image
        self.coordinates = [x, y]
        self.rect = self.image.get_rect()
        self.rect.x = self.coordinates[0]
        self.rect.y = self.coordinates[1]
        self.speed = random.randint(4, 8)

    def update(self, player, enemies, speedMultiplier, bulletList, score):
        for bullet in bulletList:
            if self.rect.colliderect(bullet.rect):
                if bullet.name == "bullet" or bullet.name == "shotgun":
                    try:
                        player.hp += 1
                        bulletList.remove(bullet)
                        enemies.remove(self)
                    except:
                        pass
        if self.coordinates[1] >= SCREEN_Y:
            enemies.remove(self)
        else:
            self.coordinates[1] += self.speed * speedMultiplier
            self.rect.y = self.coordinates[1]
        if self.rect.colliderect(player.top_piece.rect) or self.rect.colliderect(player.bot_piece.rect) or self.rect.colliderect(player.mid_piece.rect):
            player.hp += 1
            try:
                enemies.remove(self)
            except:
                pass

    def draw(self, screen):
        screen.blit(self.image, (self.coordinates[0], self.coordinates[1]))


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
            if enemy.type != "boss" and enemy.type != "bullet":
                enemy.coordinates[0] += self.pull
                enemy.rect.x = enemy.coordinates[0]
                enemy.coordinates[1] -= 2
                enemy.rect.y = enemy.coordinates[1]
                if enemy.coordinates[0] <= 0:
                    enemy.coordinates[0] = SCREEN_X -100
                    enemy.rect.x = enemy.coordinates[0]
                if enemy.coordinates[0] >= SCREEN_X-50:
                    enemy.coordinates[0] = 50
                    enemy.rect.x = enemy.coordinates[0]
        if player.top_piece.x + self.pull*2 + 80 <= SCREEN_X and player.top_piece.x + self.pull*2 >= 0:
            player.top_piece.x += self.pull*2/3
            player.bot_piece.x += self.pull*2/3
            player.mid_piece.x += self.pull*2/3

            player.top_piece.rect.x = player.top_piece.x
            player.bot_piece.rect.x = player.bot_piece.x
            player.mid_piece.rect.x = player.mid_piece.x
        if self.rect.colliderect(player.top_piece.rect) or self.rect.colliderect(player.bot_piece.rect) or self.rect.colliderect(player.mid_piece.rect):
            if self.invulnerableFrames >= 60:
                if player.invincibility <= 0:
                    player.hp -= 1
                    player.invincibility = player.invincibilityFrames
                    if player.passive == "bIFrames":
                        player.speed += 4
                self.kill()


class Boss():
    def __init__(self, x, y, image, hurtImage, hp):
        self.type = "boss"
        self.tracked = False
        self.image = image
        self.injuredImage = hurtImage
        # self.injuredImage = image.convert(24)
        # self.injuredImage.set_alpha(128)
        self.coordinates = [x, y]
        self.rect = self.image.get_rect()
        self.rect.x = self.coordinates[0]
        self.rect.y = self.coordinates[1]
        self.speed = 3
        self.hp = hp
        self.invincibility = 0
        self.fireCounter = 30

    def update(self, player, enemies, speedMultiplier, bulletList, score):
        if self.fireCounter > 0:
            self.fireCounter -= 1
        if self.invincibility > 0:
            self.invincibility -= 1
        if self.hp <= 0:
            enemies.remove(self)
        if self.coordinates[1] < 150:
            self.coordinates[1] += self.speed*speedMultiplier
            self.rect.y = self.coordinates[1]
        self.coordinates[0] = 500
        if self.fireCounter == 0:
            self.fire(enemies)

        # print(piece.position)
        if self.rect.colliderect(player.top_piece.rect) or self.rect.colliderect(player.bot_piece.rect) or self.rect.colliderect(player.mid_piece.rect):
            if self.invincibility == 0:
                if player.invincibility <= 0:
                    player.hp -= 1
                    player.invincibility = player.invincibilityFrames
                    if player.passive == "bIFrames":
                        player.speed += 4
                self.hp -= 1
                self.invincibility = 25
                score[0] += 500
        for bullet in bulletList:
            if self.rect.colliderect(bullet.rect):
                if bullet.name == "laser":
                    try:
                        if self.invincibility == 0:
                            self.hp -= 1
                            score[0] += 500
                            self.invincibility = 25
                    except:
                        pass
                elif bullet.name == "mine":
                    bullet.timeTillBoom = 1

                elif bullet.name == "shotgun":
                    try:
                        if self.invincibility == 0:
                            self.hp -= 1
                            score[0] += 500
                    except:
                        pass
                    try:
                        bulletList.remove(bullet)
                    except:
                        pass
                else:
                    try:
                        if self.invincibility == 0:
                            self.hp -= 1
                            score[0] += 500
                            self.invincibility = 25
                            self.tracked = False
                    except:
                        pass
                    try:
                        bulletList.remove(bullet)
                    except:
                        pass
    def fire(self, enemyList):
        bullet = bossBullet(self.coordinates[0]+100, self.coordinates[1]+100, -3, 2)
        enemyList.append(bullet)
        bullet = bossBullet(self.coordinates[0]+100, self.coordinates[1]+100, 0, 3)
        enemyList.append(bullet)
        bullet = bossBullet(self.coordinates[0]+100, self.coordinates[1]+100, 3, 2)
        enemyList.append(bullet)
        self.fireCounter = 60
    def draw(self, screen):
        if self.invincibility == 0:
            screen.blit(self.image, (self.coordinates[0], self.coordinates[1]))
        else:
            screen.blit(self.injuredImage, (self.coordinates[0], self.coordinates[1]))


class BossShooter():
    def __init__(self, x, y, image, hurtImage, hp):
        self.type = "boss"
        self.tracked = False
        self.image = image
        self.injuredImage = hurtImage
        self.coordinates = [x, y]
        self.rect = self.image.get_rect()
        self.rect.x = self.coordinates[0]
        self.rect.y = self.coordinates[1]
        self.speed = 5
        self.x_speed = self.speed
        self.hp = hp
        self.invincibility = 0
        self.fireCounter = 80
        self.bulletSpeed = 13

    def update(self, player, enemies, speedMultiplier, bulletList, score):
        self.coordinates[0] += self.x_speed*speedMultiplier
        self.rect.x = self.coordinates[0]
        #print(self.coordinates[0])
        if self.coordinates[0] > SCREEN_X-self.rect.width or self.coordinates[0] < 0:
            self.x_speed *= -1
        if self.fireCounter > 0:
            self.fireCounter -= 1
        if self.invincibility > 0:
            self.invincibility -= 1
        if self.hp <= 0:
            enemies.remove(self)
        if self.coordinates[1] < 0:
            self.coordinates[1] += self.speed*speedMultiplier
            self.rect.y = self.coordinates[1]
        #self.coordinates[0] = 500
        if self.fireCounter == 0:
            self.fire(enemies, player)

        # print(piece.position)
        if self.rect.colliderect(player.top_piece.rect) or self.rect.colliderect(player.bot_piece.rect) or self.rect.colliderect(player.mid_piece.rect):
            if self.invincibility == 0:
                if player.invincibility <= 0:
                    player.hp -= 1
                    player.invincibility = player.invincibilityFrames
                    if player.passive == "bIFrames":
                        player.speed += 4
                self.hp -= 1
                self.invincibility = 25
                score[0] += 1200
        for bullet in bulletList:
            if self.rect.colliderect(bullet.rect):
                if bullet.name == "laser":
                    try:
                        if self.invincibility == 0:
                            self.hp -= 1
                            score[0] += 1200
                            self.invincibility = 25
                    except:
                        pass
                elif bullet.name == "mine":
                    bullet.timeTillBoom = 1
                elif bullet.name == "shotgun":
                    try:
                        if self.invincibility == 0:
                            self.hp -= 1
                            score[0] += 500
                    except:
                        pass
                    try:
                        bulletList.remove(bullet)
                    except:
                        pass
                else:
                    try:
                        if self.invincibility == 0:
                            self.hp -= 1
                            score[0] += 1200
                            self.invincibility = 25
                            self.tracked = False
                    except:
                        pass
                    try:
                        bulletList.remove(bullet)
                    except:
                        pass

    def fire(self, enemyList, player):
        self.xDifference = self.coordinates[0]+100 - player.top_piece.x
        self.yDifference = self.coordinates[1]+100 - player.top_piece.y
        self.ratio = self.bulletSpeed/(abs(self.xDifference) + abs(self.yDifference))
        self.xSpeed = self.xDifference*self.ratio
        self.ySpeed = self.yDifference * self.ratio
        bullet = bossBullet(
            self.coordinates[0]+100, self.coordinates[1]+100, -self.xSpeed, -self.ySpeed, 4)
        enemyList.append(bullet)
        self.fireCounter = 30

    def draw(self, screen):
        if self.invincibility == 0:
            screen.blit(self.image, (self.coordinates[0], self.coordinates[1]))
        else:
            screen.blit(self.injuredImage,
                        (self.coordinates[0], self.coordinates[1]))

class bossBullet:
    def __init__(self, x, y, dx, dy, size = 8):
        self.type = "bullet"
        self.tracked = False
        self.x = x
        self.y = y
        self.coordinates = [-1000, -1000]
        #print(x, y)
        self.size = size
        self.dx = dx
        self.dy = dy
        self.rect = pg.rect.Rect(x, y, self.size, self.size)

    def update(self, player, enemies, speedMultiplier, bulletList, score):
        self.rect = pg.rect.Rect(round(self.x), round(self.y), self.size, self.size)
        if self.y >= SCREEN_Y or self.x >= SCREEN_X or self.x <= 0:
            enemies.remove(self)
        else:
            self.x += self.dx
            self.y += self.dy
        if self.rect.colliderect(player.top_piece.rect) or self.rect.colliderect(player.bot_piece.rect) or self.rect.colliderect(player.mid_piece.rect):
            if player.invincibility <= 0:
                player.hp -= 1
                player.invincibility = player.invincibilityFrames
                if player.passive == "bIFrames":
                    player.speed += 4
            #print(player.hp)
            enemies.remove(self)
        for bullet in bulletList:
            if self.rect.colliderect(bullet.rect):
                if bullet.name == "laser":
                    try:
                        enemies.remove(self)
                    except:
                        pass
                elif bullet.name == "mine":
                    bullet.timeTillBoom = 1
                else:
                    try:
                        enemies.remove(self)
                    except:
                        pass
                    try:
                        bulletList.remove(bullet)
                    except:
                        pass
    def draw(self, screen):
        pg.draw.circle(screen, pg.Color("red"), (round(self.x), round(self.y)), self.size)
