import os
import gamemap
import textfield
import timer
import person
import statusbox
from configs import misc
import textout


class World:
    def __init__(self, stdscr, w, h, filename = -1, maps = [3, 3],
                 mapPos = -1):
        self.maps = maps
        self.w = w
        self.h = h
        if mapPos == -1:
            self.mapPos = [maps[0]/2, maps[1]/2]
        else:
            self.mapPos = mapPos
        self.softPos = [self.mapPos[0] * 200, self.mapPos[1] * 200]
        
        self.textField = textfield.Textfield(2, 6, self.w/2 - 5, self.h - 7)
        self.persons = []
        self.cheatWalkEverywhere = False

        self.statusBox = statusbox.statusBox(stdscr, w, h)
        self.stdscr = stdscr



        if filename == -1:
            # If no filename is given, I will create an empty world
            self.walkArea = 3
            self.gMaps = []
            for i in range(maps[1]):
                self.gMaps.append([])
            for i in range(maps[0]):
                for j in range(maps[0]):
                    self.gMaps[j].append(gamemap.GameMap(self.w/2 + 2, 6,
                                                         self.w/2 - 5, self.h - 8))
                    self.gMaps[j][i].pos = [(self.mapPos[0] - j) * \
                                            self.gMaps[j][i].size[0],
                                            (self.mapPos[1] - i) * \
                                            self.gMaps[j][i].size[1]]
                    self.gMaps[j][i].textField = self.textField
                    

    def getPlayerPos(self):
        return self.player.pos, self.mapPos

    def setCheatWalkEverywhere(self, newCheat):
        self.cheatWalkEverywhere = newCheat
        self.player.cheatWalkEverywhere = newCheat

    def save(self, filename):
        self.sendText("Bitte Warten, Karte wird gespeichert")
        self.draw(self.stdscr)
        try:
            os.mkdir(filename)
        except:
            pass
        i = 0
        j = 0
           
        for row in self.gMaps:
            for elem in row:
                elem.saveToFile(filename + "/map" +
                                str(i) + "_" + str(j))
                j = j + 1

            j = 0
            i = i + 1

    def load(self, filename):
        i = 0
        j = 0
        for row in self.gMaps:
            for elem in row:
                elem.loadFromFile(filename + "/map" + str(i) + "_" + str(j))
                j = j + 1
            j = 0
            i = i + 1
        self.redrawAllMaps()
        importString = "import " + filename + " as curLevel"
        importCode = compile(importString, filename + "/rules.py", "single")
        exec(importCode)
        self.curLevel = curLevel
        curLevel.start(self)

    def addPerson(self, person):
        person.gMap = self.gMaps[self.mapPos[0]][self.mapPos[1]]
        person.tf = self.textField
        self.persons.append(person)
    
    def resize(self, w, h):
        self.w = w
        self.h = h
        self.textField.resize(self.w/2 - 5, self.h - 7)
        for i in range(self.maps[1]):
            for j in range(self.maps[0]):
                self.gMaps[j][i].resize(self.w/2 + 2, 6,
                                        self.w/2 - 5, self.h - 8)
        self.statusBox.resize(w, h)

    def setMapPos(self, x, y):
        for i in range(self.maps[1]):
            for j in range(self.maps[0]):
                self.gMaps[j][i].pos = [-j * self.player.gMap.size[0] + x,
                                        -i * self.player.gMap.size[1] + y]
#        self.mapPos = [x / self.player.gMap.size[0],
#                       y / self.player.gMap.size[1]]
        self.softPos = [x, y]

#        self.mapPos = [(self.player.gMap.size[0] - x) / \
#                    self.player.gMap.size[0],
#                    (self.player.gMap.size[1] - y) / \
#                    self.player.gMap.size[1]]
#        self.softPos = [(self.player.gMap.size[0] - x) % \
#                        self.player.gMap.size[0],
#                        (self.player.gMap.size[1] - y) % \
#                        self.player.gMap.size[1]]
            
    def setPlayer(self, player):
        self.player = player
        player.tf = self.textField
        player.gMap = self.gMaps[self.mapPos[0]][self.mapPos[1]]

    # TODO: Same code four times - that's bad -.- (playerGo...)

    def redrawAllMaps(self):
        for i in range(self.mapPos[1] - 1, self.mapPos[1] + 2):
            for j in range(self.mapPos[0] - 1, self.mapPos[0] + 2):
                self.gMaps[j][i].drawAllFlag = True

    def jumpPlayerTo(self, x, y, mx, my):
        self.player.pos = [x, y]
        self.player.mapPos = [mx, my]
        self.player.gMap = self.gMaps[mx][my]


    def playerGoRight(self):
        self.player.gMap.drawPos.append([self.player.pos[0], self.player.pos[1]])


        if self.player.pos[0] >= (self.player.gMap.size[1] - 1):
            self.mapPos = [self.mapPos[0] + 1, self.mapPos[1]]
            self.player.gMap = self.gMaps[self.mapPos[0]][self.mapPos[1]]
            self.player.pos[0] = self.player.pos[0] - self.player.gMap.size[0]
            if misc.DEBUG == True:
                self.textField.sendText("DEBUG: Changed Map")
        if ((self.player.gMap.size[0] * self.mapPos[0] +
             self.player.pos[0]) - self.softPos[0]) > self.walkArea:
            self.setMapPos(self.softPos[0] + 1, self.softPos[1])
            self.redrawAllMaps()
        self.player.goRight()
        try:
            self.curLevel.playerMoved()
        except:
            pass

    def playerGoLeft(self):
        self.player.gMap.drawPos.append([self.player.pos[0], self.player.pos[1]])

        if self.player.pos[0] <= 0:
            self.mapPos = [self.mapPos[0] - 1, self.mapPos[1]]
            self.player.gMap = self.gMaps[self.mapPos[0]][self.mapPos[1]]
            self.player.pos[0] = self.player.pos[0] + self.player.gMap.size[0]
            if misc.DEBUG == True:
                self.textField.sendText("DEBUG: Changed Map")
        if ((self.player.gMap.size[0] * self.mapPos[0] +
             self.player.pos[0]) - self.softPos[0]) < -self.walkArea:
            
            self.setMapPos(self.softPos[0] - 1, self.softPos[1])
            self.redrawAllMaps()
        self.player.goLeft()
        try:
            self.curLevel.playerMoved()
        except:
            pass

    def playerGoUp(self):
        self.player.gMap.drawPos.append([self.player.pos[0], self.player.pos[1]])

        if self.player.pos[1] <= 0:
            self.mapPos = [self.mapPos[0], self.mapPos[1] - 1]
            self.player.gMap = self.gMaps[self.mapPos[0]][self.mapPos[1]]
            self.player.pos[1] = self.player.pos[1] + self.player.gMap.size[1]
            if misc.DEBUG == True:
                self.textField.sendText("DEBUG: Changed Map")
        if ((self.player.gMap.size[1] * self.mapPos[1] +
             self.player.pos[1]) - self.softPos[1]) < -self.walkArea:
            self.setMapPos(self.softPos[0], self.softPos[1] - 1)
            self.redrawAllMaps()
        self.player.goUp()
        try:
            self.curLevel.playerMoved()
        except:
            pass

    def playerGoDown(self):
        self.player.gMap.drawPos.append([self.player.pos[0], self.player.pos[1]])

        if self.player.pos[1] >= (self.player.gMap.size[1] - 1):
            self.mapPos = [self.mapPos[0], self.mapPos[1] + 1]
            self.player.gMap = self.gMaps[self.mapPos[0]][self.mapPos[1]]
            self.player.pos[1] = self.player.pos[1] - self.player.gMap.size[1]
            if misc.DEBUG == True:
                self.textField.sendText("DEBUG: Changed Map")
        if ((self.player.gMap.size[1] * self.mapPos[1] +
             self.player.pos[1]) - self.softPos[1]) > self.walkArea:
            self.setMapPos(self.softPos[0], self.softPos[1] + 1)
            self.redrawAllMaps()
        self.player.goDown()
        try:
            self.curLevel.playerMoved()
        except:
            pass

    def draw(self, dst):
        for elem in self.persons:
            if (self.player.pos[0] == elem.pos[0]) & \
                   (self.player.pos[1] == elem.pos[1]):
                elem.crashWith(elem, self.player)
        self.textField.draw()
        for i in range(self.mapPos[1] - 1, self.mapPos[1] + 2):
            for j in range(self.mapPos[0] - 1, self.mapPos[1] + 2):
                self.gMaps[j][i].draw(dst)
#        for i in range(self.maps[1]):        
#            for j in range(self.maps[0]):         # Old because every map will be drawn and not just nine
#                self.gMaps[j][i].draw(dst)
        self.player.draw(dst)
        for elem in self.persons:
            elem.draw(dst)

        self.statusBox.draw()

    def sendText(self, text):
        self.textField.sendText(text)
            
            
