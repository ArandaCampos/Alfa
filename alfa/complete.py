# --------------------------------------------
#   Author: Renan Campos
#   Github: github.com/ArandaCampos
# --------------------------------------------

import os
from items import Text, Button, Image, Page, Component
from constants import Colors, Params

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

# Constantes
COLOR = Colors()
PARAMS = Params()

def to_read(word: str):
    # Lê o texto escrito pelo usuário
    tts = gTTS(word, lang='pt', tld="com.br")
    tts.save("audio.mp3")
    sound = pygame.mixer.Sound('audio.mp3')
    sound.play()

class Toggle_letter(Component):
    def __init__ (self, screen, word: str, options: (str), answer: (str), size: int =  [0,0], margins: (int, int) = [0,0]):
        super().__init__(screen, size, margins)

        # Parâmetros do Jogo
        self.letters = word.upper().split("*")
        self.options = list(options)
        self.key     = self.letters.index("")
        self.answer = answer
        self.components = []
        # Componentes
        self.sound_win = PARAMS.SOUND_WIN
        self.sound_fail = PARAMS.SOUND_FAIL


    def init(self):
        self.letters[self.key] = self.options[0]
        self.render()

    def next_round(self, word, answer):
        self.letters = word.upper().split("*")
        self.key     = self.letters.index("")
        self.answer = answer
        self.size = [0,0]
        self.margins = [0,0]
        self.init()

    def toggle_value(self, value: int = None, increment: bool = False, decrement: bool = False, letter: str = False):
        if letter:
            for i, option in enumerate(self.options):
                if letter.upper() in option:
                    self.letters[self.key] = self.options[i]
                    break
        else:
            index = self.options.index(self.letters[self.key])
            if increment:
                self.letters[self.key] = self.options[index + 1] if index < len(self.options) - 1 else self.options[0]
            elif decrement:
                self.letters[self.key] = self.options[index - 1] if index > 1 else self.options[-1]
        self.components[self.key].text = self.letters[self.key]

    def render(self):
        self.components = []
        for i, letter in enumerate(self.letters):
            self.components.append(Text(self.screen, letter, 80, COLOR.ORANGE if i == self.key else COLOR.BLUE_DARK))
            self.components[-1].init()
            self.size[0] += self.components[-1].size[0]
            self.size[1] = self.components[-1].size[1] if self.components[-1].size[1] > self.size[1] else self.size[1]
        self.margins = ((PARAMS.WIDTH - self.size[0])/2, 390)
        self.components[0].set_margins(self.margins)
        for i in range(1, len(self.letters)):
            self.components[i].set_margins((self.components[i-1].get_right(), 390 + (self.components[0].size[1] - self.components[i].size[1])))

    def get_right(self):
        return self.components[-1].get_right()

    def response(self, cancel: bool = False):
        response = self.letters[self.key] == self.answer
        self.components[self.key].text = self.answer
        self.letters[self.key] = self.answer
        for component in self.components:
            component.color = COLOR.GREEN_DARK
        return response

    def get_word(self):
        return "".join(self.letters).lower()

    def draw(self):
        for components in self.components:
            components.draw()

class Game_complete(Page):
    def __init__(self, screen, func):
        super().__init__(screen, "COMPLETAR - ALFA", COLOR.WHITE, func)
        # Componentes
        self.sound_win = PARAMS.SOUND_WIN
        self.sound_fail = PARAMS.SOUND_FAIL
        # Gabarito da rodada
        self.game = None
        self.df = None
        self.stage = None
        self.play = 1
        self.round = 0
        self.option = None

    def wait(self):
        self.components[2].able = False
        self.components[3].able = False
        self.components[8].able = True
        self.components[6].set_keydown(self.func_to_next)

    def get_result(self, cancel: bool = False):
        result = self.components[6].response()
        if cancel or not result:
            self.sound_fail.play()
        else:
            self.sound_win.play()
            self.components[1].text = str(int(self.components[1].text) + 1)
        self.wait()

    def func_to_next(self, event = None):
        self.components[6].set_keydown(self.func_keydown)
        self.components[2].able = True
        self.components[3].able = True
        self.components[8].able = False
        self.next_round()

    def func_back(self, event=None):
        self.func(Menu_complete(self.screen, self.func))

    def func_click_sound(self, event=None):
        to_read(self.components[6].get_word())

    def func_click_btn_send(self, event=None):
        self.get_result()

    def func_click_btn_cancel(self, event=None):
        self.get_result(cancel=False)

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
            self.get_result()
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
        self.components.append(Image(self.screen, 'medal.png', (42, 42), (PARAMS.WIDTH - 42 - 25, 25)))
        self.components.append(Text(self.screen, '0', 28, COLOR.BLUE_DARK))
        self.components.append(Button(self.screen, label="NÃO SEI", margin_box=(120, PARAMS.HEIGHT - 110), src="cancel.png"))
        self.components.append(Button(self.screen,
                                      label="ENVIAR",
                                      color_label=COLOR.BLUE_DARK,
                                      margin_box=(PARAMS.WIDTH - 120 - 220, PARAMS.HEIGHT - 110),
                                      color_box=COLOR.GREEN, src="send.png"
                                      ))
        self.components.append(Image(self.screen, 'back.png', (25, 25), (25,25)))
        self.components.append(Image(self.screen, self.df["file"][self.round], (250, 250), ((PARAMS.WIDTH - 250) / 2, 50)))
        self.components.append(Toggle_letter(self.screen, self.df["word"][self.round], self.option, self.df["answer"][self.round]))
        self.components.append(Image(self.screen, 'sound.png', (31.4, 30)))
        self.components.append(Text(self.screen, 'PRESSIONE ENTER', 28, COLOR.BLUE_DARK))
        for component in self.components:
            component.init()
        # Marigins relativas
        self.components[1].set_margins((PARAMS.WIDTH - 42 - 25 - self.components[1].size[0] - 10, 25 + (42 - self.components[1].size[1])/2))
        self.components[7].set_margins((
            self.components[6].get_right() + 60,
            self.components[6].margins[1] + (self.components[6].size[1] - self.components[-1].size[1]) / 2
        ))
        self.components[8].set_margins(((PARAMS.WIDTH - self.components[8].size[0])/2, PARAMS.HEIGHT - 110))
        # Eventos
        self.components[2].set_click(self.func_click_btn_cancel)
        self.components[2].set_hover(COLOR.ORANGE_DARK, COLOR.WHITE)
        self.components[3].set_click(self.func_click_btn_send)
        self.components[3].set_hover(COLOR.GREEN_DARK, COLOR.BLUE_DARK)
        self.components[4].set_click(self.func_back)
        self.components[6].set_keydown(self.func_keydown)
        self.components[7].set_click(self.func_click_sound)
        self.components[8].set_blink()
        self.components[8].able = False

    def set_stage(self, stage: str):
        self.stage = stage

    def load_data(self):
        self.df = pd.DataFrame(pd.read_csv(f'data/{self.stage}.csv', sep=" "))
        self.option = self.df["answer"].unique()
        self.df = self.df.sample(frac=1).reset_index(drop=True)

    def next_round(self):
        if self.round == 9 or self.round == len(self.df) - 1:
            # Fim de jogo (10 rodadas ou até o fim das imagens)
            try:
                rank = pd.DataFrame(pd.read_csv(f"data/rank_{self.stage}.csv", sep=" "))
            except:
                rank = pd.DataFrame({"user": [], "score": []})
            last_game = pd.DataFrame({
                "user": ["Mônica"],
                "score": [int(self.components[1].text)]
            })
            rank = pd.concat([rank, last_game], ignore_index=True)
            rank = rank.sort_values(by='score', ascending=False)
            #position = rank.index[rank['score'] == self.score].tolist()
            rank.to_csv(f"data/rank_{self.stage}.csv", sep=" ", index=False)

            self.play = 0
            self.func(Rank_complete(self.screen, self.func, self.components[1].text, self.stage))
        else:
            # Próxima rodada
            self.round += 1
            self.components[5].file = self.df["file"][self.round]
            self.components[5].init()
            self.components[6].next_round(self.df["word"][self.round], self.df["answer"][self.round])
            self.components[7].margins = [
                self.components[6].get_right() + 60,
                self.components[6].margins[1] + (self.components[6].size[1] - self.components[-1].size[1]) / 2
            ]

class Menu_complete(Page):
    def __init__(self, screen, func):
        super().__init__(screen, "MENU DE OPÇÕES - ALFA", COLOR.WHITE, func)

        # [7, 10, 22, 24] =~ [H, K, Y, W]
        self.options = [65 + i for i in range(25) if i not in [7, 10, 22, 24]]
        # Positionamento
        self.grid = (4, 6)
        self.gap = 70 * self.grid[1] + 30 * (self.grid[1] - 1)

    def func_generic(self, letter):
        def func_click():
            nonlocal letter
            game = Game_complete(self.screen, self.func)
            game.set_stage(letter.lower())
            self.func(game)
        return func_click

    def func_keydown(self, event):
        if ord(event.unicode.upper()) in self.options:
            game = Game_complete(self.screen, self.func)
            game.set_stage(event.unicode.lower())
            self.func(game)

    def init(self):
        self.components.append(Text(self.screen, 'ALFA', 90, COLOR.BLUE_DARK))
        self.components[-1].init()
        self.components[-1].set_margins(((PARAMS.WIDTH - self.components[-1].size[0])/ 2, 50))

        for l in range(self.grid[0]):
            for c in range(self.grid[1]):
                if c + self.grid[1] * l in range(len(self.options)):
                    char = chr(self.options[c + self.grid[1] * l])
                    self.components.append(Button(
                                  self.screen,
                                  label=char, color_label=COLOR.BLUE_DARK,
                                  size_box=(70,70), color_box=COLOR.GREEN,
                                  margin_box=((PARAMS.WIDTH - self.gap)/2 + 100 * c, 200 + 100 * l)
                            ))
                    self.components[-1].init()
                    self.components[-1].set_hover(COLOR.ORANGE, COLOR.WHITE)
                    self.components[-1].set_click(self.func_generic(char))

        self.components[-1].set_keydown(self.func_keydown)

class Rank_complete(Page):
    def __init__(self,screen, func, score: int, stage: str):
        super().__init__(screen, "FIM DE JOGO - ALFA", COLOR.WHITE, func)
        self.score = score
        self.stage = stage

    def func_to_menu(self, event = None):
        self.func(Menu_complete(self.screen, self.func))

    def init(self):
        self.components.append(Image(self.screen, 'medal.png', (250, 250)))
        self.components.append(Text(self.screen, f'JOGO - {self.stage.upper()}', 24, COLOR.BLUE_DARK))
        self.components.append(Text(self.screen, f'{self.score} PONTOS', 50, COLOR.ORANGE_DARK))
        self.components.append(Text(self.screen, 'PRESSIONE QUALQUER TECLA PARA CONTINUAR', 24, COLOR.BLUE_DARK))
        for component in self.components:
            component.init()
        self.components[0].set_margins((
            (PARAMS.WIDTH - self.components[0].size[0])/2,
            120
        ))
        self.components[1].set_margins(((PARAMS.WIDTH - self.components[1].size[0]) / 2, self.components[0].get_bottom() + 30))
        self.components[2].set_margins(((PARAMS.WIDTH - self.components[2].size[0]) / 2, self.components[1].get_bottom() + 10))
        self.components[3].set_margins(((PARAMS.WIDTH - self.components[3].size[0]) / 2, self.components[2].get_bottom() + 30))
        self.components[3].set_blink()
        self.components[3].set_keydown(self.func_to_menu)
