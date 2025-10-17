# Whisper Speech-to-Text (faster-whisper)

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

## What's here

- `usingfilemodel.py` — Download audio from YouTube and transcribe it using faster-whisper. Saves transcription to `transcription_sm.txt`.
- `realtimemodel.py` — Stream from your microphone and print live transcriptions in real-time.
- `report.py` — Compute word/character error metrics between two text files and save a formatted report to `wer_report.txt`.
- `transcription_sm.txt`, `youtube_transcription.txt` — Example hypothesis/reference transcripts used for evaluation.
- `report.txt`, `wer_report.txt` — Example evaluation outputs.

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

# 5) Run the scripts (examples below)
```

Now you're ready to run any of the milestone_2 scripts from this directory.

## 1) Download YouTube audio and transcribe

`usingfilemodel.py` downloads audio from a YouTube video using yt-dlp and transcribes it with faster-whisper.

```powershell
python usingfilemodel.py
```

**What it does:**
- Downloads audio from the YouTube URL specified in the script (default: `https://www.youtube.com/watch?v=IYtDS27znnM`)
- Converts it to WAV format (`video_audio.wav`)
- Transcribes using the Whisper model
- Saves the full transcription to `transcription_sm.txt`

**To use your own YouTube video:**
Edit `usingfilemodel.py` and change the `video_url` variable:
```python
video_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

**Model customization:**
- `model_size = "small.en"` — choose a different model size (e.g., `tiny`, `base`, `small`, `medium`, `large-v3`, or language-specific variants like `small.en`)
- `beam_size=5` in the `transcribe()` call — adjust for speed vs accuracy tradeoff

**Note:** This requires `yt-dlp` and `ffmpeg` to be installed. Make sure ffmpeg is in your system PATH.

## 2) Real-time microphone transcription

`realtimemodel.py` captures audio chunks from the microphone and prints recognized text every second.

```powershell
python realtimemodel.py
```

Notes:
- Stop with Ctrl+C.
- Defaults: `sample_rate = 16000`, `block_duration = 1.0s` (accumulate), `chunk_duration = 0.1s` (capture granularity), mono (`channels = 1`).
- If you see audio device errors, try a different input device or sample rate in the `sd.InputStream(...)` call.

## 3) Evaluate transcription quality (WER/CER)

`report.py` compares two text files and writes a clean report to `wer_report.txt`.

By default it expects:
- Hypothesis: `transcription_sm.txt`
- Reference: `youtube_transcription.txt`

Run it:
```powershell
python report.py
```
It prints the metrics and saves a detailed summary to `wer_report.txt`.

## Configuration tips

- Device & precision (faster-whisper):
  - In both transcribers, the model is created like:
    - `WhisperModel(model_size, device="cpu", compute_type="float32")`
  - If you have a CUDA GPU and compatible wheels, you can try:
    - `device="cuda"`, `compute_type="float16"` or `"int8_float16"`
  - GPU support depends on your environment and installed `ctranslate2` build.
- Model selection:
  - Smaller models are faster but less accurate. Larger models are slower but more accurate.
  - English-only variants (e.g., `small.en`) are fast for English.
- Audio formats:
  - WAV at 16 kHz mono is a safe default. Other formats may require ffmpeg/av.

## Troubleshooting

- Microphone stream errors (PortAudio):
  - If you get a device or samplerate error, try adjusting `samplerate`, `channels`, or explicitly set `device` in `sd.InputStream`.
  - Ensure your microphone is enabled and accessible by Windows.
- Performance:
  - Real-time on CPU works for smaller models; for larger models consider GPU acceleration.
- Unicode/encoding:
  - The scripts open files with `encoding="utf-8"`. Keep inputs as UTF-8 for best results.

## Credits
- Transcription: [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (CTranslate2 backend for Whisper)
- Metrics: [jiwer](https://github.com/jitsi/jiwer)
