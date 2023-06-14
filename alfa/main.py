import os
from complete import Game_complete, Menu_complete
from items import Button, Text, Page
from animations import Blink

try:
    import pygame
except ImportError:
    print('Erro ao importar o Pygame. Verifique se o ambiente virtual está habilitado ou o pacote instalado')
    raise SystemExit

BG_COLOR, BLUE = (222, 239, 231, 240), (1, 32, 48, 255)
ORANGE_LIGHT, GREEN_LIGHT = (242, 68, 5, 255), (154, 235, 163, 255)
HEIGHT, WIDTH = 648, 1000

class Home(Page):
    def __init__(self, screen, func):

        super().__init__(screen, "PÁGINA INICIAL - ALFA", BG_COLOR, func)

    def func_to_menu(self, event = None):
        self.func(Menu_complete(self.screen, self.func))

    def init(self):
        self.components.append(Text(self.screen, 'ALFA', 'Noto Mono', 90, ORANGE_LIGHT))
        self.components.append(Text(self.screen, 'PRESSIONE QUALQUER TECLA PARA CONTINUAR', 'Noto Mono', 24, BLUE))
        for component in self.components:
            component.init()
        # configurar margins
        self.components[0].set_margins(((WIDTH - self.components[0].size[0])/ 2, (HEIGHT - self.components[0].size[1])/ 2))
        self.components[1].set_margins(((WIDTH - self.components[1].size[0]) /2 , HEIGHT - 75 - 100))
        # configurar eventos e animações
        self.components[1].set_blink()
        self.components[1].set_hover(ORANGE_LIGHT)
        self.components[1].set_click(self.func_to_menu)
        self.components[1].set_keydown(self.func_to_menu)

class Window():
    def __init__(self):

        # Parâmetros da tela
        self.screen = None
        self.size = (1000, 648)
        # Páginas
        self.page = Home(self.screen, self.change_page)
        # Parâmetros do jogo
        self.play = True

    def init(self):
        self.screen = pygame.display.set_mode(self.size)
        self.page = Home(self.screen, self.change_page)
        self.page.init()

    def change_page(self, page):
        print("Modificando para página " + str(page))
        self.page = page
        self.page.init()

    def refresh_screen(self):
        self.page.refresh_screen()

    def get_event(self):
        for event in pygame.event.get():
            self.page.get_event(event)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.play = False

    def exit(self):
        pygame.quit()

def run(window):
    clock = pygame.time.Clock()

    while window.play:
        clock.tick(40)

        window.refresh_screen()
        window.get_event()

    print('OBRIGADO POR JOGAR <3')
    window.exit()

if __name__ == '__main__':
    window = Window()
    window.init()
    run(window)
