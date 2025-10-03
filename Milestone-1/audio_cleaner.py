import os
import time
import numpy as np
import soundfile as sf
import sounddevice as sd
import noisereduce as nr
from pydub import AudioSegment, effects
from pydub.silence import split_on_silence

# --- Configuration ---
SAMPLE_RATE = 16000  # Standard sample rate for speech recognition
CHANNELS = 1         # Mono audio

def clean_audio(input_path, output_path):
    """
    Cleans an audio file by reducing noise, normalizing volume, and removing silence.
    
    Args:
        input_path (str): Path to the input WAV file.
        output_path (str): Path to save the cleaned WAV file.
    """
    print(f"🧹 Starting cleaning process for '{input_path}'...")
    
    # 1. Load the audio file using soundfile
    try:
        data, rate = sf.read(input_path)
        print(f"Audio loaded successfully. Sample rate: {rate}, Duration: {len(data)/rate:.2f}s")
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return

    # Ensure the audio is at the correct sample rate (resampling if necessary)
    if rate != SAMPLE_RATE:
        print(f"Warning: Original sample rate ({rate} Hz) is not {SAMPLE_RATE} Hz. This script does not resample. For best results, resample your audio to {SAMPLE_RATE} Hz first.")

    # Ensure mono audio for processing
    if isinstance(data, np.ndarray) and data.ndim > 1:
        # Mix down to mono by averaging channels
        data = np.mean(data, axis=1)

    # Convert integer PCM to float32 in -1..1 for noise reduction
    if np.issubdtype(data.dtype, np.integer):
        max_val = np.iinfo(data.dtype).max
        data_float = data.astype(np.float32) / float(max_val)
    else:
        data_float = data.astype(np.float32)

    # --- Step 1: Noise Reduction ---
    print("Reducing background noise...")
    try:
        # Perform noise reduction on the float data
        reduced_noise = nr.reduce_noise(y=data_float, sr=rate)
        print("Noise reduction complete.")
    except Exception as e:
        print(f"Noise reduction failed: {e}. Proceeding with original audio.")
        reduced_noise = data_float

    # --- Step 2: Normalization and Silence Removal (with pydub) ---
    print("Normalizing audio and removing silent parts...")
    
    # Convert the noise-reduced float data back to 16-bit PCM for pydub
    reduced_noise_clipped = np.clip(reduced_noise, -1.0, 1.0)
    reduced_noise_int16 = (reduced_noise_clipped * 32767).astype(np.int16)
    
    # Create a pydub AudioSegment
    audio_segment = AudioSegment(
        reduced_noise_int16.tobytes(),
        frame_rate=rate,
        sample_width=2,  # 2 bytes for 16-bit PCM
        channels=CHANNELS
    )

    # Normalize the audio to a standard level
    normalized_segment = effects.normalize(audio_segment)

    # Split the audio on silence
    chunks = split_on_silence(
        normalized_segment,
        min_silence_len=500,    # Minimum length of silence to split on (in ms)
        silence_thresh=-40,     # Anything quieter than -40 dBFS is silence
        keep_silence=200        # Keep 200ms of silence at chunk ends
    )

    if not chunks:
        print("⚠️ No audible speech detected after cleaning. Output file will be empty.")
        return

    # Concatenate the non-silent chunks
    processed_audio = sum(chunks)
    print("Silence removal complete.")

    # --- Step 3: Export the cleaned audio ---
    print(f"Exporting cleaned audio to '{output_path}'...")
    processed_audio.export(output_path, format="wav")
    print("✅ Cleaning process finished successfully!")


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

    # Create an 'output' directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')

    if choice == 'live':
        raw_filename = "output/live_recording_raw.wav"
        cleaned_filename = "output/live_recording_cleaned.wav"
        if record_live_audio(raw_filename):
            clean_audio(raw_filename, cleaned_filename)

    elif choice == 'file':
        input_path = input("Enter the full path to your audio file (e.g., meeting.wav): ").strip()
        
        if not os.path.exists(input_path):
            print(f"Error: File not found at '{input_path}'")
            return
            
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        cleaned_filename = f"output/{base_name}_cleaned.wav"
        
        clean_audio(input_path, cleaned_filename)

    else:
        print("Invalid choice. Please run the script again and type 'live' or 'file'.")

if __name__ == "__main__":
    main()