import os
from completion import Game, Menu_page
from items import Button, Text, Page
from animations import Blink, Hover

try:
    import pygame
except ImportError:
    print('Erro ao importar o Pygame. Verifique se o ambiente virtual está habilitado ou o pacote instalado')
    raise SystemExit

BG_COLOR, BLUE = (222, 239, 231, 240), (1, 32, 48, 255)
ORANGE_LIGHT, GREEN_LIGHT = (242, 68, 5, 255), (154, 235, 163, 255)
HEIGHT, WIDTH = 648, 1000

class Home(Page):
    def __init__(self, screen):

        super().__init__(screen, "PÁGINA INICIAL - ALFA", (0, 0, 0))

    def init(self):
        # Título principal
        self.components.append(Text(self.screen, 'ALFA', 'Noto Mono', 90, BLUE))
        self.components[-1].init()
        self.components[-1].set_margins(((WIDTH - self.components[-1].size[0])/ 2, (HEIGHT - self.components[-1].size[1])/ 2))
        self.components.append(Text(self.screen, 'PRESSIONE ENTER', 'Noto Mono', 24, ORANGE_LIGHT))
        # Texto instrucional
        self.components[-1].init()
        self.components[-1].set_blink()
        self.components[-1].set_hover(BLUE)
        self.components[-1].set_margins(((WIDTH - self.components[-1].size[0]) /2 , HEIGHT - 75 - 100))
        #self.buttons.append(Button(
        #                          self.screen,
        #                          label="COMPLETAR",
        #                          margin_box=((WIDTH / 2 - 220) /2 , HEIGHT - 75 - 100),
        #                          src='play.png'
        #                        )
        #                    )
        #self.buttons[-1].set_hover(GREEN_LIGHT, BLUE)
        #self.buttons.append(Button(
        #                          self.screen,
        #                          label="FORCA",
        #                          margin_box=(WIDTH /2 + (WIDTH / 2 - 220) /2 , HEIGHT - 75 - 100),
        #                          src='play.png'
        #                        )
        #                    )

        for component in self.components:
            component.init()

        pygame.display.set_caption(self.caption)

class Window():
    def __init__(self):

        # Parâmetros da tela
        self.screen = None
        self.size = (1000, 648)
        self.caption = 'ALFA - PÁGINA INICIAL'
        # Páginas
        self.pages = {
            'home': [False, None],
            'menu': [False, None],
            'game': [False, None],
            'rank': [False, None],
            'conf': [False, None]
        }
        # Parâmetros do jogo
        self.play = True

    def init(self):
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.pages['game'] = [False, Game(self.screen)]
        self.pages['menu'] = [False, Menu_page(self.screen)]
        self.pages['home'] = [True, Home(self.screen)]
        self.pages['home'][1].init()

    def change_page(self, page_on):
        pages = [page for page in self.pages if self.pages.get(page)[0] == True]
        for page in pages:
            self.pages[page][0] = False
        self.pages[page_on][0] = True
        self.pages[page_on][1].init()

    def refresh_screen(self):
        pages = [page for page in self.pages if self.pages.get(page)[0] == True]
        for page in pages:
            self.pages[page][1].refresh_screen()

    def get_event(self):
        pages = [page for page in self.pages if self.pages.get(page)[0] == True]

        for event in pygame.event.get():
            for page in pages:
                self.pages[page][1].get_event(event)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.play = False
            if self.pages['home'][0]:
                self.pages['home'][1].get_event(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.pages['home'][1].buttons[0].box.rendered.collidepoint(pygame.mouse.get_pos()):
                        self.change_page('menu')
                        self.pages['game'][1].game = 0
                    elif self.pages['home'][1].buttons[1].box.rendered.collidepoint(pygame.mouse.get_pos()):
                        self.change_page('menu')
                        self.pages['game'][1].game = 1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.change_page('menu')
                        self.pages['game'][1].game = 0
            elif self.pages['menu'][0]:
                letters = [i + 65 for i in range(25) if i not in [7, 10, 22, 24]]
                if event.type == pygame.KEYDOWN:
                    if ord(event.unicode.upper()) in letters:
                        self.pages['game'][1].set_stage(event.unicode.lower())
                        self.pages['game'][1].init()
                        self.change_page('game')
                if event.type == pygame.MOUSEBUTTONUP:
                    for i, button in zip(letters, self.pages['menu'][1].menu.button):
                        if button.rendered.collidepoint(pygame.mouse.get_pos()):
                            self.pages['game'][1].set_stage(chr(i).lower())
                            self.pages['game'][1].init()
                            self.change_page('game')
            elif self.pages['game'][0]:
                rect_btn_back = self.pages['game'][1].back.rendered.get_rect(center=self.pages['game'][1].back.get_center())
                if event.type == pygame.MOUSEBUTTONUP:
                    if rect_btn_back.collidepoint(pygame.mouse.get_pos()):
                        self.change_page('menu')

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
