import curses
import textout
import init
import sys

menuTitle = "/\\\\ Menue //\\"
MENU_W = 55

def btExit():
    init.quit()
    sys.exit()

def btContinue():
    pass

menuList = [["Weiterspielen", btContinue],
            ["Beenden", btExit]]

def drawMenu(menuWin, choice):
    menuWin.erase()
    menuWin.box()
    h, w = menuWin.getmaxyx()
    textout.textOut(menuTitle, (w - len(menuTitle)) / 2, 0, dst = menuWin)
    for i in range(len(menuList)):
        if choice == i:
            textout.textOut(">", 2, i + 2, dst = menuWin)
        textout.textOut(menuList[i][0], 4, i + 2, dst = menuWin)

def start():
    dsth, dstw = init.stdscr.getmaxyx()
    choice = 0
    x = (dstw - MENU_W) / 2
    y = (dsth - len(menuList)) / 2
    w = MENU_W
    h = len(menuList) + 4
    menuWin = curses.newwin(h, w, y, x)
    drawMenu(menuWin, choice)
    menuWin.refresh()
    while 1:
        c = menuWin.getch()
        if c == ord("j"):
            choice = choice + 1
        elif c == ord("k"):
            choice = choice - 1
        elif (c == ord("l")) | (c == ord(" ")):
            if menuList[choice][1] == btContinue:
                break
            else:
                menuList[choice][1]()

        choice = choice % len(menuList)
        drawMenu(menuWin, choice)
    
