import configs
from person import Person

class Player (Person):
    def __init__(self, statusBox, tf, name, gMap, w, pos = [0,0],
                 mapDraw=["P", 0, 7], color = configs.color.green, profile=0):
        Person.__init__(self, tf, name, gMap, w, pos, mapDraw, color, profile)
        self.setStatusBox(statusBox)
        self.onChangeHP()

    def setStatusBox(self, statusBox):
        self.statusBox = statusBox

    def onChangeHP(self):
        self.statusBox.changeHP(self.profile["hp"])
        if self.profile['hp'][0] == 0: self.theWorld.dead()

    def onChangeMP(self):
        self.statusBox.changeHP(self.profile["mp"])

