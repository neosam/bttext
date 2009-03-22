import os
import gamemap
import textfield
import timer
import person
import statusbox
from configs import misc
import textout
import curses
from curses.textpad import Textbox


class World(object):
    def __init__(self, stdscr, w, h, filename = -1):
        self.w = w
        self.h = h
        self.mapPos = [0,0]

        self.softPos = [self.mapPos[0] * 256, self.mapPos[1] * 256]

        self.textField = textfield.Textfield(2, 6, self.w/2 - 5, self.h - 7)
        self.persons = []
        self.cheatWalkEverywhere = False

        self.statusBox = statusbox.statusBox(stdscr, w, h)
        self.stdscr = stdscr



        if filename == -1:
            # If no filename is given, I will create an empty world
            self.walkArea = 3
            self.maps = {}
            for y in range(-1, 2):
                for x in range(-1, 2):
                    self.maps[(x, y)] = gamemap.GameMap(self.w/2 + 2, 6,
                                                        self.w/2 - 5, self.h -
                                                        8)
                    self.maps[x, y].textField = self.textField
            self.setMapPos((0, 0))
            self.globalMapPos = [0, 0]


    def askCode(self):
        def out(txt):
            self.textField.sendText(txt)
        title = "/\\\\ Hack some code //\\"
        win = curses.newwin(self.h - 6, self.w - 10, 3, 5)
        win.box()
        size = win.getmaxyx()
        win.addstr(0, size[1] / 2 - len(title) / 2, title)
        win.refresh()
        win = curses.newwin(self.h - 8, self.w - 12, 4, 6)
        t = Textbox(win)
        text = t.edit()
        code = compile(text, 'fake.py', 'exec')
        try:
            eval(code)
        except:
            self.textField.sendText("error while executing code")

    def setMapPos(self, pos):
        self.softPos = pos
        for y in range(-1, 2):
            for x in range(-1, 2):
                self.maps[x, y].pos = [gamemap.LEVEL_WIDTH * x + pos[0],
                                       gamemap.LEVEL_HEIGHT * y + pos[1]]

    def getPlayerPos(self):
        return self.player.pos, self.mapPos

    def setCheatWalkEverywhere(self, newCheat):
        self.cheatWalkEverywhere = newCheat
        self.player.cheatWalkEverywhere = newCheat

    def save(self, filename):
        pass

    def load(self, filename):
        pass

    def addPerson(self, person):
        person.gMap = self.maps[0, 0]
        person.tf = self.textField
        self.persons.append(person)
    
    def resize(self, w, h):
        self.w = w
        self.h = h
        self.textField.resize(self.w/2 - 5, self.h - 7)
        for map in self.maps.values():
            map.resize(self.w/2 + 2, 6, self.w/2 - 5, self.h - 8)
        self.statusBox.resize(w, h)

#    def setMapPos(self, x, y):
#        for i in range(self.maps[1]):
#            for j in range(self.maps[0]):
#                self.gMaps[j][i].pos = [-j * self.player.gMap.size[0] + x,
#                                        -i * self.player.gMap.size[1] + y]
#        self.softPos = [x, y]

    def setPlayer(self, player):
        self.player = player
        player.tf = self.textField
        player.gMap = self.maps[0, 0]

    # TODO: Same code four times - that's bad -.- (playerGo...)

    def redrawAllMaps(self):
#        for i in range(self.mapPos[1] - 1, self.mapPos[1] + 2):
#            for j in range(self.mapPos[0] - 1, self.mapPos[0] + 2):

        for map in self.maps.values():
            map.drawAllFlag = True

    def jumpPlayerTo(self, x, y, mx, my):
        self.player.pos = [x, y]
        self.player.mapPos = [mx, my]
        self.player.gMap = self.maps[mx][my]


    def playerGoRight(self):
        self.player.gMap.drawPos.append([self.player.pos[0], 
                                         self.player.pos[1]])

        self.player.goRight()
        self.check_playerpos()

        if ((self.player.gMap.size[0] * self.mapPos[0] +
             self.player.pos[0]) - self.softPos[0]) > self.walkArea:
            self.setMapPos((self.softPos[0] + 1, self.softPos[1]))
            self.redrawAllMaps()
        try:
            self.curLevel.playerMoved()
        except:
            pass

    def check_playerpos(self):
        changed = False
        if self.player.pos[0] < 0:
            self.globalMapPos[0] -= 1
            for y in range(-1, 2):
                for x in range(0, 2):
                    self.maps[x - 1, y] = self.maps[x, y]
                    self.maps[x, y] = gamemap.FakeGameMap(self.w/2 + 2, 6,
                                                          self.w/2 - 5, self.h
                                                          - 8)
                    changed = True
        if self.player.pos[0] >= gamemap.LEVEL_WIDTH:
            self.globalMapPos[0] += 1
            for y in range(-1, 2):
                for x in range(0, -2, -1):
                    self.maps[x + 1, y] = self.maps[x, y]
                    self.maps[x, y] = gamemap.FakeGameMap(self.w/2 + 2, 6,
                                                          self.w/2 - 5, self.h -
                                                          8)
                    changed = True
        if self.player.pos[1] < 0:
            self.globalMapPos[1] -= 1
            for y in range(0, 2):
                for x in range(-1, 2):
                    self.maps[x, y - 1] = self.maps[x, y]
                    self.maps[x, y] = gamemap.FakeGameMap(self.w/2 + 2, 6,
                                                          self.w/2 - 5, self.h -
                                                          8)
                    changed = True
        if self.player.pos[1] >= gamemap.LEVEL_HEIGHT:
            self.globalMapPos[1] += 1
            for y in range(0, -2, -1):
                for x in range(-1, 2):
                    self.maps[x, y + 1] = self.maps[x, y]
                    self.maps[x, y] = gamemap.FakeGameMap(self.w/2 + 2, 6,
                                                          self.w/2 - 5, self.h -
                                                          8)
                    changed = True

        #if misc.DEBUG:
        #    self.textField.sendText(str(self.player.pos) + str(self.mapPos))

        if changed:
            self.player.pos[0] %= gamemap.LEVEL_WIDTH
            self.player.pos[1] %= gamemap.LEVEL_HEIGHT
            self.player.gMap = self.maps[0, 0]
            self.setMapPos(self.maps[0,0].pos)
        #    if misc.DEBUG:
        #        self.textField.sendText("DEBUG: Changed Map")

    def playerGoLeft(self):
        self.player.gMap.drawPos.append([self.player.pos[0], self.player.pos[1]])
        self.player.goLeft()
        self.check_playerpos()

        if ((self.player.gMap.size[0] * self.mapPos[0] +
             self.player.pos[0]) - self.softPos[0]) < -self.walkArea:
            self.setMapPos((self.softPos[0] - 1, self.softPos[1]))
            self.redrawAllMaps()
        try:
            self.curLevel.playerMoved()
        except:
            pass

    def playerGoUp(self):
        self.player.gMap.drawPos.append([self.player.pos[0], 
                                         self.player.pos[1]])

        self.player.goUp()
        self.check_playerpos()

        if ((self.player.gMap.size[1] * self.mapPos[1] +
             self.player.pos[1]) - self.softPos[1]) < -self.walkArea:
            self.setMapPos((self.softPos[0], self.softPos[1] - 1))
            self.redrawAllMaps()
        try:
            self.curLevel.playerMoved()
        except:
            pass

    def playerGoDown(self):
        self.player.gMap.drawPos.append([self.player.pos[0], self.player.pos[1]])
        self.player.goDown()
        self.check_playerpos()

        if ((self.player.gMap.size[1] * self.mapPos[1] +
             self.player.pos[1]) - self.softPos[1]) > self.walkArea:
            self.setMapPos((self.softPos[0], self.softPos[1] + 1))
            self.redrawAllMaps()
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
        for map in self.maps.values():
                map.draw(dst)
        self.player.draw(dst)
        for elem in self.persons:
            elem.draw(dst)

        self.statusBox.draw()

    def sendText(self, text):
        self.textField.sendText(text)
