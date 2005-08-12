import curses
import timer
import time
import init
from textfield import *
from gamemap import *
from configs import *
import configs
from person import *
import menu
from textout import *
import world

global stdscr

BT_SMALL_LOGO = "/\\\\"
BT_SMALL_BACKLOGO = "//\\"
BT_SMALL_LOGOTEXT = BT_SMALL_LOGO + " Bermuda Triangle " + BT_SMALL_BACKLOGO

BT_LOGO="    /\\  /\\   |\\ |-- |\\           |\\        ___ |\\ o      |\\  |  __ |   |--\n\
   /  \\/  \\  |< |-  |/ |\\/| |  | | | /\\     |  |/ |  /\\  | \\ | /   |   |-\n\
  /____\\___\\ |/ |-- |\\ |  |  \\/  |/ /--\\    |  |\\ | /--\\ |  \\| \\_\\ \\__ |--\n\
 <--------------------Die Zukunft liegt in deiner Hand-------------------->"

BT_WINDOW_TOO_SMALL = "Fenster zu klein"

def empty():
    pass

def FalcoCrashMike(self, person):
    self.say("Du wagst es!!")


def waveWare(x, y):
    ww = btText("$%2$%W$%-1$%ave $%4$%W$%-1$%are")
    textOut(ww, x, y)

def main():
    global stdscr

    print 
    print BT_LOGO
    print
    time.sleep(1)
    
    init.init()
    stdscr = init.stdscr

    h, w = stdscr.getmaxyx()

    falco = Person(-1, "Falco", -1, [0, 0], ["F", 7, 4],
                   configs.colorof["falco"][0])
    falco.jumpTo(1, 0)
    falco.crashWith = FalcoCrashMike
    
    mike = Person(-1, "Du", -1, [0, 0], ["M", 0, 3],
                  configs.colorof["mike"][0])
    
    theWorld = world.World(stdscr, w, h)
    theWorld.setPlayer(mike)
    theWorld.addPerson(falco)

    for i in range(10):
        theWorld.gMaps[1][1].gMap[10][i] = ["~", 7, 4, False, nothing]
    for i in range(10):
        theWorld.gMaps[1][0].gMap[10][198-i] = ["~", 7, 4, False, nothing]
    
    
    while 1:                     # Gameloop
        timer.fpsDelay()         # FPS-Control
        clearError()
        # +++ Event handling +++
        c = stdscr.getch()       # I don't think an eventloop is needed in an
                                 # textadventure
        if c == ord("q"):
            theWorld.sendText("Mitte im Menue Beenden ('m' druecken)")
        if c == ord("w"): misc.COLORED = not misc.COLORED
        if c == ord("m"): menu.start()
        if c == ord("h"): theWorld.playerGoLeft()
        if c == ord("j"): theWorld.playerGoDown()
        if c == ord("k"): theWorld.playerGoUp()
        if c == ord("l"): theWorld.playerGoRight()
        # --- Event handling ---

        # +++ Drawing +++
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        if (w < 70) | (h < 24):
            stdscr.addstr(h/2, (w - len(BT_WINDOW_TOO_SMALL)) / 2,
                          BT_WINDOW_TOO_SMALL)
        elif misc.BT_ERROR != "":
            stdscr.addstr(h/2, (w - len(misc.BT_ERROR)) / 2,
                          misc.BT_ERROR)
        else:
            theWorld.resize(w, h)

            stdscr.box()
            stdscr.addstr(0, (w - len(BT_SMALL_LOGOTEXT)) / 2,
                          BT_SMALL_LOGOTEXT)

            theWorld.draw(stdscr)
            waveWare(w - 10, h - 1)

        stdscr.refresh()
        # --- Drawing ---
    
    init.quit()

if __name__ == "__main__":
    main()
