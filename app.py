import streamlit as st
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
import subprocess
import os


# ===== Page setup =====
st.set_page_config(
    page_title="Arabic → English Dubbing",
    page_icon="🎙️"
)

st.title("🎙️ AI Arabic → English Dubbing")


# ===== Load Whisper model =====
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()


# ===== Upload video =====
video = st.file_uploader(
    "📁 Upload Arabic video",
    type=["mp4", "mov", "avi"]
)


if video:

    # save file
    with open("input_video.mp4", "wb") as f:
        f.write(video.read())

    st.video("input_video.mp4")


    if st.button("🚀 Start Dubbing"):

        st.info("1️⃣ Extracting audio from video...")

        subprocess.call([
            "ffmpeg",
            "-y",
            "-i", "input_video.mp4",
            "audio.mp3"
        ])


        st.info("2️⃣ Transcribing Arabic speech...")

        result = model.transcribe("audio.mp3", language="ar")
        arabic_text = result["text"]

        st.subheader("📝 Arabic Text")
        st.write(arabic_text)


        st.info("3️⃣ Translating to English...")

        english_text = GoogleTranslator(
            source="ar",
            target="en"
        ).translate(arabic_text)

        st.subheader("📝 English Text")
        st.write(english_text)


        st.info("4️⃣ Generating English voice...")

        tts = gTTS(text=english_text, lang="en")
        tts.save("voice.mp3")


        st.info("5️⃣ Merging audio with video...")

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


        st.success("🎉 Done!")

        st.video("output.mp4")

        with open("output.mp4", "rb") as f:
            st.download_button(
                "⬇️ Download Result Video",
                f,
                "dubbed_video.mp4"
            )
