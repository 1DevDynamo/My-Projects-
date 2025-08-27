import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
from notion import NotionClient
from datetime import datetime
import parsedatetime as pdt
from Due import Due_Date as dd
from dotenv import load_dotenv


r = sr.Recognizer()

ACTIVATION_COMMAND = "apple"

# Load environment variables
load_dotenv()
token = os.getenv("NOTION_TOKEN")
database_ID = os.getenv("NOTION_DATABASE_ID")

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
            print("Please say create, read, update, unmark or delete to manage your notes.")
            play_sound("Please say create, read, update, unmark or delete to manage your notes.")
            choice = get_audio()
            choice = audio_to_text(choice)
            print(f"You have choosen {choice}")
            
            # Create a new note

            if "create" in choice.lower():

                print("Creating a new note...")
                play_sound("Creating a new note...")
                print("Please say your note")
                play_sound("Please say your note")

                note = get_audio()
                note = audio_to_text(note)

                if note:
                    print(note)
                    play_sound(note)

                    # Save note in Notion
                    now = datetime.now().astimezone().isoformat()

                    #due date
                    due_date = dd.get_due_date()

                    res = client.create_page(note, now, due_date, status=False)

                    # Status_code check
                    if res.status_code == 200:
                        print("Stored new item successfully. ")
                        play_sound("Stored new item successfully.")
                    else:
                        print(" Error Response:", res.text)
                        play_sound("There was an error saving the item.")


            # Read an existing note
         
            elif "read" in choice.lower():
                pages = client.read_page()
                print("Reading existing notes...")
                play_sound("Reading existing notes...")

                if pages:
                    for i, page in enumerate(pages,start=1):
                        props = page["properties"]

                        #Description
                        title = props.get("Description", {}).get("title", [{}])[0].get("text", {}).get("content", "No Title")

                        #Dates
                        date = props.get("Date", {}).get("date", {})
                        start_date = date.get("start", "No Date")

                        #DueDate
                        due = props.get("Due Date", {}).get("date", {})
                        due_date = due.get("start", "No Due Date")

                        # Stauts
                        status_checked = props.get("Status", {}).get("checkbox", False)
                        status_text = "checked" if status_checked else "unchecked"

                        # Print
                        print(f"{i}. {title} - Due: {due_date} - Status: {status_text}")
                        play_sound(f"Task {i}: {title}, due on {due_date[:10]}, and status is {status_text}.")

                    print("Read all notes successfully. ")
                    play_sound("Read all notes successfully.")
    
                else:
                    print("No notes found.")
                    play_sound("No notes found.")
            

            # Update an existing note

            elif "update" in choice.lower() or "unmark" in choice.lower():
                pages = client.read_page()
                print("Updating existing notes...")
                play_sound("Updating existing notes...")

                if not pages:
                    print("No notes found.")
                    play_sound("No notes found.")
                    continue
                
                # Extract task number and action (done/undone)
                words = choice.lower().split()
                task_num = None
                mark_done = "unmark" not in words

                for i, word in enumerate(words,start=1):
                    if word.isdigit():
                        task_num = int(word)
                        break

                if task_num is None or task_num > len(pages) or task_num < 1:
                    print("Invalid task number.")
                    play_sound("Invalid task number.")
                    continue

                page = pages[task_num - 1]
                page_id = page["id"]
                
                status = True if mark_done else False
                res = client.update_page(page_id, status)

                if res.status_code == 200:
                    print("Updated successfully.")
                    play_sound("Updated successfully.")
                else:
                    print("Error updating status:", res.text)
                    play_sound("Error updating status.")

            
            # Delete an existing note

            elif "delete" in choice.lower() or "remove" in choice.lower():
                pages = client.read_page()
                print("Deleting existing notes...")
                play_sound("Deleting existing notes...")

                if not pages:
                    print("No notes found.")
                    play_sound("No notes found.")
                    continue

                # Extract task number
                words = choice.lower().split()
                task_num = None
                for word in words:
                    if word.isdigit():
                        task_num = int(word)
                        break
                if task_num is None or task_num > len(pages) or task_num < 1:
                    print("Invalid task number.")
                    play_sound("Invalid task number.")
                    continue
                
                page = pages[task_num - 1]
                page_id = page["id"]
                
                res = client.delete_page(page_id)

                if res.status_code == 200:
                    print("Task deleted successfully.")
                    play_sound("Task deleted successfully.")
                else:
                    print("Failed to delete task:", res.text)
                    play_sound("Failed to delete task.")

            else:
                print("Sorry, I didn't understand.")
                play_sound("Sorry, I didn't understand.")
                continue

        elif "exit" in command.lower():
            print("Goodbye!")
            play_sound("Gooooodbye!")
            break

