import time
from neopixel import *

LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 200     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


class Led(Adafruit_NeoPixel):
    def __init__(self, rangesList,  LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL):
        super().__init__(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.state = "default"

        self.perimeter_led_range = (rangesList[0], rangesList[1])
        self.perimeterCount = rangesList[1] - rangesList[0]

        self.left_vBar = (rangesList[2], rangesList[3])
        self.left_vBar_count = rangesList[3] - rangesList[2]

        self.right_vBar = (rangesList[4], rangesList[5])
        self.right_vBar_count = rangesList[5] - rangesList[4]

        self.left_hBar = (rangesList[6], rangesList[7])
        self.left_hBar_count = rangesList[7] - rangesList[6]

        self.right_hBar = (rangesList[8], rangesList[9])
        self.right_hBar_count = rangesList[9] - rangesList[8]

        self.layersList = [Color(0,0,0),Color(0,200,127),Color(255,255,0),Color(0,0,255),Color(255,0,0)]
        self.instructions = self.createRainbowList()
        self.started = False
        self.color = (0,0,0)
        
        self.enabled = True

    def update(self, color=(0,0,255), player="null", color2 = (0,0,255)):
        if self.enabled:
            if self.state == "default":
                self.default(color)
            if self.state == "chain":
                self.chain(color)
            if self.state == "flicker":
                self.flicker(color) 
            if self.state == "rainbow":
                self.rainbow()
            if self.state =="alternate":
                self.alternate(color, color2)
                #print("buffalo")
            #print(self.state)
        else:
            self.default((0,0,0))
        self.show()

    def updateHP(self, player):
        layers = int(player.hp/self.right_vBar_count)
        remainder = player.hp-(layers*self.right_vBar_count)
        for x in range(self.right_vBar_count):
            try:
                if remainder > x:
                    color = self.layersList[layers+1]
                else:
                    color = self.layersList[layers]
            except:
                color = Color(255, 255, 255)
            self.setPixelColor(x+self.right_vBar[0], color)


    def updateFuel(self, player):
        fuelRatio = player.fuel/player.maxFuel
        if fuelRatio > .35:
            for x in range(self.left_vBar_count):
                if 1/self.left_vBar_count <= fuelRatio - ((1/self.left_vBar_count)*x):
                    color = (255,0,0)
                elif 1/self.left_vBar_count <= fuelRatio - ((1/self.left_vBar_count)*(x-1)):
                    color = (255, 165, 0)
                else:
                    color = (0,0,0)
                self.setPixelColor(x+self.left_vBar[0], Color(color[0], color[1], color[2]))
        else:
            for x in range(self.left_vBar_count):
                if 1/self.left_vBar_count <= fuelRatio - ((1/self.left_vBar_count)*x):
                    color = (0,255,0)
                elif 1/self.left_vBar_count <= fuelRatio - ((1/self.left_vBar_count)*(x-1)) and player.fuel > 0:
                    color = (0, 255, 80)
                else:
                    color = (0,0,0)
                self.setPixelColor(x+self.left_vBar[0], Color(color[0], color[1], color[2]))

    def updateAbility(self, player):
        percentage = (player.abilityDelay+player.timeStopIncreaseToCooldown - player.abilityTimer[0]) / (player.abilityDelay+player.timeStopIncreaseToCooldown)
        for x in range(self.left_hBar_count):
            if percentage >= 1:
                color = (255,0,0)
            else:
                share = 1/self.left_hBar_count
                if percentage - ((x)*share) > 0:
                    color = (0,0,255)
                elif percentage-((x-1)*share) > 0:
                    color = (0,0,abs(round(255*(1-abs(self.left_hBar_count*((percentage-(x*share))))))))
                    #print(color)
                else:
                    #percentageToFull = percentage - ((1/self.left_hBar_count)*x)/(1/self.left_hBar_count)
                    color = (0,0, 0)
                    #print("jello")
            #print(color)
            self.setPixelColor(x+self.left_hBar[0], Color(abs(color[0]), abs(color[1]), color[2]))

    def updateGun(self, player):
        percentage = ((player.abilityDelay2 - player.abilityTimer2[0]) /player.abilityDelay2)
        for x in range(self.right_hBar_count):
            if percentage >= 1:
                color = (255,0,0)
            else:
                share = 1/self.right_hBar_count
                if percentage - ((x)*share) > 0:
                    color = (0,0,255)
                elif percentage-((x-1)*share) > 0:
                    color = (0,0,abs(round(255*(1-abs(self.right_hBar_count*((percentage-(x*share))))))))
                    #print(color)
                else:
                    #percentageToFull = percentage - ((1/self.left_hBar_count)*x)/(1/self.left_hBar_count)
                    color = (0,0, 0)
                    #print("jello")
            #print(color)
            self.setPixelColor(x+self.right_hBar[0], Color(abs(color[0]), abs(color[1]), color[2]))
    def clearAll(self):
        for x in range(150):
            self.setPixelColor(x, Color(0,0,0))

    def default(self, color=[255,0,0]):
        for x in range(self.perimeterCount):
            self.setPixelColor(x, Color(color[0], color[1], color[2]))

    def chain(self, color=[127, 0, 0], amount=4):
        if not self.started:
            self.pointList = []
            for x in range(amount):
                item = round(x/amount*self.perimeterCount)
                self.pointList.append(item)
            self.started = True
        for x in range(self.perimeterCount):
            if x in self.pointList:
                self.setPixelColor(x, Color(color[0], color[1], color[2]))
            else:
                self.setPixelColor(x, Color(0, 0, 0))
        for x in range(len(self.pointList)):
            #print(self.pointList)
            self.pointList[x] += 1
            #print(self.pointList)
            if self.pointList[x] > self.perimeterCount:
                self.pointList[x] = 0
                
    def flicker(self, color=(255, 127, 0), fadeoutTicks=400):
        if not self.started:
            self.red = color[0]
            self.green = color[1]
            self.blue = color[2]
            self.red = 0
            self.green = 120
            self.blue = 255
            #self.color = color
            self.fadeTimer = fadeoutTicks
            #print(self.fadeTimer)
            self.currentTimer = 0
            #self.totalPixel = color[0]+color[1]+color[2]
            self.rDecrease = self.red/self.fadeTimer
            self.gDecrease = self.green/self.fadeTimer
            self.bDecrease = self.blue/self.fadeTimer
            #print(self.red)
            #print(color[1])
            #print(color[1]/self.fadeTimer)
            self.started = True
        for x in range(self.perimeterCount):
            #self.setPixelColor(x, Color(self.instructions[x][0], self.instructions[x][1], self.instructions[x][2]))
            self.setPixelColor(x, Color(round(self.red), (round(self.green)), (round(self.blue))))
        if self.currentTimer < self.fadeTimer:
            self.currentTimer += 1
            self.red -= self.rDecrease
            self.green -= self.gDecrease
            self.blue -= self.bDecrease
            #print(self.green)
            #print(self.gDecrease)
        elif self.red >= 255 or self.green >= 255 or self.blue >= 255:
            self.currentTimer = 0
        elif self.red < 255  or self.green < 255 or self.blue < 255:
            #print(self.red)
            self.red += self.rDecrease
            #print(self.red)
            self.green += self.gDecrease
            self.blue += self.bDecrease
        #print(self.currentTimer)
        if self.red < 0:
            self.red = 0 
        if self.red > 255:
            self.red = 255
        if self.blue < 0:
            self.blue = 0 
        if self.blue > 255:
            self.blue = 255
        if self.green < 0:
            self.green = 0 
        if self.green > 255:
            self.greens = 255
        
    def rainbow(self):
        if not self.started:
            self.instructions = self.createRainbowList()
            self.started = True
        for x in range(self.perimeterCount):
            #print(self.instructions[x])
            self.setPixelColor(x, Color(self.instructions[x][0], self.instructions[x][1], self.instructions[x][2]))
        self.instructions += [self.instructions.pop(0)]
        

    def createRainbowList(self):
        #print(self.perimeterCount)
        changeAmount = 255*12/self.perimeterCount
        generatedList = []
        red = 255
        green = 0
        blue = 0
        #print(color, red, green, blue)
        for x in range(self.perimeterCount):
            color = (round(red), round(green), round(blue))
            generatedList.append(color)
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
        #print(generatedList)
        return generatedList
    def alternate(self, color=(0,255,0), color2 = (0,255,0), thimeBetween=25):
            if not self.started:
                self.color = color
                self.color2 = color2
                self.timeBetween = thimeBetween
                self.currentTimer = 0
                self.stateThing = 0
                self.started = True
                #print("beb")
     
            #print("doge")
            #print(self.timeBetween)
            self.currentTimer += 1
            #print(self.timeBetween)
            #print(self.timeBetween)
            if self.timeBetween < self.currentTimer:
                self.currentTimer = 0
                if self.stateThing == 0:
                    self.stateThing = 1
                    #print("dumb")
                else:
                    self.stateThing = 0
            for x in range(self.perimeterCount):
                if self.stateThing:
                    if x % 2 == 0:
                        self.setPixelColor(x, Color(self.color[0], self.color[1], self.color[2]))
                    else:
                        self.setPixelColor(x, Color(0,0,0))
                    #print("ro[s")
                else:
                    if x % 2 != 0:
                        self.setPixelColor(x, Color(self.color2[0], self.color2[1], self.color2[2]))
                    else:
                        self.setPixelColor(x, Color(0,0,0))
            #print(self.currentTimer)
            
                
    
    