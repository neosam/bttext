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
import textout
import world
import traceback


global stdscr

BT_VERSION = "0.0.2"

BT_SMALL_LOGO = "/\\\\"
BT_SMALL_BACKLOGO = "//\\"
BT_SMALL_LOGOTEXT = BT_SMALL_LOGO + " Bermuda Triangle" + BT_SMALL_BACKLOGO

BT_LOGO = file("btlogo.txt").read()

BT_WINDOW_TOO_SMALL = "Fenster zu klein"

def empty():
    pass

#def FalcoCrashMike(self, person):
#    """ This happens if Falco and Mike stand on one field """
#    self.say("Fass mich nich an!!")


def waveWare(x, y, dst):
    blue = str(curses.color_pair(curses.COLOR_BLUE))
    white = str(curses.color_pair(curses.COLOR_WHITE))
    ww = textout.btText("$%" + blue + "$%W$%" + white + "$%ave $%" + blue + "$%W$%" + white + "$%are")
    textout.textOut(ww, x, y, dst)

def main():
    global stdscr

    print BT_LOGO
    time.sleep(1)

    try: # Crash protection ;)
        init.init()
        stdscr = init.stdscr

        h, w = stdscr.getmaxyx()

        # Create falco and put him into the map
#        falco = Person(-1, "Falco", -1, [0, 0], ["F", curses.COLOR_WHITE, curses.COLOR_BLUE],
#                   configs.colorof["falco"][0])
#        falco.jumpTo(1, 0)
#        falco.crashWith = FalcoCrashMike

        theWorld = world.World(stdscr, w, h)

        # Mike is the hero!
        mike = Player(theWorld.statusBox, -1, "Du", -1, [0, 0], ["M", curses.COLOR_BLACK, curses.COLOR_RED],
                      configs.colorof["mike"][0], profile={"hp": [100, 100],
                                                       "mp": [0, 0]})

        # Adding mike and falco to Bermuda Triangle World
        theWorld.setPlayer(mike)
#        theWorld.addPerson(falco)

        theWorld.setCheatWalkEverywhere(False)

        # Adding water in map (mike cannot move on it)
        for i in range(10):
            theWorld.gMaps[1][1].gMap[10][i] = ["~", curses.COLOR_WHITE, curses.COLOR_BLUE, True, nothing]
        for i in range(10):
            theWorld.gMaps[1][0].gMap[10][198-i] = ["~", curses.COLOR_WHITE, curses.COLOR_BLUE, False, nothing]

        theWorld.load("testsave")
    
    
        while 1:                     # Gameloop
            timer.fpsDelay()         # FPS-Control
            clearError()
                                     # +++ Event handling +++
            c = stdscr.getch()       # I don't think an eventloop is needed in a
                                     # textadventure
            if c == ord("q"):
                theWorld.sendText("Bitte im Menue Beenden ('m' druecken)")
            if c == ord("w"): # Switches between colored and b/w
                misc.COLORED = not misc.COLORED
                theWorld.redrawAllMaps()
            if c == ord("m"): menu.start() # Enter menu
            if c == ord("h"): theWorld.playerGoLeft()  #
            if c == ord("j"): theWorld.playerGoDown()  #  Player
            if c == ord("k"): theWorld.playerGoUp()    #  movement
            if c == ord("l"): theWorld.playerGoRight() #
            if c == ord("s"): theWorld.load("testsave.btt")  # Loading doesn't really work ;)
            if c == ord("x"): theWorld.sendText(str(mike.gMap.pos))
            # --- Event handling ---

            # +++ Drawing +++
            oldH = h   # Need this for resizing
            oldW = w
            h, w = stdscr.getmaxyx()
            #stdscr.erase()
            # Window size exception
            if (w < 70) | (h < 24):
                stdscr.erase()
                stdscr.addstr(h/2, (w - len(BT_WINDOW_TOO_SMALL)) / 2,
                              BT_WINDOW_TOO_SMALL)
            elif misc.BT_ERROR != "":
                stdscr.addstr(h/2, (w - len(misc.BT_ERROR)) / 2,
                              misc.BT_ERROR)
            else:
                # Check for resize event
                if (oldH != h) | (oldW != w):
                    stdscr.erase()  # Have to clear the whole screen. Maybe this should do the theWorld object...
                    theWorld.resize(w, h)

                # Painting wonderful border ;)
                stdscr.box()
                stdscr.addstr(0, (w - len(BT_SMALL_LOGOTEXT)) / 2,
                              BT_SMALL_LOGOTEXT)

                theWorld.draw(stdscr)
                waveWare(w - 10, h - 1, stdscr)

            stdscr.refresh()
        # --- Drawing ---
    
        init.quit()

    except SystemExit:   # This is not really an error so there happens nothing
        pass
    except:              # If there was an error python will do this:
        # Exiting curses
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()

        # Telling there is went something wrong
        print "Hardcore error in Bermuda Triangle " + BT_VERSION + " :`(  Exiting forced!!!"
        print "Please send bt_last_error.log and a  description what you did"
        print "to neosam@gmail.com"

        # Writing error to file
        errorFile = file("bt_last_error.log", "w")
        errorFile.write("Error in Bermuda Triangle Text - Version " + BT_VERSION + "\n")
        traceback.print_exc(file=errorFile)
        errorFile.close()

        # If debug is switched on it will print the error to stdout
        if misc.DEBUG:
            traceback.print_exc()



if __name__ == "__main__":
    main()
