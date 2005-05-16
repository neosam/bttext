import curses
import configs
import sys
import color

global stdscr, mainWin
stdscr = 0

def btInit():
    configs.colorof = {"talk": [0, False, False, False,
                    curses.COLOR_GREEN, curses.COLOR_BLACK],
           "move": [0, False, False, False,
                    curses.COLOR_YELLOW, curses.COLOR_BLACK],
           
           #Persons
           "mike": [0, False, False, False,
                    curses.COLOR_BLUE, curses.COLOR_BLACK],
           "falco": [0, False, False, False,
                     curses.COLOR_YELLOW, curses.COLOR_BLACK]}
    configs.recreateColors()


def init():
    """ init() -> None """
    global stdscr, mainWin
    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)
        stdscr.nodelay(1)
        try:
            curses.curs_set(0)
        except:
            pass

        try:
            curses.start_color()
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
            curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        except:
            configs.misc.COLORED = False
        btInit()
        color.init()
        print configs.colorof

    except:
        quit()
        print "Problems while initialize"
        print "Unexpected error:", sys.exc_info()[2].tb_next
        print sys.exc_info()[1]
        print configs.colorof
        
        sys.exit()

def quit():
    """ quit() -> None """
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
