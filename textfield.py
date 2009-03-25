import curses
import init
#from textout import btText, textOut
import textout

STD_MAX_LINES = 100

class Textfield(object):
    def __init__(self, x, y, w, h, max = STD_MAX_LINES):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.maxLines = max
        self.lines = 0
        self.line = []
        self.colors = []
        self.f = file('messages.log', 'a')

    def newLine(self):
        self.lines = self.lines + 1

    def sendText(self, text2):
        self.f.write(str(text2) + '\n')
        self.f.flush()
        text = textout.btText(text2)
        while len(text) > self.w:
            line = text.getRegion(0, self.w)
            other = text.getRegion(self.w, len(text))
            words = line.split(" ")
            if (len(words[0]) < self.w):
                col = line.getColor(len(text))
                text = textout.btText("$%"+col+"$%" + words.pop() + other)
                self.line.append(textout.btText("$%" + col + "$%" + " ".join(words)))
            else:
                self.line.append(textout.btText(words[0]))
                words.remove(textout.btText(words[0]))
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

        blankLine = " " * self.w

        for i in range(begin, height):
            textout.textOut(blankLine, self.x, self.y + i - begin)
            if len(self.line[i]) > self.w:
                textout.textOut(self.line[i].getRegion(0, self.w), self.x,
                        self.y + i - begin)
                #textOut("".join([self.line[i][elem] for elem in range(self.w)]),
                    #self.x, self.y + i - begin)
                    
            else:
                textout.textOut(self.line[i], self.x, self.y + i - begin)

    def resize(self, w, h):
        self.w = w
        self.h = h
