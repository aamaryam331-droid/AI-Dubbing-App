import streamlit as st
import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
import os


st.set_page_config(
    page_title="Arabic To English Dubbing",
    page_icon="🎙️"
)


st.title("🎙️ Arabic → English AI Dubbing")


@st.cache_resource
def load_whisper():
    return whisper.load_model("base")


model = load_whisper()


video = st.file_uploader(
    "Upload Arabic video",
    type=["mp4", "mov", "avi"]
)


if video:

    with open("input_video.mp4", "wb") as f:
        f.write(video.read())


    st.video("input_video.mp4")


    if st.button("Start Dubbing 🚀"):


        st.info("Extracting audio...")


        video_clip = VideoFileClip(
            "input_video.mp4"
        )


        video_clip.audio.write_audiofile(
            "arabic_audio.mp3"
        )


        st.info("Understanding Arabic speech...")


        result = model.transcribe(
            "arabic_audio.mp3",
            language="ar"
        )


        arabic_text = result["text"]


        st.subheader("Arabic text:")
        st.write(arabic_text)



        st.info("Translating Arabic to English...")


        english_text = GoogleTranslator(
            source="ar",
            target="en"
        ).translate(arabic_text)



        st.subheader("English text:")
        st.write(english_text)



        st.info("Creating English voice...")


        voice = gTTS(
            text=english_text,
            lang="en"
        )


        voice.save(
            "english_voice.mp3"
        )



        st.info("Adding English voice to video...")


        new_audio = AudioFileClip(
            "english_voice.mp3"
        )


        final_video = video_clip.set_audio(
            new_audio
        )


        final_video.write_videofile(
            "dubbed_video.mp4"
        )



        st.success("Done 🎉")


        st.video(
            "dubbed_video.mp4"
        )


        with open(
            "dubbed_video.mp4",
            "rb"
        ) as file:


            st.download_button(
                label="Download English Dubbed Video",
                data=file,
                file_name="english_dubbed.mp4"
            )
