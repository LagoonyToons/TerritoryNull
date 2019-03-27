import pygame as pg
from options import *
import pickle
import sys

class HighScoreMenu:
    def __init__(self, screen, music, score, strip, joystick):
        self.strip = strip
        self.strip.started = False
        self.strip.state = "chain"
        self.score = score[0]
        self.screen = screen
        self.music = music
        self.indexes = [1, 3, 5, 7, 9]
        self.joystick = joystick
        self.timer = 30
        self.genStars()

        try:
            with open("High_Scores.txt", "rb") as f:
                self.highscores = pickle.load(f)
                f.close()
        except:
            self.highscores = ["aaaa", 10, "bbbb", 8, "cccc", 6, "dddd", 4, "eeee", 2]

        self.modifyHighscores()
        self.loop()



    def loop(self):
        while True:
            self.timer -= 1
            self.strip.update((0,0,100))
            self.music.songState()
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    return
                elif event.type == pg.JOYBUTTONDOWN:
                    if self.joystick.get_button(4):
                        self.music.volumeToggle()
                    if self.joystick.get_button(6):
                        self.music.switchSong()
                    if self.joystick.get_button(8):
                        if self.strip.enabled:
                            self.strip.enabled = False
                        else:
                            self.strip.enabled = True
                if self.joystick.get_button(2) and self.timer <= 0:
                    return
            self.starBlit()
            text = basicFont.render(str(self.highscores[0]) + " : " + str(self.highscores[1]), True, pg.Color("royalblue"))
            self.screen.blit(text,(SCREEN_X/4, SCREEN_Y*2/8))
            text = basicFont.render(str(self.highscores[2]) + " : " + str(self.highscores[3]), True, pg.Color("green"))
            self.screen.blit(text,(SCREEN_X/4, SCREEN_Y*3/8))
            text = basicFont.render(str(self.highscores[4]) + " : " + str(self.highscores[5]), True, pg.Color("yellow"))
            self.screen.blit(text,(SCREEN_X/4, SCREEN_Y*4/8))
            text = basicFont.render(str(self.highscores[6]) + " : " + str(self.highscores[7]), True, pg.Color("orange"))
            self.screen.blit(text,(SCREEN_X/4, SCREEN_Y*5/8))
            text = basicFont.render(str(self.highscores[8]) + " : " + str(self.highscores[9]), True, pg.Color("red"))
            self.screen.blit(text,(SCREEN_X/4, SCREEN_Y*6/8))
            text = basicFont.render("Your Score:   " + str(self.score), True, pg.Color("magenta"))
            self.screen.blit(text,(SCREEN_X/8, 100))
            pg.display.update()
            self.screen.fill(pg.Color("black"))

    def modifyHighscores(self):
        for x in self.indexes:
            if self.score > self.highscores[x]:
                playerName = self.findPlayerName()
                self.highscores.insert((x-1), playerName)
                self.highscores.insert(((x)), self.score)
                del self.highscores[10]
                del self.highscores[10]
                with open("High_Scores.txt", "wb") as f:
                    f.truncate(0)
                    pickle.dump(self.highscores, f, pickle.HIGHEST_PROTOCOL)
                    f.close()
                for x in self.highscores:
                    print(x)
                break

    def findPlayerName(self):
        self.done = False
        self.initTimer = 20
        self.letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
             'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', "u", "v", "w", "x", "y", "z",
             "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " "]
        self.letter1 = self.letter2 = self.letter3 = self.letter4 = self.letters
        self.numpos1 = self.numpos2 = self.numpos3 = self.numpos4 = 0
        self.cursorpos = 0
        self.name = [self.letter1, self.letter2, self.letter3, self.letter4]
        while not self.done:
            self.initTimer -= 1
            self.strip.update((0,0,100))
            self.music.songState()
            self.eventHandler()

            self.name = "".join([str(self.letter1[self.numpos1]), str(self.letter2[self.numpos2]), str(self.letter3[self.numpos3]), str(self.letter4[self.numpos4])])
            rect=(80+self.cursorpos*140, 150, 130, 200)
            pg.draw.rect(self.screen, pg.Color("grey"), rect)
            text = basicFont.render(str(self.letter1[self.numpos1]), True, pg.Color("blue"))
            self.screen.blit(text,(80, SCREEN_Y*3/14))
            text = basicFont.render(str(self.letter2[self.numpos2]), True, pg.Color("blue"))
            self.screen.blit(text,(220, SCREEN_Y*3/14))
            text = basicFont.render(str(self.letter3[self.numpos3]), True, pg.Color("blue"))
            self.screen.blit(text,(360, SCREEN_Y*3/14))
            text = basicFont.render(str(self.letter4[self.numpos4]), True, pg.Color("blue"))
            self.screen.blit(text,(500, SCREEN_Y*3/14))
            pg.display.update()
            self.screen.fill(pg.Color("black"))
        self.name = "".join([str(self.letter1[self.numpos1]), str(self.letter2[self.numpos2]), str(self.letter3[self.numpos3]), str(self.letter4[self.numpos4])])
        print(self.name)
        return self.name

    def eventHandler(self):
        events = pg.event.get()
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.done = True
                if event.key == pg.K_DOWN:
                    if self.cursorpos == 0:
                        self.numpos1 -= 1
                        if self.numpos1 < 0:
                            self.numpos1 = 36
                    elif self.cursorpos == 1:
                        self.numpos2 -= 1
                        if self.numpos2 < 0:
                            self.numpos2 = 36
                    elif self.cursorpos == 2:
                        self.numpos3 -= 1
                        if self.numpos3 < 0:
                            self.numpos3 = 36
                    elif self.cursorpos == 3:
                        self.numpos4 -= 1
                        if self.numpos4 < 0:
                            self.numpos4 = 36
                            #name[cursorpos] -= 1
                if event.key == pg.K_UP:
                    if self.cursorpos == 0:
                        self.numpos1 += 1
                        if self.numpos1 > 36:
                            self.numpos1 = 0
                    elif self.cursorpos == 1:
                        self.numpos2 += 1
                        if self.numpos2 > 36:
                            self.numpos2 = 0
                    elif self.cursorpos == 2:
                        self.numpos3 += 1
                        if self.numpos3 > 36:
                            self.numpos3 = 0
                    elif self.cursorpos == 3:
                        self.numpos4 += 1
                        if self.numpos4 > 36:
                            self.numpos4 = 0
                if event.key == pg.K_LEFT:
                    self.cursorpos -= 1
                    if self.cursorpos < 0:
                        self.cursorpos = 3
                if event.key == pg.K_RIGHT:
                    self.cursorpos += 1
                    if self.cursorpos > 3:
                        self.cursorpos = 0
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            elif event.type == pg.JOYBUTTONDOWN:
                if self.joystick.get_button(4):
                    self.music.volumeToggle()
                if self.joystick.get_button(6):
                    self.music.switchSong()
                if self.joystick.get_button(8):
                    if self.strip.enabled:
                        self.strip.enabled = False
                    else:
                        self.strip.enabled = True
                if self.joystick.get_button(2) and self.initTimer <= 0:
                    self.done = True
            if self.joystick.get_axis(0) > 0 and self.initTimer <= 0:
                self.initTimer = 15
                self.cursorpos -= 1
                if self.cursorpos < 0:
                    self.cursorpos = 3
            if self.joystick.get_axis(0) < 0 and self.initTimer <= 0:
                self.initTimer = 15
                self.cursorpos += 1
                if self.cursorpos > 3:
                    self.cursorpos = 0
            if self.joystick.get_axis(1) < 0 and self.initTimer <= 0:
                self.initTimer = 15
                if self.cursorpos == 0:
                    self.numpos1 -= 1
                    if self.numpos1 < 0:
                        self.numpos1 = 36
                elif self.cursorpos == 1:
                    self.numpos2 -= 1
                    if self.numpos2 < 0:
                        self.numpos2 = 36
                elif self.cursorpos == 2:
                    self.numpos3 -= 1
                    if self.numpos3 < 0:
                        self.numpos3 = 36
                elif self.cursorpos == 3:
                    self.numpos4 -= 1
                    if self.numpos4 < 0:
                        self.numpos4 = 36
            if self.joystick.get_axis(1) > 0 and self.initTimer <= 0:
                self.initTimer = 15
                if self.cursorpos == 0:
                    self.numpos1 += 1
                    if self.numpos1 > 36:
                        self.numpos1 = 0
                elif self.cursorpos == 1:
                    self.numpos2 += 1
                    if self.numpos2 > 36:
                        self.numpos2 = 0
                elif self.cursorpos == 2:
                    self.numpos3 += 1
                    if self.numpos3 > 36:
                        self.numpos3 = 0
                elif self.cursorpos == 3:
                    self.numpos4 += 1
                    if self.numpos4 > 36:
                        self.numpos4 = 0
            

    def starBlit(self):
        for star in self.screen_1_rects:
            pg.draw.circle(self.screen, pg.Color("snow"),
                           (star[0], round(star[1])), star[2])
            #print(star[0][1])
            star[1] += .8
            if star[1] >= SCREEN_Y:
                star[1] = 0
        for star in self.screen_2_rects:
            pg.draw.circle(self.screen, pg.Color("snow"),
                           (star[0], round(star[1])), star[2])
            star[1] += 1
            if star[1] >= SCREEN_Y:
                star[1] = 0
        for star in self.screen_3_rects:
            pg.draw.circle(self.screen, pg.Color("snow"),
                           (star[0], round(star[1])), star[2])
            star[1] += 1.5
            if star[1] >= SCREEN_Y:
                star[1] = 0

    def genStars(self):
        self.screen_1_rects = []
        self.screen_2_rects = []
        self.screen_3_rects = []
        for x in range(120):
            holder = []
            holder.append(random.randint(0, SCREEN_X))
            holder.append(random.randint(0, SCREEN_Y))
            holder.append(
                random.choice([
                    1,
                    1,
                    2,
                    2,
                    2,
                    3,
                    3,
                    3,
                    3,
                    3,
                    4,
                    4,
                ]))
            #pg.draw.circle(self.screen, silver, (rand_x, rand_y), randSize)
            self.screen_1_rects.append(holder)
        for x in range(120):
            holder = []
            holder.append(random.randint(0, SCREEN_X))
            holder.append(random.randint(0, SCREEN_Y))
            holder.append(
                random.choice(
                    [1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4]))
            #pg.draw.circle(self.screen, silver, (rand_x, rand_y), randSize)
            self.screen_2_rects.append(holder)
        for x in range(120):
            holder = []
            holder.append(random.randint(0, SCREEN_X))
            holder.append(random.randint(0, SCREEN_Y))
            holder.append(
                random.choice(
                    [1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4]))
            #pg.draw.circle(self.screen, silver, (rand_x, rand_y), randSize)
            self.screen_3_rects.append(holder)
