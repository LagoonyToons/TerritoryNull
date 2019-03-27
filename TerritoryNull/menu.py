import pygame as pg
from options import *
from my_game import *
from highscore import *
from selectionScreen import *
class Menu:
    def __init__(self, screen, music, strip, joystick):
        self.strip = strip
        self.strip.started = False
        self.strip.state = "rainbow"
        self.joystick=joystick
        self.music = music
        self.running = True
        self.screen = screen
        self.loadImages()
        self.location1 = (SCREEN_X/2-150, SCREEN_Y*8/14-20)
        self.rotation = 0
        self.clock = pg.time.Clock()
        self.genStars()
        self.loop()
    def BMO(self):
        self.music.pause()
        self.strip.started = False
        self.strip.state = "rainbow"
        self.tQuit = 60
        self.soundTime = 3000
        going = True
        x =random.randint(0, 50)
        y = random.randint(0,400)
        choices = [-4, -3, 3,  4]
        xSpeed = random.choice(choices)
        ySpeed = random.choice(choices)
        while going:
            self.soundTime += 1
            if self.soundTime > 3050:
                 pg.mixer.Channel(1).play(random.choice(self.music.thread1.adventureTime))
                 self.soundTime = 0
            #self.music.songState()
            self.strip.update()
            self.tQuit -= 1
            pg.display.update()
            self.screen.fill((200,227,194))
            #self.screen.fill((0,0,0))
            x += xSpeed
            y += ySpeed
            self.screen.blit(self.BMO_IMAGE, (x, y))
            if x > SCREEN_X - 550 or x < -130:
                xSpeed *= -1
                x+= xSpeed
            if y > SCREEN_Y - 300 or y < -100:
                ySpeed *= -1
                y += ySpeed
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    going = False
                elif self.tQuit < 0 and event.type == pg.JOYBUTTONDOWN:
                    going = False
        self.music.unpause()
                             
    def loadImages(self):
        self.arrowImg = pg.image.load("image/arrow.png")
        self.logo = pg.transform.scale(pg.image.load("image/logo.png"), (SCREEN_X, SCREEN_X))
        self.BMO_IMAGE = pg.transform.scale(pg.image.load("image/BMO.png"), (SCREEN_X, round(SCREEN_X*.5)))        

        
    def loop(self):
        self.idleTimer = 0
        while self.running:
            if self.idleTimer > 400:
                self.BMO()
                self.idleTimer = 0
            self.idleTimer += 1
            self.strip.update()
            self.music.songState()
            for star in self.starList:
                star.update()
                pg.draw.circle(self.screen, (star.brightness, star.brightness, star.brightness), (star.x,star.y), star.size)
            self.screen.blit(self.logo, (0,0))
            #print("jehalksjd;flk")
            #self.rotation += 5
            #self.rotation *= -1.1
            #self.arrow = pg.transform.rotate(self.arrowImg, self.rotation)
            #self.screen.blit(self.arrow, self.location1)

            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    #return
                    self.running = False
                    self.music.thread1.going = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        selection = selectionScreen(self.screen, self.music, self.strip, self.joystick)
                        gamestate = Game(self.screen, self.music, selection.finalList, self.strip, self.joystick)
                        self.strip.clearAll()
                        highScore = HighScoreMenu(self.screen, self.music, gamestate.highScore, self.strip, self.joystick)
                        self.strip.state = "rainbow"
                        self.idleTimer = 0
                    if event.key == pg.K_q:
                        self.music.thread1.going = False
                        sys.exit()
                        pg.quit()
                        #print(gamestate.highScore)
                elif event.type == pg.JOYBUTTONDOWN:
                    self.idleTimer = 0
                    if self.joystick.get_button(2):
                        selection = selectionScreen(self.screen, self.music, self.strip, self.joystick)
                        gamestate = Game(self.screen, self.music, selection.finalList, self.strip, self.joystick)
                        self.strip.clearAll()
                        highScore = HighScoreMenu(self.screen, self.music, gamestate.highScore, self.strip, self.joystick)
                        self.strip.state = "rainbow"
                    if self.joystick.get_button(4):
                        self.music.volumeToggle()
                    if self.joystick.get_button(6):
                        self.music.switchSong()
                    if self.joystick.get_button(8):
                        if self.strip.enabled:
                            self.strip.enabled = False
                        else:
                            self.strip.enabled = True
                    if self.joystick.get_button(10):
                        self.BMO()
           # fps = basicFont.render(str(int(self.clock.get_fps())), True, pg.Color("blue"))
            #self.screen.blit(fps, (500, 0))
           # fps = basicFont.render(str(self.idleTimer), True, pg.Color("green"))
           #self.screen.blit(fps, (50, SCREEN_Y/1.2))
            credit = descriptionFont.render("Programming: Logan Wrinkle", True, pg.Color("blue"))
            self.screen.blit(credit, (10, SCREEN_Y-120))
            credit = descriptionFont.render("Art: Vicky Chakpuang", True, pg.Color("blue"))
            self.screen.blit(credit, (10, SCREEN_Y-90))
            credit = descriptionFont.render("Arcade Design: Noah Miller", True, pg.Color("blue"))
            self.screen.blit(credit, (10, SCREEN_Y-60))
            pg.display.update()
            self.screen.fill(pg.Color("black"))
            self.clock.tick(50)
    def genStars(self):
                    self.starList = []
                    for x in range(450):
                        locx = random.randint(0, SCREEN_X)
                        locy = random.randint(0, SCREEN_Y)
                        self.starList.append(Star(locx, locy))
                
                    
            

class Star:
    def  __init__(self, x, y):
        self.brightness = random.randint(60, 255)
        self.changeRate = random.randint(3, 10)
        self.size = random.randint(1, 4)
        self.x = x
        self.y = y
        self.speed = random.randint(0, 2)
    def update(self):
        self.brightness += self.changeRate
        if self.brightness > 255or self.brightness < 60:
            self.changeRate *= -1
            self.brightness += self.changeRate
        
        self.y += self.speed
        
        if self.y > SCREEN_Y:
            self.y = 0
