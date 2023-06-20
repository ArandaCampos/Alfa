from items import Image, Text, Page, Button
from constants import Colors, Params

# Constantes
COLOR = Colors()
PARAMS = Params()

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
