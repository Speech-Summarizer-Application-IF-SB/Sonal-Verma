# Speech-to-Text Dashboard (milestone_3)

A small Streamlit app that demonstrates live audio capture (webrtc), simple processing placeholders (transcription / diarization / summary), and export/copy of results.

This app was built as a demonstration of a lightweight browser-based workflow for capturing audio, running speech processing steps, and surfacing human-friendly outputs. It intentionally uses simple UI patterns so developers can quickly replace the placeholder processing steps with production-grade models or services.

Key goals:
- Keep the UI minimal so experiments with ASR and diarization are easy to iterate.
- Show how to combine live capture (webrtc) and file upload modes in the same app.
- Provide simple export and clipboard interactions so outputs can be shared or used in other tools.


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
## How to use

1. Open the app in your browser once Streamlit starts.
2. Choose `🎙️ Live Recording` to use the Start/Stop toggle:
   - Click the button to "▶️ Start Recording" — This will show the recorder widget.
   - Click the same button (now labeled "⏹️ Stop Recording") to stop recording and trigger the (demo) processing steps.
3. Alternatively select `📁 Upload Audio File` and upload a `.wav`, `.mp3`, or `.m4a` file, then click `🚀 Process Audio`.
4. View results in the Output tabs. Use the `⬇️ Download` button to download text files. Click the `📋 Copy` button to copy text to the clipboard — a browser alert will confirm success.


## Credits & acknowledgements

- Author / repository: Speech Summarizer Application — Sonal Verma (Speech-Summarizer-Application-IF-SB / Sonal-Verma)
- UI & live capture: Streamlit and the `streamlit-webrtc` community package.
- Processing and model ideas: Hugging Face `transformers`, `pyannote.audio`, and Whisper / community implementations such as `faster-whisper` inspired parts of the project.
- Thank you to the open-source maintainers whose libraries make quick prototyping like this possible.

If you want, I can now either (a) replace the placeholder processing with a small working ASR pipeline (CPU-friendly) or (b) add a short credits/attribution file under `docs/` — tell me which you prefer.

