import time
import RPi.GPIO as GPIO
 
# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


class Led(Adafruit_WS2801.WS2801Pixels):
    def __init__(self, count, rangesList,  clk=None, do=None, spi=None, gpio=None):
        super.__init__(count, clk=None, do=None, spi=None, gpio=None)
        self.state = "default"

        self.perimeter_led_range = (rangesList[0], rangesList[1])
        self.perimeterCount = self.perimeter_led_range[1] - self.perimeter_led_range[0]

        self.left_vBar = (rangesList[2], rangesList[3])
        self.left_vBar_count = self.left_vBar[1] - self.left_vBar[0]

        self.right_vBar = (rangesList[4], rangesList[5])
        self.right_vBar_count = self.right_vBar[1] - self.right_vBar[0]

        self.left_hBar = (rangesList[6], rangesList[7])
        self.left_hBar_count = self.left_hBar[1] - self.left_hBar[0]

        self.right_hBar = (rangesList[8], rangesList[9])
        self.right_hBar_count = self.right_hBar[1] - self.right_hBar[0]

        self.layersList = [(0,0,0),(255,0,0),(255,255,0),(0,0,255),(0,255,0)]

        self.started = False
        self.color = (0,0,0)

    def update(self, player):
        self.clear()
        if self.state == "default":
            self.default(color)
        if self.state == "chain":
            self.chain(color)
        if self.state == "flicker":
            self.flicker(color) 
        if self.state == "rainbow":
            self.rainbow()

        self.updateAbility(player)
        self.updateGun(player)
        self.updateFuel(player)
        self.updateHP(player)

        self.show()

    def updateHP(self, player):
        layers = int(player.hp/self.right_vBar_count)
        remainder = player.hp-layers
        for x in self.right_vBar_count:
            if remainder > x:
                color = self.layersList[layers]
            else:
                color = self.layersList[layers-1]
            self.set_pixel(x+self.right_vBar[0], self.RGB_to_color(color))


    def updateFuel(self, player):
        fuelRatio = player.fuel/player.maxFuel
        if fuelRatio > .35:
            for x in self.left_vBar_count:
                if 1/self.left_hBar_count <= fuelRatio - ((1/self.left_hBar_count)*x):
                    color = (255,165,0)
                else:
                    color = (0,0,0)
                self.set_pixel(x+self.left_vBar[0], self.RGB_to_color(color))
        else:
            for x in self.left_vBar_count:
                if 1/self.left_hBar_count <= fuelRatio - ((1/self.left_hBar_count)*x):
                    color = (255,0,0)
                else:
                    color = (0,0,0)
                self.set_pixel(x+self.left_vBar[0], self.RGB_to_color(color))

    def updateAbility(self, player):
        percentage = (player.abilityDelay+player.timeStopIncreaseToCooldown - player.abilityTimer[0]) / (player.abilityDelay+player.timeStopIncreaseToCooldown)
        for x in self.left_hBar_count:
            if percentage >= 1:
                color = (0,255,0)
            else:
                if 1/self.left_hBar_count <= percentage - ((1/self.left_hBar_count)*x):
                    color = (0,0,255)
                else:
                    percentageToFull = percentage - ((1/self.left_hBar_count)*x)/(1/self.left_hBar_count)
                    color = (round(255*percentageToFull), round(255*percentageToFull), 0)
            self.set_pixel(x+self.left_hBar[0], self.RGB_to_color(color))

    def updateGun(self, player):
        percentage = ((player.abilityDelay2 - player.abilityTimer2[0]) /player.abilityDelay2)
        for x in self.right_hBar_count:
            if percentage >= 1:
                color = (0,255,0)
            else:
                if 1/self.right_hBar_count <= percentage - ((1/self.right_hBar_count)*x):
                    color = (0,0,255)
                else:
                    percentageToFull = percentage - ((1/self.right_hBar_count)*x)/(1/self.right_hBar_count)
                    color = (round(255*percentageToFull), round(255*percentageToFull), 0)
            self.set_pixel(xself.right_hBar[0], self.RGB_to_color(color))


    def default(self, color=[255,0,0]):
        for x in self.perimeterCount:
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



