from person import Person
import random

class Enemy(Person):
    def onFrame(self):
        if random.randrange(10) == 0:
            random.choice([self.goLeft, self.goRight, 
                           self.goUp, self.goDown])()
