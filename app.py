import streamlit as st
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
import subprocess
import gdown
import os


st.set_page_config(
    page_title="Arabic → English Dubbing",
    page_icon="🎙️"
)

st.title("🎙️ AI Dubbing (Google Drive + Stable Version)")


# ====== session state ======
if "step" not in st.session_state:
    st.session_state.step = 0


# ====== تحميل Whisper ======
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()


# ====== تحميل من Google Drive ======
def download_from_drive(url, output="input_video.mp4"):
    try:
        file_id = url.split("/d/")[1].split("/")[0]
        gdown.download(
            f"https://drive.google.com/uc?id={file_id}",
            output,
            quiet=False
        )
        return output
    except:
        return None


# ====== إدخال الرابط ======
drive_url = st.text_input("📎 Paste Google Drive video link")


# ====== تحميل الفيديو ======
if drive_url and st.button("Load Video 🚀"):

    st.info("Downloading video from Google Drive...")

    video_path = download_from_drive(drive_url)

    if video_path is None:
        st.error("Invalid Google Drive link ❌")
        st.stop()

    st.session_state.step = 1

    st.video(video_path)


# ====== Start Dubbing ======
if st.session_state.step == 1:

    if st.button("Start Dubbing 🎙️"):

        st.info("Extracting audio...")

        subprocess.call([
            "ffmpeg",
            "-y",
            "-i", "input_video.mp4",
            "audio.mp3"
        ])

        st.info("Transcribing Arabic speech...")

        result = model.transcribe("audio.mp3", language="ar")
        arabic_text = result["text"]

        st.subheader("Arabic Text")
        st.write(arabic_text)

        st.info("Translating to English...")

        english_text = GoogleTranslator(
            source="ar",
            target="en"
        ).translate(arabic_text)

        st.subheader("English Text")
        st.write(english_text)

        st.info("Generating voice...")

        tts = gTTS(text=english_text, lang="en")
        tts.save("voice.mp3")

        st.info("Merging video + audio...")

        subprocess.call([
            "ffmpeg",
            "-y",
            "-i", "input_video.mp4",
            "-i", "voice.mp3",
            "-c:v", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "output.mp4"
        ])

        st.success("Done 🎉")

        st.video("output.mp4")

        with open("output.mp4", "rb") as f:
            st.download_button(
                "Download Video",
                f,
                "dubbed_video.mp4"
            )
