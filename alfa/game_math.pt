# --------------------------------------------
#   Author: Renan Campos
#   Github: github.com/ArandaCampos
# --------------------------------------------

import os, random
from items import Text, Button, Image, Page, Component, Rank, Menu
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

class Game_math(Page):
    def __init__(self, screen, func):
        super().__init__(screen, "MATEMÁTICA - ALFA", COLOR.WHITE, func)
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
        self.components[6].able = True
        self.components[5].set_keydown(self.func_to_next)

    def get_result(self, cancel: bool = False):
        result = self.components[5].response()
        if cancel or not result:
            self.sound_fail.play()
        else:
            self.sound_win.play()
            self.components[1].text = str(int(self.components[1].text) + 1)
        self.wait()

    def func_to_next(self, event = None):
        self.components[5].set_keydown(self.func_keydown)
        self.components[2].able = True
        self.components[3].able = True
        self.components[6].able = False
        self.next_round()

    def func_back(self, event=None):
        self.func(Menu_math(self.screen, self.func))

    def func_click(self, cancel: bool = False):
        def click():
            nonlocal cancel
            self.get_result(cancel)
        return click

    def func_keydown(self, event):
        if event.key == pygame.K_UP or event.key == pygame.K_RIGHT:
            self.components[5].toggle_value(increment=True)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_LEFT:
            self.components[5].toggle_value(decrement=True)
        elif event.key == pygame.K_BACKSPACE:
            self.components[5].toggle_value(backspace=True)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            self.get_result()
        else:
            self.components[5].toggle_value(value=event.unicode)

    def init(self):
        """
         +----------------------------+
         | [0]   ->   ícone 'medalha' |
         | [1]   ->   pontuação       |
         | [2]   ->   botão 'não sei' |
         | [3]   ->   botão 'enviar'  |
         | [4]   ->   ícone 'voltar'  |
         | [5]   ->   operação        |
         | [6]   ->   próximo         |
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
        self.components.append(Basic_math(self.screen, self.op, self.result))
        self.components.append(Text(self.screen, 'PRESSIONE ENTER', 20, COLOR.BLUE_DARK))
        for component in self.components:
            component.init()
        # Marigins relativas
        self.components[1].set_margins((PARAMS.WIDTH - 42 - 25 - self.components[1].size[0] - 10, 25 + (42 - self.components[1].size[1])/2))
        self.components[6].set_margins(((PARAMS.WIDTH - self.components[6].size[0])/2, PARAMS.HEIGHT - 110))
        # Eventos
        self.components[2].set_click(self.func_click(cancel=True))
        self.components[2].set_hover(COLOR.ORANGE_DARK, COLOR.WHITE)
        self.components[3].set_click(self.func_click())
        self.components[3].set_hover(COLOR.GREEN_DARK, COLOR.BLUE_DARK)
        self.components[4].set_click(self.func_back)
        self.components[5].set_keydown(self.func_keydown)
        #self.components[6].set_keydown(self.func_to_next)
        self.components[6].set_blink()
        self.components[6].able = False

    def set_stage(self, stage: str):
        self.stage = stage

    def load_data(self):
        num1, num2 = random.randint(0, 9), random.randint(1, 9)
        if self.stage == "sum":
            self.op = str(num1) + " + " + str(num2) + " = "
            self.result = num1 + num2
        elif self.stage == 'sub':
            self.op = str(num1) + " - " + str(num2) + " = "
            self.result = num1 - num2
        elif self.stage == 'mul':
            self.op = str(num1) + " x " + str(num2) + " = "
            self.result = num1 * num2
        elif self.stage == 'div':
            self.op = str(num1 * num2) + " / " + str(num2) + " = "
            self.result = num1

    def next_round(self):
        if self.round == 9:
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
            self.func(Rank(self.screen, self.func, self.components[1].text, self.stage))
        else:
            # Próxima rodada
            self.round += 1
            self.load_data()
            self.components[5].next_round(self.op, self.result)

class Menu_math(Menu):
    def __init__(self, screen, func):
        super().__init__(
            screen,
            "MENU DE OPÇÕES - ALFA (MATEMÁTICA BÁSICA)",
            func,
            ("SOMA (+)", "SUBTRAÇÃO (-)", "MULTIPLICAÇÃO (x)", "DIVISÃO (%)"),
            ("sum", "sub", "mul", "div"),
            # Positionamento
            (220, 75),
            (2, 2),
            (50, 50),
        )

        self.margin_menu[1] = (PARAMS.HEIGHT - 75 * 2 - 50) / 2 + 50

    def func_generic(self, number):
        def func_click():
            nonlocal number
            game = Game_math(self.screen, self.func)
            game.set_stage(number)
            self.func(game)
        return func_click

   #def func_keydown(self, event):
   #    if ord(event.unicode.upper()) in self.options:
   #        game = Game_math(self.screen, self.func)
   #        game.set_stage(event.unicode.lower())
   #        self.func(game)
