# --------------------------------------------
#   Author: Renan Campos
#   Github: github.com/ArandaCampos
# --------------------------------------------

import os
from items import Text, Score, Sound, Rank, Menu, Button, Image

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
BG_COLOR, BLUE, WHITE = (222, 239, 231, .94), (1, 32, 48, 1.), (240, 240, 242, .95)
ORANGE_LIGHT, ORANGE, GREEN_LIGHT = (242, 68, 5, 1.), (250, 127, 8, .98), (154, 235, 163, 1.)

# Altura e largura da tela
HEIGHT, WIDTH = 648, 1000

# Carregar diretório "Audio"
ABS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
AUD_PATH = os.path.join(ABS_PATH, 'Audio')

def to_read(word: str):
    """
        Carrega o texto digitado no campo '' e
        o salva em portugês-Brasil no 'audio.mp3'
    """

    tts = gTTS(word, lang='pt', tld="com.br")
    tts.save("audio.mp3")
    playsound("audio.mp3")

class Toggle_letter():
    MARGIN_TOP = 390

    """
    --------------------------------------------

               +--------+--------+---> fields
               |        |        |
           +--------+--------+--------+
           | option | option | option |
           +--------+--------+--------+
               |
               +--> key

    --------------------------------------------
    """

    def __init__ (self, screen, word: str, options: (str), answers: (str)):

        self.screen = screen
        # Parâmetros do Jogo
        self.letters = word.upper().split("*")
        self.options = list(options)
        self.values  = [0 for i, item in enumerate(self.letters) if item == '']
        self.fields  = [i for i, item in enumerate(self.letters) if item == '']
        self.key     = 0
        self.answers = answers
        # Aparência das letras
        self.color_text = BLUE
        self.color_answer = ORANGE
        self.size_font = 80
        self.font = pygame.font.SysFont('Noto Mono', self.size_font)
        # Posicionamento
        self.size = []
        self.size_letters = []
        self.rendered_letters = []
        self.margins = []

    def init(self):
        self.render_letters_and_set_position()
        self.set_margins()

    def update_fields(self):
        for i, field in enumerate(self.fields):
            self.letters[field] = self.options[self.values[i]]

    def toggle_value(self, value: int = None, increment: bool = False, decrement: bool = False, letter: str = False):
        if value:
            self.values[self.key] = value if value in range(len(self.options) - 1) else self.values[self.key]
        elif increment:
            self.values[self.key] = self.values[self.key] + 1 if self.values[self.key] < len(self.options) - 1 else 0
        elif decrement:
            self.values[self.key] = self.values[self.key] - 1 if self.values[self.key] > 0 else len(self.options) - 1
        elif letter:
            if len(self.options[0]) == 1:
                self.values[self.key] = self.options.index(letter.upper()) if letter.upper() in self.options else self.values[self.key]
            else:
                for key, option in enumerate(self.options):
                    self.values[self.key] = key if letter.upper() == option[1] else self.values[self.key]

    def toggle_key(self, value: int = None, increment: bool = False, decrement: bool = False):
        if value:
            self.key = value if value in range(len(self.values)) else self.key
        elif increment:
            self.key = self.key + 1 if self.key < len(self.values) - 1 else 0
        elif decrement:
            self.key = self.key - 1 if self.key > 0 else len(self.values) - 1

    def render_letters_and_set_position(self):
        self.rendered_letters = []
        self.update_fields()
        for i, item in enumerate(self.letters):
            render = self.font.render('{}'.format(item), True, self.color_answer if i in self.fields else self.color_text)
            _, _, w, h = render.get_rect()
            self.size_letters.append((w, h))
            self.rendered_letters.append(render)
        self.get_size()

    def get_size(self):
        sum_w = max_h = 0
        for w, h in self.size_letters:
            sum_w += w
            max_h = h if h > max_h else max_h
        self.size = (sum_w, max_h)

    def response(self):
        for index, value in enumerate(self.values):
            if self.options[value] != self.answers:
                return 0
        return 1

    def get_word(self):
        return "".join(self.letters).lower()

    def set_margins(self):
        self.margins = []
        self.margins.append([(WIDTH - self.size[0]) / 2, 390])
        for i in range(1, len(self.size_letters)):
            self.margins.append(
                [
                self.margins[i -1][0] + self.size_letters[i - 1][0],
                self.margins[0][1] + (self.size_letters[0][1] - self.size_letters[i][1])
                ]
            )

    def draw(self):
        self.render_letters_and_set_position()
        if self.screen:
            for i in range(len(self.margins)):
                self.screen.blit(self.rendered_letters[i],(self.margins[i][0], self.margins[i][1]))

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
        self.back = Image(self.screen, 'back.png', (30, 30), (25,25))
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
        #self.word = Hangman(self.screen, self.df["word"][self.round])
        self.word.init()
        self.figure = Image(self.screen, self.df["file"][self.round], (250, 250), ((WIDTH - 250) / 2, 50))
        self.figure.init()

    def load_sound(self):
        self.sound = Sound(self.screen, [self.word.margins[0][0] + self.word.size[0], 390 + self.word.size[1] / 2])
        self.sound.init()

    def load_score(self):
        self.score_board = Score(self.screen)
        self.score_board.init()

    def load_btn_cancel(self):
        self.button_cancel = Button(self.screen, label="CANCELAR", margin_box=(120, HEIGHT - 110), src='cancel.png')
        self.button_cancel.init()

    def load_btn_send(self):
        self.button_send = Button(
                                  self.screen,
                                  label="ENVIAR",
                                  color_label=BLUE,
                                  margin_box=(WIDTH - 120 - 220, HEIGHT - 110),
                                  color_box = GREEN_LIGHT,
                                  src='send.png'
                                )
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
            sound_rect = self.sound.image.rendered.get_rect(center=self.sound.image.get_center())
            send_rect = self.button_send.box.rendered
            cancel_rect = self.button_cancel.box.rendered
            if sound_rect.collidepoint(pygame.mouse.get_pos()):
                to_read(self.word.get_word())
            elif send_rect.collidepoint(pygame.mouse.get_pos()):
                if self.word.response():
                    self.sound_win.play()
                    self.score_board.update(increment=True)
                else:
                    self.sound_fail.play()
                self.next_round()
            elif cancel_rect.collidepoint(pygame.mouse.get_pos()):
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
            if pos[0] > button.margins[0] and pos[0] < button.margins[0] + button.size[0] and pos[1] > button.margins[1] and pos[1] < button.margins[1] + button.size[1]:
                    button.color = ORANGE_LIGHT
                    label.color = WHITE
            else:
                button.color = GREEN_LIGHT
                label.color = BLUE

    def draw(self):
        self.menu.draw()
        self.title.draw()
