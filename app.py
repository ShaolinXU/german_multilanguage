import streamlit as st

from image_search import search_duckduckgo_image
from langchain_utils import work_on_the_word as get_word_info
from text_to_audio import text_to_audio

st.set_page_config(page_title="German Dictionary Assistant", page_icon="📚")
st.title("German Dictionary Assistant")
deepseek = st.checkbox("Use DeepSeek, otherwise use OpenAI", value=True)
st.markdown(
    """
    Enter a German word to get English translation, IPA pronunciation, articles, example sentences, and images.
    """
)


word = st.text_input("Enter a German word:", "")

if st.button("Search") and word.strip():
    with st.spinner("Searching, please wait..."):
        try:
            if deepseek:
                info = get_word_info(word.strip(), deepseek=True)
            else:
                info = get_word_info(word.strip(), deepseek=False)
            st.subheader("Translation and Information:")
            st.markdown(f"**{info['input']}**")
            st.markdown(info["translation"])
            st.markdown(info["explanation"])
            st.markdown(
                f"English example sentence: {info['example_sentence']['english']}"
            )
            st.markdown(
                f"German example sentence: {info['example_sentence']['german']}"
            )
            audio_bytes = text_to_audio(info["example_sentence"]["german"])
            st.audio(audio_bytes, format="audio/mp3")
            st.subheader("Image:")
            img_url = search_duckduckgo_image(word.strip())
            if img_url:
                st.image(img_url)
            else:
                st.info("No related images found.")
        except Exception as e:
            st.error(f"Search failed: {e}")
            st.write(e)
