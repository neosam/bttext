import sys
import curses
import timer
import time
import init
from textfield import *
from gamemap import *
from configs import *
import configs
from person import *
from player import *
import menu
from textout import *
import world

global stdscr

BT_VERSION = "16102005"

BT_SMALL_LOGO = "/\\\\"
BT_SMALL_BACKLOGO = "//\\"
BT_SMALL_LOGOTEXT = BT_SMALL_LOGO + " Bermuda Triangle " + BT_SMALL_BACKLOGO

#BT_LOGO="    /\\  /\\   |\\ |-- |\\           |\\        ___ |\\ o      |\\  |  __ |   |--\n\
#   /  \\/  \\  |< |-  |/ |\\/| |  | | | /\\     |  |/ |  /\\  | \\ | /   |   |-\n\
#  /____\\___\\ |/ |-- |\\ |  |  \\/  |/ /--\\    |  |\\ | /--\\ |  \\| \\_\\ \\__ |--\n\
# <--------------------Die Zukunft liegt in deiner Hand-------------------->"
BT_LOGO = file("btlogo.txt").read()

BT_WINDOW_TOO_SMALL = "Fenster zu klein"

def empty():
    pass

def FalcoCrashMike(self, person):
    """ This happens if Falco and Mike stand on one field """
    self.say("Du wagst es!!")


def waveWare(x, y):
    # TODO: WaveWare Logo is not colored?
    ww = btText("$%4$%W$%-1$%ave $%4$%W$%-1$%are")
    textOut(ww, x, y)

def main():
    global stdscr

    print BT_LOGO
    time.sleep(1)

    try: # Crash protection ;)
        init.init()
        stdscr = init.stdscr

        h, w = stdscr.getmaxyx()

        # Create falco and put him into the map
        falco = Person(-1, "Falco", -1, [0, 0], ["F", 7, 4],
                   configs.colorof["falco"][0])
        falco.jumpTo(1, 0)
        falco.crashWith = FalcoCrashMike

        theWorld = world.World(stdscr, w, h)

        # Mike is the hero!
        mike = Player(theWorld.statusBox, -1, "Du", -1, [0, 0], ["M", 0, 3],
                      configs.colorof["mike"][0], profile={"hp": [100, 100],
                                                       "mp": [0, 0]})
        
        # Adding mike and falco to Bermuda Triangle World
        theWorld.setPlayer(mike)
        theWorld.addPerson(falco)

        # Adding whater in map (mike cannot move on it)
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
                theWorld.sendText("Bitte im Menue Beenden ('m' druecken)")
            if c == ord("w"): misc.COLORED = not misc.COLORED # Switches between colored and b/w
            if c == ord("m"): menu.start() # Enter menu
            if c == ord("h"): theWorld.playerGoLeft()  #
            if c == ord("j"): theWorld.playerGoDown()  #  Player
            if c == ord("k"): theWorld.playerGoUp()    #  movement
            if c == ord("l"): theWorld.playerGoRight() #
            if c == ord("s"): theWorld.save("testsave.btt")  # Loading doesn't really work ;)
            # --- Event handling ---

            # +++ Drawing +++
            h, w = stdscr.getmaxyx()
            #stdscr.erase()
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

    except:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        errorString = ""
#        print dir(sys.exc_info()[2].tb_lasti)
        print "Hardcore error in Bermuda Triangle " + BT_VERSION + " :`(  Exiting forced!!!"
        print "Please send bt_last_error.log to neosam@gmail.com"
        # TODO: There really should be a bt_last_error.log ;)


if __name__ == "__main__":
    main()
