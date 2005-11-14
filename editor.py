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
import traceback


global stdscr

BT_VERSION = "07112005"

BT_SMALL_LOGO = "/\\\\"
BT_SMALL_BACKLOGO = "//\\"
BT_SMALL_LOGOTEXT = BT_SMALL_LOGO + " Bermuda Triangle Editor " + BT_SMALL_BACKLOGO

BT_LOGO = file("btlogo.txt").read()

BT_WINDOW_TOO_SMALL = "Fenster zu klein"

theWorld = 0
curser = 0
foreground = curses.COLOR_BLACK
background = curses.COLOR_WHITE
walkable = True

def waveWare(x, y, dst):
    blue = str(curses.color_pair(4))
    white = str(curses.color_pair(7))
    ww = textout.btText("$%" + blue + "$%W$%" + white + "$%ave $%" + blue + "$%W$%" + white + "$%are")
    textout.textOut(ww, x, y, dst)

def insertAscii():
    global theWorld, foreground

    goon = True
    while goon:
        try:
            asciiValue = stdscr.getkey()
            goon = False
        except:
            goon = True
        
    
    if cursor.gMap.setAscii(cursor.pos[0], cursor.pos[1], asciiValue):
        cursor.gMap.setFG(cursor.pos[0], cursor.pos[1], foreground)
        cursor.gMap.setBG(cursor.pos[0], cursor.pos[1], background)
        cursor.gMap.setWalkable(cursor.pos[0], cursor.pos[1], walkable)
    return asciiValue

def insertText():
    global cursor, stdscr, theWorld

    asciiValue = insertAscii()
    while asciiValue != "\n":
        theWorld.playerGoRight()
        theWorld.draw(stdscr)
        stdscr.refresh()
        asciiValue = insertAscii()
        


def changeForeground():
    global stdscr, foreground

    newForeground = ""
    goon = True
    while goon:
        try:
            newForeground = stdscr.getkey()
            goon = False
        except:
            goon = True

        if newForeground == "b":
            foreground = curses.COLOR_BLUE
        elif newForeground == "w":
            foreground = curses.COLOR_WHITE
        elif newForeground == "x":
            foreground = curses.COLOR_BLACK
        elif newForeground == "g":
            foreground = curses.COLOR_GREEN
        elif newForeground == "y":
            foreground = curses.COLOR_YELLOW

def changeBackground():
    global stdscr, background

    newBackground = ""
    goon = True
    while goon:
        try:
            newBackground = stdscr.getkey()
            goon = False
        except:
            goon = True

        if newBackground == "b":
            background = curses.COLOR_BLUE
        elif newBackground == "w":
            background = curses.COLOR_WHITE
        elif newBackground == "x":
            background = curses.COLOR_BLACK
        elif newBackground == "g":
            background = curses.COLOR_GREEN
        elif newBackground == "y":
            background = curses.COLOR_YELLOW

def changeWalkable():
    global stdscr, walkable

    newWalkable = ""
    goon = True
    while goon:
        try:
            newWalkable = stdscr.getkey()
            goon = False
        except:
            goon = True

        if newWalkable == "t":
            walkable = True
        elif newWalkable == "f":
            walkable = False

def saveMap():
    global theWorld

    theWorld.save("testsave.btt")

def main():
    global stdscr, theWorld, cursor

    print BT_LOGO
    time.sleep(1)

    try: # Crash protection ;)
        init.init()
        stdscr = init.stdscr

        h, w = stdscr.getmaxyx()


        theWorld = world.World(stdscr, w, h)

        shortcutList = [
            ["h", theWorld.playerGoLeft],
            ["j", theWorld.playerGoDown],
            ["k", theWorld.playerGoUp],
            ["l", theWorld.playerGoRight],
            ["a", insertAscii],
            ["t", insertText],
            ["f", changeForeground],
            ["b", changeBackground],
            ["g", changeWalkable],
            ["s", saveMap]]
        # Initialize cursor object
        cursor = Player(theWorld.statusBox, -1, "Cursor", -1, [0, 0], ["C", 0, 3],
                      configs.colorof["mike"][0], profile={"hp": [100, 100],
                                                       "mp": [0, 0]})

        theWorld.sendText("BTText Map Editor!")
        
        # Adding cursor to the world
        theWorld.setPlayer(cursor)

        theWorld.setCheatWalkEverywhere(True)

        while 1:                     # Gameloop
            timer.fpsDelay()         # FPS-Control
            clearError()
                                     # +++ Event handling +++
            c = stdscr.getch()       # I don't think an eventloop is needed in a
                                     # textadventure
            if c == ord("q"):
                init.quit()
                sys.exit()
            if c == ord("w"): # Switches between colored and b/w
                misc.COLORED = not misc.COLORED
                theWorld.redrawAllMaps()
            for elem in shortcutList:
                if c == ord(elem[0]):
                    elem[1]()
#            if c == ord("m"): menu.start() # Enter menu
#            if c == ord("h"): theWorld.playerGoLeft()  #
#            if c == ord("j"): theWorld.playerGoDown()  #  Cursor
#            if c == ord("k"): theWorld.playerGoUp()    #  movement
#            if c == ord("l"): theWorld.playerGoRight() #
#            if c == ord("s"): theWorld.save("testsave.btt")  # Loading doesn't really work ;)
#            if c == ord("a"): insertAscii()
#            if c == ord("t"): insertText()
#            if c == ord("f"): changeForeground()
#            if c == ord("b"): changeBackground()

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
