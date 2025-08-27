# **Vocal CRUDing Notion**

A voice-activated task management system built in **Python** that uses **speech recognition** and **text-to-speech (TTS)** to interact with the user. The system integrates with the **Notion API** to store and manage tasks with due dates.

---

## ✅ **Features**
- 🎙 **Voice Commands**: Create, read, update, delete tasks using speech.
- 🗓 **Due Date Parsing**: Extract due dates from natural language.
- 🔗 **Notion API Integration**: Store and manage tasks in your Notion workspace.
- 🔐 **Secure Credentials**: Environment variables for API token and database ID.
- 🗣 **Text-to-Speech Feedback**: Confirms actions via audio output.
- 📋 **Task Management**:
  - **Create** new tasks.
  - **Read** all existing tasks.
  - **Update** task status (mark as done/undone).
  - **Delete** tasks by voice command.

---

## 🛠 **Tech Stack**
- **Python 3.x**
- **Libraries**:
  - `speechrecognition` – Speech to text.
  - `gtts` – Text-to-speech conversion.
  - `playsound` – Audio playback.
  - `requests` – API communication.
  - `parsedatetime` – Natural language date parsing.
  - `dotenv` – Securely load environment variables.
- **API**: [Notion API](https://developers.notion.com)

---

## 📂 **Project Structure**

