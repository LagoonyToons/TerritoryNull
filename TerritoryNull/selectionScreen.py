import pygame as pg
from options import *
from selectionList import *
from textFile import *
import sys

class selectionScreen:
    def __init__(self, screen, music, strip, joystick):
        self.screen = screen
        self.music = music
        self.strip = strip
        self.strip.started = False
        self.strip.state = "alternate"
        self.joystick = joystick
        self.stickTimer = 20

        self.listOfTop = ["image/rocket_top.png", "image/basicTop.png", "image/penTop.png"]
        self.listOfMid = ["image/rocket_mid.png", "image/basicMid.png", "image/penMid.png"]
        self.listOfBot = ["image/rocket_bot.png", "image/basicBot.png", "image/penBot.png"]

        self.listOfAbilities = ["image/heart.png", "image/stopwatch.png", "image/transfusion.png", "image/explosion.png"]
        self.abilityNames = ["heal", "timeStop", "transfusion", "deathBoost"]
        self.abilityTimers = [600, 70, 450, 1]

        self.listOfBullets = ["image/laser.png", "image/bullet.png", "image/tracker.png", "image/energy.png", "image/shotgun.png", "image/mine.png"]
        self.bulletNames = ["laserFire", "bullet", "tracker", "explosion", "shotgun", "mine"]
        self.bulletTimers = [40, 25, 75, 50, 65, 125]

        self.listOfPassives = ["image/passives/hp.png",
                               "image/passives/speed.png", "image/passives/fuel.png", "image/passives/invincible.png",  "image/passives/cooldown.png", "image/passives/frate.png", "image/passives/score.png"]
        self.passivesNames = ["bHealth", "bSpeed", "bFuel", "bIFrames", "dACooldown", "dGCooldown", "bScore"]
        self.count = 0
        self.secondaryCount = 0
        self.loadImages()
        self.genStats()
        self.loop()

    def loop(self):
        self.done = False
        self.cursorpos = 0
        self.arrowFlipX = 20
        self.arrowX = 180
        self.offset = 25
        self.finalList = [self.tops[0], self.mids[0], self.bots[0], self.abilities[0], self.bullets[0], self.passives[0]]
        self.place = [0,0,0,0,0,0]
        while not self.done:
            if self.stickTimer > 0:
                self.stickTimer -= 1
            #print(self.joystick.get_button(2))
            self.controls()
            self.blitImages()
            self.strip.update()
            #print(self.strip.timeBetween)

    def controls(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    if self.cursorpos == 0:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0 :
                            self.place[self.cursorpos] = len(self.listOfTop)-1
                        self.finalList[self.cursorpos] = self.tops[self.place[self.cursorpos]]
                    elif self.cursorpos == 1:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0 :
                            self.place[self.cursorpos] = len(self.listOfMid)-1
                        self.finalList[self.cursorpos] = self.mids[self.place[self.cursorpos]]
                    elif self.cursorpos == 2:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0 :
                            self.place[self.cursorpos] = len(self.listOfBot)-1
                        self.finalList[self.cursorpos] = self.bots[self.place[self.cursorpos]]
                    elif self.cursorpos == 3:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0:
                            self.place[self.cursorpos] = len(self.listOfAbilities)-1
                        self.finalList[self.cursorpos] = self.abilities[self.place[self.cursorpos]]
                    elif self.cursorpos == 4:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0:
                            self.place[self.cursorpos] = len(
                                self.listOfBullets) - 1
                        self.finalList[self.cursorpos] = self.bullets[self.place[self.cursorpos]]
                    elif self.cursorpos == 5:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0:
                            self.place[self.cursorpos] = len(
                                self.listOfPassives) - 1
                        self.finalList[self.cursorpos] = self.passives[self.place[self.cursorpos]]

                elif event.key == pg.K_RIGHT:
                    if self.cursorpos == 0:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > len(self.listOfTop)-1 :
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.tops[self.place[self.cursorpos]]
                    elif self.cursorpos == 1:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > len(self.listOfTop)-1 :
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.mids[self.place[self.cursorpos]]
                    elif self.cursorpos == 2:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > len(self.listOfTop)-1 :
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.bots[self.place[self.cursorpos]]
                    elif self.cursorpos == 3:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > len(self.listOfAbilities)-1:
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.abilities[self.place[self.cursorpos]]
                    elif self.cursorpos == 4:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > len(self.listOfBullets)-1:
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.bullets[self.place[self.cursorpos]]
                    elif self.cursorpos == 5:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > len(self.listOfPassives)-1:
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.passives[self.place[self.cursorpos]]
                elif event.key == pg.K_UP:
                    self.cursorpos -= 1
                    if self.cursorpos < 0:
                        self.cursorpos = 6

                elif event.key == pg.K_DOWN:
                    self.cursorpos += 1
                    if self.cursorpos > 6:
                        self.cursorpos = 0

                elif event.key == pg.K_SPACE and self.cursorpos == 6:
                    self.done = True
            elif event.type == pg.JOYBUTTONDOWN:
                if self.joystick.get_button(2) and self.cursorpos == 6:
                    self.done = True
                if self.joystick.get_button(4):
                    self.music.volumeToggle()
                if self.joystick.get_button(6):
                    self.music.switchSong()
                if self.joystick.get_button(8):
                    if self.strip.enabled:
                        self.strip.enabled = False
                    else:
                        self.strip.enabled = True
            if event.type == pg.JOYAXISMOTION:
                if self.joystick.get_axis(0) > 0 and self.stickTimer <= 0:
                    if self.cursorpos == 0:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0 :
                            self.place[self.cursorpos] = len(self.listOfTop)-1
                        self.finalList[self.cursorpos] = self.tops[self.place[self.cursorpos]]
                    elif self.cursorpos == 1:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0 :
                            self.place[self.cursorpos] = len(self.listOfMid)-1
                        self.finalList[self.cursorpos] = self.mids[self.place[self.cursorpos]]
                    elif self.cursorpos == 2:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0 :
                            self.place[self.cursorpos] = len(self.listOfBot)-1
                        self.finalList[self.cursorpos] = self.bots[self.place[self.cursorpos]]
                    elif self.cursorpos == 3:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0:
                            self.place[self.cursorpos] = len(self.listOfAbilities)-1
                        self.finalList[self.cursorpos] = self.abilities[self.place[self.cursorpos]]
                    elif self.cursorpos == 4:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0:
                            self.place[self.cursorpos] = len(
                                self.listOfBullets) - 1
                        self.finalList[self.cursorpos] = self.bullets[self.place[self.cursorpos]]
                    elif self.cursorpos == 5:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0:
                            self.place[self.cursorpos] = len(
                                self.listOfPassives) - 1
                        self.finalList[self.cursorpos] = self.passives[self.place[self.cursorpos]]
                    self.stickTimer = 20

                if self.joystick.get_axis(0) < 0 and self.stickTimer <= 0:
                    if self.cursorpos == 0:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > len(self.listOfTop)-1 :
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.tops[self.place[self.cursorpos]]
                    elif self.cursorpos == 1:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > len(self.listOfTop)-1 :
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.mids[self.place[self.cursorpos]]
                    elif self.cursorpos == 2:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > len(self.listOfTop)-1 :
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.bots[self.place[self.cursorpos]]
                    elif self.cursorpos == 3:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > len(self.listOfAbilities)-1:
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.abilities[self.place[self.cursorpos]]
                    elif self.cursorpos == 4:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > len(self.listOfBullets)-1:
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.bullets[self.place[self.cursorpos]]
                    elif self.cursorpos == 5:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > len(self.listOfPassives)-1:
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.passives[self.place[self.cursorpos]]
                    self.stickTimer = 20
                if self.joystick.get_axis(1) > 0 and self.stickTimer <= 0:
                    self.cursorpos -= 1
                    if self.cursorpos < 0:
                        self.cursorpos = 6
                    self.stickTimer = 20
                if self.joystick.get_axis(1) < 0 and self.stickTimer <= 0:
                    self.cursorpos += 1
                    if self.cursorpos > 6:
                        self.cursorpos = 0
                    self.stickTimer = 20
    def blitImages(self):
        if self.count == 0:
            rect=(82, 20+(70*self.cursorpos-1) + (self.offset*self.cursorpos), 100, 100)
            pg.draw.rect(self.screen, pg.Color("grey"), rect)
            self.secondaryCount += 1
            if self.secondaryCount > 35:
                self.count = 20
                self.secondaryCount = 0
        else:
            self.count -= 1
        for x in range(3):
            self.screen.blit(self.finalList[x][3], (90, 20+(70*(x)) + (self.offset*x)))
        for x in range(2):
            self.screen.blit(self.finalList[(x+3)][0], (90, 20+(70*(x+3)) + (self.offset*(x+4))))
        self.screen.blit(self.finalList[(5)][0], (70, (70*(6.5)) + (self.offset+(8))))
        for x in range(6):
            self.screen.blit(self.arrow, (self.arrowX, 20+ (70*x-1) + (35*x)))
            self.screen.blit(self.arrowFlip, (self.arrowFlipX, 20 + (70*x-1) + (35*x)))
        # self.finalList[self.cursorpos] = self.abilities[self.place[self.cursorpos]]
        for x in range(len(abilityText[self.place[3]])):
            text = descriptionFont.render((abilityText[self.place[3]][x]), True, pg.Color("green"))
            self.screen.blit(text, (SCREEN_X/2-100, 350 + (x*40)))
        for x in range(len(gunText[self.place[4]])):
            text = descriptionFont.render(
                (gunText[self.place[4]][x]), True, pg.Color("green"))
            self.screen.blit(text, (SCREEN_X/2-100, 450 + (x*40)))
        for x in range(len(passiveText[self.place[5]])):
            text = descriptionFont.render(
                (passiveText[self.place[5]][x]), True, pg.Color("green"))
            self.screen.blit(text, (SCREEN_X/2-100, 550 + (x*40)))
        text = basicFont.render("START!", True, pg.Color("green"))
        self.screen.blit(text, (80, 150+(70*(6-1)) + (self.offset*5)))
        self.blitStats()
        pg.display.update()
        self.screen.fill(pg.Color("black"))

    def blitStats(self):
        #storage list, [hp, fuel, speed, img]
        tophp = self.finalList[0][0]
        topfuel = self.finalList[0][1]
        topspeed = self.finalList[0][2]

        midhp = self.finalList[1][0]
        midfuel = self.finalList[1][1]
        midspeed = self.finalList[1][2]

        bothp = self.finalList[2][0]
        botfuel = self.finalList[2][1]
        botspeed = self.finalList[2][2]

        textTotalHp = tophp + midhp + bothp
        textTotalFuel = topfuel + midfuel + botfuel
        textTotalSpeed = topspeed + midspeed + botspeed

        HP = basicFont.render("HP: " + str(textTotalHp), True, pg.Color("green"))
        self.screen.blit(HP, (30, SCREEN_Y/2+70))
        FUEL = basicFont.render("FUEL: " + str(textTotalFuel), True, pg.Color("green"))
        self.screen.blit(FUEL, (30, SCREEN_Y/2+140))
        SPEED = basicFont.render("SPEED: " + str(textTotalSpeed), True, pg.Color("green"))
        self.screen.blit(SPEED, (30, SCREEN_Y/2+210))

        for x in range(textTotalHp):
            rect=(250 + (x*20), SCREEN_Y/2+70, 15, 25)
            pg.draw.rect(self.screen, pg.Color("red"), rect)
        for x in range(round(textTotalFuel/500)):
            rect=(250 + (x*20), SCREEN_Y/2+140, 15, 25)
            pg.draw.rect(self.screen, pg.Color("red"), rect)
        for x in range(round(textTotalSpeed)):
            rect=(250 + (x*20), SCREEN_Y/2+210, 15, 25)
            pg.draw.rect(self.screen, pg.Color("red"), rect)

    def loadImages(self):
        #self.loadedImages = []
        self.topImages = []
        self.midImages = []
        self.botImages = []
        self.abilityImages = []
        self.bulletImages = []
        self.passivesImages = []
        for x in self.listOfTop:
            self.img = pg.transform.scale(pg.image.load(x), (80, 80))
            self.topImages.append(self.img)
            #print(len(self.topImages))
        for x in self.listOfMid:
            self.img = pg.transform.scale(pg.image.load(x), (80, 80))
            self.midImages.append(self.img)
        for x in self.listOfBot:
            self.img = pg.transform.scale(pg.image.load(x), (80, 80))
            self.botImages.append(self.img)
        for x in self.listOfAbilities:
            self.img = pg.transform.scale(pg.image.load(x), (80, 80))
            self.abilityImages.append(self.img)
        for x in self.listOfBullets:
            self.img = pg.transform.scale(pg.image.load(x), (80, 80))
            self.bulletImages.append(self.img)
        for x in self.listOfPassives:
            self.img = pg.transform.scale(pg.image.load(x), (120, 120))
            self.passivesImages.append(self.img)


        self.arrow = pg.transform.scale(pg.image.load("image/arrow.png"), (64, 64))
        self.arrowFlip = pg.transform.rotate(self.arrow, 180)

    def genStats(self):
        count = 0
        self.tops = []
        self.bots = []
        self.mids = []
        self.abilities = []
        self.bullets = []
        self.passives = []
        #print(len(self.loadedImages[0]))
        for item in self.topImages:
            #print(len(self.topImages))
            #storage list, [hp, fuel, speed, img]
            storageList = statLists[count]
            storageList.append(item)
            count+= 1
            self.tops.append(storageList)

        for item in self.midImages:
            #storage list, [hp, fuel, speed, img]
            #print(item)
            storageList = statLists[count]
            storageList.append(item)
            count+= 1
            self.mids.append(storageList)

        for item in self.botImages:
            #storage list, [hp, fuel, speed, img]
            #print(item)
            storageList = statLists[count]
            storageList.append(item)
            count+= 1
            self.bots.append(storageList)
        thingy = 0
        for item in self.abilityImages:
            storageList = [item]
            itemName = self.abilityNames[thingy]
            storageList.append(itemName)
            itemName = self.abilityTimers[thingy]
            storageList.append(itemName)
            thingy += 1
            self.abilities.append(storageList)
        thingy = 0
        for item in self.bulletImages:
            storageList = [item]
            itemName = self.bulletNames[thingy]
            storageList.append(itemName)
            itemName = self.bulletTimers[thingy]
            storageList.append(itemName)
            thingy += 1
            self.bullets.append(storageList)
        thingy = 0
        for item in self.passivesImages:
            storageList = [item]
            itemName = self.passivesNames[thingy]
            storageList.append(itemName)
            thingy += 1
            self.passives.append(storageList)
