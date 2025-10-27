# Speech-to-Text Dashboard (milestone_3)

A small Streamlit app that demonstrates live audio capture (webrtc), simple processing placeholders (transcription / diarization / summary), and export/copy of results.

This README covers quick setup and how to run the app.

## Features

- Single Start / Stop toggle for live recording (webrtc).
- Upload audio file and process it (demo placeholder).
- Outputs: Transcription, Speaker-diarized text, and Summarized notes.
- Download results as plain text files.
- Copy-to-clipboard button (uses browser clipboard API) with a browser alert on success or failure.

## Prerequisites

- Python 3.8+ installed
- Microphone access for live recording
- A modern browser (Chrome/Edge/Firefox) that supports navigator.clipboard for the copy button

## Quick start (Windows PowerShell)

```powershell
# 1) Clone the repo (if you haven't already)
git clone https://github.com/Speech-Summarizer-Application-IF-SB/Sonal-Verma.git
cd Sonal-Verma

# 2) Create and activate a virtual environment
python -m venv .venv
. .venv\Scripts\Activate.ps1

# 3) Install dependencies (recommended)
pip install -r requirements.txt
# If you prefer to install only what is needed for this app:
# pip install streamlit streamlit-webrtc

# 4) Run the Streamlit app
streamlit run milestone_3/app.py
```

## Quick start (macOS / Linux)

```bash
# 1) Clone the repo
git clone https://github.com/Speech-Summarizer-Application-IF-SB/Sonal-Verma.git
cd Sonal-Verma

# 2) Create & activate venv
python3 -m venv .venv
source .venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Run the app
streamlit run milestone_3/app.py
```

## How to use

1. Open the app in your browser once Streamlit starts.
2. Choose `🎙️ Live Recording` to use the Start/Stop toggle:
   - Click the button to "▶️ Start Recording" — This will show the recorder widget.
   - Click the same button (now labeled "⏹️ Stop Recording") to stop recording and trigger the (demo) processing steps.
3. Alternatively select `📁 Upload Audio File` and upload a `.wav`, `.mp3`, or `.m4a` file, then click `🚀 Process Audio`.
4. View results in the Output tabs. Use the `⬇️ Download` button to download text files. Click the `📋 Copy` button to copy text to the clipboard — a browser alert will confirm success.

