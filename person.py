# from init import *
import init
import sys
import color
import configs
from textout import btText

class Person(object):
    def __init__(self, tf, name, gMap, w, pos = [0,0], mapDraw=["?", 0, 7],
                 color = configs.color.green, profile=0):
        self.tf = tf
        self.color = color
        self.name = name
        self.gMap = gMap
        self.pos = pos
        self.mapDraw = mapDraw
        self.theWorld = w
        self.message = ''

        if profile == 0:
            profile = { "hp": [100,100] }
        self.profile = profile

    def __getstate__(self):
        return {'color': self.color,
                'name': self.name,
                'mapDraw': self.mapDraw,
                'message': self.message,
                'profile': self.profile}

    def say(self, text):
        try:
            text = str(btText(text))
            name = str(btText(self.name))
            self.tf.sendText("$%" + str(self.color) + "$%" + name +
                             ":$%" + str(configs.colorof["talk"][0]) + "$% " + text)
        except:
            init.quit()
            print "Unexpected error:", sys.exc_info()[2].tb_next
            print sys.exc_info()[1]
            print configs.colorof
            sys.exit()

    def comes(self):
        try:
            self.tf.sendText("$%" + str(configs.colorof["move"][0]) + "$%" +
                             self.name + " naehert sich")
        except:
            init.quit()
            print sys.exc_info()[2].tb_next
            print sys.ext_info()[1]

    def draw(self, dst):
        pos = [self.gMap.x + self.gMap.w/2 + self.pos[0] - self.gMap.pos[0] + self.gMap.w%2,#xa,
               self.gMap.y + self.gMap.h/2 + self.pos[1] - self.gMap.pos[1] + self.gMap.h%2]#ya]

        if (pos[0] >= self.gMap.x) & \
           (pos[1] >= self.gMap.y) & \
           (pos[0] <= (self.gMap.x + self.gMap.w)) & \
           (pos[1] <= (self.gMap.y + self.gMap.h)):

            if configs.misc.COLORED == True:
                dst.addstr(pos[1], pos[0], self.mapDraw[0],
                           color.color(self.mapDraw[1],
                                       self.mapDraw[2]))
            else:
                dst.addstr(pos[1], pos[0], self.mapDraw[0])

    def jumpTo(self, x, y):
        self.pos = [x, y]

    def crashWith(self, person):
        pass

    def setHP(self, hp):
        self.profile["hp"][0] = hp
        self.onChangeHP()

    def onCrash(self):
        if self.message != '':
            self.tf.sendText('')
            for i in range(len(self.message)):
                if (i % 2) == 0:
                    self.say(self.message[i])
                else:
                    self.theWorld.player.say(self.message[i])

    def onFrame(self):
        pass

    def onChangeHP(self):
        if self.profile['hp'][0] <= 0:
            if tuple(self.pos) in self.gMap.persons:
                self.gMap.persons.pop(tuple(self.pos))

def go(posmodifier):
     def action(self, force=False):
         pos = posmodifier(self.pos)
         gMap = self.theWorld.maps[pos[0] / 256 * (-1),
                                   pos[1] / 256 * (-1)]
         pos = [x % 256 for x in pos]
         if (gMap[pos]['walkable'] == True) and \
            (tuple(pos) not in gMap.persons) and \
            (pos != self.theWorld.player.pos) or force:
             if (tuple(self.pos) in self.gMap.persons) and \
                ("Player" not in str(type(self))):
                 self.gMap.persons.pop(tuple(self.pos))
                 self.gMap.persons[tuple(pos)] = self
             self.gMap.drawPos.append(self.pos)
             self.gMap.drawPos.append(pos)
             self.jumpTo(*posmodifier(self.pos))
         if pos == self.theWorld.player.pos:
             self.onCrash()
     return action

Person.goLeft = go(lambda(pos): [pos[0] - 1, pos[1]])
Person.goRight = go(lambda(pos): [pos[0] + 1, pos[1]])
Person.goUp = go(lambda(pos): [pos[0], pos[1] - 1])
Person.goDown = go(lambda(pos): [pos[0], pos[1] + 1])
