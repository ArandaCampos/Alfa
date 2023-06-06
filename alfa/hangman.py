# --------------------------------------------
#
#              +--------+--------+---> fields
#             |        |        |
#       +--------+--------+--------+
#       | option | option | option |
#       +--------+--------+--------+
#
# --------------------------------------------

try:
    import pygame
except ImportError:
    print('Erro ao importar a biblioteca Pygame.')
    raise SystemExit
#from components import Text

WIDTH = 1000
ORANGE, BLUE = (250, 127, 8, .98), (1, 32, 48, 1.)
MARGIN_TOP = 390

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

    def toggle_value(self, letter: str = False):
        key = self.letters.index(letter.upper()) if letter.upper() in self.letters else -1
        if key != -1:
            self.answers[key] = letter.upper()

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
