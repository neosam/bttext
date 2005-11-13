import curses
import textout
import color
import configs
import textfield
import init

LEVEL_WIDTH = 200
LEVEL_HEIGHT = 200

def nothing():
	pass

class GameMap:
	def __init__(self, x, y, w, h):
		# Screen position
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.pos = [100, 100]
		self.size = [LEVEL_WIDTH, LEVEL_HEIGHT]
		self.drawPos = []
		self.drawAllFlag = True
		
		# Preparing level
		self.gMap = []
		for i in range(LEVEL_WIDTH):
			self.gMap.append([])
		for elem in self.gMap:
			for i in range(LEVEL_HEIGHT):
				elem.append([" ", 3, 7, True, 0])

	def __repr__(self):
		return str([[self.x, self.y, self.w, self.h], self.size, self.gMap])

	def getAscii(self, x, y):
		return self.gMap[x][y][0]
	def getFG(self, x, y):
		return self.gMap[x][y][1]
	def getBG(self, x, y):
		return self.gMap[x][y][2]
	def isWalkable(self, x, y):
		return self.gMap[x][y][3]
	def getElem(self, x, y):
		return self.gMap[x][y]
	def setAscii(self, x, y, ascii):
		if ascii != "\n":
			self.gMap[x][y][0] = ascii
			return True
		return False
	def setFG(self, x, y, color):
		self.gMap[x][y][1] = color
	def setBG(self, x, y, color):
		self.gMap[x][y][2] = color
	def saveToFile(self, filename):
		saveFile = file(filename, "w")
		saveFile.write( str(self.size[0]) + "\n" + str(self.size[1]))
		i = 0
		j = 0
		for row in self.gMap:
			for elem in row:
				saveFile.write( 
					     str(elem[0]) + "\n" + 
					     str(elem[1]) + "\n" +
					     str(elem[2]) + "\n" +
					     str(elem[3]) + "\n")
				i = i + 1
			j = j + 1
			textout.textOut ("[" + str(i) + ", " + str(j) + "]", 5, 5)
			init.stdscr.refresh()
			
				
				

	def resize(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def draw(self, dst):
		if self.drawAllFlag == True:
			self.drawAll(dst)
		else:
			for elem in self.drawPos:
#				pos = [self.pos[0] + (self.w/2 - elem[0]), 
#				       self.pos[1] + (self.h/2 - elem[1])]
                                pos = [elem[0],
				       elem[1]]

				if (pos[0] >= 0) & (pos[1] >= 0) & \
				       (pos[0] < LEVEL_WIDTH) & \
				       (pos[1] < LEVEL_HEIGHT):
					if configs.misc.COLORED == True:
						dst.addstr(self.y + elem[1] + self.h/2 - self.pos[1] + self.h%2,
							   self.x + elem[0] + self.w/2 - self.pos[0] + self.w%2,
							   self.gMap[pos[0]][pos[1]][0],
							   color.color(self.gMap[pos[0]][pos[1]][1],
								       self.gMap[pos[0]][pos[1]][2]))
					else:
						dst.addstr(self.y + elem[1] + self.h/2 - self.pos[1] + self.h%2,
							   self.x + elem[0] + self.w/2 - self.pos[0] + self.w%2,
							   self.gMap[pos[0]][pos[1]][0])
			self.drawPos = []

	def drawAll(self, dst):
		self.drawAllFlag = False
		for h in range(self.h):
			for  w in range(self.w):
				pos = [self.pos[0] + (self.w/2 - w),
				       self.pos[1] + (self.h/2 - h)]
				if (pos[0] >= 0) & (pos[1] >= 0) & \
				   (pos[0] < LEVEL_WIDTH) & \
				   (pos[1] < LEVEL_HEIGHT):
					if configs.misc.COLORED == True:
						dst.addstr(self.y + self.h - h,
							   self.x + self.w - w,
							   self.gMap[pos[0]][pos[1]][0],
							   color.color(self.gMap[pos[0]][pos[1]][1],
								       self.gMap[pos[0]][pos[1]][2]))
					else:
						dst.addstr(self.y + self.h - h,
							   self.x + self.w - w,
							   self.gMap[pos[0]][pos[1]][0])

