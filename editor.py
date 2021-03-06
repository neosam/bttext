import textbox
import statusbox
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
from curses.textpad import Textbox

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
mapFlags = []

def waveWare(x, y, dst):
    blue = str(curses.color_pair(4))
    white = str(curses.color_pair(7))
    ww = textout.btText("$%" + blue + "$%W$%" + white + "$%ave $%" + blue + "$%W$%" + white + "$%are")
    textout.textOut(ww, x, y, dst)

def borderFunction(self, w, h):
    self.border = w / 2

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
        theWorld.playerGoRight(force=True)
        theWorld.draw(stdscr)
        stdscr.refresh()
        asciiValue = insertAscii()

def insertVText():
    global cursor, stdscr, theWorld

    asciiValue = insertAscii()
    while asciiValue != "\n":
        theWorld.playerGoDown(force=True)
        theWorld.draw(stdscr)
        stdscr.refresh()
        asciiValue = insertAscii()

def fill():
    global cursor, stdscr, theWorld

    st = list()
    done = set()
    bg = theWorld.player.gMap[theWorld.player.pos].copy()
    goon = True
    while goon:
        try:
            asciiValue = stdscr.getkey()
            goon = False
        except:
            goon = True

    x, y = theWorld.player.pos

    st.append((x, y))
    while len(st) != 0:
        x, y = st.pop()

        if (x >= 0) and (x < LEVEL_WIDTH) and \
           (y >= 0) and (y < LEVEL_HEIGHT) and \
           ((x, y) not in done) and \
           (theWorld.player.gMap[x, y]['ascii'] == bg['ascii']) and \
           (theWorld.player.gMap[x, y]['bg'] == bg['bg']) and \
           (theWorld.player.gMap[x, y]['fg'] == bg['fg']):
            theWorld.player.gMap.setAscii(x, y, asciiValue)
            theWorld.player.gMap.setFG(x, y, foreground)
            theWorld.player.gMap.setBG(x, y, background)
            theWorld.player.gMap.setWalkable(x, y, walkable)

            st.append((x, y + 1))
            st.append((x, y - 1))
            st.append((x + 1, y))
            st.append((x - 1, y))
            done.add((x, y))
    theWorld.redrawAllMaps()

def insertFile():
    global cursor, stdscr, theWorld


    title = "/\\\\ Set field name //\\"
    win = curses.newwin(3, theWorld.w - 10, theWorld.h / 2 - 1, 6)
    win.box()
    size = win.getmaxyx()
    win.addstr(0, size[1] / 2 - len(title) / 2, title)
    win.refresh()
    win = curses.newwin(1, theWorld.w - 12, theWorld.h / 2, 7)
    t = Textbox(win)
    filename = t.edit()
    f = file(filename[:-1])

    x, y = theWorld.player.pos

    for line in f.readlines():
        for letter in line:
            theWorld.player.gMap.setAscii(x, y, letter)
            theWorld.player.gMap.setFG(x, y, foreground)
            theWorld.player.gMap.setBG(x, y, background)
            theWorld.player.gMap.setWalkable(x, y, walkable)
            x += 1
        x = theWorld.player.pos[0]
        y += 1


def addTrigger():
    global cursor, stdscr, theWorld

    dst = cursor.gMap[cursor.pos]
    text = ""
    if 'trigger' in dst:
        text = dst['trigger']
    dst['trigger'] = textbox.textEdit(theWorld, "Add trigger code", text)

def addRTrigger():
    global cursor, stdscr, theWorld

    dst = cursor.gMap[cursor.pos]
    text = ""
    if 'rtrigger' in dst:
        text = dst['rtrigger']
    dst['rtrigger'] = textbox.textEdit(theWorld, "Add rtrigger code", text)

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
        elif newForeground == "r":
            foreground = curses.COLOR_RED
        world.foreground = foreground

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
        elif newBackground == "r":
            background = curses.COLOR_RED
        world.background = background

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
    global theWorld, mapFlags

    theWorld.save("testsave")

    flagFile = file("testsave/mapFlags", "w")
    for elem in mapFlags:
        flagFile.write(",".join(elem) + "\n")

def insertFlag():
    global cursor, stdscr, theWorld

    k = textbox.lineEdit(theWorld, 'Set named field')
    cursor.gMap.setNamedField(k, cursor.pos)

def executeCode():
    global theWorld
    text = textbox.textEdit(theWorld,'hack')
    theWorld.evalCode(text)
    theWorld.lastExecuted = text

def repeatCode():
    global theWorld
    theWorld.evalCode(theWorld.lastExecuted)
    

def main():
    global stdscr, theWorld, cursor

    print BT_LOGO
    time.sleep(1)

    try: # Crash protection ;)
        init.init()
        stdscr = init.stdscr

        h, w = stdscr.getmaxyx()

        world.foreground = foreground
        world.background = background
        theWorld = world.World(stdscr, w, h, filename = sys.argv[1])
        theWorld.statusBox = statusbox.EditorStatusBox(stdscr, w, h, 
                                                       w / 2)
        theWorld.statusBox.newField(theWorld.maps[0, 0][0, 0])
        world.World.borderFunction = borderFunction
        theWorld.resize(w, h)

        theWorld.keys = {
            "h": [theWorld.playerGoLeft, (True,)],
            "j": [theWorld.playerGoDown, (True,)],
            "k": [theWorld.playerGoUp, (True,)],
            "l": [theWorld.playerGoRight, (True,)],
            "c": [executeCode, ()],
            "C": [repeatCode, ()],
            "A": [insertFile, ()],
            "a": [insertAscii, ()],
            "t": [insertText, ()],
            "v": [insertVText, ()],
            "F": [fill, ()],
            "T": [addTrigger, ()],
            "r": [addRTrigger, ()],
            "f": [changeForeground, ()],
            "b": [changeBackground, ()],
            "g": [changeWalkable, ()],
            "s": [saveMap, ()],
            "e": [insertFlag, ()]
        }
        # Initialize cursor object
        cursor = Player(theWorld.statusBox, -1, "Cursor", -1, theWorld, [0, 0], ["C", 0, 3],
                      configs.colorof["mike"][0], profile={"hp": [100, 100],
                                                       "mp": [0, 0]})

        theWorld.sendText("BTText Map Editor!")
        
        # Adding cursor to the world
        theWorld.setPlayer(cursor)

        # Loading editor initializing file
        try:
            filename = "%s/editinit.py" % sys.argv[1]
            initFile = file(filename).read()
            theWorld.evalCode(initFile, filename)
        except:
            theWorld.sendText(btText('Could not load editinit.py'))
            theWorld.sendText(btText('Use this file to extend this editor'))
            theWorld.sendText(str(sys.exc_info()[0]))
            theWorld.sendText(str(sys.exc_info()[1]))


        while 1:                     # Gameloop
            timer.fpsDelay()         # FPS-Control
            clearError()

            c = None
                                     # +++ Event handling +++
            try:
                c = stdscr.getkey()
            except curses.error:
                pass
                                     # textadventure
            if c == "q":
                init.quit()
                sys.exit()
#            if c == "w": # Switches between colored and b/w
#                misc.COLORED = not misc.COLORED
#                theWorld.redrawAllMaps()
            keys = theWorld.keys
            if c in keys:
                elem = keys[c]
                elem[0](*elem[1])
                if '' in keys:
                    elem = keys['']
                    elem[0](*elem[1])
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
