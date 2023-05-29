import pygame
from components import Button_play_game, Menu
from items import Text

# Paleta de cor
BG_COLOR, BLUE = (222, 239, 231, .94), (1, 32, 48, 1.)
ORANGE_LIGHT, GREEN_LIGHT = (242, 68, 5, 1.), (154, 235, 163, 1.)
WHITE = (240, 240, 242, .95)

HEIGHT, WIDTH = 648, 800

class Menu_page():
    def __init__(self, screen):

        self.screen = screen
        self.caption = 'ALFA - MENU'
        # Título
        self.title = None
        # Botão
        self.button = None
        self.menu = None

    def init(self):
        self.menu = Menu(self.screen)
        self.menu.init()
        self.title = Text(self.screen, 'ALFA', 'Noto Mono', 90, BLUE)
        self.title.init()
        self.title.set_margins(((WIDTH - self.title.size[0])/ 2, 150))
        #self.button = Button_play_game(self.screen)
        #self.button.init()

    def refresh_screen(self):
        self.screen.fill(BG_COLOR)
        #self.button.draw() if self.button else None
        self.title.draw() if self.title else None
        self.menu.draw() if self.menu else None
        pygame.display.set_caption(self.caption)
        pygame.display.flip()

    def get_event(self, event):
        pos = pygame.mouse.get_pos()

        for button, label in zip(self.menu.button, self.menu.label):
            if pos[0] > button.margins[0] and pos[0] < button.margins[0] + button.size[0] and pos[1] > button.margins[1] and pos[1] < button.margins[1] + button.size[1]:
                    button.color = ORANGE_LIGHT
                    label.color = WHITE
            else:
                button.color = GREEN_LIGHT
                label.color = BLUE

    def draw(self):
        self.menu.draw()
        self.title.draw()
        #self.button.draw()
