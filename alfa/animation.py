from time import sleep

def blink(alfa, velocity = 20):
    print('Entrou + ' + str(alfa))
    if alfa > 10:
        return alfa - velocity
    return 255
