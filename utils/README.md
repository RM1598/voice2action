# Voice2Action

Voice2Action is a prototype that helps users turn short spoken notes into structured dashboard entries. It supports local transcription and AI-based classification into tasks, calendar candidates, notes, or unclear items.

## Features

* direct voice recording in the interface
* audio upload fallback
* local speech-to-text transcription
* AI-based categorization into:

  * Task
  * Calendar
  * Note
  * Unclear
* editable review dashboard
* simulated export to calendar or notes
* uncertainty-aware feedback

## Tech Stack

* Python
* Streamlit
* Whisper
* Ollama with a local open-weight language model

## Setup

1. Clone or unzip the project folder.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Install Ollama.
5. Pull the model:

   ```bash
   ollama pull llama3
   ```

## Run

From the project folder, start the app with:

```bash
streamlit run app.py
```

## Notes

* short audio clips work best
* transcripts may contain recognition errors
* calendar and notes export are simulated in this prototype
