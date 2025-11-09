# Milestone 2 — Whisper Speech-to-Text (faster-whisper)

Simple speech-to-text utilities powered by faster-whisper:
- Download and transcribe audio from YouTube videos
- Transcribe local audio files
- Transcribe from the microphone in (near) real-time
- Compare your transcription against a reference using WER/CER

## 📂 Project Structure

```
milestone_2/
├── usingfilemodel.py           # Download YouTube audio & transcribe
├── realtimemodel.py            # Real-time microphone transcription
├── report.py                   # Evaluate transcription quality (WER/CER)
├── transcription_sm.txt        # Sample hypothesis transcript
├── youtube_transcription.txt   # Sample reference transcript
├── report.txt                  # Sample evaluation output
├── wer_report.txt             # Detailed WER/CER metrics report
└── read.md                     # This documentation file
```

## File overview
- `realtimemodel.py` — Script intended to run the realtime model (live or streaming inference). Check the top of the file for any configurable options (device, model path, etc.).
- `usingfilemodel.py` — Script to run inference on an existing audio file or on stored text inputs. Use this when you have an audio file to transcribe.
- `report.py` — Small utility to calculate / summarize evaluation metrics (for example WER). It reads the model output and reference transcripts and writes `wer_report.txt`.
- `transcription_sm.txt` — Sample transcription produced by the model (artifact).
- `youtube_transcription.txt` — Sample transcription extracted from a YouTube source.
- `wer_report.txt` — Example output produced by `report.py` with Word Error Rate (WER) and other simple stats.

## Quick start (Windows PowerShell)

```powershell
# 1) Clone the repository
git clone https://github.com/Speech-Summarizer-Application-IF-SB/Sonal-Verma.git
cd Sonal-Verma

# 2) Create & activate a virtual environment
python -m venv .venv
. .venv\Scripts\Activate.ps1

# 3) Install dependencies
pip install -r requirements.txt

# 4) Navigate to milestone_2
cd milestone_2

```

Now you're ready to run any of the milestone_2 scripts from this directory.

Note: If you want to install only packages needed for Milestone 2, inspect imports at the top of `realtimemodel.py`, `usingfilemodel.py` and `report.py` and install them individually.

## How to run

General guidance — scripts are Python programs that may accept arguments or require you to edit a few constants at the top. If a script includes an argument parser, run it with `-h` or `--help` to see options.

Examples (adjust paths / options as needed):

Transcribe a local audio file (example):

```powershell
python milestone_2\usingfilemodel.py --input "path\to\audio.wav" --output "out_transcription.txt"
```

Run the realtime model (if supported by your environment):

```powershell
python milestone_2\realtimemodel.py
```

Generate an evaluation / WER report from an output and a reference:

```powershell
python milestone_2\report.py --pred predicted_transcript.txt --ref reference_transcript.txt --out wer_report.txt
```

If these scripts do not expose CLI flags, open the script and set the input/output file paths near the top where constants are defined. The code usually contains clear variable names like `INPUT_PATH` or `OUTPUT_FILE`.

## Expected outputs
- Transcribed text files (plain `.txt`).
- `wer_report.txt` with WER and simple summary statistics.

## Common troubleshooting
- Make sure the virtual environment is activated and dependencies are installed.
- If GPU/torch errors appear, ensure PyTorch is installed for your CUDA / CPU environment (see https://pytorch.org/get-started/locally/).
- If audio decoding fails, confirm `ffmpeg` is installed and available on PATH (or use packages that bundle audio decoders). On Windows, add `ffmpeg\bin` to your PATH.
- For missing model files or weights, check the code comments — some scripts expect a local model file or will download a model at first run (this requires internet).

## Edge cases to consider
- Empty or very short audio files — may produce empty or low-quality transcripts.
- Different audio sampling rates — resampling may be necessary before inference.
- Long audio files — some models require chunking to avoid out-of-memory errors.
 
### Libraries & tools
This project uses (or can use) several open-source libraries and tools for audio processing, modeling and evaluation. Examples include:

- PyTorch — deep learning framework for model training and inference.
- OpenAI Whisper (or similar ASR models) — for speech-to-text transcription.
- librosa, soundfile — audio I/O and feature utilities.
- ffmpeg — audio decoding and format conversion.
- pytube or youtube-dl — for downloading YouTube audio when needed.
- jiwer — Word Error Rate (WER) calculation and other simple metrics.
- numpy, scipy, pandas — common scientific and data utilities.

If your environment uses different libraries, update this section to reflect the exact dependencies present in `requirements.txt`.

### Data sources and third-party models
- Example transcriptions in this folder (`youtube_transcription.txt`, `transcription_sm.txt`) are artifacts or examples and may originate from public audio sources.
- Any pre-trained models used may be distributed under their own licenses; check the model provider's terms of use before redistribution.