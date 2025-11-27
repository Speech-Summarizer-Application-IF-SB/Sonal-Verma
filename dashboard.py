import os
import io
import time
import tempfile
import streamlit as st
from pydub import AudioSegment
from main import (
    step_clean_audio,
    step_transcription,
    step_diarization,
    step_merge_transcripts,
    step_summarization,
)


# === Function to process the full pipeline and return results ===
def process_pipeline(input_audio_bytes, status_placeholder):
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "input.wav")
            cleaned_audio = os.path.join(tmpdir, "cleaned.wav")
            transcript_txt = os.path.join(tmpdir, "transcript.txt")
            transcript_json = os.path.join(tmpdir, "transcription.json")
            diarization_json = os.path.join(tmpdir, "diarization.json")
            diarized_txt = os.path.join(tmpdir, "diarized_transcript.txt")
            summary_txt = os.path.join(tmpdir, "summary.txt")

            audio = AudioSegment.from_file(input_audio_bytes, format="wav")
            audio.export(input_path, format="wav")

            # Step 1
            st.session_state.status = "🔊 Cleaning audio..."
            status_placeholder.info(f"**Status:** {st.session_state.status}")
            with st.spinner("Cleaning audio... ⏳"):
                if not step_clean_audio(input_path, cleaned_audio):
                    return "Audio cleaning failed!", "", ""

            # Step 2
            st.session_state.status = "📝 Transcribing..."
            status_placeholder.info(f"**Status:** {st.session_state.status}")
            with st.spinner("Transcribing... 📝"):
                if not step_transcription(cleaned_audio, transcript_txt, transcript_json):
                    return "Transcription failed!", "", ""
                with open(transcript_txt, "r", encoding="utf-8") as f:
                    transcription = f.read()
                st.session_state.transcription = transcription

            # Step 3
            st.session_state.status = "👥 Performing diarization..."
            status_placeholder.info(f"**Status:** {st.session_state.status}")
            with st.spinner("Performing diarization... 👥"):
                if not step_diarization(cleaned_audio, diarization_json):
                    return "Diarization failed!", "", ""

            # Step 4
            st.session_state.status = "🔗 Merging results..."
            status_placeholder.info(f"**Status:** {st.session_state.status}")
            with st.spinner("Merging results... 🔗"):
                if not step_merge_transcripts(transcript_json, diarization_json, diarized_txt):
                    return "Merging failed!", "", ""
                with open(diarized_txt, "r", encoding="utf-8") as f:
                    diarized = f.read()
                st.session_state.diarized = diarized

            # Step 5
            st.session_state.status = "🧠 Summarizing..."
            status_placeholder.info(f"**Status:** {st.session_state.status}")
            with st.spinner("Summarizing... 🧠"):
                if not step_summarization(diarized_txt, summary_txt):
                    return "Summarization failed!", "", ""
                with open(summary_txt, "r", encoding="utf-8") as f:
                    summary = f.read()
                st.session_state.summary = summary

            st.session_state.status = "✅ Completed"
            status_placeholder.success(f"**Status:** {st.session_state.status}")

            return transcription, diarized, summary

    except Exception as e:
        return f"❌ Error: {e}", "", ""



# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="Meeting Summarization",
    layout="wide",
    page_icon="🎙️"
)

# ------------------- CUSTOM CSS -------------------
st.markdown(
    """
    <style>
    .main-title { text-align: center; font-size: 38px; font-weight: 700; color: #3A86FF; }
    .subtext { text-align: center; color: #666; margin-bottom: 2rem; }
    .controls-right { display:flex; justify-content:flex-end; gap:10px; align-items:center;
                      margin-top:8px; margin-bottom:8px; }
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

# ------------------- AUTHENTICATION -------------------
if not st.user.is_logged_in:
    if( st.button("Log in with Google")):
        st.login("google")
    st.stop()

col1, col2 = st.columns([10,1], gap="small")

with col1:
    st.header(f"Welcome! {st.user.name}")
with col2:
    st.logout_button = st.button("Log out", on_click=st.logout)

# ------------------- SESSION STATE -------------------
if "status" not in st.session_state:
    st.session_state.status = "Idle"
if "transcription" not in st.session_state:
    st.session_state.transcription = "Transcription will appear here..." 
if "diarized" not in st.session_state:
    st.session_state.diarized = "Diarized transcription will appear here..."
if "summary" not in st.session_state:
    st.session_state.summary = "Summary will appear here..."
    
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

# ------------------- LAYOUT -------------------
left, right = st.columns([1, 2], gap="large")

# ------------------- LEFT PANEL -------------------
with left:
    st.header("🎧 Input Options")
    input_mode = st.radio("**Select Input Mode** (must at least 2 minutes long):", ["🎙️ Live Recording", "📁 Upload Audio File"])

    if input_mode == "🎙️ Live Recording":
        st.info("💾 Please save this file to use it later for transcription.")
        input_audio = st.audio_input("Click on 🎙️ to start recording", sample_rate=48000)
        

    elif input_mode == "📁 Upload Audio File":
        input_audio = st.file_uploader("Upload an audio file (.wav, .mp3)", type=["wav", "mp3"])
        
        if input_audio is not None:
            file_name = input_audio.name.lower()

            # ✅ Check if file is MP3   
            if file_name.endswith(".mp3"):

                # Convert and save
                audio = AudioSegment.from_mp3(input_audio)
                wav_buffer = io.BytesIO()
                audio.export(wav_buffer, format="wav")
                wav_buffer.seek(0)

                 # Replace input_audio with the converted WAV buffer
                input_audio = wav_buffer
                file_name = file_name.replace(".mp3", ".wav")

            elif not file_name.endswith(".wav"):
                st.warning("Unsupported file format!")
            
            st.audio(input_audio)


    #  process button
    if input_audio:
        st.toast(f"Audio {input_mode[2:]} successfully!", icon="✅")

        try:
            audio_segment = AudioSegment.from_file(input_audio, format="wav")
            duration_seconds = len(audio_segment) / 1000  # convert ms → seconds
            duration_minutes = duration_seconds / 60

            if duration_minutes < 1:
                st.error("❌ The audio file must be at least **1 minute long**. Please upload a longer recording.")
                st.stop()
            else:
                st.info(f"✅ Audio duration: {duration_minutes:.2f} minutes")
        except Exception as e:
            st.error(f"⚠️ Could not read audio file. Error: {e}")
            st.stop()

            
        if st.button("🚀 Process Audio"):
            st.session_state.status = "Initializing..."
            st.toast("Starting full pipeline 🚀", icon="🧠")

            status_placeholder = st.empty()

            status_placeholder.write(f"**Status:** {st.session_state.status}")

            # Run pipeline (no st.spinner)
            transcription, diarized, summary = process_pipeline(input_audio, status_placeholder)

            if transcription.startswith("❌") or transcription.endswith("failed!"):
                st.error(transcription)
            else:
                st.success("🎉 Processing completed successfully!")
                st.balloons()

            

# ------------------- RIGHT PANEL (OUTPUT TABS) -------------------
with right:
    st.header("🧾 Output Results")
    st.write("you can copy text by selecting and copying by pressing 📝  Ctrl+C ")

    tab1, tab2, tab3 = st.tabs(["📝 Transcription", "👥 Diarized Transcription", "🧠 Summarized Notes"])
    with tab1:
        col1, col2 = st.columns([9, 1])
        with col1:
            st.subheader("Raw Transcription")
        with col2:
            st.download_button(
                label="📥",
                data=st.session_state.transcription,
                file_name="transcription.txt",
                mime="text/plain"
            )

        with st.container(border=True,height=250):
            st.write_stream(stream_data(st.session_state.transcription))

    with tab2:
        col1, col2 = st.columns([9, 1])
        with col1:
            st.subheader("Speaker-Diarized Transcription")
        with col2:
            st.download_button(
                label="📥",
                data=st.session_state.diarized,
                file_name="diarized_transcription.txt",
                mime="text/plain"
            )
        
        with st.container(border=True,height=250):
            st.write_stream(stream_data(st.session_state.diarized))
    
    
    with tab3:
        col1, col2 = st.columns([9, 1])
        with col1:
            st.subheader("Meeting Notes / Summary")
        with col2:
            st.download_button(
                label="📥",
                data=st.session_state.summary,
                file_name="summary.txt",
                mime="text/plain"
            )
        
        with st.container(border=True,height=250):
            st.write_stream(stream_data(st.session_state.summary))

# ------------------- FOOTER -------------------
st.markdown("""<hr><p style='text-align:center; color:#999;'>Built with ❤️ using Streamlit</p>""", unsafe_allow_html=True)
