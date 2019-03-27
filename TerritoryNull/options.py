import os.path
import os
import pygame as pg
import threading
import random
SCREEN_X, SCREEN_Y = (720, 1280)
pg.font.init()
basicFont = pg.font.Font('ARCADE_N.TTF', 18)
descriptionFont = pg.font.Font('ARCADE_N.TTF', 8)


# simple version for working with CWD
class songThread(threading.Thread):
    def __init__(self, threadID, name, songList):
        self.initializedSongs = []
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.going = True
        self.name = name
        self.songList = songList
        self.adventureTime = [pg.mixer.Sound("egg/1.ogg"), pg.mixer.Sound("egg/2.ogg"), pg.mixer.Sound("egg/3.ogg")]
    def stop(self):
        threading.Event.set()
    def run(self):
        #beginning_time = time.time()
        for item in self.songList:
            if ".ogg" in item:
                if self.going:
                    self.initialized_song = pg.mixer.Sound(item)
                    self.initializedSongs.append(self.initialized_song)
            #print("Song initialized, terminating process")
        # print("Loading Complete")
        # end_time = time.time()
        # completion_time = end_time - beginning_time
        # print(str(completion_time) + " Seconds  " + self.name + " Complete")
# class Song():
#     def __init__(self, path, name, creator):
#         self.path = path
#         self.name = name
#         self.creator = creator
#songList = ['sounds/as.ogg', 'sounds/pwt.ogg', 'sounds/hellfire.ogg', 'sounds/duckTales.ogg', 'sounds/afterBurn.ogg', 'sounds/kats.ogg',
            #'sounds/kirby.ogg', 'sounds/mappy.ogg', 'sounds/megaDrive.ogg', 'sounds/ninjaGaiden.ogg',
             #'sounds/powerRangers.ogg', 'sounds/shinobi.ogg', 'sounds/egyptian.ogg', 'sounds/megalovania.ogg',
             #'sounds/megaMan.ogg', 'sounds/numberone.ogg', 'sounds/OPM.ogg', 'sounds/PunchOut.ogg', 'sounds/safetyDance.ogg',
             #'sounds/Skyhawk.ogg', 'sounds/soulEater.ogg', 'sounds/spiderMan.ogg', 'sounds/TankEngine.ogg',
             #'sounds/WagonWheel.ogg', 'sounds/zelda.ogg', 'sounds/bonetrousle.ogg', 'sounds/allstar.ogg']
class Start:
    def __init__(self):
        self.songList = []
        for item in os.listdir("sounds/"):
            try:
                self.songList.append("sounds/" + item)
            except:
                print(item + " Could not be loaded")
        self.thread1 = songThread(1, "Thread-1", self.songList)
        self.thread1.start()
        self.volume = 1

        # self.currentsong = random.choice(self.thread1.initializedSongs)
        # self.currentsongI = self.thread1.initializedSongs.index(self.currentsong)
        # self.pg.mixer.Channel(0).play(self.currentsong)
    def songState(self):
        if not pg.mixer.Channel(0).get_busy():
            if len(self.thread1.initializedSongs) > 0:
                self.currentsong = random.choice(self.thread1.initializedSongs)
                self.currentsongI = self.thread1.initializedSongs.index(self.currentsong)
                pg.mixer.Channel(0).play(self.currentsong)
        
    def volumeToggle(self):
        if self.volume == 0:
            pg.mixer.Channel(0).set_volume(1)
            self.volume = 1
        elif self.volume == 1:
            pg.mixer.Channel(0).set_volume(0)
            self.volume = 0
            
    def switchSong(self):
        self.currentsong = random.choice(self.thread1.initializedSongs)
        self.currentsongI = self.thread1.initializedSongs.index(self.currentsong)
        pg.mixer.Channel(0).play(self.currentsong)

    def returnInitializedSongs(self):
        return self.thread1.initializedSongs
    
    def pause(self):
        pg.mixer.Channel(0).pause()
    def unpause(self):
        pg.mixer.Channel(0).unpause()

    # while True: # main game loop
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             pg.quit()
    #             sys.exit()
    #         if event.type == pg.KEYDOWN:
    #             if event.key == pg.K_SPACE:
    #                 try:
                    # except:
                    #     "failed to complete task"
                # if event.key == pg.K_a:
                #     try:
                #         if volume <= 1:
                #             volume += .1
                #             pg.mixer.Channel(0).set_volume(volume)
                #     except:
                #         pass
                # if event.key == pg.K_s:
                #     try:
                #         if volume >= 0:
                #             volume -= .1
                #             pg.mixer.Channel(0).set_volume(volume)
                #     except:
                #         pass
    # if not pg.mixer.Channel(0).get_busy():
    #     try:
    #         currentsong = random.choice(initializedSongs)
    #         currentsongI = initializedSongs.index(currentsong)
    #         pg.mixer.Channel(0).play(currentsong)
    #     except:
                # pass
        # display.fill(pg.Color('black'))
        # if len(initializedSongs) > 0:
            # creator = font.render(songList[currentsongI].creator, True, pg.Color("white"))
            # songName = font.render(songList[currentsongI].name, True, pg.Color("white"))
            # display.blit(creator, (75, 75))
            # display.blit(songName, (100, 100))
        # fps = font.render(str(int(clock.get_fps())), True, pg.Color("white"))
        # display.blit(fps, (50, 50))
        # pg.display.update()
        # clock.tick()
