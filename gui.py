import curses
import init
import textout

# This object can added to a window
class WinObj:
    def __init__(self, parent):
        self.parent = parent
        self.active = False
        pass

    def getSize(self):
        return 0, 0

    def draw(self, x, y):
        pass

# a button
class ObjButton(WinObj):
    def __init__(self, parent, title):
        WinObj.__init__(self, parent)

        self.title = title
        self.onClick = None

    def getSize(self):
        WinObj.getSize(self)
        return len(self.title) + 2, 3

    def draw(self, x, y):
        WinObj.draw(self, x, y)

        textout.textOut(self.title, x, y, dst=self.dst)
#        self.parent.dst.addstr(y + 1, x + 1, self.title)




class Window:
    def __init__(self, parent):
        self.parent = parent
        self.winObjs = []
        self.size = [2,2]
        self.reallocDrawArea()

    def reallocDrawArea(self):
        dstH, dstW = init.stdscr.getmaxyx()
        x = (dstW - self.size[0]) / 2
        y = (dstH - self.size[1]) / 2
        w = self.size[0]
        h = self.size[1]
        self.dst = curses.newwin(h, w, y, x)
        for elem in self.winObjs:
            elem.dst = self.dst

    def recalcSize(self):
        width = 2
        height = 2
        for elem in self.winObjs:
            w, h = elem.getSize()
            width = w + 2
            height = height + h
        self.size[0] = width
        self.size[1] = height

    def getSize(self):
        return self.size
    
    def addObj(self, obj):
        self.winObjs.append(obj)
        self.recalcSize()
        self.reallocDrawArea()

    def draw(self):
        self.dst.erase()
        self.dst.box()
        pos = 1
        for elem in self.winObjs:
            elem.draw(1, pos)
            pos = pos + elem.getSize()[1]
        self.dst.refresh()
        init.stdscr.refresh()

    def wait(self):
        self.dst.getch()
