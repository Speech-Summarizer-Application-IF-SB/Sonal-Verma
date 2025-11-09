# Milestones — AI Meeting Summarizer

## 🧩 Project Overview

The AI Live Meeting Summarizer is a multi-milestone, end-to-end application designed to automate the entire meeting analysis workflow — from raw audio to structured summaries. It processes uploaded or live-recorded meeting audio by cleaning it, transcribing speech with Whisper (via Faster Whisper), identifying speakers using Pyannote.ai diarization, merging speaker segments with their spoken text, and generating concise summaries using Facebook BART or other transformer-based models.

The system is built with a modular architecture, allowing each stage — audio cleaning, speech-to-text, diarization, transcript merging, and summarization — to be tested and executed independently.
A Streamlit dashboard provides an interactive interface for real-time experimentation, result visualization, and seamless integration of all components.

#### Key Highlights:

- 🎙️ Real-time or uploaded meeting transcription
- 🧠 Speaker diarization with Pyannote.ai
- 🪄 AI-powered summarization using transformer models
- 🧰 Modular, milestone-based pipeline for independent testing
- 🖥️ Intuitive Streamlit frontend for easy control and visualization

Tech Stack:
`Streamlit` · `Faster Whisper` · `Pyannote.audio` · `Transformers (BART)` · `Torch` · `Librosa` · `SoundFile`

## Quick Start (Windows PowerShell)

###### 1. Clone the repository and change directory:

```git
git clone https://github.com/Speech-Summarizer-Application-IF-SB/Sonal-Verma.git
cd Sonal-Verma
```

###### 2. Create and activate a virtual environment:
```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
```
###### 3. Install dependencies:
```p
   pip install -r requirements.txt
```
###### 4. Run the Streamlit dashboard (web UI):
```powershell
   streamlit run dashboard.py
```
   The dashboard lets you upload or record audio and runs the same pipeline in a temporary
   directory, returning Transcription, Diarized Transcript, and Summary in the UI.

###### 5. Optional: Run the command-line pipeline (example):
```p
   python main.py
```

This will prompt for a path to an audio file and run the full pipeline writing files to
   `processed_audio/`.

Notes:
- Make sure `ffmpeg` is installed and available on PATH for audio conversion where needed.
- For diarization you must set a pyannote API key (see Environment Variables).

## Project Layout (high level)

- `main.py` — Orchestrates the 5-step pipeline (clean → transcribe → diarize → merge → summarize).
- `dashboard.py` — Streamlit UI wrapper that calls functions in `main.py`.
- `milestone_1/audio_cleaner.py` — Preprocessing: resampling, mono conversion, noise reduction,
  and normalization.
- `milestone_2/usingfilemodel.py` — Uses Faster Whisper to transcribe audio into time-stamped segments.
- `milestone_4/dairization.py` — Polls the pyannote.ai job for diarization results (by job id).
- `milestone_4/getJobId.py` — (not documented here — expected to create a diarization job and return its id).
- `milestone_4/merge.py` — Aligns transcription segments with diarization timestamps and writes
  a speaker-attributed transcript.
- `milestone_4/summarizer.py` — Splits long transcripts into overlapping chunks and runs a
  Transformers summarization pipeline (default: `facebook/bart-large-cnn`).

## How the model(s) are built and used

1. Transcription — Faster Whisper
   - The code uses the `faster_whisper` wrapper to load an offline Whisper model (`small.en` by default).
   - `milestone_2/usingfilemodel.py` loads audio, runs `model.transcribe(...)`, and formats each
     segment into a JSON-friendly structure: id, start, end, text.
   - Output: `text`, `duration`, `segments` (list of time-stamped segments).

2. Diarization — pyannote.ai (remote API)
   - The pipeline uploads audio (via `getJobId`) and polls the pyannote API for job status
     (see `milestone_4/dairization.py`). When the job finishes, the code extracts `diarization`
     from the API's `output` field.
   - Output: a list of speaker segments: objects with `speaker`, `start`, `end` fields.

3. Merge — simple overlap/nearest mapping
   - `milestone_4/merge.py` computes intersection between each transcript segment and diarization
     segments and assigns the speaker with the largest overlap (or `Unknown` if none).
   - Writes a simple text file where every transcript segment is prefixed with `[SpeakerX] : ...`.

4. Summarization — Hugging Face Transformers
   - `milestone_4/summarizer.py` splits the (potentially long) transcript into chunks with a
     configurable overlap, then runs a `pipeline('summarization', model=...)` over each chunk and
     concatenates the chunk summaries into a final summary.

## Tech stack and libraries

- Python 3.8+ (tested) — primary language
- Audio processing: `librosa`, `pydub`, `soundfile`, `sounddevice`, `noisereduce`
- Speech recognition: `faster_whisper` (Whisper model runner)
- YouTube audio download (optional): `yt-dlp`
- Speaker diarization: remote `pyannote.ai` API (HTTP requests)
- Summarization / NLP: `transformers` pipeline (`facebook/bart-large-cnn` by default)
- Data handling: `pandas`, `numpy`
- CLI/UX: `tqdm` for progress bars
- Web UI: `streamlit` (dashboard.py)

## Environment variables and external services

- PYANNOTE_API_KEY — required to call pyannote.ai for diarization (used in `main.py` / `dairization.py`).
- Before running the project, set your Pyannote API key as an environment variable:
🪟 Windows (PowerShell)
```p
$env:PYANNOTE_API_KEY = "your_api_key_here"
```
🍎 macOS / 🐧 Linux
```p
export PYANNOTE_API_KEY="your_api_key_here"
```
- Large model downloads — transcription and summarization models will be downloaded the first time
  they are used. Make sure you have sufficient disk space and a network connection.

## Example outputs and file locations

- `processed_audio/` (created by `main.py`) contains:
  - `file_cleaned.wav` — cleaned audio
  - `transcript.txt` — joined transcript text
  - `transcription.json` — transcript metadata with `segments`
  - `diarization.json` — diarization output (list of speaker segments)
  - `diarized_transcript.txt` — speaker-attributed transcript
  - `final_summary.txt` — summary generated by the summarization pipeline

### Core Functionality & Workflow

The application pipeline consists of five main stages:

1) Audio Cleaning (Preprocessing)
   - Removes background noise, normalizes volume, and resamples audio to 16 kHz (ASR-friendly).
   - Implemented in `milestone_1/audio_cleaner.py` using `librosa`, `noisereduce`, and `pydub`.
   - Input modes: live microphone recording (via `sounddevice`) or uploaded file.
   - Output: cleaned, mono `.wav` file.

2) Speech-to-Text (STT) Transcription
   - Uses Whisper models through the `faster_whisper` wrapper (`milestone_2/usingfilemodel.py`).
   - Supports file-based transcription (and has hooks to support real-time modes).
   - Produces timestamped JSON segments plus a joined raw text file.
   - WER is measured using `jiwer` in `milestone_2/report.py`.

3) Speaker Diarization
   - Uses pyannote.ai remote API to identify who spoke when.
   - Upload + job creation handled in `milestone_4/getJobId.py`; job polling and output retrieval
     are in `milestone_4/dairization.py`.

4) Transcript Merging
   - Aligns speaker segments with STT segments using timestamp overlap logic (`milestone_4/merge.py`).
   - Result: `diarized_transcript.txt` where each segment is prefixed with a speaker label.

5) Summarization
   - Uses Hugging Face `transformers` summarization pipeline (`milestone_4/summarizer.py`).
   - Splits long transcripts into overlapping chunks and summarizes each chunk, then combines
     chunk summaries into a final human-readable meeting summary.

### Independent Module Testing

Each milestone can be executed and tested independently. This makes debugging easier and allows
you to validate intermediate outputs (cleaned audio, raw transcript, diarization JSON, merged
transcript, and summary).

Milestone | Functionality | Test / Script | Evaluation
---|---:|---|---
Milestone 1 | Audio Cleaning | `milestone_1/audio_cleaner.py` | Clean waveform checks (manual / visual)
Milestone 2 | STT Transcription | `milestone_2/usingfilemodel.py` + `milestone_2/report.py` | WER (target < 0.15)
Milestone 3 | Streamlit UI | `app.py` / `dashboard.py` | Manual UI tests
Milestone 4 | Diarization & Summarization | `milestone_4/getJobId.py`, `milestone_4/dairization.py`, `milestone_4/merge.py`, `milestone_4/summarizer.py` | manual test

## Self-testing features (how to test locally)

This section explains how you (or CI) can exercise individual components and measure quality.

1) Quick smoke tests (run components individually)

   - Audio cleaning (CLI):

     ```powershell
     python milestone_1/audio_cleaner.py
     # follow prompts to use 'file' or 'live'
     ```

   - Transcription (file-based):

     ```powershell
     # Ensure you have an audio file named 'video_audio.wav' or update the code call
     python -c "from milestone_2.usingfilemodel import modelCall; print(modelCall('processed_audio/file_cleaned.wav'))"
     ```

   - Diarization + upload test (pyannote):

     ```powershell
     # Set API key first
     $env:PYANNOTE_API_KEY = 'your_key_here'

     # Use main pipeline (recommended) which calls getJobId and polls for diarization
     python main.py
     ```

   - Merge and summarization (run via `main.py` or call the functions directly):

     ```powershell
     python main.py
     # or call summarize directly from a REPL
     python -c "from milestone_4.summarizer import summarize_large_text; print(summarize_large_text('processed_audio/diarized_transcript.txt'))"
     ```

2) Evaluation: compute WER, CER (jiwer) and save a report

   - `milestone_2/report.py` compares two transcription files (`transcription_sm.txt` and
     `youtube_transcription.txt` by default). To use it:

     - Place a reference transcript at `milestone_2/youtube_transcription.txt` (ground truth).
     - Place your generated transcript at `milestone_2/transcription_sm.txt` (or update paths in file).
     - Run:

       ```powershell
       python milestone_2/report.py
       ```

     - Output: `wer_report.txt` with WER, MER, WIL, WIP, substitutions, insertions, deletions, CER.

3) Diarization job checks

   - `milestone_4/getJobId.py` performs a three-step flow: request pre-signed upload URL, upload
     audio, and create a diarization job. Use it indirectly via `main.py` or call the function in a
     small Python snippet after setting `PYANNOTE_API_KEY`.

   - `milestone_4/dairization.py` polls the job until it is `succeeded` and returns the diarization
     output. You can test the poller with a known jobId (if you have one) to verify parsing logic.

### Deliverables & Features Checklist ✅ 

- Real-time audio capture and STT — implemented via `dashboard.py` and `milestone_1`.
- Accurate diarization using Pyannote — implemented as remote API flow in `milestone_4`.
- Transformer-based summarization — implemented in `milestone_4/summarizer.py` (BART by default).
- Streamlit UI with status updates — `dashboard.py`.
- WER report generation — `milestone_2/report.py`.

----

## Credits

Thanks and credits to the open-source projects, research teams, and community contributors
whose work this project builds upon:

- Repository / Maintainers: Speech-Summarizer-Application-IF-SB / `Sonal-Verma`
- Speech recognition and model research: OpenAI (Whisper family)
- Transcription tooling: `faster_whisper` (efficient Whisper runtime)
- Speaker diarization: `pyannote.audio` and the pyannote.ai service
- Summarization & NLP: Hugging Face `transformers` (BART and other models)
- Audio processing and utilities: `librosa`, `pydub`, `soundfile`, `sounddevice`, `noisereduce`
- Download and media handling: `yt-dlp`, `ffmpeg`
- Evaluation and metrics: `jiwer` (WER calculation), ROUGE tooling
- Data and helpers: `pandas`, `numpy`, `tqdm`, `requests`, `pytest`, `streamlit`

Special thanks to the research and open-source communities for model weights, tutorials,
and issue support that made development and testing possible. If you'd like to provide a
more detailed contributors list (individual authors or institutions), I can add a
`CONTRIBUTORS.md` and link to it from here.

License: see the `LICENSE` file in the repository root.
