import speech_recognition as sr
from gtts import gTTS
import os
import pyjokes
import wikipedia
import webbrowser
from pygame import mixer
from googletrans import Translator


def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1

        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except sr.UnknownValueError:
            speak("Sorry, I did not get that.")
        except sr.RequestError:
            speak("Sorry, the service is not available")
    return said.lower()


def speak(text: str):
    text = text.lower()
    translator = Translator()
    idioma = translator.detect(text)
    print(idioma)
    translated = translator.translate(text, src=idioma.lang, dest='pt')

    tts = gTTS(text=translated.text, lang='pt')
    filename = "voice.mp3"

    try:
        os.remove(filename)
    except OSError:
        pass
    tts.save(filename)
    playmusic(filename)


def respond(text):
    print("Text from get audio " + text)
    if 'youtube' in text:
        speak("O que você deseja buscar ?")
        keyword = get_audio()

        if keyword != '':
            url = f"https://www.youtube.com/results?search_query={keyword}"
            webbrowser.get().open(url)
            speak(f"Here is what I have found for {keyword} on youtube")

    elif 'busca' in text:
        speak("O que você gostaria de buscar na wikipedia ?")
        query = get_audio()

        if query != '':
            result = wikipedia.summary(query, sentences=3)
            speak("De acordo com a wikipedia")
            print(result)
            speak(result)

    elif 'piada' in text:
        speak(pyjokes.get_joke())

    elif 'play music' in text or 'play song' in text:
        speak("Now playing...")
        music_dir = "/home/keven/Cursos/Python/machine-learning-dio"
        songs = os.listdir(music_dir)
        print(songs)
        playmusic(music_dir + "/" + songs[2])

    elif 'stop music' in text:
        speak("Stopping playback.")
        stopmusic()

    elif 'exit' in text:
        speak("Goodbye, till next time")
        exit()


# play music
def playmusic(song):
    mixer.init()
    mixer.music.load(song)
    mixer.music.play()


# stop music
def stopmusic():
    mixer.music.stop()


while True:
    print("I am listening...")
    text = get_audio()
    respond(text)
