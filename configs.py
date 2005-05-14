import curses
import init

class color:
    black = 0
    red = 1
    green = 2
    yellow = 3
    blue = 4
    magenta = 5
    cyan = 6
    white = 7


colorof = {}

def recreateColors():
    if misc.COLORED:
        for elem in colorof:
            colorof[elem][0] = curses.color_pair(colorof[elem][4])


def addError(text):
    misc.BT_ERROR = misc.BT_ERROR + text
def clearError():
    misc.BT_ERROR = ""

class misc:
    BT_ERROR = ""
    COLORED = True
