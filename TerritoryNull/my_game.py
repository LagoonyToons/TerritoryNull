import pygame as pg
from options import *
from player import *
from enemy import *
import random
import sys
import time
import math

class Game:
    def __init__(self, screen, music, playerStats, strip, joystick):
        self.clock = pg.time.Clock()
        self.load_images()
        self.load_sounds()
        self.player = Player(playerStats, self.soundEffects)
        self.joystick = joystick
        self.screen = screen
        self.highScore = [0]
        self.music = music
        self.strip = strip
        self.strip.started = False
        self.strip.state = "alternate"
        self.color = (0,125, 0)
        self.color2 = (0,0,125)
        

        self.all_sprites = pg.sprite.Group()
        self.player_pieces = pg.sprite.Group()
        self.enemies = []
        self.grav = pg.sprite.Group()
        self.bulletList = []

        self.genStars()

        self.dead = False

        for piece in self.player.pieceList:
            self.all_sprites.add(piece)
            self.player_pieces.add(piece)

        self.loopCount = 0
        self.fuelBlit = self.player.fuel

        self.time = time.time()

        self.gameloop()

    def gameloop(self):
        self.counter = 0
        self.difficultyCount = 0
        self.difficultyLevel = 3
        while not self.dead:
            self.strip.update(self.color, self.player, self.color2)
            self.currentTime = time.time()
            try:
                self.frameRate = round(1/(self.currentTime - self.time))
            except:
                self.frameRate = 60
            self.time = self.currentTime
            self.speedMultiplier = 60/self.frameRate

            self.music.songState()
            self.controls()
            if self.player.timeStopTimer > 0:
                self.player.timeStopTimer -= 1*self.speedMultiplier
            else:
                self.enemySpawn()
                for enemy in self.enemies:
                    enemy.update(self.player, self.enemies, self.speedMultiplier, self.bulletList, self.highScore)
                for bullet in self.bulletList:
                    bullet.update(self.player.top_piece, self.bulletList, self.speedMultiplier)
                for gravObj in self.grav:
                    gravObj.update(self.enemies, self.player)
            self.highScore[0] += round(11*self.speedMultiplier)
            self.dead = self.player.update(self.speedMultiplier)
            self.screenManagement()
        if self.player.passive == "bScore":
            self.highScore[0] = round(self.highScore[0]*1.35)
            return self.highScore[0]
        else:
            return self.highScore[0]

    def enemySpawn(self):
        self.counter += 1
        self.difficultyCount += 1
        difficultyLevel = basicFont.render(
            str(int(self.difficultyLevel)), True, pg.Color("green"))
        self.screen.blit(difficultyLevel, (800, 50))
        if round(self.difficultyCount*self.speedMultiplier) > 350 and self.difficultyLevel < 24:
            self.difficultyLevel += 1
            self.difficultyCount = 0
        if round(self.counter*self.speedMultiplier) >= 30-self.difficultyLevel:
            self.counter = 0
            randomSize = random.randint(1, 4)
            x = random.randint(0, SCREEN_X-100)
            randomEnemyChoice = random.randint(0,200)
            randomsquid = random.randint(1,25000)
            if randomEnemyChoice <= 10:
                self.enemies.append(BigAsteroid(x,-150, self.biggestAsteroid, self.asteroids1))
            if randomEnemyChoice <= 150:
                if randomsquid == 2:
                    enemy = Asteroid(x, 0, self.asteroids5)
                else:
                    #randomListIndex = random.randint(0,9)
                    if randomSize == 1:
                        enemy = Asteroid(x, 0, self.asteroids1)
                    elif randomSize == 2:
                        enemy = Asteroid(x, 0, self.asteroids2)
                    elif randomSize == 3:
                        enemy = Asteroid(x, 0, self.asteroids3)
                    elif randomSize == 4:
                        enemy = Asteroid(x, 0, self.asteroids4)
                self.enemies.append(enemy)
            elif randomEnemyChoice <= 160:
                if len(self.grav) == 0:
                    gravObj = GravityField(self.holeAnim)
                    self.grav.add(gravObj)
            elif randomEnemyChoice <= 162:
                enemy = Heal(x, 0, self.healImg)
                self.enemies.append(enemy)
            elif randomEnemyChoice <= 168:
                bossExists = False
                for enemy in self.enemies:
                    if enemy.type == "boss":
                        bossExists = True
                        randomEnemyChoice = random.randint(0, 200)
                        break
                if not bossExists:
                    boss = BossShooter(500, -200, self.bossImg, self.hurtBossImg, 4)
                    self.enemies.append(boss)
            elif randomEnemyChoice <= 174:
                bossExists = False
                for enemy in self.enemies:
                    if enemy.type == "boss":
                        bossExists = True
                        randomEnemyChoice = random.randint(0, 200)
                        break
                if not bossExists:
                    boss = Boss(200, -200, self.bossImg, self.hurtBossImg, 6)
                    self.enemies.append(boss)
            else:
                enemy = Fuel(x, 0, self.fuelImg)
                self.enemies.append(enemy)

    def controls(self):
        if self.joystick.get_button(0):
                self.player.abilityStateMachine(self.player.ability, 1, self.highScore, self.bulletList, self.difficultyLevel)
        if self.joystick.get_button(1):
            if self.player.ability2 == "explosion" and self.player.explodyBar > 0 and self.player.abilityTimer2[0] <= 0 and self.player.exploding == False:
                self.player.exploding = True
                self.bulletList.append(
                    Explode(self.player.ability2Image, self.player.top_piece.x, self.player.top_piece.y))
                self.player.speed = round(self.player.speed*.5)
            elif self.player.ability2 == "laserFire" and self.player.abilityTimer2[0] <= 0 and self.player.exploding == False and self.player.explodyBar > 100 and len(self.bulletList) <= 0: 
                self.player.firing = True
                self.bulletList.append(
                    Laser(self.player.ability2Image, self.player.top_piece.x, self.player.top_piece.y))
            elif self.player.ability2 != "mine":
                self.player.abilityStateMachine(self.player.ability2, 2, self.highScore, self.bulletList, self.enemies, self.difficultyLevel, self.bulletImages)
            
        if self.player.exploding == True and self.player.explodyBar <= 0:
            self.player.exploding = False
            self.bulletList = []
            self.player.abilityTimer2[0] = self.player.abilityDelay2
            self.player.speed = self.player.storedSpeed
        if self.player.firing and self.player.explodyBar <= 0:
            self.player.firing = False
            self.bulletList = []
            self.player.abilityTimer2[0] = self.player.abilityDelay2
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.music.switchSong()
                if event.key == pg.K_SPACE:
                    self.player.abilityStateMachine(self.player.ability, 1, self.highScore, self.bulletList, self.difficultyLevel)
                if event.key == pg.K_e:
                    if self.player.ability2 == "explosion" and self.player.explodyBar > 0 and self.player.abilityTimer2[0] <= 0:
                        self.player.exploding = True
                        self.bulletList.append(
                            Explode(self.player.ability2Image, self.player.top_piece.x, self.player.top_piece.y))
                        self.player.speed = round(self.player.speed*.5)
                    elif self.player.ability2 == "laserFire" and self.player.abilityTimer2[0] <= 0 and self.player.exploding == False and self.player.explodyBar > 100:
                        self.player.firing = True
                        self.bulletList.append(
                            Laser(self.player.ability2Image, self.player.top_piece.x, self.player.top_piece.y))
                    else:
                        self.player.abilityStateMachine(self.player.ability2, 2, self.highScore, self.bulletList, self.enemies, self.difficultyLevel, self.bulletImages)
                if event.key == pg.K_q:
                    self.music.volumeToggle()
            if event.type == pg.KEYUP:
                if event.key == pg.K_e and self.player.ability2 == "explosion" and self.player.exploding == True:
                    self.player.exploding = False
                    self.bulletList = []
                    self.player.abilityTimer2[0] = self.player.abilityDelay2
                    self.player.speed = self.player.storedSpeed
            elif event.type == pg.JOYBUTTONDOWN:
                if self.joystick.get_button(1) and self.player.ability2 == "mine":
                    self.player.abilityStateMachine(self.player.ability2, 2, self.highScore, self.bulletList, self.enemies, self.difficultyLevel, self.bulletImages)
                if self.joystick.get_button(4):
                    self.music.volumeToggle()
                if self.joystick.get_button(6):
                    self.music.switchSong()
                if self.joystick.get_button(8):
                    if self.strip.enabled:
                        self.strip.enabled = False
                    else:
                        self.strip.enabled = True
    
            if not self.joystick.get_button(1) and self.player.exploding == True:
                self.player.exploding = False
                self.bulletList = []
                self.player.abilityTimer2[0] = self.player.abilityDelay2
                self.player.speed = self.player.storedSpeed
            if not self.joystick.get_button(1) and self.player.firing == True:
                self.player.firing = False
                self.bulletList = []
                self.player.abilityTimer2[0] = self.player.abilityDelay2
                
               
        pressed = pg.key.get_pressed()
        if pressed[pg.K_LEFT] or self.joystick.get_axis(0) > 0:
            if self.player.fuel > 0:
                self.player.mid_piece.update(-self.player.speed*self.speedMultiplier, 0, self.player.top_piece.x, self.player.top_piece.y)
                self.player.bot_piece.update(-self.player.speed*self.speedMultiplier, 0, self.player.top_piece.x, self.player.top_piece.y)
                self.player.top_piece.update(-self.player.speed*self.speedMultiplier, 0)
                self.player.fuel -= round(2*self.speedMultiplier)
        elif pressed[pg.K_RIGHT] or self.joystick.get_axis(0) < 0:
            if self.player.fuel > 0:
                self.player.mid_piece.update(self.player.speed*self.speedMultiplier, 0, self.player.top_piece.x, self.player.top_piece.y)
                self.player.bot_piece.update(self.player.speed*self.speedMultiplier, 0, self.player.top_piece.x, self.player.top_piece.y)
                self.player.top_piece.update(self.player.speed*self.speedMultiplier, 0)
                self.player.fuel -= round(2*self.speedMultiplier)
        else:
            self.player.mid_piece.update(0, 0, self.player.top_piece.x, self.player.top_piece.y)
            self.player.bot_piece.update(0, 0, self.player.top_piece.x, self.player.top_piece.y)
            self.player.top_piece.update(0, 0)
            if self.player.fuel > 0:
                self.player.fuel -= round(1*self.speedMultiplier)
        if pressed[pg.K_UP] or self.joystick.get_axis(1) > 0:
            if self.player.fuel > 0:
                self.player.mid_piece.update(0, -self.player.speed*self.speedMultiplier, self.player.top_piece.x, self.player.top_piece.y)
                self.player.bot_piece.update(0, -self.player.speed*self.speedMultiplier, self.player.top_piece.x, self.player.top_piece.y)
                self.player.top_piece.update(0, -self.player.speed*self.speedMultiplier)
                self.player.fuel -= round(1*self.speedMultiplier)
        elif pressed[pg.K_DOWN] or self.joystick.get_axis(1) < 0:
            if self.player.fuel > 0:
                self.player.mid_piece.update(0, self.player.speed*self.speedMultiplier, self.player.top_piece.x, self.player.top_piece.y)
                self.player.bot_piece.update(0, self.player.speed*self.speedMultiplier, self.player.top_piece.x, self.player.top_piece.y)
                self.player.top_piece.update(0, self.player.speed*self.speedMultiplier)
                self.player.fuel -= round(1*self.speedMultiplier)

    def screenManagement(self):
        self.starBlit()
        for gravObj in self.grav:
            self.screen.blit(gravObj.imageList[gravObj.currentFrame], (gravObj.x, gravObj.y))
        self.loopCount += 1
        if self.loopCount >= 30:
            self.fuelBlit = self.player.fuel
            self.loopCount = 0
            #40, SCREEN_Y- 100
        #cooldownNumber = basicFont.render(str(self.player.abilityDelay+self.player.timeStopIncreaseToCooldown), True,
          #                         pg.Color("red"))
        #self.screen.blit(cooldownNumber, (SCREEN_X/2-100, 80))
        for x in range(self.player.mineCount):
            self.screen.blit(self.player.ability2Image, (SCREEN_X-50, SCREEN_Y-(50*(x+1))))
        fuelThingy = basicFont.render(str(self.fuelBlit), True, pg.Color("blue"))
        self.screen.blit(fuelThingy, (20, SCREEN_Y - 50))
        #songsLoaded = basicFont.render(
            #str(len(self.music.returnInitializedSongs())), True, pg.Color("blue"))
        #self.screen.blit(songsLoaded, (20, 100))
        for enemy in self.enemies:
                enemy.draw(self.screen)
        for bullet in self.bulletList:
            bullet.draw(self.screen)
        if self.player.hp <= 9:
            for x in range(0, self.player.hp):
                self.screen.blit(self.livesImg, (100+(x*30), SCREEN_Y-80))
        else:
            hpBlit = basicFont.render(
                "Health:"+str(self.player.hp), True, pg.Color("pink"))
            self.screen.blit(hpBlit, (100, SCREEN_Y-80))
        if self.player.ability2 == "explosion" or self.player.ability2 == "laserFire":
            pg.draw.rect(self.screen, pg.Color("red"), [SCREEN_X-100, SCREEN_Y-100, 50, -(300*(self.player.explodyBar/1200))])
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
            #self.screen.blit(gravObj.imageSurround, (gravObj.x2, gravObj.y2))
        self.screen.blit(self.player.top_piece.image, (self.player.top_piece.x, self.player.top_piece.y))
        self.screen.blit(self.player.mid_piece.image, (self.player.mid_piece.x, self.player.mid_piece.y))
        self.screen.blit(self.player.bot_piece.image, (self.player.bot_piece.x, self.player.bot_piece.y))
        if self.player.invincibility > 0:
            invTxt = descriptionFont.render("Invincibility Frames:  " + str(self.player.invincibility), True, pg.Color("yellow"))
            self.screen.blit(invTxt, (SCREEN_X-240, 100))
        self.fuelblit()
        self.abilityCooldown()
       #fps = basicFont.render(str(int(self.clock.get_fps())), True, pg.Color("green"))
       #self.screen.blit(fps, (500, 0))
        if self.player.passive == "bScore":
            highScoreBlit = basicFont.render(
                str(round(self.highScore[0]*1.35)), True, pg.Color("red"))
        else:
            highScoreBlit = basicFont.render(str(self.highScore[0]), True, pg.Color("red"))
        self.screen.blit(highScoreBlit, (50, 150))
        pg.display.update()
        self.screen.fill(pg.Color("black"))
        self.clock.tick(60)

    def load_images(self):
        self.holeAnim = []
        for x in range(36):
            self.thisNameDoesntEvenMatter = pg.transform.scale(pg.transform.rotate(pg.transform.scale(pg.image.load("image/grav.png"), (120, 120)), x*10), (120, 120))
            self.holeAnim.append(self.thisNameDoesntEvenMatter)
        self.bullet = pg.transform.scale(pg.image.load("image/bullet.png"), (20, 20))
        self.bullet1 = pg.transform.rotate(self.bullet, 30)
        self.bullet2 = pg.transform.rotate(self.bullet, 15)
        self.bullet3 = pg.transform.rotate(self.bullet, -30)
        self.bullet4 = pg.transform.rotate(self.bullet, -15)
        self.bulletImages = [self.bullet, self.bullet1, self.bullet2, self.bullet3, self.bullet4]
        self.livesImg = pg.transform.scale(pg.image.load("image/lives.png"), (80, 80))
        self.asteroids1 = pg.transform.scale(pg.image.load("image/asteroids/small.png"), (80, 80))
        self.asteroids2 = pg.transform.scale(pg.image.load("image/asteroids/medium.png"), (90, 90))
        self.asteroids3 = pg.transform.scale(pg.image.load("image/asteroids/small.png"), (70, 70))
        self.asteroids4 = pg.transform.scale(pg.image.load("image/asteroids/big.png"), (128, 128))
        self.asteroids5 = pg.transform.scale(pg.image.load("image/asteroids/squidward.png"), (100, 100))
        self.biggestAsteroid = pg.transform.scale(pg.image.load("image/asteroids/big.png"), (150, 150))
        self.fuelImg = pg.transform.scale(pg.image.load('image/fuel.png'), (80, 80))
        self.healImg = pg.transform.scale(pg.image.load('image/heart.png'), (40, 40))
        self.bossImg=pg.transform.scale(pg.image.load("image/cthuhlu.png"), (200, 200))
        self.hurtBossImg=pg.transform.scale(pg.image.load("image/cthuhluHit.png"), (200, 200))

    def load_sounds(self):
        self.soundEffects = []
        self.zaWarudo = pg.mixer.Sound("soundEffects/ZAWARUDO.ogg")
        self.soundEffects.append(self.zaWarudo)

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
            pg.draw.arc(
                self.screen, pg.Color("red"),
                [round(SCREEN_X / 3), SCREEN_Y - 100, 80, 80], 0,
                (math.pi * 2 *
                 (self.player.abilityDelay+self.player.timeStopIncreaseToCooldown - self.player.abilityTimer[0]) /
                 (self.player.abilityDelay+self.player.timeStopIncreaseToCooldown)), 5)
        else:
            pg.draw.arc(
                self.screen, pg.Color("green"),
                [round(SCREEN_X / 3), SCREEN_Y - 100, 80, 80], 0,
                (math.pi * 2 *
                 (self.player.abilityDelay+self.player.timeStopIncreaseToCooldown - self.player.abilityTimer[0]) /
                 (self.player.abilityDelay+self.player.timeStopIncreaseToCooldown)), 5)

    # pg.draw.circle(self.screen, pg.Color("white"), (round(SCREEN_X/3), SCREEN_Y - 80), 30, 1)
    #self.screen.blit(self.player.abilityImage, (SCREEN_X/3-30, SCREEN_Y-180))

        if self.player.abilityTimer2[0] > 0:
            pg.draw.arc(
                self.screen, pg.Color("red"),
                [round(SCREEN_X / 3 * 2-80), SCREEN_Y - 100, 80, 80], 0,
                (math.pi * 2 *
                 (self.player.abilityDelay2 - self.player.abilityTimer2[0]) /
                 self.player.abilityDelay2), 5)
        else:
            pg.draw.arc(
                self.screen, pg.Color("green"),
                [round(SCREEN_X / 3*2-80), SCREEN_Y - 100, 80, 80], 0,
                (math.pi * 2 *
                 (self.player.abilityDelay2 - self.player.abilityTimer2[0]) /
                 self.player.abilityDelay2), 5)
    def starBlit(self):
        for star in self.screen_1_rects:
            pg.draw.circle(self.screen, pg.Color("snow"), (star[0], round(star[1])), star[2])
            #print(star[0][1])
            star[1] += .5*self.speedMultiplier
            if star[1] >= SCREEN_Y:
                star[1] = 0
        for star in self.screen_2_rects:
            pg.draw.circle(self.screen, pg.Color("snow"), (star[0], round(star[1])), star[2])
            star[1] += .8*self.speedMultiplier
            if star[1] >= SCREEN_Y:
                star[1] = 0
        for star in self.screen_3_rects:
            pg.draw.circle(self.screen, pg.Color("snow"), (star[0], round(star[1])), star[2])
            star[1] += 1.3*self.speedMultiplier
            if star[1] >= SCREEN_Y:
                star[1] = 0
        #print(len(self.screen_1_rects))
    def genStars(self):
        self.screen_1_rects = []
        self.screen_2_rects = []
        self.screen_3_rects = []
        for x in range(40):
            holder = []
            holder.append(random.randint(0,SCREEN_X))
            holder.append(random.randint(0,SCREEN_Y))
            holder.append(random.choice([1,1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5,]))
            #pg.draw.circle(self.screen, silver, (rand_x, rand_y), randSize)
            self.screen_1_rects.append(holder)
        for x in range(40):
            holder = []
            holder.append(random.randint(0,SCREEN_X))
            holder.append(random.randint(0,SCREEN_Y))
            holder.append(random.choice([1,1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5,  6, 7]))
            #pg.draw.circle(self.screen, silver, (rand_x, rand_y), randSize)
            self.screen_2_rects.append(holder)
        for x in range(40):
            holder = []
            holder.append(random.randint(0,SCREEN_X))
            holder.append(random.randint(0,SCREEN_Y))
            holder.append(random.choice([1,1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5, 5,  6, 7]))
            #pg.draw.circle(self.screen, silver, (rand_x, rand_y), randSize)
            self.screen_3_rects.append(holder)
