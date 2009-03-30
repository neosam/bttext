import curses
from textout import btText


class statusBox(object):
    def __init__(self, stdscr, w, h, border):
        self.stdscr = stdscr
        self.w = w
        self.h = h
        self.border = border
        self.field = {'walkable': False}
        self.mp_active = False
        self.changeHP([0, 0])
        self.changeMP([0, 0])
        

    def draw(self):
        w = self.w
        h = self.h
        clearLine = " " * (self.w - 12)
        msg = btText('Messages:')
        map = btText('Map:')
        state = btText("State:")
        self.stdscr.vline(4, self.border, curses.ACS_VLINE, h - 5)
        self.stdscr.addstr(4, 2, str(msg), curses.A_BOLD)
        self.stdscr.addstr(4, self.border + 2, str(map), curses.A_BOLD)
        self.stdscr.addstr(2, 2, str(state), curses.A_BOLD)
        self.stdscr.addstr(2, 10, clearLine)
        self.stdscr.addstr(2, 10, self.statusString)

    def resize(self, w, h, border):
        self.w = w
        self.h = h
        self.border = border

    def createStatusString(self):
        self.statusString = "HP: " + str(self.hp[0]) + "/" + str(self.hp[1])
        if self.mp_active:
            self.statusString = self.statusString + "   MP: " + str(self.mp[0]) + "/" + \
                                 self.mp[1]

    def changeHP(self, hp):
        self.hp = hp
        self.createStatusString()
        
    def changeMP(self, mp):
        self.mp = mp
        self.createStatusString()

    def newField(self, field):
        self.field = field
        self.createStatusString()


class EditorStatusBox(statusBox):
    def createStatusString(self):
        self.statusString = "Walkable: %s   Trigger: %s" % \
                            (str(self.field['walkable']),
                             str('trigger' in self.field))
