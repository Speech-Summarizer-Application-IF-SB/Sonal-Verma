import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import time
import base64
import json

# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="Speech-to-Text Dashboard",
    layout="wide",
    page_icon="🎙️"
)

# ------------------- CUSTOM CSS -------------------
st.markdown(
    """
    <style>
    .main-title { text-align: center; font-size: 38px; font-weight: 700; color: #3A86FF; }
    .subtext { text-align: center; color: #666; margin-bottom: 2rem; }
    .status-box { text-align: center; background-color: #f1f3f5; border-radius: 10px;
                  padding: 10px; font-weight: 600; color: #333; margin-bottom: 1rem; }
    .controls-right { display:flex; justify-content:flex-end; gap:10px; align-items:center;
                      margin-top:8px; margin-bottom:8px; }
    a.download-link { text-decoration:none; padding:2px 4px; border-radius:6px;
                      background:#fff; font-weight:600; }
    button.copy-btn { padding:1px 4px; border-radius:6px; border:1px solid #fff;
                      background:white; cursor:pointer; font-weight:600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------- PAGE HEADER -------------------
st.markdown("<h1 class='main-title'>🎙️ AI Speech-to-Text Dashboard</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtext'>Record or upload audio → Transcribe, Diarize, and Summarize meetings effortlessly</p>",
    unsafe_allow_html=True,
)

# ------------------- SESSION STATE -------------------
if "status" not in st.session_state:
    st.session_state.status = "Idle"
if "transcription" not in st.session_state:
    st.session_state.transcription = ""
if "diarized" not in st.session_state:
    st.session_state.diarized = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
# control flag for showing the webrtc widget
if "show_webrtc" not in st.session_state:
    st.session_state.show_webrtc = False

# ------------------- HELPERS -------------------
def make_download_and_copy_html(text: str, filename: str) -> str:
    b64 = base64.b64encode(text.encode()).decode()
    download_link = f'<a class="download-link" href="data:file/txt;base64,{b64}" download="{filename}">⬇️</a>'
    js_text = json.dumps(text)  # safe quoting for JS
    copy_button = f'<button class="copy-btn" onclick="navigator.clipboard.writeText({js_text})">📋</button>'
    return f'<div class="controls-right">{download_link}{copy_button}</div>'

# ------------------- STATUS TRACKER -------------------
st.markdown(f"<div class='status-box'>🟢 Current Stage: {st.session_state.status}</div>", unsafe_allow_html=True)

# ------------------- LAYOUT -------------------
left, right = st.columns([1, 2], gap="large")

# ------------------- LEFT PANEL -------------------
with left:
    st.header("🎧 Input Options")
    input_mode = st.radio("Select Input Mode:", ["🎙️ Live Recording", "📁 Upload Audio File"])

    if input_mode == "🎙️ Live Recording":
        st.markdown("Use the Start button to show the recorder. Stop will end the recording and process the audio.")

        # Start button: set flag. Button click triggers a rerun automatically.
        if not st.session_state.show_webrtc:
            if st.button("▶️ Start Recording"):
                st.session_state.show_webrtc = True
                st.session_state.status = "Recording..."

        # When flag is True, render the webrtc widget
        if st.session_state.show_webrtc:
            ctx = webrtc_streamer(
                key="audio",
                mode=WebRtcMode.SENDONLY,
                media_stream_constraints={"audio": True, "video": False},
                async_processing=False,
            )

            if st.button("⏹️ Stop Recording"):
                # Stop -> hide widget and process captured audio (replace with real processing)
                st.session_state.show_webrtc = False
                st.session_state.status = "Processing (Transcribing)..."

                # --- Replace these demo steps with actual audio handling/transcription ---
                time.sleep(1)
                st.session_state.transcription = "This is a sample transcription from your recorded audio."
                st.session_state.status = "Processing (Diarizing)..."
                time.sleep(1)
                st.session_state.diarized = "Speaker 1: Hello!\nSpeaker 2: Hi there!"
                st.session_state.status = "Processing (Summarizing)..."
                time.sleep(1)
                st.session_state.summary = "Summary: Two speakers greeted each other briefly."
                st.session_state.status = "✅ Completed"
                # No explicit rerun needed — button click already triggered a rerun.

    elif input_mode == "📁 Upload Audio File":
        uploaded_audio = st.file_uploader("Upload an audio file (.wav, .mp3, .m4a)", type=["wav", "mp3", "m4a"])
        if uploaded_audio:
            st.audio(uploaded_audio)
            st.success("✅ Audio uploaded successfully!")
            if st.button("🚀 Process Audio"):
                st.session_state.status = "Processing (Transcribing)..."
                # Demo processing — replace with your model call
                time.sleep(1)
                st.session_state.transcription = "This is a sample transcription from your uploaded audio file."
                st.session_state.diarized = "Speaker 1: Hey\nSpeaker 2: Hi"
                st.session_state.summary = "Summary: Short greeting exchange."
                st.session_state.status = "✅ Completed"

# ------------------- RIGHT PANEL (OUTPUT TABS) -------------------
with right:
    st.header("🧾 Output Results")
    tab1, tab2, tab3 = st.tabs(["📝 Transcription", "👥 Diarized Transcription", "🧠 Summarized Notes"])

    with tab1:
        st.subheader("Raw Transcription")
        st.text_area("Transcribed Text", value=st.session_state.transcription, height=250, key="ta_transcription")
        st.markdown(make_download_and_copy_html(st.session_state.transcription, "transcription.txt"), unsafe_allow_html=True)

    with tab2:
        st.subheader("Speaker-Diarized Transcription")
        st.text_area("Diarized Output", value=st.session_state.diarized, height=250, key="ta_diarized")
        st.markdown(make_download_and_copy_html(st.session_state.diarized, "diarized_output.txt"), unsafe_allow_html=True)

    with tab3:
        st.subheader("Meeting Notes / Summary")
        st.text_area("Summarized Notes", value=st.session_state.summary, height=250, key="ta_summary")
        st.markdown(make_download_and_copy_html(st.session_state.summary, "summary.txt"), unsafe_allow_html=True)

# ------------------- FOOTER -------------------
st.markdown("""<hr><p style='text-align:center; color:#999;'>Built with ❤️ using Streamlit</p>""", unsafe_allow_html=True)
