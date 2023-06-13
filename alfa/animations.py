import pygame

class Blink():
    def __init__(self, velocity: int = 12):
        self.velocity = velocity
        self.alpha = 255

    def play(self, surface = None, rendered = None):
        self.alpha = self.alpha - self.velocity if self.alpha >= self.velocity else 255
        surface.set_alpha(self.alpha)

class Hover():
    def __init__(self, first_color, secound_color):
        self.first_color = first_color
        self.color_on_hover = secound_color

    def get_events(self, surface = None, rendered = None):
        try:
            return rendered.collidepoint(pygame.mouse.get_pos())
        except AttributeError:
            return False
