import os
import requests

def get_job_id(input_path, api_key):
    try:
        # === Configuration ===

        object_key = "myMeeting"        # Unique identifier for your file

        if not api_key:
            raise ValueError("Missing API key. Set PYANNOTE_API_KEY as an environment variable.")

        # === Step 1: Request a pre-signed PUT URL ===
        try:
            response = requests.post(
                "https://api.pyannote.ai/v1/media/input",
                json={"url": f"media://{object_key}"},
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )
            response.raise_for_status()
            data = response.json()
            presigned_url = data["url"]
            print(f"✅ Pre-signed URL obtained for object key '{object_key}'")
        except requests.exceptions.RequestException as e:
            print("❌ Error requesting pre-signed URL:", e)
            raise

        # === Step 2: Upload your audio file ===
        try:
            print(f"⬆️  Uploading {input_path} to {presigned_url} ...")
            with open(input_path, "rb") as input_file:
                upload_response = requests.put(presigned_url, data=input_file)
                upload_response.raise_for_status()
            print("✅ File uploaded successfully!")
        except FileNotFoundError:
            print(f"❌ File not found: {input_path}")
            raise
        except requests.exceptions.RequestException as e:
            print("❌ Error uploading file:", e)
            raise

        # === Step 3 : Start diarization ===
        try:
            print("🚀 Starting diarization job...")
            diarize_response = requests.post(
                "https://api.pyannote.ai/v1/diarize",
                json={"url": f"media://{object_key}"},
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )
            diarize_response.raise_for_status()
            print("✅ Diarization job created successfully!")
            print(diarize_response.json())
            return diarize_response.json().get("jobId")
        except requests.exceptions.RequestException as e:
            print("❌ Error starting diarization job:", e)
            raise

    except Exception as e:
        print("⚠️ Unexpected error occurred:", e)
