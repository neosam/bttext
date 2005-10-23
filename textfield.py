import curses
import init
from textout import btText, textOut

STD_MAX_LINES = 100

class Textfield:
    def __init__(self, x, y, w, h, max = STD_MAX_LINES):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.maxLines = max
        self.lines = 0
        self.line = []
        self.colors = []

    def newLine(self):
        self.lines = self.lines + 1

    def sendText(self, text2):
        text = btText(text2)
        while len(text) > self.w:
            line = text.getRegion(0, self.w)
            other = text.getRegion(self.w, len(text))
            words = line.split(" ")
            if (len(words[0]) < self.w):
                col = line.getColor(len(text))
                text = btText("$%"+col+"$%" + words.pop() + other)
                self.line.append(btText("$%" + col + "$%" + " ".join(words)))
            else:
                self.line.append(btText(words[0]))
                words.remove(btText(words[0]))
                text = other
            self.newLine()
            
        self.line.append(text)
        self.newLine()

    def draw(self):
        if self.lines > self.h:
            height = self.lines
            begin = self.lines - self.h
        else:
            begin = 0
            height = self.lines

        for i in range(begin, height):
            if len(self.line[i]) > self.w:
                textOut(self.line[i].getRegion(0, self.w), self.x,
                        self.y + i - begin)
                #textOut("".join([self.line[i][elem] for elem in range(self.w)]),
                    #self.x, self.y + i - begin)
                    
            else:
                textOut(self.line[i], self.x, self.y + i - begin)

    def resize(self, w, h):
        self.w = w
        self.h = h
