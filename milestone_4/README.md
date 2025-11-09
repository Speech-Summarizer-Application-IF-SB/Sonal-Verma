# Milestone 4 — Speaker Diarization & Summarization

This folder contains utilities for simple speaker diarization, merging diarized segments, fetching job IDs (helper), and generating short summaries from transcriptions. The scripts are intended as utilities you can run on pre-recorded audio or transcripts as part of a larger speech-to-text + post-processing pipeline.

## 📂 Project structure

```
milestone_4/
├── dairization.py      # Speaker diarization helper / demo script
├── getJobId.py        # Utility to obtain or parse job IDs (helper)
├── merge.py           # Merge diarization/segment files into single transcript
├── summarizer.py      # Summarize transcript text (abstractive/extractive)
├── __init__.py
└── README.md          # This file
```

## File overview

- `dairization.py` — Script that demonstrates or runs a speaker diarization step on audio. Check the file header for configurable options like input path, model/device selection, and output formats.
- `getJobId.py` — Small helper to generate, fetch, or parse job IDs used by other scripts (for example when kicking off async jobs or tracking results). Inspect the top of the file to see how it should be used.
- `merge.py` — Utility that reads diarization segment outputs (or multiple partial transcripts) and merges them into a single, time-aligned transcript. Useful after chunked transcription.
- `summarizer.py` — Script to create short summaries from a transcript. It may use simple heuristics or an external model — check the imports at the top of the file to see what it requires.

> Note: If a script uses interactive args or an argument parser, run it with `-h` or `--help` to view options. Otherwise, edit constants at the top of the file (names like `INPUT_PATH`, `OUTPUT_PATH`) to configure behavior.

## Quick start (Windows PowerShell)

```powershell
# 1) Create & activate a virtual environment (if you haven't already)
python -m venv .venv
. .venv\Scripts\Activate.ps1

# 2) Install dependencies from the repository root
pip install -r requirements.txt

# 3) Change to the milestone_4 directory
cd milestone_4
```

After this you're ready to run the scripts in this folder.

## How to run (examples)

Important: the scripts in this folder currently do not provide a full CLI. Most functions are callable from Python or use hard-coded/example values at the bottom of the file. Use one of the two approaches below depending on the script:

1) Run the script directly (uses the file's example/hard-coded values)

```powershell
# Run the diarization helper (edit the job_id/api key inside the file before running)
python milestone_4\dairization.py

# Run the summarizer example (edit the example path at the bottom of the file if needed)
python milestone_4\summarizer.py
```

2) Import the function and call it from Python (recommended for `merge.py` and programmatic use)

Open a Python REPL or a short runner script and call the functions directly. Examples:

```python
# Example: call diarization polling helper programmatically
from milestone_4.dairization import get_diarization_result
result = get_diarization_result(job_id="YOUR_JOB_ID", api_key="YOUR_API_KEY")
print(result)

# Example: use merge_transcriptions from merge.py
from milestone_4.merge import merge_transcriptions
# diarization_txt_path: path to write merged text
# transcript_segments: list of dicts with 'start','end','text'
# diarize_df: pandas DataFrame with columns ['start','end','speaker']
merge_transcriptions("out_diarized.txt", transcript_segments, diarize_df)

# Example: call summarizer programmatically
from milestone_4.summarizer import summarize_large_text
summary = summarize_large_text("../processed_audio/diarized_transcript.txt")
print(summary)
```

Notes:
- `dairization.py` contains a polling helper (`get_diarization_result(job_id, api_key)`) — edit the `job_id` and supply an API key or call the function directly from Python.
- `merge.py` exposes `merge_transcriptions(diarization_txt_path, transcript_segments, diarize_df)` as a library function — it is intended to be used programmatically rather than as a CLI tool.
- `summarizer.py` provides `summarize_large_text(transcript_path, ...)` and includes a small example invocation when run as `__main__`.

If you prefer CLI-style execution, I can add `argparse` wrappers for each script and update the README again.

## Expected outputs

- Diarization output: JSON or text files containing speaker-labeled segments with start/end timestamps.
- Merged transcript: a single plain-text file with time-aligned or speaker-labeled content.
- Summary: a short plain-text summary (one-paragraph or bullet points) produced by `summarizer.py`.

## Common troubleshooting

- Ensure your virtual environment is active and dependencies are installed.
- If audio processing fails, confirm `ffmpeg` is installed and present on PATH (on Windows add `ffmpeg\bin` to PATH).
- If a script imports a model or deep-learning library and you see CUDA/torch errors, make sure PyTorch is installed for your CUDA version, or force CPU-only execution if GPU is not available.

## Edge cases to consider

- Very short or silent audio may produce no speaker segments or an empty transcript.
- Overlapping speech or noisy recordings may confuse diarization models — quality can vary with model choice and audio preprocessing.
- Long files may need chunking to avoid memory/OOM issues; use `merge.py` to recombine chunked outputs.

## Libraries & tools

This milestone may use some of the following (check imports to confirm exact requirements):

- PyTorch (if any model-based diarization or summarization is used)
- pyannote.audio or other diarization libraries
- librosa, soundfile, or ffmpeg for audio I/O and preprocessing
- transformers or other NLP libraries for summarization
- numpy, scipy for low-level utilities

If you prefer to install only the packages used here, open the scripts and install the imports shown at the top of each file.

## Data sources and models

- Any example transcripts or diarization outputs used in tests are project artifacts.
- Pretrained models used by the scripts are governed by their providers' licenses; check model docs before redistributing.

