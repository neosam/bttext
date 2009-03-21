import curses
import textout
import color
import configs
import textfield
import init

LEVEL_WIDTH = 256
LEVEL_HEIGHT = 256

def nothing():
    pass

class GameMap(object):
    def __init__(self, x, y, w, h):
        # Screen position
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.pos = [LEVEL_WIDTH/2, LEVEL_HEIGHT/2]
        self.size = [LEVEL_WIDTH, LEVEL_HEIGHT]
        self.drawPos = []
        self.drawAllFlag = True

        # Preparing level
        self.clear()

    def clear(self):
        self.map = [[" ", 3, 7, True, 0]] * \
               (LEVEL_WIDTH * LEVEL_HEIGHT)

    def __getitem__(self, pos):
        x, y = pos
        return self.map[y * LEVEL_WIDTH + x]

    def __setitem__(self, pos, v):
        x, y = pos
        self.map[y * LEVEL_WIDTH + x] = v

    def getAscii(self, x, y):
        return self[x, y][0]

    def getFG(self, x, y):
        return self[x, y][1]

    def getBG(self, x, y):
        return self[x, y][2]

    def isWalkable(self, x, y):
        return self[x, y][3]

    def getElem(self, x, y):
        return self[x, y]

    def setAscii(self, x, y, ascii):
        if ascii != "\n":
            self[x, y][0] = ascii
            return True
        return False

    def setFG(self, x, y, color):
        self[x, y][1] = color

    def setBG(self, x, y, color):
        self[x, y][2] = color

    def setWalkable(self, x, y, walkable):
        self[x, y][3] = walkable

    def saveToFile(self, filename):
        pass

    def loadFromFile(self, filename):
        pass

    def resize(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def to_screenpos(self, x, y):
        ret = (x + self.x + self.w/2 - self.pos[0] + self.w%2, \
               y + self.y + self.h/2 - self.pos[1] + self.h%2)
        if (ret[0] < 0) or (ret[1] < 0) or (ret[0] >= 80) or (ret[1] >= 24):
            raise "%i, %i, %i, %i, %i, %i" % (self.pos[0], self.pos[1],
                                              x, y, ret[0], ret[1])
        return ret

    def draw_colored(self, pos, elem):
        dst.addstr(self.y + elem[1] + self.h/2 - self.pos[1] + self.h%2,
                   self.x + elem[0] + self.w/2 - self.pos[0] + self.w%2,
                   self[pos][0], color.color(self[pos][1], self[pos][2]))

    def draw_bw(self, pos, elem):
        dst.addstr(self.y + elem[1] + self.h/2 - self.pos[1] + self.h%2,
                   self.x + elem[0] + self.w/2 - self.pos[0] + self.w%2,
                   self[pos][0])

    def draw(self, dst):
        if self.drawAllFlag == True:
            self.drawAll(dst)
        else:
            for elem in self.drawPos:
                pos = (elem[0], elem[1])

                if (pos[0] < 0) or (pos[1] < 0) or \
                   (pos[0] >= LEVEL_WIDTH) or \
                   (pos[1] >= LEVEL_HEIGHT):
                    continue

                screenpos = self.to_screenpos(pos[0], pos[1])
                if configs.misc.COLORED == True:
                    dst.addstr(screenpos[1], screenpos[0], self[pos][0],
                               color.color(self[pos][1], self[pos][2]))
                else:
                    dst.addstr(screenpos[1], screenpos[0], self[pos][0])


                self.drawPos = []

    def drawAll(self, dst):
        self.drawAllFlag = False
        for h in range(self.h):
            for  w in range(self.w):
                pos = (self.pos[0] + (self.w/2 - w),
                       self.pos[1] + (self.h/2 - h))
                if (pos[0] < 0) or (pos[1] < 0) or \
                   (pos[0] >= LEVEL_WIDTH) or \
                   (pos[1] >= LEVEL_HEIGHT):
                    continue

                if configs.misc.COLORED == True:
                    dst.addstr(self.y + self.h - h,
                               self.x + self.w - w,
                               self[pos][0],
                               color.color(self[pos][1],
                               self[pos][2]))
                else:
                    dst.addstr(self.y + self.h - h,
                               self.x + self.w - w,
                               self[pos][0])

