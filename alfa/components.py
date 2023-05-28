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

class Back_home():
    def __init__(self, screen):

        self.screen = screen
        # Imagem
        self.image = Image(screen, 'back.png', (32, 32))

    def init(self):
        self.image.init()
        self.image.set_margins((25, 25))

    def draw(self):
        self.image.draw()


class Sound():
    def __init__(self, screen, margins: [int, int], padding: int = 60):

        self.screen = screen

        # Icone de áudio
        self.image = Image(screen, 'sound.png', (31.4, 30))
        self.margins = margins
        self.padding = padding

    def init(self):
        self.image.init()
        self.image.set_margins((self.margins[0] + self.padding, self.margins[1] - self.image.size[1] /2))

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
        self.image.set_margins((self.button.margins[0] + self.button.size[0] - self.image.size[0] - 35, HEIGHT - 75 - self.image.size[1]/2))

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

class Button_play_game():
    def __init__(self, screen):

        self.screen = screen
        # Botão
        self.button = Box(screen, (220, 75), ((WIDTH - 220) / 2, HEIGHT - 75 - 50), ORANGE_LIGHT, 8)
        # Etiqueta
        self.label = Text(screen, 'JOGAR', 'Noto Mono', 20, WHITE)
        # Ícone
        self.image = Image(screen, 'play.png', (20,20))

    def init(self):
        self.button.init()
        self.label.init()
        self.label.set_margins((self.button.margins[0] + 35 , self.button.margins[1] + (75 - self.label.size[1]) / 2))
        self.image.init()
        self.image.set_margins((self.button.margins[0] + self.button.size[0] - self.image.size[0] - 35, self.button.margins[1] + (75 - self.image.size[1])/2))

    def draw(self):
        self.button.draw()
        self.label.draw()
        self.image.draw()

"""
class Rank():
    def __init__(self,screen):

        self.screen = screen
        # Imagem
        self.image = Image(screen, 'medal.png', (250, 250))
        # Texto
        self.text_1 = Text(screen, 'jogador    pontos', 'Noto Mono', 20, BLUE)
        self.text_2 = Text(screen, 'Jogador 1    33', 'Noto Mono', 35, BLUE)
        self.text_3 = Text(screen, 'Jogador 2    30', 'Noto Mono', 35, ORANGE_LIGHT)
        self.text_4 = Text(screen, 'Jogador 3     5', 'Noto Mono', 35, BLUE)

    def init(self):
        self.image.init()
        self.image.set_margins(((WIDTH - self.image.size[0]) / 2, 50))
        self.text_1.init()
        self.text_2.init()
        self.text_3.init()
        self.text_4.init()
        self.text_1.set_margins(((WIDTH - self.text_1.size[0]) / 2, self.image.size[1] + self.image.margins[1] + 50))
        self.text_2.set_margins(((WIDTH - self.text_2.size[0]) / 2, self.text_1.margins[1] + 50))
        self.text_3.set_margins(((WIDTH - self.text_3.size[0]) / 2, self.text_2.margins [1] + 50))
        self.text_4.set_margins(((WIDTH - self.text_4.size[0]) / 2, self.text_3.margins [1] + 50))

    def draw(self):
        self.image.draw()
        self.text_1.draw()
        self.text_2.draw()
        self.text_3.draw()
        self.text_4.draw()
"""
