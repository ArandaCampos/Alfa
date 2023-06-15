import pygame

class Blink():
    def __init__(self, velocity: int = 12):
        self.velocity = velocity
        self.alpha = 255

    def play(self, surface = None, rendered = None):
        self.alpha = self.alpha - self.velocity if self.alpha >= self.velocity else 255
        surface.set_alpha(self.alpha)

class Wait():
    def __init__(self, time: int, func_wait):
        self.time = time
        self.count = 0
        self.func_wait = func_wait

    def play(self, surface = None, rendered = None):
        if self.count == self.time:
            self.func_wait()
            self.count += 1
        elif self.count < self.time:
            self.count += 1
