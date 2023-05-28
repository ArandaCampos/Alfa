import pygame, os, csv
from game import Game
from home import Home

class Window():
    def __init__(self):

        # Parâmetros da tela
        self.screen = None
        self.size = (800, 648)
        self.caption = 'ALFA - MENU INICIAL'
        # Páginas
        self.pages = {
            'home': [False, None],
            'game': [False, None],
            'rank': [False, None],
            'conf': [False, None]
        }
        # Parâmetros do jogo
        self.play = True

    def init(self):
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.pages['game'] = [False, Game(self.screen, ('A', 'E', 'I', 'O', 'U'))]
        self.pages['game'][1].init()
        self.pages['home'] = [True, Home(self.screen)]
        self.pages['home'][1].init()

    def change_page(self, page_on):
        pages = [page for page in self.pages if self.pages.get(page)[0] == True]
        for page in pages:
            self.pages[page][0] = False
        self.pages[page_on][0] = True

    def refresh_screen(self):
        pages = [page for page in self.pages if self.pages.get(page)[0] == True]
        for page in pages:
            self.pages[page][1].refresh_screen()

    def get_event(self):
        pages = [page for page in self.pages if self.pages.get(page)[0] == True]

        for event in pygame.event.get():
            for page in pages:
                self.pages[page][1].get_event(event)
            if event.type == pygame.QUIT:
                self.play = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.pages['home'][1].button.button.rendered.collidepoint(pygame.mouse.get_pos()):
                    self.change_page('game')
                elif self.pages['game'][1].back.image.rendered.get_rect(center=self.pages['game'][1].back.image.get_center()).collidepoint(pygame.mouse.get_pos()):
                    self.change_page('home')



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
