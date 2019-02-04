import pygame as pg
from options import *
from player import *
from enemy import *
import random
import sys

class Game:
    def __init__(self, screen, music, playerStats):
        self.clock = pg.time.Clock()
        self.player = Player(playerStats)
        self.screen = screen
        self.highScore = 0
        self.music = music

        self.all_sprites = pg.sprite.Group()
        self.player_pieces = pg.sprite.Group()
        self.enemies = []
        self.grav = pg.sprite.Group()

        self.load_images()

        self.dead = False

        for piece in self.player.pieceList:
            self.all_sprites.add(piece)
            self.player_pieces.add(piece)

        self.loopCount = 0
        self.fuelBlit = self.player.fuel

        self.gameloop()

    def gameloop(self):
        self.counter = 0
        while not self.dead:
            self.music.songState()
            self.controls()
            if self.player.timeStopTimer > 0:
                self.player.timeStopTimer -= 1
            else:
                self.enemySpawn()
                for enemy in self.enemies:
                    enemy.update(self.player, self.enemies)
                for gravObj in self.grav:
                    gravObj.update(self.enemies, self.player)
            self.highScore += 11
            self.dead = self.player.update()
            self.screenManagement()
        return self.highScore

    def enemySpawn(self):
        self.counter += 1
        if self.counter >= 30:
            self.counter = 0
            randomSize = random.randint(1, 5)
            x = random.randint(0, SCREEN_X-100)
            randomEnemyChoice = random.randint(0,200)
            if randomEnemyChoice <= 150:
                if randomSize == 1:
                    enemy = Asteroid(x, 0, self.asteroids1)
                elif randomSize == 2:
                    enemy = Asteroid(x, 0, self.asteroids2)
                elif randomSize == 3:
                    enemy = Asteroid(x, 0, self.asteroids3)
                elif randomSize == 4:
                    enemy = Asteroid(x, 0, self.asteroids4)
                elif randomSize == 5:
                    enemy = Asteroid(x, 0, self.asteroids5)
                self.enemies.append(enemy)
            elif randomEnemyChoice <= 170:
                if len(self.grav) == 0:
                    gravObj = GravityField()
                    self.grav.add(gravObj)
            elif randomEnemyChoice <= 171:
                enemy = Heal(x, 0, self.healImg)
                self.enemies.append(enemy)
            else:
                enemy = Fuel(x, 0, self.fuelImg)
                self.enemies.append(enemy)

    def controls(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.music.switchSong()
                if event.key == pg.K_SPACE:
                    self.player.abilityStateMachine(self.player.ability, 1)
                if event.key == pg.K_e:
                    self.player.abilityStateMachine(self.player.ability2, 2)
                if event.key == pg.K_q:
                    self.music.volumeToggle()
        pressed = pg.key.get_pressed()
        if pressed[pg.K_LEFT] and self.player.fuel > 0:
            self.player.mid_piece.update(-self.player.speed, 0, self.player.top_piece.x, self.player.top_piece.y)
            self.player.bot_piece.update(-self.player.speed, 0, self.player.top_piece.x, self.player.top_piece.y)
            self.player.top_piece.update(-self.player.speed, 0)
            self.player.fuel -= 2
        elif pressed[pg.K_RIGHT] and self.player.fuel > 0:
            self.player.mid_piece.update(self.player.speed, 0, self.player.top_piece.x, self.player.top_piece.y)
            self.player.bot_piece.update(self.player.speed, 0, self.player.top_piece.x, self.player.top_piece.y)
            self.player.top_piece.update(self.player.speed, 0)
            self.player.fuel -= 2
        else:
            self.player.mid_piece.update(0, 0, self.player.top_piece.x, self.player.top_piece.y)
            self.player.bot_piece.update(0, 0, self.player.top_piece.x, self.player.top_piece.y)
            self.player.top_piece.update(0, 0)
            if self.player.fuel > 0:
                self.player.fuel -= 1
        if pressed[pg.K_UP] and self.player.fuel > 0:
            self.player.mid_piece.update(0, -self.player.speed, self.player.top_piece.x, self.player.top_piece.y)
            self.player.bot_piece.update(0, -self.player.speed, self.player.top_piece.x, self.player.top_piece.y)
            self.player.top_piece.update(0, -self.player.speed)
            self.player.fuel -= 1
        elif pressed[pg.K_DOWN] and self.player.fuel > 0:
            self.player.mid_piece.update(0, self.player.speed, self.player.top_piece.x, self.player.top_piece.y)
            self.player.bot_piece.update(0, self.player.speed, self.player.top_piece.x, self.player.top_piece.y)
            self.player.top_piece.update(0, self.player.speed)
            self.player.fuel -= 1

    def screenManagement(self):
        self.loopCount += 1
        if self.loopCount >= 30:
            self.fuelBlit = self.player.fuel
            self.loopCount = 0
            #40, SCREEN_Y- 100
        fuelThingy = basicFont.render(str(self.fuelBlit), True, pg.Color("blue"))
        self.screen.blit(fuelThingy, (20, SCREEN_Y - 50))
        for enemy in self.enemies:
            self.screen.blit(enemy.image, (enemy.x, enemy.y))
        if self.player.hp <= 9:
            for x in range(0, self.player.hp):
                self.screen.blit(self.livesImg, (100+(x*30), SCREEN_Y-80))
        else:
            hpBlit = basicFont.render(
                "Health:"+str(self.player.hp), True, pg.Color("pink"))
            self.screen.blit(hpBlit, (100, SCREEN_Y-80))
        if self.player.fuel <= 0:
            lowFuel = basicFont.render("NO FUEL!!!", True,
                                       pg.Color("red"))
            self.screen.blit(lowFuel, (SCREEN_X/2-100, 80))
        elif self.player.fuel <= self.player.maxFuel/6:
            lowFuel = basicFont.render("CRITICAL FUEL!!!", True, pg.Color("red"))
            self.screen.blit(lowFuel, (SCREEN_X/2-100, 80))
        elif self.player.fuel <= self.player.maxFuel/4:
            lowFuel = basicFont.render("LOW FUEL!!!", True,
                                      pg.Color("yellow"))
            self.screen.blit(lowFuel, (SCREEN_X/2-100, 80))
        for gravObj in self.grav:
            self.screen.blit(gravObj.imageCenter, (gravObj.x, gravObj.y))
            self.screen.blit(gravObj.imageSurround, (gravObj.x2, gravObj.y2))
        self.screen.blit(self.player.top_piece.image, (self.player.top_piece.x, self.player.top_piece.y))
        self.screen.blit(self.player.mid_piece.image, (self.player.mid_piece.x, self.player.mid_piece.y))
        self.screen.blit(self.player.bot_piece.image, (self.player.bot_piece.x, self.player.bot_piece.y))
        self.fuelblit()
        self.abilityCooldown()
        fps = basicFont.render(str(int(self.clock.get_fps())), True, pg.Color("green"))
        self.screen.blit(fps, (500, 0))
        highScoreBlit = basicFont.render(str(self.highScore), True, pg.Color("red"))
        self.screen.blit(highScoreBlit, (50, 150))
        pg.display.update()
        self.screen.fill(pg.Color("black"))
        self.clock.tick(60)

    def load_images(self):
        self.livesImg = pg.transform.scale(pg.image.load("image/lives.png"), (80, 80))
        self.asteroids1 = pg.transform.scale(pg.image.load("image/meteor.png"), (80, 80))
        self.asteroids2 = pg.transform.scale(pg.image.load("image/meteor.png"), (90, 90))
        self.asteroids3 = pg.transform.scale(pg.image.load("image/meteor.png"), (70, 70))
        self.asteroids4 = pg.transform.scale(pg.image.load("image/meteor.png"), (128, 128))
        self.asteroids5 = pg.transform.scale(pg.image.load("image/meteor.png"), (100, 100))
        self.fuelImg = pg.transform.scale(pg.image.load('image/fuel.png'), (80, 80))
        self.healImg = pg.transform.scale(pg.image.load('image/heart.png'), (40, 40))

    def fuelblit(self):
        fuelratio = self.player.fuel/self.player.maxFuel
        if fuelratio > 0:
            pg.draw.rect(self.screen, pg.Color("green"), [40, SCREEN_Y- 100, 48, 16], 0)
        if fuelratio > 0.1:
            pg.draw.rect(self.screen, pg.Color("green"), [40, SCREEN_Y- 120, 48, 16], 0)
        if fuelratio > 0.2:
            pg.draw.rect(self.screen, pg.Color("green"), [40, SCREEN_Y- 140, 48, 16], 0)
        if fuelratio > 0.3:
            pg.draw.rect(self.screen, pg.Color("green"), [40, SCREEN_Y- 160, 48, 16], 0)
        if fuelratio > 0.4:
            pg.draw.rect(self.screen, pg.Color("green"), [40, SCREEN_Y- 180, 48, 16], 0)
        if fuelratio > 0.5:
            pg.draw.rect(self.screen, pg.Color("green"), [40, SCREEN_Y- 200, 48, 16], 0)
        if fuelratio > 0.6:
            pg.draw.rect(self.screen, pg.Color("green"), [40, SCREEN_Y- 220, 48, 16], 0)
        if fuelratio > 0.7:
            pg.draw.rect(self.screen, pg.Color("green"), [40, SCREEN_Y- 240, 48, 16], 0)
        if fuelratio > 0.8:
            pg.draw.rect(self.screen, pg.Color("green"), [40, SCREEN_Y- 260, 48, 16], 0)
        if fuelratio > 0.9:
            pg.draw.rect(self.screen, pg.Color("green"), [40, SCREEN_Y- 280, 48, 16], 0)

    def abilityCooldown(self):
        if self.player.abilityTimer[0] > 0:
            pg.draw.circle(
                self.screen, pg.Color("yellow"),
                (round(SCREEN_X / 3), SCREEN_Y - 150),
                round(30 *
                      (self.player.abilityDelay - self.player.abilityTimer[0])
                      / self.player.abilityDelay))
        else:
            pg.draw.circle(self.screen, pg.Color("green"), (round(SCREEN_X/3), SCREEN_Y - 150), 30)

        pg.draw.circle(self.screen, pg.Color("white"), (round(SCREEN_X/3), SCREEN_Y - 150), 30, 1)
        #self.screen.blit(self.player.abilityImage, (SCREEN_X/3-30, SCREEN_Y-180))

        if self.player.abilityTimer2[0] > 0:
            pg.draw.circle(
                self.screen, pg.Color("yellow"),
                (round(SCREEN_X / 3 * 2), SCREEN_Y - 150),
                round(30 *
                      (self.player.abilityDelay2 - self.player.abilityTimer2[0])
                      / self.player.abilityDelay2))
        else:
            pg.draw.circle(self.screen, pg.Color("green"),
                           (round(SCREEN_X / 3 * 2), SCREEN_Y - 150), 30)
        pg.draw.circle(self.screen, pg.Color("white"),
                       (round(SCREEN_X / 3 * 2), SCREEN_Y - 150), 30, 1)
