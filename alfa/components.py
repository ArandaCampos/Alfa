import pygame
import os
from read_word import read_word
from items import Box, Text, Image, Text, Image

## criar o def event() em Sound e Buttons

HEIGHT, WIDTH = 648, 800
WHITE, BLUE = (240, 240, 242, .95), (1, 32, 48, 1.)
ORANGE_LIGHT, GREEN_LIGHT = (242, 68, 5, 1.), (154, 235, 163, 1.)

# Carregar diretório "Images"
ABS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
IMG_PATH = os.path.join(ABS_PATH, 'Images')

class Figure():
    def __init__(self, screen, file):

        self.screen = screen
        #Imagem
        self.image = Image(screen, file, (250,250))

    def init(self):
        self.image.init()
        self.image.set_margins(((WIDTH - 250) / 2, 50))

    def draw(self):
        self.image.draw()

#### Arrumar o sound (instanciar o Image() e exluir o ABS_PATH e IMG_PATH)
class Sound():
    def __init__(self, screen, file: str, margins: [int, int], size: (int, int) = (31.4, 30), padding: int = 60):

        self.screen = screen

        # Icone de áudio
        self.image = Image(screen, 'sound.png', size)
        self.size = size
        self.margins = margins
        self.padding = padding

    def init(self):
        self.image.init()
        self.image.set_margins((self.margins[0] + self.padding, self.margins[1] - self.size[1] /2))

    def draw(self):
        self.image.draw()

class Button_cancel():
    def __init__(self, screen):

        self.screen = screen
        # Botão
        self.button = Box(screen, (220, 75), (120, HEIGHT - 110), ORANGE_LIGHT, 8)
        # Etiqueta
        self.label = Text(screen, 'CANCELAR', 'Noto Mono', 20, WHITE)
        # Ícone
        self.image = Image(screen, 'cancel.png', (20,20))

    def init(self):
        self.button.init()
        self.label.init()
        self.label.set_margins((self.button.margins[0] + 35 , HEIGHT - 75 - self.label.size[1] / 2))
        self.image.init()
        self.image.set_margins((120 + self.button.size[0] - self.image.size[0] - 35, HEIGHT - 75 - self.image.size[1]/2))

    def draw(self):
        self.button.draw()
        self.label.draw()
        self.image.draw()

class Button_send():
    def __init__(self, screen):

        self.screen = screen
        # Botão
        self.button = Box(screen, (220, 75), (WIDTH - 120 - 220, HEIGHT - 110), GREEN_LIGHT, 8)
        # Etiqueta
        self.label = Text(screen, 'ENVIAR', 'Noto Mono', 20, BLUE)
        # Ícone
        self.image = Image(screen, 'send.png', (20,20))

    def init(self):
        self.button.init()
        self.label.init()
        self.label.set_margins((self.button.margins[0] + 35 , HEIGHT - 75 - self.label.size[1] / 2))
        self.image.init()
        self.image.set_margins((WIDTH - 120 - 220 + self.button.size[0] - self.image.size[0] - 35, HEIGHT - 75 - self.image.size[1]/2))

    def draw(self):
        self.button.draw()
        self.label.draw()
        self.image.draw()

class Score():
    def __init__(self, screen):

        # Janela
        self.screen = screen
        # Imagem
        self.image = Image(screen, 'medal.png', (42,42))
        # Texto
        self.score = 0
        self.text = Text(screen, self.score, 'Noto Mono', 28, BLUE)

    def init(self):
        self.image.init()
        self.image.set_margins((WIDTH - self.image.size[0]- 25, 25))
        self.text.init()
        self.text.set_margins((WIDTH - self.image.size[0] - 25 - self.text.size[0] - 10, 25 + (42 - self.text.size[1])/2))

    def update(self, point: int = False, increment: bool = False, decrement: bool = False):
        if point: self.score = point
        elif increment: self.score += 1
        elif decrement: self.score = self.score - 1
        self.text.update(self.score)
        self.text.set_margins((WIDTH - self.image.size[0] - 25 - self.text.size[0] - 10, 25))

    def draw(self):
        self.text.draw()
        self.image.draw()
