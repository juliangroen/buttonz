import random

import pyxel

RUNNING = False
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


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, fps=FPS)
        pyxel.load("../assets.pyxres")
        self.sp_mid_x = (WINDOW_WIDTH // 2) - 8
        self.sp_mid_y = (WINDOW_HEIGHT // 2) - 8
        self.animated_sprite_index = 0
        self.button_generator = self.create_button_generator()
        self.difficulty = 4
        self.button_pattern = []
        self.confirm_delay = 0
        self.input_counter = 0
        self.hp = 4
        self.score = 0
        self.flash = 0
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def restart_game(self):
        self.confirm_delay = 0
        self.input_counter = 0
        self.hp = 4
        self.score = 0
        self.flash = 0
        self.button_pattern = []

    def update(self):
        global RUNNING

        if self.hp <= 0:
            RUNNING = False
            self.restart_game()

        if self.flash > 0:
            self.flash -= 1

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if pyxel.mouse_x > WINDOW_WIDTH - 24 and pyxel.mouse_x < WINDOW_WIDTH:
                if pyxel.mouse_y > WINDOW_HEIGHT - 24 and pyxel.mouse_y < WINDOW_HEIGHT:
                    RUNNING = not RUNNING
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START):
            RUNNING = not RUNNING

        if RUNNING:
            self.button_input_controller()
            if self.pattern_checker():
                if self.confirm_delay >= 15:
                    self.pattern_maker()
                    self.confirm_delay = 0
                self.confirm_delay += 1

    def draw(self):
        pyxel.cls(0)

        pyxel.rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 13)
        pyxel.rectb(
            WINDOW_WIDTH // 4,
            WINDOW_HEIGHT // 4,
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT // 2,
            0,
        )

        if self.flash > 0:
            pyxel.rectb(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 8)
            pyxel.rectb(1, 1, WINDOW_WIDTH - 2, WINDOW_HEIGHT - 2, 8)

        for button in self.button_pattern:
            if button.hit:
                pyxel.dither(0.5)
            button.draw_sprite()
            pyxel.dither(1)

        if RUNNING:
            pyxel.blt(WINDOW_WIDTH - 24, WINDOW_HEIGHT - 24, 0, 48, 16, 16, 16, 13)
        else:
            pyxel.blt(WINDOW_WIDTH - 24, WINDOW_HEIGHT - 24, 0, 32, 16, 16, 16, 13)

        pyxel.text(8, 8, f"LIVES: {self.hp}/4", 0)
        pyxel.text(8, 16, f"SCORE: {self.score}", 0)

    def animated_sprite(self, x, y, sprite):
        if RUNNING:
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
        button = self.button_pattern[self.input_counter]

        if button.name == button_key:
            if button.hit == 0:
                button.hit = 1
                self.score += 1

            if self.input_counter == 3:
                self.input_counter = 0
            else:
                self.input_counter += 1
        else:
            self.flash = 15
            self.hp -= 1

    def pattern_checker(self):
        for button in self.button_pattern:
            if not button.hit:
                return False
        return True

    def pattern_maker(self):
        self.button_pattern = []
        grid = self.button_grid_cords()
        for _ in range(self.difficulty):
            button = next(self.button_generator)
            button.x, button.y = next(grid)
            self.button_pattern.append(button)

    def button_grid_cords(self):
        coordinates = []
        total = self.difficulty
        cell = 24
        width = cell * total
        x = (WINDOW_WIDTH // 2) - (width // 2) + 4
        y = WINDOW_HEIGHT // 2

        for i in range(total):
            coordinates.append((x + (cell * i), y))

        for coord in coordinates:
            yield coord

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


class Button:
    def __init__(self, x, y, sprite_name):
        self._x = x
        self._y = y
        self._sprite = BUTTON_SPRITES[sprite_name]
        self._name = sprite_name
        self._width = self.sprite[0][3]
        self._height = self.sprite[0][4]
        self._hit = 0
        self._animated_sprite_index = 0

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

    @property
    def hit(self):
        return self._hit

    @hit.setter
    def hit(self, value):
        self._hit = value

    def draw_sprite(self):
        if RUNNING:
            if (pyxel.frame_count // 30) % 2 == 0:
                self._animated_sprite_index = 1
            else:
                self._animated_sprite_index = 0

        pyxel.blt(self._x, self._y, *self._sprite[self._animated_sprite_index])


App()
