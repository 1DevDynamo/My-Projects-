import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import parsedatetime as pdt
from datetime import datetime
from sounding import get_audio, audio_to_text, play_sound

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



# Class: Handles natural language date parsing
class Due_Date:
    @staticmethod
    def get_due_date():
        print("State thy deadline, brave task-slayer! For example, July 9 2025 or tomorrow.")
        play_sound("State thy deadline, brave task-slayer! ")
        due_audio = get_audio()
        due_text = audio_to_text(due_audio)

        cal = pdt.Calendar()
        try:
            time_struct, _ = cal.parse(due_text)
            due_date = datetime(*time_struct[:6]).isoformat()
            print("Parsed due date:", due_date)
   
        except Exception as e:
            play_sound("Sorry, I couldn't understand the date. Setting to today.")
            print("Date parsing error:", e)
            due_date = datetime.now().isoformat()

        play_sound(f"The due date is set to {due_date[:10]}")
        print(f"The due date is set to {due_date[:10]}")
        return due_date
    

    
