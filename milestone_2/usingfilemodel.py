from faster_whisper import WhisperModel
import yt_dlp

def download_youtube_wav(url, output_path="video_audio.wav"):
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

video_url = "https://www.youtube.com/watch?v=IYtDS27znnM"
download_youtube_wav(video_url, "video_audio")

model_size = "small.en"

model = WhisperModel(model_size, device="cpu", compute_type="float32")

segments, info = model.transcribe("video_audio.wav", beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

text = ""

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    text += segment.text + " "

with open("transcription_sm.txt", "w", encoding="utf-8") as f:
    f.write(text)