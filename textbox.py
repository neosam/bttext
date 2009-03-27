import curses
from curses.textpad import Textbox

def textEdit(theWorld, title, text=""):
    title = "/\\\\ %s //\\" % title

    win = curses.newwin(theWorld.h - 6, theWorld.w - 10, 3, 5)
    win.box()
    size = win.getmaxyx()
    win.addstr(0, size[1] / 2 - len(title) / 2, title)
    win.refresh()
    win = curses.newwin(theWorld.h - 8, theWorld.w - 12, 4, 6)
    win.addstr(text)
    t = Textbox(win)
    return t.edit()

def lineEdit(theWorld, title, text=""):
    title = "/\\\\ %s //\\" % title

    win = curses.newwin(3, theWorld.w - 10, theWorld.h / 2 - 1, 6)
    win.box()
    size = win.getmaxyx()
    win.addstr(0, size[1] / 2 - len(title) / 2, title)
    win.refresh()
    win = curses.newwin(1, theWorld.w - 12, theWorld.h / 2, 7)
    t = Textbox(win)
    return t.edit()
