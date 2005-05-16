import curses

def init():
    curses.start_color()
    if curses.has_colors():
        for i in range(8):
            for j in range(8):
                if (i * 8 + j) != 0:
                    curses.init_pair(i * 8 + j, j, i)

def color(fg, bg):
    return curses.color_pair(bg * 8 + fg)
