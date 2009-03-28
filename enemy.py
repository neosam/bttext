from person import Person
import random

class Enemy(Person):
    def onFrame(self):
        if random.randrange(10) == 0:
            random.choice([self.goLeft, self.goRight, 
                           self.goUp, self.goDown])()
    def onCrash(self):
        self.theWorld.sendText('')
        self.theWorld.sendText(self.name + ' hurts you')
        self.theWorld.player.setHP(self.theWorld.player.profile['hp'][0] - 10)
