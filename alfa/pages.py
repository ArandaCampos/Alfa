# --------------------------------------------
#   Author: Renan Campos
#   Github: github.com/ArandaCampos
# --------------------------------------------

import random
from items import Text, Button, Image, Page, Component
from constants import Colors, Params
from games import Basic_math, Toggle_letter

PARAMS, COLOR = Params(), Colors()

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

class Goodbye(Page):
    def __init__(self, screen, func):

        super().__init__(screen, "ATÉ MAIS - ALFA", COLOR.WHITE, func)

    def init(self):

        self.components.append(Text(self.screen, 'ALFA', 90, COLOR.ORANGE))
        self.components.append(Text(self.screen, 'OBRIGADO POR JOGAR', 20, COLOR.BLUE_DARK))
        self.components.append(Image(self.screen, 'heart.png', (22, 22)))
        for component in self.components:
            component.init()
        self.components[0].set_margins_center()
        self.components[1].set_margins(((PARAMS.WIDTH - self.components[1].size[0] - 27) /2 , PARAMS.HEIGHT - 75 - 100))
        self.components[2].set_margins((self.components[1].size[0] + self.components[1].margins[0] + 5 , PARAMS.HEIGHT - 75 - 100))

class Home(Page):
    def __init__(self, screen, func):
        super().__init__(screen, "PÁGINA INICIAL - ALFA", COLOR.WHITE, func)

    def func_wait_for(self):
        self.components[1].text = 'PRESSIONE QUALQUER TECLA PARA CONTINUAR'
        self.components[1].render()
        self.components[1].set_margins(((PARAMS.WIDTH - self.components[1].size[0]) /2 , PARAMS.HEIGHT - 75 - 100))
        # Configurar eventos e animações
        self.components[1].set_blink()
        self.components[1].set_hover(COLOR.BLUE)
        self.components[1].set_click(self.func_visible)
        self.components[1].set_keydown(self.func_visible)

    def visible_menu(self):
        self.components[0].set_move(0.2 * PARAMS.FPS, (self.components[0].margins[0], 50))
        self.components[1].able = False
        self.components[2].able = True
        self.components[3].able = True

    def go_to(self, page):
        def func(event = None):
            nonlocal page
            self.func(page)
        return func

    def func_visible(self, event = None):
        self.visible_menu()

    def init(self):
        self.components.append(Text(self.screen, 'ALFA', 90, COLOR.ORANGE))
        self.components.append(Text(self.screen, 'SEJA BEM-VINDO(A)', 20, COLOR.BLUE_DARK))
        self.components.append(Button(self.screen, label="ALFABETIZAÇÃO", margin_box=(PARAMS.WIDTH / 2 - 250, PARAMS.HEIGHT / 2)))
        self.components.append(Button(self.screen, label="MATEMÁTICA", margin_box=(PARAMS.WIDTH / 2 + 30, PARAMS.HEIGHT / 2)))
        for component in self.components:
            component.init()
        self.components[0].set_margins_center()
        self.components[1].set_margins(((PARAMS.WIDTH - self.components[1].size[0]) /2 , PARAMS.HEIGHT - 75 - 100))
        # configurar eventos e animações
        self.components[0].set_wait(2*PARAMS.FPS, self.func_wait_for)
        self.components[2].set_click(self.go_to(Menu_complete(self.screen, self.func)))
        self.components[3].set_click(self.go_to(Menu_math(self.screen, self.func)))
        self.components[2].set_hover(COLOR.ORANGE, COLOR.WHITE)
        self.components[3].set_hover(COLOR.ORANGE, COLOR.WHITE)
        self.components[2].able = False
        self.components[3].able = False

class Menu(Page):
    def __init__(self, screen, caption, func, options, stage, size_box, grid, gap):
        super().__init__(screen, caption, COLOR.WHITE, func)

        self.options = options
        self.stage = stage
        # Positionamento
        self.size_box = size_box
        self.grid = grid
        self.gap = gap
        self.space = (size_box[0] + gap[0], size_box[1] + gap[1])
        self.margin_menu = [
            (PARAMS.WIDTH - size_box[0] * self.grid[0] - gap[0] * (self.grid[0] - 1)) / 2,
            (PARAMS.HEIGHT - size_box[1] * self.grid[1] - gap[1] * (self.grid[1] - 1)) / 2
        ]

    def func_generic(self, number):
        pass

    def func_back(self, event=None):
        self.func(Home(self.screen, self.func))

    def func_keydown(self, event):
        pass

    def init(self):
        # Título
        self.components.append(Text(self.screen, 'ALFA', 90, COLOR.ORANGE))
        self.components.append(Image(self.screen, 'back.png', (25, 25), (25,25)))
        self.components[0].init()
        self.components[1].init()
        self.components[0].set_margins(((PARAMS.WIDTH - self.components[0].size[0])/ 2, 50))
        self.components[1].set_click(self.func_back)
        # Botões
        for index, option in enumerate(self.options):
            c, l = index % self.grid[0], index // self.grid[0]
            self.components.append(Button(
                self.screen, label=option, size_box=self.size_box,
                margin_box=(self.margin_menu[0] + self.space[0] * c, self.margin_menu[1] + self.space[1] * l)
            ))
            self.components[-1].init()
            self.components[-1].set_hover(COLOR.ORANGE, COLOR.WHITE)
            self.components[-1].set_click(self.func_generic(self.stage[index]))

        self.components[-1].set_keydown(self.func_keydown)

class Menu_complete(Menu):
    def __init__(self, screen, func):
        super().__init__(
            screen,
            "MENU DE OPÇÕES - ALFA (MATEMÁTICA BÁSICA)",
            func,
            [chr(65 + i) for i in range(25) if i not in [7, 10, 22, 24]],
            [chr(65 + i) for i in range(25) if i not in [7, 10, 22, 24]],
            # Positionamento
            (70, 70),
            (6, 4),
            (30, 30),
        )
        self.margin_menu[1] = 200

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

class Rank(Page):
    def __init__(self, screen, func, score: int, stage: str, func_to_menu):
        super().__init__(screen, "FIM DE JOGO - ALFA", COLOR.WHITE, func)

        self.score = score
        self.stage = stage
        self.func_to_menu = func_to_menu

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

class Game(Page):
    def __init__(self, screen, caption, func):
        super().__init__(screen, caption, COLOR.WHITE,  func)
        # Componentes
        self.sound_win = PARAMS.SOUND_WIN
        self.sound_fail = PARAMS.SOUND_FAIL
        # Gabarito da rodada
        self.df = None
        self.stage = None
        self.play = 1
        self.round = 0
        self.option = None

    def wait(self):
        self.components[2].able = False
        self.components[3].able = False
        self.components[5].able = True
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
        self.components[5].able = False
        self.next_round()

    def func_back(self, event=None):
        pass

    def func_click(self, cancel: bool = False):
        def click():
            nonlocal cancel
            self.get_result(cancel)
        return click

    def func_keydown(self, event):
        if event.key == pygame.K_UP or event.key == pygame.K_RIGHT:
            self.components[6].toggle_value(increment=True)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_LEFT:
            self.components[6].toggle_value(decrement=True)
        elif event.key == pygame.K_BACKSPACE:
            self.components[6].toggle_value(backspace=True)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            self.get_result()
        else:
            self.components[6].toggle_value(value=event.unicode)

    def init(self):
        """
         +----------------------------+
         | [0]   ->   ícone 'medalha' |
         | [1]   ->   pontuação       |
         | [2]   ->   botão 'não sei' |
         | [3]   ->   botão 'enviar'  |
         | [4]   ->   ícone 'voltar'  |
         | [5]   ->   próximo         |
         | [...] ->   parâmetros add  |
         +----------------------------+
        """
        self.round, self.play = 0, 1
        self.components.append(Image(self.screen, 'medal.png', (42, 42), (PARAMS.WIDTH - 42 - 25, 25)))
        self.components.append(Text(self.screen, '0', 28, COLOR.BLUE_DARK))
        self.components.append(Button(self.screen,
                                      label="NÃO SEI", color_label=COLOR.WHITE, color_box=COLOR.ORANGE_DARK,
                                      margin_box=(120, PARAMS.HEIGHT - 110), src="cancel.png"))
        self.components.append(Button(self.screen, label="ENVIAR", margin_box=(PARAMS.WIDTH - 120 - 220, PARAMS.HEIGHT - 110), src="send.png"))
        self.components.append(Image(self.screen, 'back.png', (25, 25), (25,25)))
        self.components.append(Text(self.screen, 'PRESSIONE ENTER', 20, COLOR.BLUE_DARK))
        for component in self.components:
            component.init()
        # Marigins relativas
        self.components[1].set_margins((PARAMS.WIDTH - 42 - 25 - self.components[1].size[0] - 10, 25 + (42 - self.components[1].size[1])/2))
        self.components[5].set_margins(((PARAMS.WIDTH - self.components[5].size[0])/2, PARAMS.HEIGHT - 110))
        # Eventos
        self.components[2].set_click(self.func_click(cancel=True))
        self.components[2].set_hover(COLOR.ORANGE, COLOR.WHITE)
        self.components[3].set_click(self.func_click())
        self.components[3].set_hover(COLOR.GREEN_DARK, COLOR.BLUE_DARK)
        self.components[4].set_click(self.func_back)
        self.components[5].set_blink()
        self.components[5].able = False
        self.init_game()

    def set_stage(self, stage: str):
        self.stage = stage

    def next_round(self):
        pass

class Game_math(Game):
    def __init__(self, screen, func):
        super().__init__(screen, "MATEMÁTICA - ALFA", func)

    def func_back(self, event=None):
        self.func(Menu_math(self.screen, self.func))

    def init_game(self):
        """
         +----------------------------+
         | [6]   ->   jogo            |
         +----------------------------+
        """
        self.load_data()
        self.components.append(Basic_math(self.screen, self.op, self.result))
        self.components[6].init()
        # Marigins relativas
        self.components[6].set_margins(((PARAMS.WIDTH - self.components[6].size[0])/2, PARAMS.HEIGHT - 110))
        self.components[6].set_keydown(self.func_keydown)

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

    def func_to_menu(self, event):
        self.func(Menu_math(self.screen, self.func))

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
            rank.to_csv(f"data/rank_{self.stage}.csv", sep=" ", index=False)
            #position = rank.index[rank['score'] == self.components[1].text].tolist()
            self.play = 0
            self.func(Rank(self.screen, self.func, self.components[1].text, self.stage, self.func_to_menu))
        else:
            # Próxima rodada
            self.round += 1
            self.load_data()
            self.components[6].next_round(self.op, self.result)

class Game_complete(Game):
    def __init__(self, screen, func):
        super().__init__(screen, "COMPLETAR - ALFA", func)

    def func_back(self, event=None):
        self.func(Menu_complete(self.screen, self.func))

    def func_click_sound(self, event=None):
        self.to_read(self.components[6].get_word())

    def func_to_menu(self, event):
        self.func(Menu_complete(self.screen, self.func))

    def to_read(self, word: str):
        # Lê o texto escrito pelo usuário
        tts = gTTS(word, lang='pt', tld="com.br")
        tts.save("audio.mp3")
        PARAMS.load_sound()

    def init_game(self):
        """
         +----------------------------+
         | [6]   ->   jogo            |
         | [7]   ->   ilustração      |
         | [8]   ->   ícone áudio     |
         +----------------------------+
        """
        self.load_data()
        self.components.append(Toggle_letter(self.screen, self.df["word"][self.round], self.option, self.df["answer"][self.round]))
        self.components.append(Image(self.screen, self.df["file"][self.round], (250, 250), ((PARAMS.WIDTH - 250) / 2, 50)))
        self.components.append(Image(self.screen, 'sound.png', (31.4, 30)))
        for i in (6, 7, 8):
            self.components[i].init()
        # Marigins relativas
        self.components[8].set_margins((
            self.components[6].get_right() + 60,
            self.components[6].margins[1] + (self.components[6].size[1] - self.components[8].size[1]) / 2
        ))
        # Eventos
        self.components[6].set_keydown(self.func_keydown)
        self.components[8].set_click(self.func_click_sound)

    def load_data(self):
        self.df = pd.DataFrame(pd.read_csv(f'data/{self.stage}.csv', sep=" "))
        self.option = self.df["answer"].unique()
        self.df = self.df.sample(frac=1).reset_index(drop=True)

    def next_round(self):
        if self.round == 1 or self.round == len(self.df) - 1:
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
            rank.to_csv(f"data/rank_{self.stage}.csv", sep=" ", index=False)
            print("Posição: " + str(rank.index[rank['score'] == int(self.components[1].text)].tolist()))
            self.play = 0
            self.func(Rank(self.screen, self.func, self.components[1].text, self.stage, self.func_to_menu))
        else:
            # Próxima rodada
            self.round += 1
            self.components[6].next_round(self.df["word"][self.round], self.df["answer"][self.round])
            self.components[7].file = self.df["file"][self.round]
            self.components[7].init()
            self.components[8].margins = [
                self.components[6].get_right() + 60,
                self.components[6].margins[1] + (self.components[6].size[1] - self.components[-1].size[1]) / 2
            ]
