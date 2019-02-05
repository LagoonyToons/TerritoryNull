import pygame as pg
from options import *
from selectionList import *
import sys

class selectionScreen:
    def __init__(self, screen, music):
        self.screen = screen
        self.music = music

        self.listOfTop = ["image/rocket_top.png", "image/basicTop.png", "image/penTop.png"]
        self.listOfMid = ["image/rocket_mid.png", "image/basicMid.png", "image/penMid.png"]
        self.listOfBot = ["image/rocket_bot.png", "image/basicBot.png", "image/penBot.png"]
        self.listOfAbilities = ["image/heart.png", "image/stopwatch.png", "image/shrink.png", "image/transfusion.jpg", "image/explosion.png"]
        self.abilityNames = ["heal", "timeStop",
                             "shrink", "transfusion", "deathBoost"]
        self.abilityTimers = [60, 600, 1200, 240, 0]
        self.loadImages()
        self.genStats()
        self.loop()

    def loop(self):
        self.done = False
        self.cursorpos = 0
        self.arrowFlipX = SCREEN_X/2-120
        self.arrowX = SCREEN_X/2+60
        self.offset = 30
        self.finalList = [self.tops[0], self.mids[0], self.bots[0], self.abilities[0], self.abilities2[0]]
        self.place = [0,0,0,0,0]
        while not self.done:
            self.controls()
            self.blitImages()

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
                            self.place[self.cursorpos] = len(self.listOfAbilities)-1
                        self.finalList[self.cursorpos] = self.abilities2[self.place[self.cursorpos]]

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
                        if self.place[self.cursorpos] > len(self.listOfAbilities)-1:
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.abilities2[self.place[self.cursorpos]]

                elif event.key == pg.K_UP:
                    self.cursorpos -= 1
                    if self.cursorpos < 0:
                        self.cursorpos = 5

                elif event.key == pg.K_DOWN:
                    self.cursorpos += 1
                    if self.cursorpos > 5:
                        self.cursorpos = 0

                elif event.key == pg.K_SPACE and self.cursorpos == 5:
                    self.done = True

    def blitImages(self):
        rect=(SCREEN_X/2-40, 80+(80*self.cursorpos-1) + (self.offset*self.cursorpos), 90, 90)
        pg.draw.rect(self.screen, pg.Color("grey"), rect)
        for x in range(3):
            self.screen.blit(self.finalList[x][3], (SCREEN_X/2-40, 80+(80*x-1) + (self.offset*x)))
        for x in range(2):
            self.screen.blit(self.finalList[(x+3)][0], (SCREEN_X/2-40, 80+(80*(x+4-1)) + (self.offset*(x+4))))
        for x in range(5):
            self.screen.blit(self.arrow, (self.arrowX, 80 + (80*x-1) + (35*x)))
            self.screen.blit(self.arrowFlip, (self.arrowFlipX, 80 + (80*x-1) + (35*x)))
        text = basicFont.render("START!", True, pg.Color("green"))
        self.screen.blit(text, (SCREEN_X/2-40, 150+(80*(5-1)) + (self.offset*5)))
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
        self.screen.blit(HP, (30, 400))
        FUEL = basicFont.render("FUEL: " + str(textTotalFuel), True, pg.Color("green"))
        self.screen.blit(FUEL, (30, 470))
        SPEED = basicFont.render("SPEED: " + str(textTotalSpeed), True, pg.Color("green"))
        self.screen.blit(SPEED, (30, 540))

        for x in range(textTotalHp):
            rect=(250 + (x*20), 400, 15, 25)
            pg.draw.rect(self.screen, pg.Color("red"), rect)
        for x in range(round(textTotalFuel/500)):
            rect=(250 + (x*20), 470, 15, 25)
            pg.draw.rect(self.screen, pg.Color("red"), rect)
        for x in range(round(textTotalSpeed)):
            rect=(250 + (x*20), 540, 15, 25)
            pg.draw.rect(self.screen, pg.Color("red"), rect)

    def loadImages(self):
        #self.loadedImages = []
        self.topImages = []
        self.midImages = []
        self.botImages = []
        self.abilityImages = []
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


        self.arrow = pg.transform.scale(pg.image.load("image/arrow.png"), (64, 64))
        self.arrowFlip = pg.transform.rotate(self.arrow, 180)

    def genStats(self):
        count = 0
        self.tops = []
        self.bots = []
        self.mids = []
        self.abilities = []
        self.abilities2 = []
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
        for item in self.abilityImages:
            storageList = [item]
            itemName = self.abilityNames[thingy]
            storageList.append(itemName)
            itemName = self.abilityTimers[thingy]
            storageList.append(itemName)
            thingy += 1
            self.abilities2.append(storageList)
