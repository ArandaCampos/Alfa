# --------------------------------------------
#   Author: Renan Campos
#   Github: github.com/ArandaCampos
# --------------------------------------------

import os
from items import Text, Component
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
    from gtts import gTTS
except ImportError:
    print("Erro ao importar a biblioteca gTTS. Tente $ pip install gTTs")
    raise SystemExit

# Constantes
COLOR = Colors()
PARAMS = Params()

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

    def toggle_value(self, value: str = False, increment: bool = False, decrement: bool = False, backspace: bool = False):
        if value:
            for i, option in enumerate(self.options):
                if value.upper() in option:
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

class Basic_math(Component):
    def __init__ (self, screen, op: str, result: str, size: int =  [0,0], margins: (int, int) = [0,0]):
        super().__init__(screen, size, margins)

        # Parâmetros do Jogo
        self.operation = op
        self.answer = 0
        self.result = result
        self.components = []
        # Componentes
        self.sound_win = PARAMS.SOUND_WIN
        self.sound_fail = PARAMS.SOUND_FAIL

    def init(self):
        self.components = []
        self.components.append(Text(self.screen, self.operation, 80, COLOR.BLUE_DARK))
        self.components.append(Text(self.screen, self.answer, 80, COLOR.ORANGE))
        for component in self.components:
            component.init()
        # Margens
        self.margins = ((PARAMS.WIDTH - self.components[0].size[0] - self.components[1].size[0])/2, (PARAMS.HEIGHT - 80)/2)
        self.size = self.components[-1].size
        self.components[0].set_margins(self.margins)
        self.components[1].set_margins((self.components[0].get_right(), self.margins[1]))

    def next_round(self, op, result):
        self.operation = op
        self.answer = 0
        self.result = result
        self.size = [0,0]
        self.margins = [0,0]
        self.init()

    def is_number(self, value):
        try:
             float(value)
        except ValueError:
             return False
        return True

    def toggle_value(self, value: int = None, backspace: bool = False, increment: bool = False, decrement: bool = False):
        if value:
            if self.is_number(value):
                self.answer = str(self.answer) + str(value)
        elif backspace:
            self.answer = self.answer[0:-1] if len(self.answer) > 1 else "0"
        else:
            self.answer = str(int(self.answer) + 1) if increment else str(int(self.answer) - 1)
        self.components[1].text = self.answer

    def get_right(self):
        return self.components[-1].get_right()

    def response(self, cancel: bool = False):
        response = int(self.result) == int(self.answer)
        self.components[1].text = self.result
        for component in self.components:
            component.color = COLOR.GREEN_DARK
        return response

    def draw(self):
        for components in self.components:
            components.draw()

class Hangman():
    def __init__ (self, screen, word: str):

        self.screen = screen
        # Parâmetros do Jogo
        self.letters = [letter.upper() for letter in word]
        self.answers  = ["-" for _ in self.letters]
        # Aparência das letras
        self.color = ORANGE
        self.size_font = 80
        self.font = pygame.font.SysFont('Noto Mono', self.size_font)
        # Posicionamento
        self.size = []
        self.rendered_letters = []
        self.margins = []

    def init(self):
        self.render_letters_and_set_position()
        self.set_margins()

    def toggle_value(self, value: int = None, increment: bool = False, decrement: bool = False, letter: str = False):
        if increment or decrement or value:
            return
        key = []
        for i, l in enumerate(self.letters):
            if letter.upper() == l:
                key.append(i)
        for i in key:
            self.answers[i] = letter.upper()

    def toggle_key(self, value: int = None, increment: bool = False, decrement: bool = False):
        pass

    def render_letters_and_set_position(self):
        answer = "".join(self.answers)
        self.rendered_letters = self.font.render('{}'.format(answer), True, self.color)
        _, _, w, h = self.rendered_letters.get_rect()
        self.size = (w, h)

    def response(self):
        word = "".join(self.letters)
        answer = "".join(self.answers)
        if word == answer:
            return 1
        return 0

    def get_word(self):
        return "".join(self.letters).lower()

    def set_margins(self):
        self.margins = []
        self.margins.append([(WIDTH - self.size[0]) / 2, MARGIN_TOP])

    def draw(self):
        self.render_letters_and_set_position()
        if self.screen:
            self.screen.blit(self.rendered_letters,(self.margins[0][0], self.margins[0][1]))
