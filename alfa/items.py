import pygame
import os, pandas as pd
from animations import Blink, Wait#, Move_to
from constants import Colors, Params

# Constantes
COLOR, PARAMS = Colors(), Params()

class Page():
    def __init__ (self, screen, caption, bg_color: (int, int, int) = COLOR.WHITE, func = None):

        self.screen = screen
        # Estilização
        self.caption = caption
        self.bg_color = bg_color
        pygame.display.set_caption(self.caption)
        # Componentes
        self.components = []
        # Função herdada
        self.func = func

    def __str__(self):
        return self.__class__.__name__

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
        self.colors = None
        # Posicionamento
        self.margins = margins
        # Renderizado
        self.able = True
        self.rendered = None
        self.surface =  None
        # Animação
        self.animations = []
        # Eventos
        self.hover = None
        self.click = None
        self.keydown = None

    def set_margins(self, margins: [int, int]):
        self.margins = margins

    def set_size(self, size: str):
        self.size = size

    def set_hover(self, secondary: (int, int, int)):
        self.colors = [self.color, secondary]
        self.hover = True

    def set_click(self, func):
        self.click = func

    def set_keydown(self, func):
        self.keydown = func

    def set_margins_center(self):
        self.margins = [(PARAMS.WIDTH - self.size[0]) /2, (PARAMS.HEIGHT - self.size[1]) /2]

    def get_right(self):
        return self.margins[0] + self.size[0]

    def get_bottom(self):
        return self.margins[1] + self.size[1]

    def events(self, event: pygame.event):
        if self.able:
            pos = pygame.mouse.get_pos()
            if self.hover:
                self.color = self.colors[1] if self.rendered.collidepoint(pos) else self.colors[0]
            if self.click:
                if event.type == pygame.MOUSEBUTTONUP and self.rendered.collidepoint(pos):
                    self.click()
            if self.keydown:
                if event.type == pygame.KEYDOWN:
                    self.keydown(event)

    def set_blink(self, velocity: int = 12):
        self.animations.append(Blink(velocity))

    def set_wait(self, time: int, func):
        self.animations.append(Wait(time, func))

    #def move(self, x, y):
    #    self.margins[0] += x
    #    self.margins[1] += y

    #def set_move(self, time: int, x: int = None, y: int = None):
    #    self.animations.append(Move_to(time, x0=self.margins[0], x=x, y0=self.margins[1], y=y, func=self.move))

    def play(self):
        if self.able:
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

    def get_center(self) -> [int, int]:
        return [self.margins[0] + self.size[0] /2, self.margins[1] + self.size[1] /2]

    def get_rect_center(self):
        return self.rendered.get_rect(center=self.get_center())

    def render(self):
        self.surface = pygame.image.load(os.path.join(PARAMS.IMG_PATH, self.file)).convert_alpha()
        self.surface = pygame.transform.scale(self.surface, self.size)

    def draw(self):
        if self.able:
            self.rendered = self.screen.blit(self.surface, self.margins)
            self.play()

class Text(Component):
    def __init__(self, screen, txt: str, size_font: int, color: [int, int, int, float], bold: bool = False, size:int=0, margins=(0,0)):
        super().__init__(screen, size, margins)

        self.text = txt
        # Estilização
        self.size = size_font
        self.color = color
        self.font = None
        self.bold = bold

    def init(self):
        if self.bold:
            self.font = pygame.font.Font(os.path.join(PARAMS.FONT_PATH, "Inconsolata-Bold.ttf"), self.size)
        else:
            self.font = pygame.font.Font(os.path.join(PARAMS.FONT_PATH, "Inconsolata-Regular.ttf"), self.size)
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
        if self.able:
            self.surface = self.font.render('{}'.format(self.text), True, self.color)
            self.play()
            self.rendered = self.screen.blit(self.surface, self.margins)

class Box(Component):
    def __init__(self, screen, size, margins = (0, 0), color = COLOR.ORANGE, border_radius = 8):
        super().__init__(screen, size, margins)

        # Estilização
        self.color = color
        self.border_radius = border_radius

    def init(self):
        self.rendered = pygame.Rect(self.margins[0], self.margins[1], self.size[0], self.size[1])

    def get_center(self) -> [int, int]:
        return [self.margins[0] + self.size[0] /2, self.margins + self.size[1] /2]

    def draw(self):
        if self.able:
            self.surface = pygame.draw.rect(self.screen, self.color, self.rendered, border_radius=self.border_radius)
            self.play()

class Button(Component):
    def __init__(self,
                 screen,
                 label: str = None,
                 color_label: (int, int, int) = COLOR.BLUE_DARK,
                 size_label: int = 20,
                 size_box: (int, int) = (220, 75),
                 margin_box: (int, int) = (0,0),
                 color_box: (int, int, int) = COLOR.GREEN,
                 border_radius: int = 8,
                 src: str = None,
                 size_img: (int, int) =  (20, 20)
                ):
        super().__init__(screen, size_box, margin_box)

        self.box = Box(screen, size_box, margin_box, color=color_box, border_radius=border_radius)
        self.color_box = color_box
        self.label = Text(screen, label, size_label, color_label) if label else None
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
                self.box.margins[0] + (self.box.size[0] - self.label.size[0]) / 2,
                # y
                self.box.margins[1] + (self.box.size[1] - self.label.size[1]) / 2
            ))

    def set_hover(self, secondary_box: (int, int, int), secondary_label: (int, int, int) = None):
        self.box_colors = [self.color_box, secondary_box]
        self.label_colors = [self.color_label, secondary_label] if self.label else None
        self.hover = True

    def events(self, event: pygame.event):
        if self.able:
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
            if self.click:
                if event.type == pygame.MOUSEBUTTONUP and self.box.rendered.collidepoint(pos):
                    self.click()
            if self.keydown:
                if event.type == pygame.KEYDOWN:
                    self.keydown(event)

    def draw(self):
        if self.able:
            self.box.draw()
            self.label.draw() if self.label else None
            self.image.draw() if self.image else None
            self.play()

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

    def func_keydown(self, event):
        pass

    def init(self):
        # Título
        self.components.append(Text(self.screen, 'ALFA', 90, COLOR.BLUE_DARK))
        self.components[0].init()
        self.components[0].set_margins(((PARAMS.WIDTH - self.components[-1].size[0])/ 2, 50))
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


class Rank(Page):
    def __init__(self,screen, func, score: int, stage: str):
        super().__init__(screen, "FIM DE JOGO - ALFA", COLOR.WHITE, func)
        self.score = score
        self.stage = stage

    def func_to_menu(self, event = None):
        self.func(Menu_complete(self.screen, self.func))

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
