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
        if self.state == "rainbow":
            self.rainbow()
        self.show()

    def default(self, color=[255,0,0]):
        for x in self.count():
            self.set_pixel(x, self.RGB_to_color(color))

    def chain(self, color=[255, 0, 0]):
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

    def flicker(self, color=[255, 0, 0], fadeoutTicks=180):
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
        if self.currentTimer < self.fadeTimer:
            self.currentTimer += 1
            self.color[0] -= self.rDecrease
            self.color[1] -= self.gDecrease
            self.color[2] -= self.bDecrease
        elif self.color[0] < 255  or self.color[1] < 255 or self.color[2] < 255:
            self.color[0] -= self.rDecrease
            self.color[1] -= self.gDecrease
            self.color[2] -= self.bDecrease
        else:
            self.currentTimer = 0

        for x in range(3):
            if color[x] < 0:
                color[x] = 0 
            if color[x] > 255:
                color[x] = 255

    def rainbow(self):
        if not self.started:
            self.instructions = self.createRainbowList()
            self.started = True
        for x in range(self.count()):
            self.set_pixel(x, self.RGB_to_color(round(self.instructions[x][0]), round(self.instructions[x][1]), round(self.instructions[x][2])))
            self.instructions += [self.instructions.pop(0)]
        

   def createRainbowList(self):
        changeAmount = 255*6/self.count()
        generatedList = []
        red = 255
        green = 0
        blue = 0
        #print(color, red, green, blue)
        for x in range(count):
            color = (red, green, blue)
            putColor = (round(red), round(green), round(blue))
            generatedList.append(putColor)
            if red <= 255 and green >= 255 and blue == 0 and red > 0:
                red -= changeAmount
            elif green <= 255 and blue >= 255 and red == 0 and green > 0:
                green -= changeAmount
            elif blue <= 255 and red >= 255 and green == 0 and blue > 0:
                blue -= changeAmount
            elif red >= 255 and green <= 255 and blue == 0:
                green += changeAmount
            elif green >= 255 and blue <= 255 and red == 0:
                blue += changeAmount
            elif blue >= 255 and red <= 255 and green == 0:
                red += changeAmount
            if red > 255:
                red = 255
            if green > 255:
                green = 255
            if blue > 255:
                blue=255
            if red < 0:
                red=0
            if green < 0:
                green=0
            if blue < 0:
                blue=0
        return generatedList



