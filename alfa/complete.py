# --------------------------------------------
#   Author: Renan Campos
#   Github: github.com/ArandaCampos
# --------------------------------------------

import os
from items import Text, Rank, Button, Image, Page
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
ORANGE_LIGHT, ORANGE, GREEN_LIGHT, GREEN = (242, 68, 5, 255), (250, 127, 8, 250), (154, 235, 163, 255), (131, 199, 115, 198)
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

class Game_complete(Page):
    pygame.init()
    def __init__(self, screen, func):
        super().__init__(screen, "COMPLETAR - ALFA", BG_COLOR, func)
        self.name = 'Game'
        # Componentes
        self.sound_win = pygame.mixer.Sound(os.path.join(AUD_PATH, 'win.wav'))
        self.sound_fail = pygame.mixer.Sound(os.path.join(AUD_PATH, 'failed.wav'))
        # Gabarito da rodada
        self.game = None
        self.df = None
        self.stage = None
        self.play = 1
        self.round = 0
        self.option = None

    def func_click_sound(self, event=None):
        to_read(self.components[6].get_word())

    def func_click_btn_send(self, event=None):
        if self.components[6].response():
            self.sound_win.play()
            self.components[1].text = str(int(self.components[1].text) + 1)
        else:
            self.sound_fail.play()
        self.next_round()

    def func_click_btn_cancel(self, event=None):
        self.sound_fail.play()
        self.next_round()

    def func_keydown(self, event):
        if event.key == pygame.K_UP:
            self.components[6].toggle_value(increment=True)
        elif event.key == pygame.K_DOWN:
            self.components[6].toggle_value(decrement=True)
        elif event.key == pygame.K_RIGHT:
            self.components[6].toggle_key(increment=True)
        elif event.key == pygame.K_LEFT:
            self.components[6].toggle_key(decrement=True)
        elif event.key == pygame.K_RETURN:
            if self.components[6].response():
                self.sound_win.play()
                self.components[1].text = str(int(self.components[1].text) + 1)
            else:
                self.sound_fail.play()
            self.next_round()
        else:
            self.components[6].toggle_value(letter=event.unicode)

    def init(self):
        """
         +----------------------------+
         | [0]   ->   ícone 'medalha' |
         | [1]   ->   pontuação       |
         | [2]   ->   botão 'não sei' |
         | [3]   ->   botão 'enviar'  |
         | [4]   ->   ícone 'voltar'  |
         | [5]   ->   ilustração      |
         | [6]   ->   palavra         |
         | [7]   ->   ícone 'áudio'   |
         +----------------------------+
        """
        self.round, self.play = 0, 1
        self.load_data()
        self.components.append(Image(self.screen, 'medal.png', (42, 42), (WIDTH - 42 - 25, 25)))
        self.components.append(Text(self.screen, '0', 'Noto Mono', 28, BLUE))
        self.components.append(Button(self.screen, label="NÃO SEI", margin_box=(120, HEIGHT - 110), src="cancel.png"))
        self.components.append(Button(self.screen,
                                      label="ENVIAR",
                                      color_label=BLUE,
                                      margin_box=(WIDTH - 120 - 220, HEIGHT - 110),
                                      color_box=GREEN_LIGHT, src="send.png"
                                      ))
        self.components.append(Image(self.screen, 'back.png', (30, 30), (25,25)))
        self.components.append(Image(self.screen, self.df["file"][self.round], (250, 250), ((WIDTH - 250) / 2, 50)))
        self.components.append(Toggle_letter(self.screen, self.df["word"][self.round], self.option, self.df["answer"][self.round]))
        self.components.append(Image(self.screen, 'sound.png', (31.4, 30)))
        for component in self.components:
            component.init()
        # Marigins relativas
        self.components[1].set_margins((WIDTH - 42 - 25 - self.components[1].size[0] - 10, 25 + (42 - self.components[1].size[1])/2))
        self.components[7].set_margins((
            self.components[6].margins[0][0] + self.components[6].size[0] + 60,
            self.components[6].margins[0][1] + (self.components[6].size[1] - self.components[-1].size[1]) / 2
        ))
        # Eventos
        self.components[2].set_click(self.func_click_btn_cancel)
        self.components[2].set_hover(ORANGE, WHITE)
        self.components[3].set_click(self.func_click_btn_send)
        self.components[3].set_hover(GREEN, BLUE)
        self.components[6].set_keydown(self.func_keydown)
        self.components[7].set_click(self.func_click_sound)

    def set_stage(self, stage: str):
        self.stage = stage

    def load_data(self):
        self.df = pd.DataFrame(pd.read_csv(f'data/{self.stage}.csv', sep=" "))
        self.option = self.df["answer"].unique()
        self.df = self.df.sample(frac=1).reset_index(drop=True)

    def next_round(self):
        if self.round == 9 or self.round == len(self.df) - 1:
            # Fim de jogo (10 rodadas ou até o fim das imagens)
            game = pd.DataFrame({"user": ["Renan"], "score": [self.components[1].text]})
            self.play = 0
            self.func(Menu_complete(self.screen, self.func))
            #self.rank = Rank(self.screen, self.components[0].text.text, self.stage)
            #self.rank.init()
        else:
            # Próxima rodada
            self.round += 1
            self.components[5].file = self.df["file"][self.round]
            self.components[5].render()
            self.components[6].new_game(self.df["word"][self.round], self.option, self.df["answer"][self.round])
            self.components[6].init()
            self.components[7].margins = [
                self.components[6].margins[0][0] + self.components[6].size[0] + 60,
                self.components[6].margins[0][1] + (self.components[6].size[1] - self.components[-1].size[1]) / 2
            ]


class Menu_complete(Page):
    def __init__(self, screen, func):
        super().__init__(screen, "MENU DE OPÇÕES - ALFA", BG_COLOR, func)

        self.name = 'Menu'
        # [7, 10, 22, 24] =~ [H, K, Y, W]
        self.options = [65 + i for i in range(25) if i not in [7, 10, 22, 24]]
        # Positionamento
        self.grid = (4, 6)
        self.gap = 70 * self.grid[1] + 30 * (self.grid[1] - 1)

    def func_click(self):
        for component in self.components:
            try:
                if component.box.rendered.collidepoint(pygame.mouse.get_pos()):
                    game = Game_complete(self.screen, self.func)
                    game.set_stage(component.label.text.lower())
                    self.func(game)
                    print(component.label.text)
            except:
                pass

    def func_keydown(self, event):
        print('clicou '+ event.unicode)
        if ord(event.unicode.upper()) in self.options:
            game = Game_complete(self.screen, self.func)
            game.set_stage(event.unicode.lower())
            self.func(game)

    def init(self):
        self.components.append(Text(self.screen, 'ALFA', 'Noto Mono', 90, BLUE))
        self.components[-1].init()
        self.components[-1].set_margins(((WIDTH - self.components[-1].size[0])/ 2, 50))

        for l in range(self.grid[0]):
            for c in range(self.grid[1]):
                if c + self.grid[1] * l in range(len(self.options)):
                    self.components.append(Button(
                                  self.screen,
                                  label=chr(self.options[c + self.grid[1] * l]), color_label=BLUE,
                                  size_box=(70,70), color_box=GREEN_LIGHT,
                                  margin_box=((WIDTH - self.gap)/2 + 100 * c, 200 + 100 * l)
                            ))
                    self.components[-1].init()
                    self.components[-1].set_hover(ORANGE_LIGHT, WHITE)

        self.components[-1].set_click(self.func_click)
        self.components[-1].set_keydown(self.func_keydown)
