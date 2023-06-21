import os, time
from pages import Home, Goodbye
from constants import Params

try:
    import pygame
except ImportError:
    print('Erro ao importar o Pygame. Tente $ pip install pygame')
    raise SystemExit

PARAMS = Params()

class Window():
    def __init__(self):

        # Parâmetros da tela
        self.screen = None
        self.size = (PARAMS.WIDTH, PARAMS.HEIGHT)
        # Páginas
        self.page = None
        # Parâmetros do jogo
        self.play = True

    def init(self):
        self.screen = pygame.display.set_mode(self.size)
        self.page = Home(self.screen, self.change_page)
        self.page.init()

    def change_page(self, page):
        self.page = page
        self.page.init()

    def refresh_screen(self):
        self.page.refresh_screen()

    def get_event(self):
        for event in pygame.event.get():
            self.page.get_event(event)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.page = Goodbye(self.screen, self.change_page)
                self.page.init()
                self.page.refresh_screen()
                time.sleep(2)
                self.play = False

    def exit(self):
        pygame.quit()

def run(window):
    clock = pygame.time.Clock()

    while window.play:
        clock.tick(PARAMS.FPS)
        window.refresh_screen()
        window.get_event()

    window.exit()

if __name__ == '__main__':
    window = Window()
    window.init()
    run(window)
