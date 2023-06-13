# --------------------------------------------
#   Author: Renan Campos
#   Github: github.com/ArandaCampos
# --------------------------------------------

import os
from items import Text, Score, Rank, Menu, Button, Image
#from animation import blink
from games import Hangman, Toggle_letter

try:
    import pygame
except ImportError:
    print("Erro ao importar a biblioteca Pygame. Tente $ pip install pygame")
    raise SystemExit

try:
    import pandas as pd
except ImportError:
    print("Erro ao importar a biblioteca Pandas. Tente $ pip install pandas")
    raise SystemExit

try:
    import numpy as np
except ImportError:
    print("Erro ao importar a biblioteca Numpy. Tente $ pip install numpy")
    raise SystemExit

try:
    from gtts import gTTS
except ImportError:
    print("Erro ao importar a biblioteca gTTS. Tente $ pip install gTTs")
    raise SystemExit

try:
    from playsound import playsound
except ImportError:
    print("Erro ao importar a biblioteca Playsound. Tente $ pip install playsound")
    raise SystemExit

# Paleta de cor
BG_COLOR, BLUE, WHITE = (222, 239, 231, 240), (1, 32, 48, 255), (240, 240, 242, 242)
ORANGE_LIGHT, ORANGE, GREEN_LIGHT = (242, 68, 5, 255), (250, 127, 8, 250), (154, 235, 163, 255)

# Altura e largura da tela
HEIGHT, WIDTH = 648, 1000

# Carregar diretório "Audio"
ABS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
DATA_PATH = os.path.join(ABS_PATH, 'data')
AUD_PATH = os.path.join(DATA_PATH, 'Audio')

def to_read(word: str):
    # Lê o texto escrito pelo usuário
    tts = gTTS(word, lang='pt', tld="com.br")
    tts.save("audio.mp3")
    playsound("audio.mp3")

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
        self.rank = None
        self.sound_win = pygame.mixer.Sound(os.path.join(AUD_PATH, 'win.wav'))
        self.sound_fail = pygame.mixer.Sound(os.path.join(AUD_PATH, 'failed.wav'))
        # Parâmetros do jogo
        self.screen = screen
        # Gabarito da rodada
        self.game = None
        self.df = None
        self.stage = None
        self.play = 1
        self.round = 0
        self.option = None

    def init(self):
        self.round, self.play = 0, 1
        self.load_data()
        self.load_round()
        self.score_board = Score(self.screen)
        self.score_board.init()
        self.button_cancel = Button(self.screen, label="NÃO SEI", margin_box=(120, HEIGHT - 110), src='cancel.png')
        self.button_cancel.init()
        self.button_send = Button(
                                  self.screen,
                                  label="ENVIAR",
                                  color_label=BLUE,
                                  margin_box=(WIDTH - 120 - 220, HEIGHT - 110),
                                  color_box = GREEN_LIGHT,
                                  src='send.png'
                                )
        self.button_send.init()
        self.back = Image(self.screen, 'back.png', (30, 30), (25,25))
        self.back.init()
        pygame.display.set_caption(self.title)

    def set_stage(self, stage: str):
        self.stage = stage

    def load_data(self):
        # Toggle letter
        if self.game == 0:
            file = f'data/{self.stage}.csv'
        # Hangman
        elif self.game == 1:
            file = 'data/hangman.csv'
        self.df = pd.DataFrame(pd.read_csv(file, sep=" "))
        self.option = self.df["answer"].unique() if self.game == 0 else None
        self.df = self.df.sample(frac=1).reset_index(drop=True)

    def next_round(self):
        # Fim de jogo (10 rodas ou até o fim das imagens)
        if self.round == 9 or self.round == len(self.df) - 1:
            game = pd.DataFrame({"user": ["Renan"], "score": [self.score_board.text.text]})
            self.play = 0
            self.rank = Rank(self.screen, self.score_board.text.text, self.stage)
            self.rank.init()
        # Próxima rodada
        self.round = self.round + 1 if self.round < len(self.df) - 1 else 0
        self.load_round()

    def load_round(self):
        if self.game == 0:
            self.word = Toggle_letter(self.screen, self.df["word"][self.round], self.option, self.df["answer"][self.round])
        elif self.game == 1:
            self.word = Hangman(self.screen, self.df['word'][self.round])
        self.word.init()
        self.figure = Image(self.screen, self.df["file"][self.round], (250, 250), ((WIDTH - 250) / 2, 50))
        self.figure.init()
        self.sound = Image(self.screen, 'sound.png', (31.4, 30))
        self.sound.margins = [self.word.margins[0][0] + self.word.size[0] + 60, self.word.margins[0][1] + (self.word.size[1] - self.sound.size[1]) / 2]
        self.sound.init()

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
            if self.sound.get_rect_center().collidepoint(pygame.mouse.get_pos()):
                to_read(self.word.get_word())
            elif self.button_send.box.rendered.collidepoint(pygame.mouse.get_pos()):
                if self.word.response():
                    self.sound_win.play()
                    self.score_board.update(increment=True)
                else:
                    self.sound_fail.play()
                self.next_round()
            elif self.button_cancel.box.rendered.collidepoint(pygame.mouse.get_pos()):
                self.sound_fail.play()
                self.next_round()

    def exit(self):
        pygame.quit()

class Menu_page():
    def __init__(self, screen):

        self.screen = screen
        self.caption = 'ALFA - MENU'
        self.title = None
        self.menu = None

    def init(self):
        self.menu = Menu(self.screen)
        self.menu.init()
        self.title = Text(self.screen, 'ALFA', 'Noto Mono', 90, BLUE)
        self.title.init()
        self.title.set_margins(((WIDTH - self.title.size[0])/ 2, 50))

    def refresh_screen(self):
        self.screen.fill(BG_COLOR)
        self.title.draw() if self.title else None
        self.menu.draw() if self.menu else None
        pygame.display.set_caption(self.caption)
        pygame.display.flip()

    def get_event(self, event):
        pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            letters = [i + 65 for i in range(25) if i not in [7, 10, 22, 24]]
            if event.unicode.upper() in letters:
                self.word.toggle_value(letter=event.unicode)

        for button, label in zip(self.menu.button, self.menu.label):
            if button.rendered.collidepoint(pos):
                    button.color = ORANGE_LIGHT
                    label.color = WHITE
            else:
                button.color = GREEN_LIGHT
                label.color = BLUE

    def draw(self):
        self.menu.draw()
        self.title.draw()
