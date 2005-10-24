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
import gui


global stdscr

BT_VERSION = "23102005"

BT_SMALL_LOGO = "/\\\\"
BT_SMALL_BACKLOGO = "//\\"
BT_SMALL_LOGOTEXT = BT_SMALL_LOGO + " Bermuda Triangle Editor " + BT_SMALL_BACKLOGO

BT_LOGO = file("btlogo.txt").read()

BT_WINDOW_TOO_SMALL = "Fenster zu klein"


def waveWare(x, y, dst):
    blue = str(curses.color_pair(4))
    white = str(curses.color_pair(7))
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


        theWorld = world.World(stdscr, w, h)

        # Initialize cursor object
        cursor = Player(theWorld.statusBox, -1, "Du", -1, [0, 0], ["M", 0, 3],
                      configs.colorof["mike"][0], profile={"hp": [100, 100],
                                                       "mp": [0, 0]})
        
        # Adding cursor to the world
        theWorld.setPlayer(cursor)

        win = gui.Window(None)
        win.addObj(gui.ObjButton(win, "Hallo Welt"))
        win.draw()
        stdscr.getch()

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
            if c == ord("s"): theWorld.save("testsave.btt")  # Loading doesn't really work ;)
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

    except:
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()
        errorString = ""
#        print dir(sys.exc_info()[2].tb_lasti)
        print "Hardcore error in Bermuda Triangle " + BT_VERSION + " :`(  Exiting forced!!!"
        print "Please send bt_last_error.log to neosam@gmail.com"

        print "Unexpected error:", sys.exc_info()[2].tb_next
        print sys.exc_info()[1]
        
        # TODO: There really should be a bt_last_error.log ;)


if __name__ == "__main__":
    main()
