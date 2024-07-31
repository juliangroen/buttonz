import pyxel


class App:
    def __init__(self):
        pyxel.init(128, 128, fps=60)
        pyxel.load("./assets.pyxres")
        self.sprites = {
            "button_a": [(0, 0, 0, 16, 16, 13), (0, 16, 0, 16, 16, 13)],
            "button_b": [(0, 0, 16, 16, 16, 13), (0, 16, 16, 16, 16, 13)],
        }
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 0, 128, 128, 13)
        self.animated_button(0, 0, self.sprites["button_a"])
        self.animated_button(16, 0, self.sprites["button_b"])

    def animated_button(self, x, y, sprite):
        if pyxel.frame_count % 60 < 15:
            pyxel.blt(x, y, *sprite[1])
        else:
            pyxel.blt(x, y, *sprite[0])


App()
