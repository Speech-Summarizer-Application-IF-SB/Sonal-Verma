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

### 2. Setup Your Environment

It's highly recommended to use a Python virtual environment to manage project dependencies.

```bash
# 1. Create a new virtual environment
python -m venv venv

# 2. Activate the environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
3. Install Required Libraries
```

Install all necessary Python packages using pip. Run this command in your activated terminal:

```Bash
pip install numpy soundfile sounddevice noisereduce pydub
```

4. Run the Audio Cleaner
You can now run the main script. It will prompt you to choose between cleaning an existing file or recording new audio.

```Bash
python audio_cleaner.py
```

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