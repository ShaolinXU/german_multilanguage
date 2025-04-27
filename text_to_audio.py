from io import BytesIO
from pathlib import Path

import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def text_to_audio(sentence: str, lang: str = "en") -> BytesIO:
    """
    Convert a sentence to an audio file (mp3) in memory using OpenAI's TTS API (gpt-4o-mini-audio-preview), suitable for Streamlit playback.
    Args:
        sentence (str): The sentence to convert to audio.
        lang (str): Language code for TTS (default: 'en').
    Returns:
        BytesIO: In-memory mp3 audio file.
    """
    speech_file_path = Path(__file__).parent / "speech.mp3"
    with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts", voice="alloy", input=sentence
    ) as response:
        response.stream_to_file(speech_file_path)
        with open(speech_file_path, "rb") as f:
            audio_bytes = BytesIO(f.read())
    audio_bytes.seek(0)
    return audio_bytes


# Example usage in Streamlit
if __name__ == "__main__":
    # Initialize session state for last sentence if not exists
    if "last_sentence" not in st.session_state:
        st.session_state.last_sentence = "Hello, world!"

    def update_sentence():
        # 这里可以做你想做的事情，比如基于新的输入重新赋值
        st.session_state["sentence_input"] = st.session_state["sentence_input"].strip()

    sentence = st.text_area(
        "Enter a sentence:",
        "Hello, world!",
        height=88,
        key="sentence_input",
        on_change=update_sentence,
    )

    # Only generate audio if button is clicked or sentence has changed
    if st.button("Generate Audio") and (
        sentence and sentence != st.session_state.last_sentence
    ):
        audio_bytes = text_to_audio(sentence)
        st.audio(audio_bytes, format="audio/mp3")
