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
        self._name = sprite_name
        self._width = self.sprite[0][3]
        self._height = self.sprite[0][4]

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

    @property
    def height(self):
        return self._height

    @property
    def name(self):
        return self._name


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, fps=FPS)
        pyxel.load("../assets.pyxres")
        self.running = False
        self.sp_mid_x = (WINDOW_WIDTH // 2) - 8
        self.sp_mid_y = (WINDOW_HEIGHT // 2) - 8
        self.animated_sprite_index = 0
        self.button_generator = self.create_button_generator()
        self.left_button = next(self.button_generator)
        self.right_button = next(self.button_generator)
        self.left_button_state = 0
        self.right_button_state = 0
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.button_input_controller()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if pyxel.mouse_x > WINDOW_WIDTH - 24 and pyxel.mouse_x < WINDOW_WIDTH:
                if pyxel.mouse_y > WINDOW_HEIGHT - 24 and pyxel.mouse_y < WINDOW_HEIGHT:
                    self.running = not self.running
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.running = not self.running

        if self.left_button_state == 1 and self.right_button_state == 1:
            self.left_button_state = 0
            self.right_button_state = 0
            self.left_button = next(self.button_generator)
            self.right_button = next(self.button_generator)

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 13)

        self.left_button.x = self.sp_mid_x - self.left_button.width
        self.left_button.y = self.sp_mid_y

        if self.left_button_state == 1:
            pyxel.dither(0.5)
        else:
            pyxel.dither(1)

        self.animated_sprite(
            self.left_button.x, self.left_button.y, self.left_button.sprite
        )

        self.right_button.x = self.sp_mid_x + self.right_button.width
        self.right_button.y = self.sp_mid_y

        if self.right_button_state == 1:
            pyxel.dither(0.5)
        else:
            pyxel.dither(1)

        self.animated_sprite(
            self.right_button.x, self.right_button.y, self.right_button.sprite
        )

        pyxel.dither(1)

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

    def create_button_generator(self):
        while True:
            sprite_name = random.choice(list(BUTTON_SPRITES.keys()))
            yield Button(-16, -16, sprite_name)

    def button_matcher(self, button_key):
        if self.left_button_state == 0:
            if self.left_button.name == button_key:
                self.left_button_state = 1
        else:
            if self.right_button.name == button_key:
                self.right_button_state = 1

    def button_input_controller(self):
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.KEY_K):
            self.button_matcher("button_a")
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_L):
            self.button_matcher("button_b")
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.KEY_J):
            self.button_matcher("button_x")
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y) or pyxel.btnp(pyxel.KEY_I):
            self.button_matcher("button_y")
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or pyxel.btnp(pyxel.KEY_S):
            self.button_matcher("button_down")
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT) or pyxel.btnp(pyxel.KEY_D):
            self.button_matcher("button_right")
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT) or pyxel.btnp(pyxel.KEY_A):
            self.button_matcher("button_left")
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btnp(pyxel.KEY_W):
            self.button_matcher("button_up")


App()
