import time
import RPi.GPIO as GPIO
 
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


class Led(Adafruit_WS2801.WS2801Pixels):
    def __init__(self, count, clk=None, do=None, spi=None, gpio=None):
        super.__init__(count, clk=None, do=None, spi=None, gpio=None)
        self.state = "default"
        self.started = False
        self.color = 

    def update(self):
        self.clear()
        if self.state == "default":
            self.default(color)
        if self.state == "chain":
            self.chain(color)
        if self.state == "flicker":
            self.flicker(color) 
        self.show()

    def default(self, color=(255,0,0)):
        for x in self.count():
            self.set_pixel(x, self.RGB_to_color(color))

    def chain(self, color=(255, 0, 0)):
        if not self.started:
            self.storedX = 0
            self.storedY = round(self.count/2)
            self.started = True
        for x in self.count():
            if x == self.storedX or x == self.storedY:
                self.set_pixel(x, self.RGB_to_color(color))
            else:
                self.set_pixel(x, self.RGB_to_color(0, 0, 0))
        self.storedX += 1
        self.storedY += 1
        if self.storedX > self.count():
            self.storedX = 0
        if self.storedY > self.count():
            self.storedY = 0

    def flicker(self, color=(255, 0, 0), fadeoutTicks=180):
        if not self.started:
            self.color = color
            self.fadeTimer = fadeoutTicks
            self.currentTimer = 0
            #self.totalPixel = color[0]+color[1]+color[2]
            self.rDecrease = color[0]/self.fadeTimer
            self.gDecrease = color[1]/self.fadeTimer
            self.bDecrease = color[2]/self.fadeTimer
            self.started = True
        for x in self.count():
            self.set_pixel(x, self.RGB_to_color(round(color[0]), round(color[1]), round(color[2])))

        self.currentTimer += 1
        self.color[0] -= self.rDecrease
        self.color[1] -= self.gDecrease
        self.color[2] -= self.bDecrease

        for x in range(3):
            if color[x] < 0:
                color[x] = 0 

    def rainbow(self):
        if not self.started:
            self.instructions = self.createRainbowList()
            self.started = True

    def createRainbowList(self):
        rainbowColors = [(255, 0, 0), (255, 127, 0), (255,255,0), (0,255,0), (0,0,255), (75,0,130), (143,0,255)]
        self.inbetween = self.count()/7 
        generatedList = []
        for x in range(self.count()):
            
        return generatedList



