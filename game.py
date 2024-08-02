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
        """The x cordinate"""
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        """The y cordinate"""
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
        pyxel.load("./assets.pyxres")
        self.running = False
        self.target_sprite = [(0, 48, 0, 16, 16, 13), (0, 32, 0, 16, 16, 13)]
        self.sp_mid_x = (WINDOW_WIDTH // 2) - 8
        self.sp_mid_y = (WINDOW_HEIGHT // 2) - 8
        self.bpm = 120
        self.fpb = (FPS * 60) // self.bpm
        self.current_buttons = []
        self.animated_sprite_index = 0
        self.button_generator = self.create_button_generator()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.frame_count % self.fpb == 0 and self.running:
            pyxel.play(0, 0)
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.running = not self.running
        if len(self.current_buttons) < 10:
            self.button_streamer()
        if self.running:
            self.button_scroller()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 13)
        self.animated_sprite(80, 8, BUTTON_SPRITES["button_y"])
        self.animated_sprite(64, 24, BUTTON_SPRITES["button_x"])
        self.animated_sprite(96, 24, BUTTON_SPRITES["button_b"])
        self.animated_sprite(80, 40, BUTTON_SPRITES["button_a"])

        self.animated_sprite(24, 8, BUTTON_SPRITES["button_up"])
        self.animated_sprite(8, 24, BUTTON_SPRITES["button_left"])
        self.animated_sprite(40, 24, BUTTON_SPRITES["button_right"])
        self.animated_sprite(24, 40, BUTTON_SPRITES["button_down"])

        for button in self.current_buttons:
            if button.x > (self.sp_mid_x + button.width):
                pyxel.dither(0.50)
            self.animated_sprite(button.x, self.sp_mid_y, button.sprite)
            pyxel.dither(1)
        self.animated_sprite(self.sp_mid_x, self.sp_mid_y, self.target_sprite)

    def animated_sprite(self, x, y, sprite):
        if self.running:
            if pyxel.frame_count % self.fpb < (self.fpb // 2):
                self.animated_sprite_index = 1
            else:
                self.animated_sprite_index = 0

        pyxel.blt(x, y, *sprite[self.animated_sprite_index])

    def create_button_generator(self):
        while True:
            sprite_name = random.choice(list(BUTTON_SPRITES.keys()))
            yield Button(0, 0, sprite_name)

    def button_streamer(self):
        button = next(self.button_generator)
        sprite_width = button.width
        offset = -sprite_width * (len(self.current_buttons) + 1) * 1.5
        button.x = offset
        self.current_buttons.append(button)

    def button_scroller(self):
        for button in self.current_buttons:
            sprite_width = button.width
            adjustment = (sprite_width * 1.5) / self.fpb
            distance_to_center = self.sp_mid_x - button.x

            remainder = distance_to_center % adjustment

            if remainder != 0:
                adjustment = distance_to_center / round(distance_to_center / adjustment)

            button.x += adjustment


App()
