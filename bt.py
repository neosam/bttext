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

    myGM = GameMap(w/2 + 2, 6, w/2 - 4, 10)
    myGM.pos = [10, 4]
    myTF = Textfield(2, 6, w/2 - 5, h - 7)
    falco = Person(myTF, "Falco", myGM, [0, 0], ["F", 7, 4],
                   configs.colorof["falco"][0])
    falco.jumpTo(1, 0)
    mike = Person(myTF, "Du", myGM, [0, 0], ["M", 0, 3],
                  configs.colorof["mike"][0])

    for i in range(10):
        myGM.gMap[10][i] = ["~", 7, 4, False, nothing]
    
    
    myTF.sendText(BT_SMALL_LOGOTEXT + " - Kapitel 1")
    myTF.sendText("Die Kreidezeit")
    myTF.sendText("")
    myTF.sendText("Du stehst am Strand einer grossen Insel, in dessen Mitte ein grosser Vulkan empor ragt.  Neben dir auf dem Boden liegt ein Knochen, an dem ein spitzer Stein angebracht ist, sieht beinahe wie eine Waffe aus.")
    myTF.sendText("Du nimmst den Knochen")
    falco.comes()
    falco.say("Du bist auch hier??")
    mike.say("Ja, hallo Faklo!")
    falco.say("Ich heisse FALKO!!")
    mike.say("Sorry, war ein Tippfehler")
    falco.say("Verdammt... zuerst die komische vom Flughafen und dann auch noch du...")
    mike.say("Welche vom Flughafen?")
    falco.say("Vergiss es, pass auf")

    myTF.sendText("...")

    while 1:                     # Gameloop
        timer.fpsDelay()         # FPS-Control
        clearError()
        # +++ Event handling +++
        c = stdscr.getch()       # I don't think an eventloop is needed in an
                                 # textadventure
        if c == ord("q"):
            myTF.sendText("Mitte im Menue Beenden ('m' druecken)")
        if c == ord("w"): misc.COLORED = not misc.COLORED
        if c == ord("m"): menu.start()
        if c == ord("h"): mike.goLeft()
        if c == ord("j"): mike.goDown()
        if c == ord("k"): mike.goUp()
        if c == ord("l"): mike.goRight()
        # --- Event handling ---

        # +++ Drawing +++
        h, w = stdscr.getmaxyx()
        stdscr.erase()
        if (w < 70) | (h < 20):
            stdscr.addstr(h/2, (w - len(BT_WINDOW_TOO_SMALL)) / 2,
                          BT_WINDOW_TOO_SMALL)
        elif misc.BT_ERROR != "":
            stdscr.addstr(h/2, (w - len(misc.BT_ERROR)) / 2,
                          misc.BT_ERROR)
        else:
            myTF.resize(w/2 - 4, h - 7)
            myGM.resize(w/2 + 2, 6, w/2 - 5, h - 8)
            stdscr.box()
            stdscr.addstr(0, (w - len(BT_SMALL_LOGOTEXT)) / 2,
                          BT_SMALL_LOGOTEXT)
            myTF.draw()
            myGM.draw(stdscr)
            mike.draw(stdscr)
            falco.draw(stdscr)
            stdscr.vline(4, w/2, curses.ACS_VLINE, h - 5)
            stdscr.addstr(4, 2, "Meldungen:", curses.A_BOLD)
            stdscr.addstr(4, w/2 + 2, "Karte:", curses.A_BOLD)
            stdscr.addstr(2, 2, "Status: ", curses.A_BOLD)
            stdscr.addstr(2, 10, "AP: 100/100    MP: 100/100   Level: 1")
            waveWare(w - 10, h - 1)

        stdscr.refresh()
        # --- Drawing ---
    
    init.quit()

if __name__ == "__main__":
    main()
