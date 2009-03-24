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
    def __init__(self, stdscr, w, h, filename):
        self.w = w
        self.h = h
        self.mapPos = [0,0]
        self.walkArea = 3

        self.softPos = [self.mapPos[0] * 256, self.mapPos[1] * 256]

        self.textField = textfield.Textfield(*self.screenposText())
        self.persons = []
        self.cheatWalkEverywhere = False

        self.statusBox = statusbox.statusBox(stdscr, w, h)
        self.stdscr = stdscr

        self.globalMapPos = [0, 0]

        self.filename = filename
        self.maps = dict()
        for y in xrange(-1, 2):
            for x in xrange(-1, 2):
                self.loadMap((x, y))
        self.setMapPos((0, 0))
        self.redrawAllMaps()

    def screenposMap(self):
        return (self.w * 3 / 4 + 2, 6, self.w / 4 - 5, self.h - 8)

    def screenposText(self):
        return (2, 6, self.w * 3 / 4 - 5, self.h - 7)

    def step(self, pos):
        pass

    def loadMap(self, pos):
        filename = "%s/map%i_%i" % (self.filename,
                                    self.globalMapPos[0] - pos[0],
                                    self.globalMapPos[1] - pos[1])
        self.maps[pos] = gamemap.loadFromFile(filename, self)
        self.maps[pos].textField = self.textField

    def saveMap(self, pos):
        filename = "%s/map%i_%i" % (self.filename,
                                    self.globalMapPos[0] - pos[0],
                                    self.globalMapPos[1] - pos[1])
        self.maps[pos].saveToFile(filename)

    def createNewMap(self, pos):
        mappos = self.screenposMap()
        self.maps[pos] = gamemap.GameMap(*mappos)
        self.setMapPos(self.softPos)
        self.redrawAllMaps()

    def askCode(self):
        def out(txt):
            self.textField.sendText(str(txt))
        def save():
            for y in xrange(-1, 2):
                for x in xrange(-1, 2):
                    self.saveMap((x, y))
        def load():
            for y in xrange(-1, 2):
                for x in xrange(-1, 2):
                    self.loadMap((x, y))
            self.redrawAllMaps()
            self.setMapPos(self.softPos)

        def new(pos=(0, 0)):
            self.createNewMap(pos)
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
        try:
            self.player.gMap = self.maps[0, 0]
        except:
            pass

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
        mappos = self.screenposMap()
        textpos = self.screenposText()
        self.textField.resize(textpos[2], textpos[3])
        for map in self.maps.values():
            map.resize(*mappos)
        self.statusBox.resize(w, h)
        self.redrawAllMaps()

    def setPlayer(self, player):
        self.player = player
        player.tf = self.textField
        player.gMap = self.maps[0, 0]



    def redrawAllMaps(self):
        for map in self.maps.values():
            map.drawAllFlag = True

    def jumpPlayerTo(self, x, y, mx, my):
        self.player.pos = [x, y]
        self.player.mapPos = [mx, my]
        self.player.gMap = self.maps[mx][my]


    # TODO: Don't like that code
    def check_playerpos(self):
        changed = False
        mappos = self.screenposMap()
        if self.player.pos[0] < 0:
            self.globalMapPos[0] -= 1
            for y in range(-1, 2):
                for x in range(0, 2):
                    self.maps[x - 1, y] = self.maps[x, y]
                    self.maps[x, y] = gamemap.FakeGameMap(*mappos)
                    changed = True
        if self.player.pos[0] >= gamemap.LEVEL_WIDTH:
            self.globalMapPos[0] += 1
            for y in range(-1, 2):
                for x in range(0, -2, -1):
                    self.maps[x + 1, y] = self.maps[x, y]
                    self.maps[x, y] = gamemap.FakeGameMap(*mappos)
                    changed = True
        if self.player.pos[1] < 0:
            self.globalMapPos[1] -= 1
            for y in range(0, 2):
                for x in range(-1, 2):
                    self.maps[x, y - 1] = self.maps[x, y]
                    self.maps[x, y] = gamemap.FakeGameMap(*mappos)
                    changed = True
        if self.player.pos[1] >= gamemap.LEVEL_HEIGHT:
            self.globalMapPos[1] += 1
            for y in range(0, -2, -1):
                for x in range(-1, 2):
                    self.maps[x, y + 1] = self.maps[x, y]
                    self.maps[x, y] = gamemap.FakeGameMap(*mappos)
                    changed = True

        if changed:
            self.player.pos[0] %= gamemap.LEVEL_WIDTH
            self.player.pos[1] %= gamemap.LEVEL_HEIGHT
            self.player.gMap = self.maps[0, 0]
            self.setMapPos(self.maps[0,0].pos)

        self.statusBox.newField(self.player.gMap[self.player.pos])
 
    def playerGoRight(self):
        self.player.gMap.drawPos.append([self.player.pos[0], 
                                         self.player.pos[1]])
        self.step((self.player.pos[0] + 1, self.player.pos[1]))
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


    def playerGoLeft(self):
        self.player.gMap.drawPos.append([self.player.pos[0], 
                                         self.player.pos[1]])
        self.step((self.player.pos[0] - 1, self.player.pos[1]))
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
        self.step((self.player.pos[0], self.player.pos[1] - 1))

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
        self.step((self.player.pos[0], self.player.pos[1] + 1))
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
