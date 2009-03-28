from person import Person

class Enemy(person.Person):
    def onFrame(self):
        self.goLeft()
