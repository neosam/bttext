import curses
from configs import *
import init
import bt
import sys
import init

class btText(str):
    def __init__(self, text = ""):
        try:
            self.__orig__ = text
            self.__inlist__ = str(text).split("$%")
            self.__cont__ = self.__makestr__()
            self.__positions__ = [[0, 0,
                                   len(self.__inlist__[0]) - 1,
                                   len(self.__inlist__[0]) - 1, "-1"]]
            for i in range(1, len(self.__inlist__), 2):
                self.__positions__.append([self.__positions__[i/2 - 0][2] + 1,
                                           self.__positions__[i/2 - 0][3] + 5 +
                                           len(self.__inlist__[i]),
                                           self.__positions__[i/2 - 0][2] +
                                           len(self.__inlist__[i + 1]),
                                           self.__positions__[i/2 - 0][3] + 5 +
                                           len(self.__inlist__[i + 1]),
                                           self.__inlist__[i]])
            if len(self.__positions__) != 1:
                self.__positions__[len(self.__positions__)-1][3] += 1
        except:
            addError("btText Problem!!")
            
    def __add__(self, text):
        return btText(self.__cont__ + str(text))
    def __str__(self):
        return self.__orig__
    def __repr__(self):
        return "'" + self.__orig__ + "'"
    def __len__(self):
        return len(self.__cont__)
    def __contains__(self):
        return self.__orig__
    def __getitem__(self, i):
        return self.__orig__[i]

    def __makestr__(self):
        return "".join([self.__inlist__[elem] for elem in range(0, len(self.__inlist__), 2)])

    def realpos(self, pos):
        if pos > (len(self.__cont__) - 1):
            return len(self.__orig__)
        elif pos < 0:
            return 0
        for elem in self.__positions__:
            if (pos >= elem[0]) & (pos <= elem[2]):
                return pos - elem[0] + elem[1]
    
    def getRegion(self, left, right):
        return btText("$%" + self.getColor(left) + "$%" + "".join([self.__orig__[elem] for elem in range(self.realpos(left), self.realpos(right))]))
    def getList(self):
        return self.__inlist__
    def getColor(self, pos):
        if pos > (len(self.__cont__) - 1):
            return self.__positions__[len(self.__positions__)-1][4]
        for elem in self.__positions__:
            if (pos >= elem[0]) & (pos <= elem[2]):
                return elem[4]

    def draw(self, x = -2, y = 0, dst = 0):
        if dst == 0:
            dst = init.stdscr
        try:
            if x == -2:
                dst.addstr(self.__inlist__[0])
            else:
                dst.addstr(y, x, self.__inlist__[0])

            for i in range(1, len(self.__inlist__), 2):
                file("log.log", "w+").write(str(self.__inlist__) + str(i))
                if int(self.__inlist__[i]) == -1:
                    dst.addstr(self.__inlist__[i+1])
                else:
                    if misc.COLORED:
                        dst.addstr(self.__inlist__[i+1],
                                           int(self.__inlist__[i]))
                                           #curses.A_BOLD | curses.color_pair(
                            #int(self.__inlist__[i])))
                    else:
                        dst.addstr(self.__inlist__[i+1])
        except:
            addError("btText draw Problem!!!")
            
def textOut(text, x = -2, y = 0, col = -1, dst = 0):
    if dst == 0:
        dst = init.stdscr
    if type(text) == type(btText()):
        text.draw(x, y, dst)
    else:
        if not misc.COLORED: col = -1
        if (x == -2) & (col == -1):
            dst.addstr(text)
        elif (x == -2) & (col != -1):
            dst.addstr(text, curses.A_BOLD | curses.color_pair(col))
        elif (x != -2) & (col == -1):
            dst.addstr(y, x, text)
        elif (x != -2) & (col != -1):
            dst.addstr(y, x, text, curses.A_BOLD | curses.color_pair(col))
