import os, time
from complete import Game_complete, Menu_complete
from basics_math import Menu_math
from items import Button, Text, Page, Image
from constants import Colors, Params

try:
    import pygame
except ImportError:
    print('Erro ao importar o Pygame. Tente $ pip install pygame')
    raise SystemExit

COLOR = Colors()
PARAMS = Params()

class Goodbye(Page):
    def __init__(self, screen, func):

        super().__init__(screen, "ATÉ MAIS - ALFA", COLOR.WHITE, func)

    def init(self):

        self.components.append(Text(self.screen, 'ALFA', 90, COLOR.ORANGE))
        self.components.append(Text(self.screen, 'OBRIGADO POR JOGAR', 20, COLOR.BLUE_DARK))
        self.components.append(Image(self.screen, 'heart.png', (22, 22)))
        for component in self.components:
            component.init()
        self.components[0].set_margins_center()
        self.components[1].set_margins(((PARAMS.WIDTH - self.components[1].size[0] - 27) /2 , PARAMS.HEIGHT - 75 - 100))
        self.components[2].set_margins((self.components[1].size[0] + self.components[1].margins[0] + 5 , PARAMS.HEIGHT - 75 - 100))

class Home(Page):
    def __init__(self, screen, func):

        super().__init__(screen, "PÁGINA INICIAL - ALFA", COLOR.WHITE, func)

    def func_wait_for(self):
        self.components[1].text = 'PRESSIONE QUALQUER TECLA PARA CONTINUAR'
        self.components[1].render()
        self.components[1].set_margins(((PARAMS.WIDTH - self.components[1].size[0]) /2 , PARAMS.HEIGHT - 75 - 100))
        # Configurar eventos e animações
        #self.components[1].set_move(5 * PARAMS.FPS, x=10, y=10)
        self.components[1].set_blink()
        self.components[1].set_hover(COLOR.BLUE)
        self.components[1].set_click(self.func_visible)
        self.components[1].set_keydown(self.func_visible)

    def visible_menu(self):
        self.components[1].able = False
        self.components[2].able = True
        self.components[3].able = True

    def go_to(self, page):
        def func(event = None):
            nonlocal page
            self.func(page)
        return func

    def func_visible(self, event = None):
        self.visible_menu()

    def init(self):
        self.components.append(Text(self.screen, 'ALFA', 90, COLOR.ORANGE))
        self.components.append(Text(self.screen, 'SEJA BEM-VINDO(A)', 20, COLOR.BLUE_DARK))
        self.components.append(Button(self.screen, label="ALFABETIZAÇÃO", margin_box=(PARAMS.WIDTH / 2 - 250, PARAMS.HEIGHT - 210)))
        self.components.append(Button(self.screen, label="MATEMÁTICA", margin_box=(PARAMS.WIDTH / 2 + 30, PARAMS.HEIGHT - 210)))
        for component in self.components:
            component.init()
        self.components[0].set_margins_center()
        self.components[1].set_margins(((PARAMS.WIDTH - self.components[1].size[0]) /2 , PARAMS.HEIGHT - 75 - 100))
        # configurar eventos e animações
        self.components[0].set_wait(2*PARAMS.FPS, self.func_wait_for)
        self.components[2].set_click(self.go_to(Menu_complete(self.screen, self.func)))
        self.components[3].set_click(self.go_to(Menu_math(self.screen, self.func)))
        self.components[2].set_hover(COLOR.ORANGE, COLOR.WHITE)
        self.components[3].set_hover(COLOR.ORANGE, COLOR.WHITE)
        self.components[2].able = False
        self.components[3].able = False

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

    print('OBRIGADO POR JOGAR <3')
    window.exit()

if __name__ == '__main__':
    window = Window()
    window.init()
    run(window)
