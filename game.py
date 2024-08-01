import pyxel

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, fps=60)
        pyxel.load("./assets.pyxres")
        self.sprites = {
            "button_a": [(0, 0, 0, 16, 16, 13), (0, 16, 0, 16, 16, 13)],
            "button_b": [(0, 0, 16, 16, 16, 13), (0, 16, 16, 16, 16, 13)],
            "button_x": [(0, 0, 32, 16, 16, 13), (0, 16, 32, 16, 16, 13)],
            "button_y": [(0, 0, 48, 16, 16, 13), (0, 16, 48, 16, 16, 13)],
            "button_right": [(0, 0, 64, 16, 16, 13), (0, 16, 64, 16, 16, 13)],
        }
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 13)
        self.animated_button(24, 8, self.sprites["button_y"])
        self.animated_button(8, 24, self.sprites["button_x"])
        self.animated_button(40, 24, self.sprites["button_b"])
        self.animated_button(24, 40, self.sprites["button_a"])

        self.animated_button(64, 64, self.sprites["button_right"])

    def animated_button(self, x, y, sprite):
        if pyxel.frame_count % 60 < 15:
            pyxel.blt(x, y, *sprite[1])
        else:
            pyxel.blt(x, y, *sprite[0])


App()
