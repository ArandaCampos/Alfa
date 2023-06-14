try:
    import pygame
except ImportError:
    print('Erro ao importar a biblioteca Pygame.')
    raise SystemExit

from items import Component
#from components import Text

WIDTH = 1000
ORANGE, BLUE = (250, 127, 8, .98), (1, 32, 48, 1.)
MARGIN_TOP = 390

class Toggle_letter(Component):
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

    def __init__ (self, screen, word: str, options: (str), answers: (str), size: int =  None, margins: (int, int) = None):
        super().__init__(screen, size, margins)

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

    def new_game(self, word, options, answers):
        self.letters = word.upper().split("*")
        self.options = list(options)
        self.values  = [0 for i, item in enumerate(self.letters) if item == '']
        self.fields  = [i for i, item in enumerate(self.letters) if item == '']
        self.key     = 0
        self.answers = answers
        self.size = []
        self.size_letters = []
        self.rendered_letters = []
        self.margins = []


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
