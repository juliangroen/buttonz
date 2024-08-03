import random

import pyxel

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256
FPS = 60
BUTTON_SPRITES = {
    "button_a": [(0, 0, 0, 16, 16, 13), (0, 16, 0, 16, 16, 13)],
    "button_b": [(0, 0, 16, 16, 16, 13), (0, 16, 16, 16, 16, 13)],
    "button_x": [(0, 0, 32, 16, 16, 13), (0, 16, 32, 16, 16, 13)],
    "button_y": [(0, 0, 48, 16, 16, 13), (0, 16, 48, 16, 16, 13)],
    "button_down": [(0, 0, 64, 16, 16, 13), (0, 16, 64, 16, 16, 13)],
    "button_right": [(0, 0, 80, 16, 16, 13), (0, 16, 80, 16, 16, 13)],
    "button_left": [(0, 0, 96, 16, 16, 13), (0, 16, 96, 16, 16, 13)],
    "button_up": [(0, 0, 112, 16, 16, 13), (0, 16, 112, 16, 16, 13)],
}


class Button:
    def __init__(self, x, y, sprite_name):
        self._x = x
        self._y = y
        self._sprite = BUTTON_SPRITES[sprite_name]
        self._width = self.sprite[0][3]

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def sprite(self):
        return self._sprite

    @property
    def width(self):
        return self._width


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, fps=FPS)
        pyxel.load("../assets.pyxres")
        self.running = False
        self.sp_mid_x = (WINDOW_WIDTH // 2) - 8
        self.sp_mid_y = (WINDOW_HEIGHT // 2) - 8
        self.animated_sprite_index = 0
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if pyxel.mouse_x > WINDOW_WIDTH - 24 and pyxel.mouse_x < WINDOW_WIDTH:
                if pyxel.mouse_y > WINDOW_HEIGHT - 24 and pyxel.mouse_y < WINDOW_HEIGHT:
                    self.running = not self.running
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.running = not self.running

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 13)

        button = Button(self.sp_mid_x, self.sp_mid_y, "button_a")
        self.animated_sprite(button.x, button.y, button.sprite)

        if self.running:
            pyxel.blt(WINDOW_WIDTH - 24, WINDOW_HEIGHT - 24, 0, 48, 16, 16, 16, 13)
        else:
            pyxel.blt(WINDOW_WIDTH - 24, WINDOW_HEIGHT - 24, 0, 32, 16, 16, 16, 13)

    def animated_sprite(self, x, y, sprite):
        if self.running:
            if (pyxel.frame_count // 30) % 2 == 0:
                self.animated_sprite_index = 1
            else:
                self.animated_sprite_index = 0

        pyxel.blt(x, y, *sprite[self.animated_sprite_index])


App()
