import pygame

class Blink():
    def __init__(self, velocity: int = 12):
        self.velocity = velocity
        self.alpha = 255

    def play(self, surface = None, rendered = None):
        self.alpha = self.alpha - self.velocity if self.alpha >= self.velocity else 255
        surface.set_alpha(self.alpha)
