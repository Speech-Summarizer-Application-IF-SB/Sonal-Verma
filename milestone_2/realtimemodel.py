import sounddevice as sd
import numpy as np
import queue
import threading
from faster_whisper import WhisperModel

# ==== Configuration ====
sample_rate = 16000
block_duration = 3.0  # seconds per audio block
chunk_duration = 0.5  # seconds per audio chunk
channels = 1

frames_per_block = int(sample_rate * block_duration)
frames_per_chunk = int(sample_rate * chunk_duration)

audio_queue = queue.Queue()
audio_buffer = []

# Shared flag for stopping
running = True

# ==== Whisper Model ====
model_size = "small.en"
model = WhisperModel(model_size, device="cpu", compute_type="float32")


# ==== Audio callback ====
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())


# ==== Recorder thread ====
def recorder():
    global running
    with sd.InputStream(
        samplerate=sample_rate,
        channels=channels,
        callback=audio_callback,
        blocksize=frames_per_chunk,
    ):
        print("🎙️ Recording... Press Ctrl+C to stop.")
        while running:
            sd.sleep(100)
        print("🛑 Recorder stopped.")


# ==== Transcriber (main loop) ====
def transcriber():
    global running, audio_buffer
    while running:
        try:
            block = audio_queue.get(timeout=1)
        except queue.Empty:
            continue

        audio_buffer.append(block)

        total_frames = sum(len(chunk) for chunk in audio_buffer)
        if total_frames >= frames_per_block:
            audio_data = np.concatenate(audio_buffer)[:frames_per_block].flatten().astype(np.float32)
            audio_buffer = []

            segments, _ = model.transcribe(audio_data, language="en", beam_size=1)
            for segment in segments:
                print(segment.text.strip())


# ==== Main ====
if __name__ == "__main__":
    try:
        threading.Thread(target=recorder, daemon=True).start()
        transcriber()
    except KeyboardInterrupt:
        print("\n🧩 Ctrl+C detected. Stopping gracefully...")
        running = False
