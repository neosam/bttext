from distutils.core import setup
from distutils.extension import Extension
from Pyrex.Distutils import build_ext
setup(
  name = "PyrexGuide",
  ext_modules=[ 
  Extension("color",      ["color.pyx"], libraries = ["xosd"]),
  Extension("configs",    ["configs.pyx"], libraries = ["xosd"]),
  Extension("gamemap",    ["gamemap.pyx"], libraries = ["xosd"]),
  Extension("init",       ["init.pyx"], libraries = ["xosd"]),
  Extension("menu",       ["menu.pyx"], libraries = ["xosd"]),
  Extension("person",     ["person.pyx"], libraries = ["xosd"]),
  Extension("player",     ["player.pyx"], libraries = ["xosd"]),
  Extension("statusbox",  ["statusbox.pyx"], libraries = ["xosd"]),
  Extension("textfield",  ["textfield.pyx"], libraries = ["xosd"]),
#  Extension("textout",    ["textout.pyx"], libraries = ["xosd"]),
  Extension("timer",      ["timer.pyx"], libraries = ["xosd"]),
  Extension("world",      ["world.pyx"], libraries = ["xosd"])
  ],
  cmdclass = {'build_ext': build_ext}
)
