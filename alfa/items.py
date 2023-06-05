import pygame
import os, pandas as pd

# Paleta de cores
HEIGHT, WIDTH = 648, 1000
WHITE, BLUE = (240, 240, 242, .95), (1, 32, 48, 1.)
ORANGE_LIGHT, GREEN_LIGHT = (242, 68, 5, 1.), (154, 235, 163, 1.)

# Carregar diretório "Images"
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
        self.rendered = self.font.render('{}'.format(self.text), True, self.color)
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

class Menu():
    def __init__(self, screen):

        self.screen = screen
        # Botões
        self.button = []
        # Etiquetas
        self.label = []

    def init(self):
        line, column = 4, 6
        space_btn = 70 * column + 30 * (column - 1)
        # [7, 10, 22, 24] =~ [H, K, Y, W]
        letters = [i for i in range(25) if i not in [7, 10, 22, 24]]
        for j in range(line):
            for i in range(column):
                if i + column * j in range(len(letters)):
                    self.button.append(Box(self.screen, (70, 70), ((WIDTH - space_btn)/2 + 100 * i, 200 + 100 * j), GREEN_LIGHT, 8))
                    self.button[-1].init()
                    self.label.append(Text(self.screen, chr(65 + letters[i + column * j]), 'Noto Mono', 20, BLUE))
                    self.label[-1].init()
                    self.label[-1].set_margins(
                        (self.button[-1].margins[0] + (70 - self.label[-1].size[0]) / 2 , self.button[-1].margins[1] + (70 - self.label[-1].size[1]) / 2)
                    )

    def draw(self):
        for i in range(len(self.button)):
            self.button[i].draw()
            self.label[i].draw()

class Rank():
    def __init__(self,screen, score: int, stage: str):

        self.screen = screen
        # Imagem
        self.image = Image(screen, 'medal.png', (250, 250))
        # Texto
        self.stage = stage
        self.score = score
        self.legend = Text(screen, f'FAMÍLIA - {self.stage.upper()}', 'Noto Mono', 14, BLUE)
        self.text = Text(screen, f'{self.score} PONTOS', 'Noto Mono', 30, BLUE)

    def init(self):
        self.image.init()
        self.legend.init()
        self.text.init()
        self.image.set_margins(((WIDTH - self.image.size[0])/2, 120))
        self.legend.set_margins(((WIDTH - self.legend.size[0]) / 2, self.image.margins[1] + self.image.size[1] + 15))
        self.text.set_margins(((WIDTH - self.text.size[0]) / 2, self.legend.margins[1] + self.legend.size[1] + 20))
        self.save()

    def save(self):
        try:
            rank = pd.DataFrame(pd.read_csv(f"Data/rank_{self.stage}.csv", sep=" "))
        except:
            rank = pd.DataFrame({"user": [], "score": []})
        last_game = pd.DataFrame({
            "user": ["Mônica"],
            "score": [self.score]
        })
        rank = pd.concat([rank, last_game], ignore_index=True)
        rank = rank.sort_values(by='score', ascending=False)
        #position = rank.index[rank['score'] == self.score].tolist()
        rank.to_csv(f"Data/rank_{self.stage}.csv", sep=" ", index=False)

    def draw(self):
        self.image.draw()
        self.legend.draw()
        self.text.draw()
