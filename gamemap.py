import curses
import textout
import color

LEVEL_WIDTH = 20
LEVEL_HEIGHT = 20

class GameMap:
	def __init__(self, x, y, w, h):
		# Screen position
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.pos = [10, 10]
		
		# Preparing level
		self.gMap = []
		for i in range(LEVEL_WIDTH):
			self.gMap.append([])
		for elem in self.gMap:
			for i in range(LEVEL_HEIGHT):
				elem.append([" ", 0, 7, True])
		self.gMap[10][10][0] = "M"

	def resize(self, x, y, w, h):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

	def draw(self, dst):
		for h in range(self.h):
			for  w in range(self.w):
				pos = [self.pos[0] + (self.w/2 - w),
				       self.pos[1] + (self.h/2 - h)]
				if (pos[0] > 0) & (pos[1] > 1) & \
				   (pos[0] < LEVEL_WIDTH) & \
				   (pos[1] < LEVEL_HEIGHT):
					dst.addstr(self.y + h, self.x + w,
						self.gMap[pos[0]][pos[1]][0],
						   color.color(self.gMap[pos[0]][pos[1]][1],
							       self.gMap[pos[0]][pos[1]][2]))

