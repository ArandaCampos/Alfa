# ------------------------------------
#   Author: Renan Campos
#   Github: github.com/ArandaCampos
#
#   ALFA
#
#   - Falta:
#       - Transferir parâmetros imutáveis para as Class
#               - Manter aqui: instância dos objetos e as posições
#       - Página inicial
#       - Página de ranqueamento
#--------------------------------------

import pygame
import os
import random
import csv
from read_word import read_word
from toggle_letter import Toggle_letter
from components import Button_cancel, Button_send, Score, Sound, Figure

# Carregar diretório "Images"
ABS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
IMG_PATH = os.path.join(ABS_PATH, 'Images')
AUDIO_PATH = os.path.join(ABS_PATH, 'Audio')

# Paleta de cores
BG_COLOR, ORANGE, WHITE, BLUE = (222, 239, 231, .94), (250, 127, 8, .98), (240, 240, 242, .95), (1, 32, 48, 1.)
ORANGE_LIGHT, GREEN_LIGHT = (242, 68, 5, 1.), (154, 235, 163, 1.)

# Altura e largura da tela
HEIGHT, WIDTH = 648, 800

DATA = []

# carregar dados do jogo
def loading_data(file_data):
    with open(file_data, newline='') as csvfile:
        text = csv.reader(csvfile, delimiter=' ')
        for words in text:
            DATA.append(words)

class Window():
    pygame.init()
    def __init__(self,
                 option: (str),
                ):
        # Parâmetros de aparência
        self.size = (WIDTH, HEIGHT)
        self.bg_color = BG_COLOR
        self.title = 'ALFA'

        self.sound = None
        self.score_board = None
        self.button_cancel = None
        self.button_send = None
        self.word = None
        self.figure = None
        self.sound_win = pygame.mixer.Sound(os.path.join(AUDIO_PATH, 'win.wav'))
        self.sound_fail = pygame.mixer.Sound(os.path.join(AUDIO_PATH, 'failed.wav'))

        # Caixa de resposta
#        self.box = None
#        self.color_box = WHITE
#        self.padding_box = 10
#        self.margin_left_box = 0
#        self.margin_top_box = 0
#        self.size_box = [0, 80]
#        self.border_radius_box = 12

        # Parâmetros do jogo
        self.screen = None
        self.play = True
        self.score = 0

        # Gabarito da rodada
        self.round = 0
        self.score = 0
        self.option = option
        self.value = 0
        self.answer = None


    def init(self):
        """
            Inicializa:
                Tamanho
                Título
                Icones
                Imagem
        """
        # self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.screen = pygame.display.set_mode(self.size)
        self.shuffle_data()
        self.load_word()
        self.load_sound()
        self.load_score()
        self.load_btn_cancel()
        self.load_btn_send()
        pygame.display.set_caption(self.title)

    def shuffle_data(self):
        random.shuffle(DATA)

    def next_round(self):
        self.round = self.round + 1 if self.round < len(DATA) - 1 else 0
        self.load_word()
        self.load_sound()

    def load_word(self):
        file, word, answer = DATA[self.round]
        self.word = Toggle_letter(self.screen, word, self.option, answer)
        self.word.init()
        self.figure = Figure(self.screen, file)
        self.figure.init()

    def load_sound(self):
        self.sound = Sound(self.screen, "sound.png", [self.word.margins[0][0] + self.word.size[0], 390 + self.word.size[1] / 2])
        self.sound.init()

    def load_score(self):
        self.score_board = Score(self.screen)
        self.score_board.init()

    def load_btn_cancel(self):
        #Botão Cancel
        self.button_cancel = Button_cancel(self.screen)
        self.button_cancel.init()

    def load_btn_send(self):
        self.button_send = Button_send(self.screen)
        self.button_send.init()

    def refresh_screen(self):
        self.screen.fill(self.bg_color)
        self.button_cancel.draw() if self.button_cancel else None
        self.button_send.draw() if self.button_send else None
        self.word.draw() if self.word else None
        self.score_board.draw() if self.score_board else None
        self.figure.draw() if self.figure else None
        self.sound.draw() if self.sound else None
        pygame.display.flip()

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.play = False
            # Comando de botão
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.word.toggle_value(increment=True)
                elif event.key == pygame.K_DOWN:
                    self.word.toggle_value(decrement=True)
                elif event.key == pygame.K_RIGHT:
                    self.word.toggle_key(increment=True)
                elif event.key == pygame.K_LEFT:
                    self.word.toggle_key(decrement=True)
                elif event.key == pygame.K_RETURN:
                    if self.word.response():
                        self.sound_win.play()
                        self.score_board.update(increment=True)
                    else:
                        self.sound_fail.play()
                    self.next_round()
                else:
                    self.word.toggle_value(letter=event.unicode)
            # Comandos de mouse
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.sound.image.rendered.get_rect(center=self.sound.image.get_center()).collidepoint(pygame.mouse.get_pos()):
                    read_word(self.word.get_word())
                elif self.button_send.button.rendered.collidepoint(pygame.mouse.get_pos()):
                    if self.word.response():
                        self.sound_win.play()
                        self.score_board.update(increment=True)
                    else:
                        self.sound_fail.play()
                    self.next_round()
                elif self.button_cancel.button.rendered.collidepoint(pygame.mouse.get_pos()):
                    self.sound_fail.play()
                    self.next_round()

    def exit(self):
        pygame.quit()

def run(window):
    clock = pygame.time.Clock()

    while window.play:
        clock.tick(40)

        window.refresh_screen()
        window.get_event()

    window.exit()

if __name__ == '__main__':
    stage = 0
    stages = (1, 2, 3, 4, 5)
    option = (('A', 'E', 'I', 'O', 'U'),
              ('BA', 'BE', 'BI', 'BO', 'BU'))

    file_names = ['data.csv', 'data_b.csv']
    print(" ############ ALFABETIZAÇÃO ############ \n\n 1) Vogais \n 2) Letra B\n")
    while stage not in stages:
        stage = int(input(" Opção: "))
    file_data = file_names[stage - 1]

    loading_data(file_data)
    window = Window(option = option[stage - 1])
    window.init()
    run(window)
