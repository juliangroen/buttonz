import random

import pyxel

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256
FPS = 60


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, fps=FPS)
        pyxel.load("./assets.pyxres")
        self.running = False
        self.button_sprites = {
            "button_a": [(0, 0, 0, 16, 16, 13), (0, 16, 0, 16, 16, 13)],
            "button_b": [(0, 0, 16, 16, 16, 13), (0, 16, 16, 16, 16, 13)],
            "button_x": [(0, 0, 32, 16, 16, 13), (0, 16, 32, 16, 16, 13)],
            "button_y": [(0, 0, 48, 16, 16, 13), (0, 16, 48, 16, 16, 13)],
            "button_down": [(0, 0, 64, 16, 16, 13), (0, 16, 64, 16, 16, 13)],
            "button_right": [(0, 0, 80, 16, 16, 13), (0, 16, 80, 16, 16, 13)],
            "button_left": [(0, 0, 96, 16, 16, 13), (0, 16, 96, 16, 16, 13)],
            "button_up": [(0, 0, 112, 16, 16, 13), (0, 16, 112, 16, 16, 13)],
        }
        self.target_sprite = [(0, 48, 0, 16, 16, 13), (0, 32, 0, 16, 16, 13)]
        self.sp_mid_x = (WINDOW_WIDTH // 2) - 8
        self.sp_mid_y = (WINDOW_HEIGHT // 2) - 8
        self.bpm = 120
        self.fpb = (FPS * 60) // self.bpm
        self.current_buttons = []
        self.offset_counter = 1
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
        self.animated_sprite(80, 8, self.button_sprites["button_y"])
        self.animated_sprite(64, 24, self.button_sprites["button_x"])
        self.animated_sprite(96, 24, self.button_sprites["button_b"])
        self.animated_sprite(80, 40, self.button_sprites["button_a"])

        self.animated_sprite(24, 8, self.button_sprites["button_up"])
        self.animated_sprite(8, 24, self.button_sprites["button_left"])
        self.animated_sprite(40, 24, self.button_sprites["button_right"])
        self.animated_sprite(24, 40, self.button_sprites["button_down"])

        for button in self.current_buttons:
            self.animated_sprite(button["offset"], self.sp_mid_y, button["sprite"])
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
            yield random.choice(list(self.button_sprites.values()))

    def button_streamer(self):
        sprite = next(self.button_generator)
        sprite_width = sprite[0][3]
        offset = -sprite_width * (len(self.current_buttons) + 1) * 1.5
        self.current_buttons.append({"offset": offset, "sprite": sprite})

    def button_scroller(self):
        for button in self.current_buttons:
            sprite_width = button["sprite"][0][3]
            adjustment = (sprite_width * 1.5) / self.fpb
            distance_to_center = self.sp_mid_x - button["offset"]

            remainder = distance_to_center % adjustment

            if remainder != 0:
                adjustment = distance_to_center / round(distance_to_center / adjustment)

            button["offset"] += adjustment


App()
