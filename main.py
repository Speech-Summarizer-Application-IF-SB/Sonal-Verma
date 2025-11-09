import os
import sys
import json
import pandas as pd
from milestone_1.audio_cleaner import clean_audio
from milestone_2.usingfilemodel import modelCall
from milestone_4.dairization import get_diarization_result
from milestone_4.getJobId import get_job_id
from milestone_4.merge import merge_transcriptions
from milestone_4.summarizer import summarize_large_text


# ---------- Setup ----------
# ---------- Utility Functions ----------


def file_ready(path):
    """Check if a file exists and is non-empty."""
    return os.path.exists(path) and os.path.getsize(path) > 0


def load_json(path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load JSON {path}: {e}")
        return default if default is not None else {}


# ---------- STEP 1: Clean Audio ----------
def step_clean_audio(input_path, cleaned_audio):
    try:
        if not file_ready(cleaned_audio):
            print("🎧 Cleaning audio...")
            clean_audio(input_path, cleaned_audio)  # assumed defined elsewhere
        else:
            print("✅ Using existing cleaned audio.")
        return True
    except Exception as e:
        print(f"❌ Audio cleaning failed: {e}")
        return False


# ---------- STEP 2: Transcription ----------
def step_transcription(cleaned_audio, transcript_txt_path, transcript_json_path):
    try:
        if not file_ready(transcript_json_path):
            print("📝 Generating transcription...")
            transcript_result = modelCall(cleaned_audio)  # assumed defined elsewhere

            with open(transcript_txt_path, "w", encoding="utf-8") as f:
                f.write(transcript_result.get("text", ""))

            with open(transcript_json_path, "w", encoding="utf-8") as out_file:
                json.dump(
                    {
                        "duration": transcript_result.get("duration"),
                        "segments": transcript_result.get("segments", []),
                    },
                    out_file,
                    ensure_ascii=False,
                    indent=4,
                )
        else:
            print("✅ Using existing transcription file.")
            transcript_result = load_json(
                transcript_json_path, default={"segments": []}
            )

        # ensure text file exists
        if not file_ready(transcript_txt_path):
            text_joined = " ".join(
                seg.get("text", "") for seg in transcript_result.get("segments", [])
            )
            with open(transcript_txt_path, "w", encoding="utf-8") as f:
                f.write(text_joined.strip())

        if not isinstance(transcript_result.get("segments", []), list):
            print("❌ Invalid transcription JSON format: 'segments' must be a list.")
            return False

        return True
    except Exception as e:
        print(f"❌ Transcription step failed: {e}")
        return False


# ---------- STEP 3: Diarization ----------
def step_diarization(cleaned_audio, diarization_json_path):
    try:
        if not file_ready(diarization_json_path):
            print("🗣️ Performing diarization...")
            api_key = os.getenv("PYANNOTE_API_KEY")
            if not api_key:
                print("❌ Missing PYANNOTE_API_KEY in environment.")
                return False

            job_id = get_job_id(cleaned_audio, api_key)
            diarization_result = get_diarization_result(job_id, api_key)

            with open(diarization_json_path, "w", encoding="utf-8") as out_file:
                json.dump(diarization_result, out_file, ensure_ascii=False, indent=4)
        else:
            print("✅ Using existing diarization file.")
            diarization_result = load_json(diarization_json_path, default=[])

        if not isinstance(diarization_result, list):
            print("❌ Invalid diarization JSON format: expected a list.")
            return False

        return True
    except Exception as e:
        print(f"❌ Diarization step failed: {e}")
        return False


# ---------- STEP 4: Merge ----------
def step_merge_transcripts(transcript_json_path, diarization_json_path, diarization_txt_path):
    try:
        transcript_result = load_json(transcript_json_path, default={"segments": []})
        diarization_result = load_json(diarization_json_path, default=[])

        if not isinstance(transcript_result.get("segments", []), list) or not isinstance(diarization_result, list):
            
            print("❌ Invalid format for merging.")
            return False

        diarize_df = pd.DataFrame(diarization_result)

        if not file_ready(diarization_txt_path):
            print("🔗 Merging diarization with transcription...")
            merged_ok = merge_transcriptions(
                diarization_txt_path, transcript_result["segments"], diarize_df
            )
            if not merged_ok:
                print("❌ Error merging diarization with transcription.")
                return False
            print(f"✅ Speaker-attributed transcript saved to: {diarization_txt_path}")
        else:
            print("✅ Using existing diarized transcript.")

        return True
    except Exception as e:
        print(f"❌ Merging step failed: {e}")
        return False


# ---------- STEP 5: Summarization ----------
def step_summarization(diarization_txt_path, summary_txt_path):
    try:
        if not file_ready(summary_txt_path):
            print("🧠 Summarizing final transcript...")
            final_summary = summarize_large_text(diarization_txt_path)
            with open(summary_txt_path, "w", encoding="utf-8") as f:
                f.write(final_summary)
        else:
            print("✅ Using existing summary.")
        return True
    except Exception as e:
        print(f"❌ Summarization step failed: {e}")
        return False


# ---------- MAIN ----------
def main():
    OUTPUT_DIR = "processed_audio"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    input_path = input("Enter path to your audio file: ").strip()
    if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
        print("❌ File not found or empty.")
        sys.exit(1)

    cleaned_audio = os.path.join(OUTPUT_DIR, "file_cleaned.wav")
    transcript_txt_path = os.path.join(OUTPUT_DIR, "transcript.txt")
    transcript_json_path = os.path.join(OUTPUT_DIR, "transcription.json")
    diarization_txt_path = os.path.join(OUTPUT_DIR, "diarized_transcript.txt")
    diarization_json_path = os.path.join(OUTPUT_DIR, "diarization.json")
    summary_txt_path = os.path.join(OUTPUT_DIR, "final_summary.txt")

    steps = [
        ("Audio Cleaning", step_clean_audio, (input_path, cleaned_audio)),
        (
            "Transcription",
            step_transcription,
            (cleaned_audio, transcript_txt_path, transcript_json_path),
        ),
        ("Diarization", step_diarization, (cleaned_audio, diarization_json_path)),
        (
            "Merging",
            step_merge_transcripts,
            (transcript_json_path, diarization_json_path, diarization_txt_path),
        ),
        ("Summarization", step_summarization, (diarization_txt_path, summary_txt_path)),
    ]

    for name, func, args in steps:
        print(f"\n🔹 Running step: {name}")
        ok = func(*args)
        if not ok:
            print(f"🚫 {name} failed. Stopping pipeline.")
            sys.exit(1)

    print(f"\n✅ All processing complete! Files saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
