# 🚀 Audio Pre-processing Project

This project provides a simple Python script (`audio_cleaner.py`) to pre-process audio files. It can be used to reduce background noise from existing `.wav` files or to record and clean new audio directly from a microphone.

The script uses several key libraries to handle audio manipulation, including `noisereduce` for noise reduction, `pydub` for high-level audio operations, and `sounddevice` for recording.

---

## ⚙️ Features

* **Noise Reduction**: Cleans background noise from existing audio files.
* **Live Recording**: Records new audio from a microphone and cleans it on the fly.
* **Simple CLI**: Easy-to-use command-line interface to choose between processing a file or recording.
* **Organized Output**: Saves all processed and recorded files neatly into an `output/` directory.

---

## 📂 Project Structure

Ensure your project directory is set up as follows. The sample audio files (e.g., from the NOIZEUS dataset) should be placed at the root of the project folder.

```
MILESTONE-1/
├── output/
│   └── (cleaned audio files will appear here)
├── venv/
│   └── (your virtual environment)
├── audio_cleaner.py
└── sp01-train-sn10_OxrSReyA.wav
```

---

## 🛠️ How to Get Started

Follow these steps to set up your environment and run the audio pre-processing script.

### 1. Prerequisites

* **Python 3.x**
* **FFmpeg**: The `pydub` library requires FFmpeg. You must install it on your system separately. You can download it from the [official FFmpeg site](https://ffmpeg.org/download.html).

### 2. Quick Start (Windows PowerShell)

```powershell
# 1) Clone the repository
git clone https://github.com/Speech-Summarizer-Application-IF-SB/Sonal-Verma.git
cd Sonal-Verma

# 2) Create & activate a virtual environment
python -m venv .venv
. .venv\Scripts\Activate.ps1

# 3) Install dependencies
pip install -r requirements.txt

# 4) Navigate to milestone_1
cd milestone_1

# 5) Run the audio cleaner script
python audio_cleaner.py
```

**For macOS/Linux users:**
```bash
# 1) Clone the repository
git clone https://github.com/Speech-Summarizer-Application-IF-SB/Sonal-Verma.git
cd Sonal-Verma

# 2) Create & activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Navigate to milestone_1
cd milestone_1

# 5) Run the audio cleaner script
python audio_cleaner.py
```

### 3. Using the Audio Cleaner

The script will prompt you to choose between cleaning an existing file or recording new audio.

#### To clean an existing audio file:

1.  Choose the **file** option when prompted.
2.  Enter the name of the audio file you wish to clean (e.g., `sp01-train-sn10_OxrSReyA.wav`).
3.  The script will process the file and save a cleaned version in the `output/` folder.

#### To record and clean live audio:

1.  Choose the **live** option when prompted.
2.  Enter the number of seconds you want to record.
3.  The script will save both the raw recording and a cleaned version in the `output/` folder.
## 📚 Resources and References

Here are some helpful resources for this project.

**Audio Dataset:**
* **NOIZEUS Dataset**: A dataset of noisy speech samples perfect for testing.

**Key Libraries Documentation:**
* **pydub**: For high-level audio manipulation.
* **noisereduce**: For background noise reduction.
* **sounddevice**: For recording and playing audio.
* **soundfile**: For reading and writing audio data.

**Tutorials and Learning:**
* **Corey Schafer's Python Tutorials**: Excellent for general Python concepts.
* **Tech With Tim - PyDub Tutorial**: A good video tutorial on using pydub.

**AI and LLM Help:**
* **ChatGPT**: Great for asking specific coding questions and debugging.