import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os 

r = sr.Recognizer()

def get_audio():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    return audio


def audio_to_text(audio):
    text = ""
    try:
        text = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")
        play_sound("Sorry, I couldn't understand what you said. Please try again.")
    except sr.RequestError:
        print("Could not request results from the API.")
    return text


def play_sound(text):
    try:
        tts = gTTS(text)
        tempfile = "./temp.mp3"
        tts.save(tempfile)
        playsound(tempfile)
        os.remove(tempfile)
    except Exception as e:
        print(f"Could not play the sound: {e}")
