# ------------------------------------
#   Author: Renan Campos
#   Github: github.com/ArandaCampos
# ------------------------------------

import pygame, os
import pandas as pd
from read_word import read_word
from toggle_letter import Toggle_letter
from components import Button_cancel, Button_send, Score, Sound, Figure, Back_home, Rank

# Paleta de cores
BG_COLOR = (222, 239, 231, .94)
# Altura e largura da tela
HEIGHT, WIDTH = 648, 1000
# Carregar diretório "Images"
ABS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
AUD_PATH = os.path.join(ABS_PATH, 'Audio')

class Game():
    pygame.init()
    def __init__(self, screen):
        # Parâmetros de aparência
        self.bg_color = BG_COLOR
        self.title = 'ALFA - JOGO'
        # Componentes
        self.back = None
        self.sound = None
        self.score_board = None
        self.button_cancel = None
        self.button_send = None
        self.word = None
        self.figure = None
        self.sound_win = pygame.mixer.Sound(os.path.join(AUD_PATH, 'win.wav'))
        self.sound_fail = pygame.mixer.Sound(os.path.join(AUD_PATH, 'failed.wav'))
        self.rank = None
        # Parâmetros do jogo
        self.screen = screen
        # Gabarito da rodada
        self.df = None
        self.stage = None
        self.play = 1
        self.round = 0
        self.option = None

    def init(self):
        self.round = 0
        self.load_data()
        self.load_word()
        self.load_sound()
        self.load_score()
        self.load_btn_cancel()
        self.load_btn_send()
        self.play = 1
        self.back = Back_home(self.screen)
        self.back.init()
        pygame.display.set_caption(self.title)

    def set_stage(self, stage: str):
        self.stage = stage

    def load_data(self):
        self.df = pd.DataFrame(pd.read_csv(f'Data/{self.stage}.csv', sep=" "))
        self.option = self.df["answer"].unique()
        self.df = self.df.sample(frac=1).reset_index(drop=True)

    def next_round(self):
        # Fim de jogo (10 rodas ou até o fim das imagens)
        if self.round == 9 or self.round == len(self.df) - 1:
            game = pd.DataFrame({
                "user": ["Renan"],
                "score": [self.score_board.text.text]
            })
            self.play = 0
            self.rank = Rank(self.screen, self.score_board.text.text, self.stage)
            self.rank.init()
        # Próxima rodada
        self.round = self.round + 1 if self.round < len(self.df) - 1 else 0
        self.load_word()
        self.load_sound()

    def load_word(self):
        self.word = Toggle_letter(self.screen, self.df["word"][self.round], self.option, self.df["answer"][self.round])
        self.word.init()
        self.figure = Figure(self.screen, self.df["file"][self.round])
        self.figure.init()

    def load_sound(self):
        self.sound = Sound(self.screen, [self.word.margins[0][0] + self.word.size[0], 390 + self.word.size[1] / 2])
        self.sound.init()

    def load_score(self):
        self.score_board = Score(self.screen)
        self.score_board.init()

    def load_btn_cancel(self):
        self.button_cancel = Button_cancel(self.screen)
        self.button_cancel.init()

    def load_btn_send(self):
        self.button_send = Button_send(self.screen)
        self.button_send.init()

    def refresh_screen(self):
        self.screen.fill(self.bg_color)
        if self.play:
            self.button_cancel.draw() if self.button_cancel else None
            self.button_send.draw() if self.button_send else None
            self.word.draw() if self.word else None
            self.score_board.draw() if self.score_board else None
            self.figure.draw() if self.figure else None
            self.sound.draw() if self.sound else None
        else:
            self.rank.draw()
        self.back.draw() if self.back else None
        pygame.display.set_caption(self.title)
        pygame.display.flip()

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.word.toggle_value(increment=True)
            elif event.key == pygame.K_DOWN:
                self.word.toggle_value(decrement=True)
            elif event.key == pygame.K_RIGHT:
                self.word.toggle_key(increment=True)
            elif event.key == pygame.K_LEFT:
                self.word.toggle_key(decrement=True)

            elif event.key == pygame.K_RETURN:
                if self.word.response():
                    self.sound_win.play()
                    self.score_board.update(increment=True)
                else:
                    self.sound_fail.play()
                self.next_round()
            else:
                self.word.toggle_value(letter=event.unicode)
            # Comandos de mouse
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.sound.image.rendered.get_rect(center=self.sound.image.get_center()).collidepoint(pygame.mouse.get_pos()):
                read_word(self.word.get_word())
            elif self.button_send.button.rendered.collidepoint(pygame.mouse.get_pos()):
                if self.word.response():
                    self.sound_win.play()
                    self.score_board.update(increment=True)
                else:
                    self.sound_fail.play()
                self.next_round()
            elif self.button_cancel.button.rendered.collidepoint(pygame.mouse.get_pos()):
                self.sound_fail.play()
                self.next_round()

    def exit(self):
        pygame.quit()

def run(window):
    clock = pygame.time.Clock()

    while window.play:
        clock.tick(40)

        window.refresh_screen()
        window.get_event()

    window.exit()

if __name__ == '__main__':
    stage = 0
    stages = (1, 2, 3, 4, 5)
    option = (('A', 'E', 'I', 'O', 'U'),
              ('BA', 'BE', 'BI', 'BO', 'BU'))

    file_names = ['Data/data_a.csv', 'Data/data_b.csv']
    print('************ MENU - ALFA ***********\n\n 1) Vogais \n 2) Letra B\n')
    while stage not in stages:
        stage = int(input(" Opção: "))
    file_data = file_names[stage - 1]

    loading_data(file_data)
    window = Game(option = option[stage - 1])
    window.init()
    run(window)
