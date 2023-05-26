from gtts import gTTS
from playsound import playsound

def read_word(word: str):
    """
        Carrega o texto digitado no campo '' e
        o salva em portugês-Brasil no 'audio.mp3'
    """

    tts = gTTS(word, lang='pt', tld="com.br")
    tts.save("audio.mp3")
    speech_word()

def speech_word():
    """
        Toca o arquivo 'audio.mp3'
    """

    playsound("audio.mp3")
