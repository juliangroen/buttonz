import random
import sys

import pyxel

WINDOW_WIDTH = 256
WINDOW_HEIGHT = 256
FPS = 60


class App:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, fps=FPS)
        pyxel.load("./assets.pyxres")
        self.running = True
        self.sprites = {
            "button_a": [(0, 0, 0, 16, 16, 13), (0, 16, 0, 16, 16, 13)],
            "button_b": [(0, 0, 16, 16, 16, 13), (0, 16, 16, 16, 16, 13)],
            "button_x": [(0, 0, 32, 16, 16, 13), (0, 16, 32, 16, 16, 13)],
            "button_y": [(0, 0, 48, 16, 16, 13), (0, 16, 48, 16, 16, 13)],
            "button_down": [(0, 0, 64, 16, 16, 13), (0, 16, 64, 16, 16, 13)],
            "button_right": [(0, 0, 80, 16, 16, 13), (0, 16, 80, 16, 16, 13)],
            "button_left": [(0, 0, 96, 16, 16, 13), (0, 16, 96, 16, 16, 13)],
            "button_up": [(0, 0, 112, 16, 16, 13), (0, 16, 112, 16, 16, 13)],
        }
        self.sp_mid_x = (WINDOW_WIDTH // 2) - 8
        self.sp_mid_y = (WINDOW_HEIGHT // 2) - 8
        self.bpm = 120
        self.fpb = (FPS * 60) // self.bpm
        self.current_buttons = []
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.frame_count % self.fpb == 0:
            self.button_streamer()
            self.button_scroller()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 13)
        self.animated_button(80, 8, self.sprites["button_y"])
        self.animated_button(64, 24, self.sprites["button_x"])
        self.animated_button(96, 24, self.sprites["button_b"])
        self.animated_button(80, 40, self.sprites["button_a"])

        self.animated_button(24, 8, self.sprites["button_up"])
        self.animated_button(8, 24, self.sprites["button_left"])
        self.animated_button(40, 24, self.sprites["button_right"])
        self.animated_button(24, 40, self.sprites["button_down"])

        for button in self.current_buttons:
            self.animated_button(button["offset"], self.sp_mid_y, button["sprite"])

    def animated_button(self, x, y, sprite):
        if pyxel.frame_count % self.fpb < (self.fpb // 2):
            pyxel.blt(x, y, *sprite[1])
        else:
            pyxel.blt(x, y, *sprite[0])

    def button_generator(self):
        while self.running:
            yield random.choice(list(self.sprites.values()))

    def button_streamer(self):
        sprite = next(self.button_generator())
        counter = 1
        offset = -sprite[0][3] * counter
        self.current_buttons.append({"offset": offset, "sprite": sprite})
        counter += 1

    def button_scroller(self):
        for button in self.current_buttons:
            button["offset"] += (button["sprite"][0][3]) + 8


App()
