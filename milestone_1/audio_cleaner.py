import os
import time
import librosa
import numpy as np
import soundfile as sf
import sounddevice as sd
import noisereduce as nr
from pydub import AudioSegment, effects

# --- Configuration ---
SAMPLE_RATE = 16000  # Standard sample rate for speech recognition
CHANNELS = 1         # Mono audio

def clean_audio(input_path, output_path):
    """
    Cleans audio for ASR:
    - Resamples to 16kHz
    - Converts to mono
    - Reduces noise
    - Normalizes volume
    Saves cleaned audio to output_path.
    """
    print(f"Cleaning '{input_path}'...")

    # Load audio using librosa (handles resampling automatically)
    data, rate = librosa.load(input_path, sr=SAMPLE_RATE, mono=True)

    # Noise reduction
    try:
        data = nr.reduce_noise(y=data, sr=SAMPLE_RATE)
    except Exception as e:
        print(f"Noise reduction failed: {e}")

    # Convert to 16-bit PCM for pydub
    data_clipped = np.clip(data, -1.0, 1.0)
    data_int16 = (data_clipped * 32767).astype(np.int16)

    # Create AudioSegment for normalization
    audio_segment = AudioSegment(
        data_int16.tobytes(),
        frame_rate=SAMPLE_RATE,
        sample_width=2,
        channels=CHANNELS
    )

    # Normalize volume
    normalized_segment = effects.normalize(audio_segment)

    # Export cleaned audio
    normalized_segment.export(output_path, format="wav")
    print(f"Saved cleaned audio to '{output_path}'")


def record_live_audio(output_filename):
    """
    Records live audio from the microphone and saves it to a file.
    """
    try:
        duration_str = input("Enter recording duration in seconds (e.g., 10): ")
        duration = int(duration_str)

        print("\n🎙️ Get ready to record...")
        time.sleep(1)
        print("🔴 Recording started! Speak now.")

        # Record audio
        recording = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
        sd.wait()  # Wait until recording is finished

        print("⏹️ Recording finished.")

        # Save the recording to a file
        sf.write(output_filename, recording, SAMPLE_RATE)
        print(f"Live recording saved to '{output_filename}'")

        return True

    except ValueError:
        print("Invalid input. Please enter a whole number for the duration.")
        return False
    except Exception as e:
        print(f"An error occurred during recording: {e}")
        return False


def main():
    """
    Main function to drive the audio cleaning script.
    """
    print("--- 🎧 AI Live Meeting Summarizer: Audio Pre-processing ---")
    
    choice = input("Choose audio source: type 'live' to record or 'file' to select a file: ").strip().lower()

    # Create an 'processed_audio' directory if it doesn't exist
    if not os.path.exists('processed_audio'):
        os.makedirs('processed_audio')

    if choice == 'live':
        raw_filename = "processed_audio/live_recording_raw.wav"
        cleaned_filename = "processed_audio/live_recording_cleaned.wav"
        if record_live_audio(raw_filename):
            clean_audio(raw_filename, cleaned_filename)

    elif choice == 'file':
        input_path = input("Enter the full path to your audio file (e.g., meeting.wav): ").strip()
        
        if not os.path.exists(input_path):
            print(f"Error: File not found at '{input_path}'")
            return
            
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        cleaned_filename = f"processed_audio/{base_name}_cleaned.wav"
        
        clean_audio(input_path, cleaned_filename)

    else:
        print("Invalid choice. Please run the script again and type 'live' or 'file'.")

if __name__ == "__main__":
    main()