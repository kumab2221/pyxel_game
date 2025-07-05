import pyxel

pyxel.init(160, 120)
pyxel.caption = "Pyxel Test"

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    pyxel.text(50, 60, "Pyxel is working!", 7)

pyxel.run(update, draw)
