from faster_whisper import WhisperModel
import yt_dlp
import soundfile as sf
from tqdm import tqdm


def download_youtube_wav(url, output_path):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
            "preferredquality": "192",
        }],
        "quiet": False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print(f"✅ Audio saved as {output_path}")

def modelCall(audio_path):
    model_size = "small.en"
    model = WhisperModel(model_size, device="cpu", compute_type="float32")

    segments, info = model.transcribe(audio_path, beam_size=5)
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))


    with sf.SoundFile(audio_path) as f:
        duration = len(f) / f.samplerate

    formatted_segments = []
    full_text = ""
    
    for i, seg in enumerate(tqdm(segments, desc="Transcribing", unit="segment")):
        segment_id = f"seg_{i:03d}"
        segment_data = {
            "id": segment_id,
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip()
        }
        formatted_segments.append(segment_data)
        full_text += seg.text.strip() + " "

    # Build final structure
    transcription_data = {
        "duration": round(duration, 2),
        "text": full_text.strip(),
        "segments": formatted_segments,
    }
    
    print(f"\n✅ Transcription completed — {len(formatted_segments)} segments processed.")
    return transcription_data


if __name__ == "__main__":
    # video_url = "https://www.youtube.com/watch?v=i8KnCFq4Sw0"
    # download_youtube_wav(video_url, "video_audio.wav")
    modelCall("video_audio.wav")