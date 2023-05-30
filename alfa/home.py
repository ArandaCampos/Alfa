import pygame
from components import Button_play_game
from items import Text

# Paleta de cor
BG_COLOR, BLUE = (222, 239, 231, .94), (1, 32, 48, 1.)

HEIGHT, WIDTH = 648, 1000

class Home():
    def __init__(self, screen):

        self.screen = screen
        self.caption = 'ALFA - MENU'
        # Título
        self.title = None
        # Botão
        self.button = None

    def init(self):
        self.title = Text(self.screen, 'ALFA', 'Noto Mono', 90, BLUE)
        self.title.init()
        self.title.set_margins(((WIDTH - self.title.size[0])/ 2, (HEIGHT - self.title.size[1])/ 2))
        self.button = Button_play_game(self.screen)
        self.button.init()

    def refresh_screen(self):
        self.screen.fill(BG_COLOR)
        self.button.draw() if self.button else None
        self.title.draw() if self.title else None
        pygame.display.set_caption(self.caption)
        pygame.display.flip()

    def get_event(self, event):
        pass

    def draw(self):
        self.title.draw()
        self.button.draw()
