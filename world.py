import traceback
import sys
import os
import gamemap
import textfield
import timer
import person
import enemy
import statusbox
from configs import misc
import textout
import curses
from curses.textpad import Textbox

class World(object):
    def __init__(self, stdscr, w, h, filename):
        self.w = w
        self.h = h
        self.borderFunction(w, h)
        self.textField = textfield.Textfield(*self.screenposText())
        self.filename = filename
        self.maps = dict()
        self.globalMapPos = [0, 0]
        self.softPos = [0, 0]
        self.stdscr = stdscr

        self.WALK_AREA = 3

        self.load()
        self.statusBox = statusbox.statusBox(stdscr, w, h, self.border)
        self.setMapPos((0, 0))
        self.redrawAllMaps()

        textout.btText.trans['Messages:'] = {'de': 'Meldungen:'}
        textout.btText.trans['Map:'] = {'de': 'Karte:'}
        textout.btText.trans['State:'] = {'de': 'Status:'}


    def borderFunction(self, w, h):
        self.border = w * 3 / 4

    def dead(self):
        raise SystemExit

    def screenposMap(self):
        return (self.border + 2, 6, (self.w - self.border) - 5,
                self.h - 8)

    def screenposText(self):
        return (2, 6, self.border - 5, self.h - 7)

    def step(self, pos):
        pass

    def loadMap(self, pos):
        filename = "%s/map%i_%i" % (self.filename,
                                    self.globalMapPos[0] - pos[0],
                                    self.globalMapPos[1] - pos[1])
        self.maps[pos] = gamemap.loadFromFile(filename, self)

    def saveMap(self, pos):
        filename = "%s/map%i_%i" % (self.filename,
                                    self.globalMapPos[0] - pos[0],
                                    self.globalMapPos[1] - pos[1])
        self.maps[pos].saveToFile(filename)

    def createNewMap(self, pos=(0, 0)):
        mappos = self.screenposMap()
        self.maps[pos] = gamemap.GameMap(*mappos)
        self.setMapPos(self.softPos)
        self.redrawAllMaps()

    def evalCode(self, text):
        player = self.player
        theWorld = self
        def out(txt):
            self.textField.sendText(str(txt))
        save = self.save
        load = self.load
        new = self.createNewMap
        btText = textout.btText
        try:
            getNamedField = self.maps[0, 0].getNamedField
            setNamedField = self.maps[0, 0].setNamedField
        except:
            pass
        def addPerson(name, ascii, message):
            p = person.Person(self.textField, name,
                              self.maps[0, 0], self,
                              mapDraw=[ascii, foreground, background])
            p.message = message
            self.maps[0, 0].persons[tuple(self.player.pos)] = p

        def addEnemy(name, ascii):
            p = enemy.Enemy(self.textField, name,
                            self.maps[0, 0], self,
                            mapDraw=[ascii, foreground, background])
            self.maps[0, 0].persons[tuple(self.player.pos)] = p

        def removePerson():
            self.maps[0, 0].persons.pop(tuple(self.player.pos))

        if callable(text):
            text = text()

        code = compile(text, 'fake.py', 'exec')
        try:
            eval(code)
        except SystemExit:
            raise SystemExit
        except:
            tb = sys.exc_info()[2]
            while tb != None:
                self.textField.sendText(str(tb.tb_lineno))
                tb = tb.tb_next
            self.textField.sendText(sys.exc_info()[0])
            self.textField.sendText(str(sys.exc_info()[1]))

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

    def save(self):
        for y in xrange(-1, 2):
            for x in xrange(-1, 2):
                self.saveMap((x, y))

    def load(self):
        for y in xrange(-1, 2):
            for x in xrange(-1, 2):
                self.loadMap((x, y))
        self.redrawAllMaps()
        self.setMapPos(self.softPos)

    def resize(self, w, h):
        self.w = w
        self.h = h
        self.borderFunction(w, h)
        mappos = self.screenposMap()
        textpos = self.screenposText()
        self.textField.resize(textpos[2], textpos[3])
        for map in self.maps.values():
            map.resize(*mappos)
        self.statusBox.resize(w, h, self.border)
        self.redrawAllMaps()

    def setPlayer(self, player):
        self.player = player
        player.tf = self.textField
        player.gMap = self.maps[0, 0]



    def redrawAllMaps(self):
        for map in self.maps.values():
            map.drawAllFlag = True

    def check_playerpos(self):
        changed = False
        mappos = self.screenposMap()
        def scrollMaps(func, rangex, rangey):
            self.globalMapPos = func(self.globalMapPos)
            for y in rangey:
                for x in rangex:
                    self.maps[tuple(func([x, y]))] = self.maps[x, y]
                    self.maps[x, y] = gamemap.FakeGameMap(*mappos)
                    changed = True
            self.player.pos[0] %= gamemap.LEVEL_WIDTH
            self.player.pos[1] %= gamemap.LEVEL_HEIGHT
            self.player.gMap = self.maps[0, 0]
            self.setMapPos(self.maps[0,0].pos)

        if self.player.pos[0] < 0:
            scrollMaps(lambda(pos): [pos[0] - 1, pos[1]], 
                       range(0, 2), range(-1, 2))
        if self.player.pos[0] >= gamemap.LEVEL_WIDTH:
            scrollMaps(lambda(pos): [pos[0] + 1, pos[1]],
                       range(0, -2, -1), range(-1, 2))
        if self.player.pos[1] < 0:
            scrollMaps(lambda(pos): [pos[0], pos[1] - 1],
                       range(-1, 2), range(0, 2))
        if self.player.pos[1] >= gamemap.LEVEL_HEIGHT:
            scrollMaps(lambda(pos): [pos[0], pos[1] + 1],
                       range(-1, 2), range(0, -2, -1))

        self.statusBox.newField(self.player.gMap[self.player.pos])
 
    def draw(self, dst):
        self.textField.draw()
        for map in self.maps.values():
                map.draw(dst)
        self.player.draw(dst)
        self.statusBox.draw()

    def sendText(self, text):
        self.textField.sendText(text)



def playerGo(posmodifier, playerfunc):
    def action(self, force=False):
#        self.player.gMap.drawPos.append([self.player.pos[0],
#                                         self.player.pos[1]])
        self.step(posmodifier(self.player.pos))
        getattr(self.player, playerfunc)(force)  # self.player.go...
        self.check_playerpos()

        # Handler for walk area
        if abs(self.player.pos[0] - self.softPos[0]) > abs(self.WALK_AREA) or\
           abs(self.player.pos[1] - self.softPos[1]) > abs(self.WALK_AREA):
            self.setMapPos(posmodifier(self.softPos))
            self.redrawAllMaps()
    return action

World.playerGoLeft = playerGo(lambda(pos): [pos[0] - 1, pos[1]], 'goLeft')
World.playerGoRight = playerGo(lambda(pos): [pos[0] + 1, pos[1]], 'goRight')
World.playerGoUp = playerGo(lambda(pos): [pos[0], pos[1] - 1], 'goUp')
World.playerGoDown = playerGo(lambda(pos): [pos[0], pos[1] + 1], 'goDown')

def attack(directionfunc, ascii):
    def action(self):
        pos = directionfunc(self.player.pos)
        if pos in self.maps[0, 0].persons:
            person = self.maps[0, 0].persons[pos]
            person.setHP(person.profile['hp'][0] - 100)
    return action

World.attackLeft = attack(lambda(pos): (pos[0] - 1, pos[1]), '-')
World.attackRight = attack(lambda(pos): (pos[0] + 1, pos[1]), '-')
World.attackUp = attack(lambda(pos): (pos[0], pos[1] - 1), '|')
World.attackDown = attack(lambda(pos): (pos[0], pos[1] + 1), '|')
