from init import *
import init
import sys

class Person:
    def __init__(self, tf, name, color = configs.color.green):
        self.tf = tf
        self.color = color
        self.name = name

    def say(self, text):
        try:
            self.tf.sendText("$%" + str(self.color) + "$%" + self.name +
                             ":$%" + str(configs.colorof["talk"][0]) + "$% " + text)
        except:
            init.quit()
            print "Unexpected error:", sys.exc_info()[2].tb_next
            print sys.exc_info()[1]
            print configs.colorof
            sys.exit()

    def comes(self):
        try:
            self.tf.sendText("$%" + str(configs.colorof["move"][0]) + "$%" +
                             self.name + " naehert sich")
        except:
            init.quit()
            print sys.exc_info()[2].tb_next
            print sys.ext_info()[1]
