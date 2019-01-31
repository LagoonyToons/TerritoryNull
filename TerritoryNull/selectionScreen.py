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
        self.loadImages()
        self.genStats()
        self.loop()

    def loop(self):
        self.done = False
        #0-4 final; 0-3 for now (without ability selection)
        self.cursorpos = 0
        self.arrowFlipX = SCREEN_X/2-120
        self.arrowX = SCREEN_X/2+60
        self.offset = 30
        self.finalList = [self.tops[0], self.mids[0], self.bots[0]]
        self.place = [0,0,0]
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
                            self.place[self.cursorpos] = 2
                        self.finalList[self.cursorpos] = self.tops[self.place[self.cursorpos]]
                    elif self.cursorpos == 1:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0 :
                            self.place[self.cursorpos] = 2
                        self.finalList[self.cursorpos] = self.mids[self.place[self.cursorpos]]
                    elif self.cursorpos == 2:
                        self.place[self.cursorpos] -= 1
                        if self.place[self.cursorpos] < 0 :
                            self.place[self.cursorpos] = 2
                        self.finalList[self.cursorpos] = self.bots[self.place[self.cursorpos]]

                elif event.key == pg.K_RIGHT:
                    if self.cursorpos == 0:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > 2 :
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.tops[self.place[self.cursorpos]]
                    elif self.cursorpos == 1:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > 2 :
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.mids[self.place[self.cursorpos]]
                    elif self.cursorpos == 2:
                        self.place[self.cursorpos] += 1
                        if self.place[self.cursorpos] > 2 :
                            self.place[self.cursorpos] = 0
                        self.finalList[self.cursorpos] = self.bots[self.place[self.cursorpos]]

                elif event.key == pg.K_UP:
                    self.cursorpos -= 1
                    if self.cursorpos < 0:
                        self.cursorpos = 3

                elif event.key == pg.K_DOWN:
                    self.cursorpos += 1
                    if self.cursorpos > 3:
                        self.cursorpos = 0

                elif event.key == pg.K_SPACE and self.cursorpos == 3:
                    self.done = True
    
    def blitImages(self):
        rect=(SCREEN_X/2-40, 150+(80*self.cursorpos-1) + (self.offset*self.cursorpos), 90, 90)
        pg.draw.rect(self.screen, pg.Color("grey"), rect)
        for x in range(len(self.finalList)):
            self.screen.blit(self.finalList[x][3], (SCREEN_X/2-40, 150+(80*x-1) + (self.offset*x)))
        for x in range(4):
            self.screen.blit(self.arrow, (self.arrowX, 150 + (80*x-1) + (35*x)))
            self.screen.blit(self.arrowFlip, (self.arrowFlipX, 150 + (80*x-1) + (35*x)))
        text = basicFont.render("START!", True, pg.Color("green"))
        self.screen.blit(text, (SCREEN_X/2-40, 150+(80*3-1) + (self.offset*3)))
        pg.display.update()
        self.screen.fill(pg.Color("black"))

    def loadImages(self):
        #self.loadedImages = []
        self.topImages = []
        self.midImages = []
        self.botImages = []
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

        self.arrow = pg.transform.scale(pg.image.load("image/arrow.png"), (64, 64))
        self.arrowFlip = pg.transform.rotate(self.arrow, 180)

    def genStats(self):
        count = 0
        self.tops = []
        self.bots = []
        self.mids = []
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

