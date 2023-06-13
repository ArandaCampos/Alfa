import pygame
import os, pandas as pd
from animations import Blink, Hover

# Paleta de cores
HEIGHT, WIDTH = 648, 1000
BG_COLOR, BLUE, WHITE = (222, 239, 231, 240), (1, 32, 48, 255), (240, 240, 242, 242)
ORANGE_LIGHT, GREEN_LIGHT = (242, 68, 5, 255), (154, 235, 163, 255)

# Carregar diretório "Images"
ABS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
DATA_PATH = os.path.join(ABS_PATH, 'data')
IMG_PATH = os.path.join(DATA_PATH, 'Images')

class Page():
    def __init__ (self, screen, caption, bg_color: (int, int, int) = BG_COLOR):

        self.screen = screen
        # Estilização
        self.caption = caption
        self.bg_color = bg_color
        # Componentes
        self.components = []

    def modify_caption(self, caption):
        self.caption = caption
        pygame.display.set_caption(self.caption)

    def refresh_screen(self):
        self.screen.fill(self.bg_color)
        for component in self.components:
            component.draw()
        pygame.display.flip()

    def get_event(self, event):
        for component in self.components:
            component.events(event)

class Component():
    def __init__(self, screen, size, margins):
        self.screen = screen
        # Estilização
        self.size = size
        self.color = None
        self.secondary_color = None
        self.main_color = None
        # Posicionamento
        self.margins = margins
        # Renderizado
        self.rendered = None
        self.surface =  None
        # Animação
        self.animations = []
        # Eventos
        self.hover = None
        self.click = None

    def set_margins(self, margins: [int, int]):
        self.margins = margins

    def set_size(self, size: str):
        self.size = size

    def set_hover(self, secondary: (int, int, int)):
        self.colors = [self.color, secondary]
        self.hover = True

    def events(self, event: pygame.event):
        pos = pygame.mouse.get_pos()
        if self.hover:
            self.color = self.colors[1] if self.rendered.collidepoint(pos) else self.colors[0]

    def set_blink(self, velocity: int = 12):
        blink = Blink(velocity)
        self.animations.append(blink)

    def play(self):
        for animation in self.animations:
            animation.play(self.surface, self.rendered)

class Image(Component):
    def __init__(self, screen, file: str, size: (int, int), margins: (int, int) = None):
        super().__init__(screen, size, margins)

        self.file = file

    def init(self):
        self.render()

    def set_file(self, file: str):
        self.file = file

    def get_rect_center(self):
        return self.rendered.get_rect(center=self.get_center())

    def get_center(self) -> [int, int]:
        return [self.margins[0] + self.size[0] /2, self.margins[1] + self.size[1] /2]

    def render(self):
        self.rendered = pygame.image.load(os.path.join(IMG_PATH, self.file)).convert_alpha()
        self.rendered = pygame.transform.scale(self.rendered, self.size)

    def draw(self):
        self.screen.blit(self.rendered, self.margins)

class Text(Component):
    def __init__(self, screen, txt: str, family: str, size_font: int, color: [int, int, int, float], bold: bool = False, size:int=0, margins=(0,0)):
        super().__init__(screen, size, margins)

        self.text = txt
        # Estilização
        self.family = family
        self.font_size = size_font
        self.color = pygame.Color(color)
        self.font = None
        self.bold = bold

    def init(self):
        self.font = pygame.font.SysFont(self.family, self.font_size, bold=self.bold)
        self.render()

    def get_center(self) -> [int, int]:
        _, _, w, h = self.rendered.get_rect()
        return [self.margins[0] + w /2, self.margins[1] + h /2]

    def update(self, text: str = None, color: (int, int, int) = None):
        self.text = text if text else self.text
        self.color = color if color else self.color
        self.render()

    def render(self):
        self.surface = self.font.render('{}'.format(self.text), True, self.color)
        _, _, w, h = self.surface.get_rect()
        self.size = (w, h)

    def draw(self):
        self.surface = self.font.render('{}'.format(self.text), True, self.color)
        self.play()
        self.rendered = self.screen.blit(self.surface, self.margins)
        #self.play()

class Box(Component):
    def __init__(self, screen, size, margins = (0, 0), color = ORANGE_LIGHT, border_radius = 8):
        super().__init__(screen, size, margins)

        # Estilização
        self.color = color
        self.border_radius = border_radius

    def init(self):
        self.rendered = pygame.Rect(self.margins[0], self.margins[1], self.size[0], self.size[1])

    def get_center(self) -> [int, int]:
        return [self.margins[0] + self.size[0] /2, self.margins + self.size[1] /2]

    def draw(self):
        self.blited = pygame.draw.rect(self.screen, self.color, self.rendered, border_radius=self.border_radius)
        self.play()

class Button(Component):
    def __init__(self,
                 screen,
                 label: str = None,
                 color_label: (int, int, int) = WHITE,
                 size_label: int = 20,
                 size_box: (int, int) = (220, 75),
                 margin_box: (int, int) = (0,0),
                 color_box: (int, int, int) = ORANGE_LIGHT,
                 border_radius: int = 8,
                 src: str = None,
                 size_img: (int, int) =  (20, 20)
                ):
        super().__init__(screen, size_box, margin_box)

        self.box = Box(screen, size_box, margin_box, color=color_box, border_radius=border_radius)
        self.color_box = color_box
        self.label = Text(screen, label, 'Noto Mono', size_label, color_label) if label else None
        self.color_label = color_label
        self.image = Image(screen, src, (20,20)) if src else None

    def init(self):
        self.box.init() if self.box else None
        self.label.init() if self.label else None
        self.image.init() if self.image else None
        if self.image and self.label:
            # Centraliza os dois com uma margins de 35
            self.label.set_margins((
                # x
                self.box.margins[0] + 35 ,
                # y
                self.box.margins[1] + (self.box.size[1] - self.label.size[1]) / 2
            ))
            self.image.set_margins((
                # x
                self.box.margins[0] + self.box.size[0] - self.image.size[0] - 35,
                # y
                self.box.margins[1] + (self.box.size[1] - self.image.size[1])/2
            ))
        elif self.image:
            # Centraliza a imagem
            self.image.set_margins((
                # x
                self.box.margins[0] + (self.box.size[0] - self.image.size[0]) / 2,
                # y
                self.box.margins[1] + (self.box.size[1] - self.image.size[1]) / 2
            ))
        elif self.label:
            # Centraliza o label
            self.label.set_margins((
                # x
                self.box.margins[0] + (self.box.size[0] - self.image.size[0]) / 2,
                # y
                self.box.margins[1] + (self.box.size[1] - self.label.size[1]) / 2
            ))

    def set_hover(self, secondary_box: (int, int, int), secondary_label: (int, int, int) = None):
        self.box_colors = [self.color_box, secondary_box]
        self.label_colors = [self.color_label, secondary_label] if self.label else None
        self.hover = True

    def events(self, event: pygame.event):
        pos = pygame.mouse.get_pos()
        if self.hover:
            if self.box.rendered.collidepoint(pos):
                self.box.color = self.box_colors[1]
                if self.label:
                    self.label.color = self.label_colors[1]
            else:
                self.box.color = self.box_colors[0]
                if self.label:
                    self.label.color = self.label_colors[0]

    def draw(self):
        self.box.draw()
        self.label.draw() if self.label else None
        self.image.draw() if self.image else None

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
