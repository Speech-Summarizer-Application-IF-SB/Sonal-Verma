import time
import requests

def get_diarization_result(job_id, api_key):
    try:
        while True:
            try:
                headers = {"Authorization": f"Bearer {api_key}"}
                response = requests.get(
                    f"https://api.pyannote.ai/v1/jobs/{job_id}", headers=headers
                )
            except requests.exceptions.RequestException as e:
                print(f"❌ Network error while checking job status: {e}")
                time.sleep(10)
                continue  # Retry after waiting

            if response.status_code != 200:
                print(f"❌ Error: {response.status_code} - {response.text}")
                break

            try:
                data = response.json()
            except ValueError:
                print("❌ Failed to parse JSON response.")
                break

            status = data.get("status")
            if not status:
                print("❌ Missing 'status' field in response.")
                break

            if status in ["succeeded", "failed", "canceled"]:
                if status == "succeeded":
                    print("✅ Job completed successfully!")
                    return data.get("output", {}).get("diarization")
                else:
                    print(f"⚠️ Job {status}")
                break

            print(f"⏳ Job status: {status}, waiting...")
            time.sleep(10)

    except Exception as e:
        print(f"⚠️ Unexpected error occurred: {e}")


if __name__ == "__main__":
    job_id = "9361833d-33d2-48bd-b227-2c4cf861db1b"  
    get_diarization_result(job_id)