# --------------------------------------------
#   Author: Renan Campos
#   Github: github.com/ArandaCampos
# --------------------------------------------

import os
from items import Text, Component, Circle, Image
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

    def toggle_value(self, value: str = False, increment: bool = False, decrement: bool = False):
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
    def __init__ (self, screen, numbers: [int, int], op: str, result: str, size: int =  [0,0], margins: (int, int) = [0,0]):
        super().__init__(screen, size, margins)

        # Parâmetros do Jogo
        self.numbers = numbers
        self.operation = op
        self.answer = 0
        self.result = result
        self.components = []
        self.expression = f'{numbers[0]} {op} {numbers[1]} = '

    def init(self):
        self.init_jars()
        if self.pos_a:
            for i, pos in enumerate(self.pos_a):
                self.components.append(Circle(self.screen, margins=pos, color=COLOR.BLUE, radius=15))
                self.components[-1].able = True if i < self.numbers[0] else False
        if self.pos_b:
            for i, pos in enumerate(self.pos_b):
                self.components.append(Circle(self.screen, margins=pos, color=COLOR.BLUE, radius=15))
                self.components[-1].able = True if i < self.numbers[1] else False
        if self.pos_x:
            for i, pos in enumerate(self.pos_x):
                self.components.append(Circle(self.screen, margins=pos, color=COLOR.ORANGE, radius=15))
                self.components[-1].able = True if i < self.answer else False
        for i in range(self.start_a, len(self.components)):
            self.components[i].init()

    def is_number(self, value):
        try:
             float(value)
        except ValueError:
             return False
        return True

    def next_round(self, numbers, op, result):
        self.numbers = numbers
        self.operation = op
        self.answer = 0
        self.result = result
        self.restart_components()

    def draw_answer(self):
        for i in range(len(self.pos_x)):
            self.components[i + self.start_answer].able = True if i < self.answer else False

    def get_right(self):
        return self.components[-1].get_right()

    def response(self, cancel: bool = False):
        response = int(self.result) == int(self.answer)
        for i in range(self.start_a, len(self.components)):
            self.components[i].color = COLOR.GREEN_DARK
        if not response:
            self.draw_result()
        return response

    def draw_result(self):
        for i in range(self.start_answer, len(self.pos_x)):
            self.components[i].able = False
        for i in range(self.result):
            self.components[i + self.start_answer].able = True

    def restart_components(self):
        for i in range(self.start_a, len(self.components)):
            self.components[i].color = COLOR.BLUE if i < self.start_answer else COLOR.ORANGE
            self.components[i].able = False
        for i in range(self.start_a, self.numbers[0] + self.start_a):
            self.components[i].able = True
        for i in range(self.start_b, self.start_answer):
            if i < self.numbers[1] + self.start_b:
                self.components[i].able = True

    def toggle_value(self, value: int = None, increment: bool = False, decrement: bool = False):
        if increment:
            self.answer = self.answer + 1 if self.answer < len(self.pos_x) else len(self.pos_x)
        elif decrement:
            self.answer = self.answer - 1 if self.answer > 1 else 0
        elif value:
            if self.is_number(value):
                self.answer = int(value)
        self.draw_answer()

    def draw(self):
        for components in self.components:
            components.draw()

class Sum_sub(Basic_math):
    def __init__ (self, screen, numbers: (int, int), op: str, result: str, size: int =  [0,0], margins: (int, int) = [0,0]):
        super().__init__(screen, numbers, op, result, size, margins)

        self.pos_a = [
            [210, 400], [245, 400], [280, 400],
            [210, 365], [245, 365], [280, 365],
            [210, 330], [245, 330], [280, 330]
        ]
        self.pos_b = [
            [440, 400], [475, 400], [510, 400],
            [440, 365], [475, 365], [510, 365],
            [440, 330], [475, 330], [510, 330]
        ]
        self.pos_x = [
            [682, 400], [717, 400], [752, 400], [787, 400],
            [682, 365], [717, 365], [752, 365], [787, 365],
            [682, 330], [717, 330], [752, 330], [787, 330],
            [682, 295], [717, 295], [752, 295], [787, 295],
                        [717, 260], [752, 260]
        ]
        self.start_a = 5
        self.start_b = 14
        self.start_answer = 23

    def init_jars(self):
        """
            +----------------------------+
            | [0]     -   Operador       |
            | [1]     -   Operador       |
            | [2]     -   Jarro 1        |
            | [3]     -   Jarro 2        |
            | [4]     -   Jarro 3        |
            | [5-13]  -   1º numerador   |
            | [14-22] -   2º numerador   |
            | [23-40] -   resposta       |
            +----------------------------+
        """
        self.components = []
        self.components.append(Text(self.screen, self.operation, 80, COLOR.BLUE_DARK))
        self.components.append(Text(self.screen, "=", 80, COLOR.BLUE_DARK))
        self.components.append(Image(self.screen, 'jar.png', (220, 220), (135, 220)))
        self.components.append(Image(self.screen, 'jar.png', (220, 220), (365, 220)))
        self.components.append(Image(self.screen, 'jar.png', (280, 280), (595, 160)))
        for component in self.components:
            component.init()
        # Margens
        self.components[0].set_margins((340, 350 - self.components[0].size[1] /2))
        self.components[1].set_margins((570, 350 - self.components[1].size[1] /2))

class Div(Basic_math):
    def __init__ (self, screen, numbers: (int, int), op: str, result: str, size: int =  [0,0], margins: (int, int) = [0,0]):
        super().__init__(screen, numbers, op, result, size, margins)

        self.pos_a = [
            [125, 400], [160, 400], [195, 400], [230, 400],
            [125, 365], [160, 365], [195, 365], [230, 365],
            [125, 330], [160, 330], [195, 330], [230, 330],
            [125, 295], [160, 295], [195, 295], [230, 295]
        ]
        self.pos_b = []
        self.pos_x = [
            [555, 400], [670, 400], [780, 400], [890, 400],
            [595, 400], [710, 400], [820, 400], [930, 400],
            [555, 360], [670, 360], [780, 360], [890, 360],
            [595, 360], [710, 360], [820, 360], [930, 360],
        ]
        self.start_a = 6
        self.start_b = 22
        self.start_answer = 22
        self.answer = 0

    def init_jars(self):
        """
            +----------------------------+
            | [0]     -   Operador       |
            | [1]     -   Jarro a        |
            | [2]     -   Jarro 1        |
            | [3]     -   Jarro 2        |
            | [4]     -   Jarro 3        |
            | [5]     -   Jarro 4        |
            | [6-21]  -   1º numerador   |
            | [-]     -   2º numerador   |
            | [22-32] -   resposta       |
            +----------------------------+
        """
        self.components.append(Text(self.screen, f'{self.operation} {self.numbers[1]} =', 80, COLOR.BLUE_DARK))
        self.components.append(Image(self.screen, 'jar.png', (280, 280), (38, 160)))
        self.components.append(Image(self.screen, 'jar.png', (145, 145), (502, 280)))
        self.components.append(Image(self.screen, 'jar.png', (145, 145), (617, 280)))
        self.components.append(Image(self.screen, 'jar.png', (145, 145), (727, 280)))
        self.components.append(Image(self.screen, 'jar.png', (145, 145), (837, 280)))
        for component in self.components:
            component.init()
        # Margens
        self.components[0].set_margins((290, 350 - self.components[0].size[1] /2))
        # Efeito
        for i in range(2 + self.numbers[1], 6):
            self.components[i].surface.set_alpha(30)

    def toggle_value(self, value: int = None, increment: bool = False, decrement: bool = False):
        if increment:
            self.answer = self.answer + 1 if self.answer < 4 else 4
        elif decrement:
            self.answer = self.answer - 1 if self.answer > 1 else 0
        elif value:
            if self.is_number(value):
                self.answer = int(value)
        self.draw_answer()

    def draw_result(self):
        for i in range(self.start_answer, len(self.pos_x) + self.start_answer):
            self.components[i].able = False
        for i in range(self.result):
            for j in range(self.numbers[1]):
                self.components[i * 4 + j + self.start_answer].able = True

    def next_round(self, numbers, op, result):
        self.numbers = numbers
        self.operation = op
        self.answer = 0
        self.result = result
        self.restart_components()
        for i in range(2, 6):
            if i < self.numbers[1] + 2:
                self.components[i].surface.set_alpha(255)
            else:
                self.components[i].surface.set_alpha(30)
        self.components[0].text = f'{self.operation}{self.numbers[1]} = '

    def draw_answer(self):
        for i in range(int(len(self.pos_x) / 4)):
            for j in range(self.numbers[1]):
                self.components[i * 4 + j + self.start_answer].able = True if i < self.answer else False

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
