import parsedatetime as pdt
from datetime import datetime
from sounding import get_audio, audio_to_text, play_sound

# Class: Handles natural language date parsing
class Due_Date:
    @staticmethod
    def get_due_date():
        print("State thy deadline, brave task-slayer! For example, July 9 2025 or tomorrow.")
        play_sound("State thy deadline, brave task-slayer!")
        
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
