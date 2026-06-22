import streamlit as st
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
import subprocess
import os


st.set_page_config(
    page_title="Arabic → English Dubbing",
    page_icon="🎙️"
)

st.title("🎙️ Arabic → English AI Dubbing")


# تحميل Whisper
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()


# رفع الفيديو
video = st.file_uploader("Upload Arabic video", type=["mp4", "mov", "avi"])


if video:

    # حفظ الفيديو
    with open("input_video.mp4", "wb") as f:
        f.write(video.read())

    st.video("input_video.mp4")

    if st.button("Start Dubbing 🚀"):

        st.info("Extracting audio...")

        # استخراج الصوت من الفيديو
        subprocess.call([
            "ffmpeg",
            "-y",
            "-i", "input_video.mp4",
            "arabic_audio.mp3"
        ])

        st.info("Transcribing Arabic speech...")

        # تحويل الصوت لنص عربي
        result = model.transcribe(
            "arabic_audio.mp3",
            language="ar"
        )

        arabic_text = result["text"]

        st.subheader("Arabic Text")
        st.write(arabic_text)

        st.info("Translating to English...")

        # ترجمة النص
        english_text = GoogleTranslator(
            source="ar",
            target="en"
        ).translate(arabic_text)

        st.subheader("English Text")
        st.write(english_text)

        st.info("Generating English voice...")

        # تحويل النص لصوت إنجليزي
        tts = gTTS(text=english_text, lang="en")
        tts.save("english_voice.mp3")

        st.info("Merging audio with video...")

        # دمج الصوت مع الفيديو (بدون MoviePy)
        subprocess.call([
            "ffmpeg",
            "-y",
            "-i", "input_video.mp4",
            "-i", "english_voice.mp3",
            "-c:v", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "dubbed_video.mp4"
        ])

        st.success("Done 🎉")

        st.video("dubbed_video.mp4")

        with open("dubbed_video.mp4", "rb") as file:
            st.download_button(
                label="Download English Dubbed Video",
                data=file,
                file_name="english_dubbed.mp4"
            )
