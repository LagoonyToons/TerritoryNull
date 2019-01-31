import pygame as pg
from options import *
from game import *
from highscore import *
from selectionScreen import *
class Menu:
    def __init__(self, screen, music):
        self.music = music
        self.running = True
        self.screen = screen
        self.loadImages()
        self.location1 = (SCREEN_X/2-150, SCREEN_Y*8/14-20)
        self.rotation = 0
        self.clock = pg.time.Clock()
        self.loop()
    def loadImages(self):
        self.arrowImg = pg.image.load("image/arrow.png")

        
    def loop(self):
        while self.running:
            self.music.songState()
            #self.rotation += 5
            #self.rotation *= -1.1
            #self.arrow = pg.transform.rotate(self.arrowImg, self.rotation)
            #self.screen.blit(self.arrow, self.location1)

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    #return
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        selection = selectionScreen(self.screen, self.music)
                        gamestate = Game(self.screen, self.music, selection.finalList)
                        highScore = HighScoreMenu(self.screen, self.music, gamestate.highScore)
                        #print(gamestate.highScore)
                    
            fps = basicFont.render(str(int(self.clock.get_fps())), True, pg.Color("blue"))
            self.screen.blit(fps, (500, 0))
            fps = basicFont.render("Hey you're live", True, pg.Color("green"))
            self.screen.blit(fps, (SCREEN_X/4, SCREEN_Y/8))
            pg.display.update()
            self.screen.fill(pg.Color("black"))
            self.clock.tick(50)


