import pygame
import os

ABS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
IMG_PATH = os.path.join(ABS_PATH, 'Images')

class Image():
    def __init__(self, screen, file, size):

        self.screen = screen
        self.file = file
        # Estilização
        self.size = size
        # Position
        self.margins = None
        # Render
        self.rendered = None

    def init(self):
        self.render()

    def set_file(self, file: str):
        self.file = file

    def set_size(self, size: str):
        self.size = size

    def get_center(self) -> [int, int]:
        return [self.margins[0] + self.size[0] /2, self.margins[1] + self.size[1] /2]

    def set_margins(self, margins: [int, int]):
        self.margins = margins

    def render(self):
        self.rendered = pygame.image.load(os.path.join(IMG_PATH, self.file)).convert_alpha()
        self.rendered = pygame.transform.scale(self.rendered, self.size)

    def draw(self):
        self.screen.blit(self.rendered, self.margins)

class Text():
    def __init__(self, screen, txt: str, family: str, size_font: int, color: (int, int, int), bold: bool = False):

        self.screen = screen
        self.text = txt
        # Estilização
        self.family = family
        self.font_size = size_font
        self.size = 0
        self.color = color
        self.font = None
        self.bold = bold
        # Position
        self.margins = 0
        # Render
        self.rendered = None

    def init(self):
        self.font = pygame.font.SysFont(self.family, self.font_size, bold=self.bold)
        self.render()

    def set_text(self, txt: str):
        self.text = txt

    def set_font(self, family: str, size: int, bold):
        self.font = pygame.font.SysFont(family, size, bold=bold)

    def set_color(self, color: (int, int, int)):
        self.color = color

    def get_center(self) -> [int, int]:
        _, _, w, h = self.rendered.get_rect()
        return [self.margins[0] + w /2, self.margins[1] + h /2]

    def set_margins(self, margins: [int, int]):
        self.margins = margins

    def update(self, text):
        self.text = text
        self.render()

    def render(self):
        self.rendered = None
        self.rendered = self.font.render('{}'.format(self.text), True, self.color)
        _, _, w, h = self.rendered.get_rect()
        self.size = (w, h)

    def draw(self):
        self.screen.blit(self.rendered, self.margins)

class Box():
    def __init__(self, screen, size, margins, color, border_radius):

        self.screen = screen
        # Estilização
        self.color = color
        self.border_radius = border_radius
        # Position
        self.size = size
        self.margins = margins
        # Render
        self.rendered = None

    def init(self):
        self.rendered = pygame.Rect(self.margins[0], self.margins[1], self.size[0], self.size[1])

    def get_center(self) -> [int, int]:
        return [self.margins[0] + self.size[0] /2, self.margins + self.size[1] /2]

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rendered, border_radius=self.border_radius)
