import pygame, os
pygame.init()

class Colors():
    def __init__(self):

        self.BLUE = pygame.Color('#1FB4FF')
        self.BLUE_DARK = pygame.Color('#012030')

        self.GREEN = pygame.Color('#9AEBA3')
        self.GREEN_DARK = pygame.Color('#599E61')

        self.RED = pygame.Color('#FD4542')
        self.RED_DARK = pygame.Color('#D93B38')

        self.ORANGE = pygame.Color('#FF5A1F')
        self.ORANGE_DARK = pygame.Color('#F24405')

        self.BLACK = pygame.Color('#8AA699')
        self.WHITE = pygame.Color('#E1F2EA')

class Params():
    def __init__(self):
        # Diretórios
        self.ABS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
        self.DATA_PATH = os.path.join(self.ABS_PATH, 'data')
        self.AUD_PATH = os.path.join(self.DATA_PATH, 'Audio')
        self.IMG_PATH = os.path.join(self.DATA_PATH, 'Images')
        self.FONT_PATH = os.path.join(self.DATA_PATH, 'Fonts')
        # Áudio carregados
        self.SOUND_WIN = pygame.mixer.Sound(os.path.join(self.AUD_PATH, 'win.wav'))
        self.SOUND_FAIL = pygame.mixer.Sound(os.path.join(self.AUD_PATH, 'failed.wav'))
        self.SOUND_READ = pygame.mixer.Sound('audio.mp3')
        # Parâmetros do jogo
        self.HEIGHT = 648
        self.WIDTH = 1000
        self.FPS = 60
