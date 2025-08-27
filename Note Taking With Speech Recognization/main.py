import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
from notion import NotionClient
from datetime import datetime
import parsedatetime as pdt
from Due import Due_Date as dd
from sounding import get_audio, audio_to_text, play_sound


r = sr.Recognizer()

ACTIVATION_COMMAND = "hello"

token = "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"

database_ID = "2294598c16938029a6fffb1e0be543fc"

#https://www.notion.so/2294598c16938029a6fffb1e0be543fc?v=2294598c1693803185e3000c8f558b1a&source=copy_link

client = NotionClient(token, database_ID)




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


if __name__ == "__main__":
    while True:
        play_sound("Speak your password now")
        a = get_audio()
        command = audio_to_text(a)
        print(command)

        if ACTIVATION_COMMAND in command.lower():
            print("Password accepted. Accessing the database...")
            play_sound("Password accepted. Accessing the database...")

            # Play greeting sound
            print("")
            play_sound("Please say One to create a new note and Two to read the existing note and Three to delete the note")

            note = get_audio()
            note = audio_to_text(note)

            if note:
                print(note)
                play_sound(note)

                # Save note in Notion
                now = datetime.now().astimezone().isoformat()

                #due date
                due_date = dd.get_due_date()

                res = client.create_page(note, now, due_date, status=True)
                
                if res.status_code == 200:
                    print("Stored new item successfully. ")
                    play_sound("Stored new item successfully.")
                else:
                    print(" Error Response:", res.text)
                    play_sound("There was an error saving the item.")

        elif "exit" in command.lower():
            print("Goodbye!")
            play_sound("Gooooodbye!")
            break

