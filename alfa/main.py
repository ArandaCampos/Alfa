import os
from completion import Game, Home, Menu_page

try:
    import pygame
except ImportError:
    print('Erro ao importar o Pygame. Verifique se o ambiente virtual está habilitado ou o pacote instalado')
    raise SystemExit

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
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.pages['home'][1].button.button.rendered.collidepoint(pygame.mouse.get_pos()):
                        self.change_page('menu')
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.change_page('menu')
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
                rect_btn_back = self.pages['game'][1].back.image.rendered.get_rect(center=self.pages['game'][1].back.image.get_center())
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
