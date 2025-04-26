import base64
import re

import requests
import streamlit as st
from bs4 import BeautifulSoup

st.set_page_config(
    page_title="German Pronunciation Finder", page_icon="🔊", layout="centered"
)

st.title("German Word Pronunciation")
st.write("Enter a German word to hear its pronunciation from Forvo")


def get_pronunciation_url(word):
    url = f"https://forvo.com/search/{word}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all pronunciation elements
        play_elements = soup.find_all("div", class_="play", onclick=True)

        # First try to find German pronunciations
        for element in play_elements:
            onclick = element.get("onclick", "")
            if "German" in onclick:
                # Extract the MP3 URL parameters
                match = re.search(
                    r"Play\(\d+,'([^']+)','[^']+',false,'([^']+)','[^']+','h'", onclick
                )
                if match:
                    mp3_param1, mp3_param2 = match.groups()
                    mp3_param1 = base64.b64decode(mp3_param1).decode("utf-8")
                    mp3_param2 = base64.b64decode(mp3_param2).decode("utf-8")
                    return f"https://audio00.forvo.com/{mp3_param1}"

        # If no German pronunciation found, check if we need to follow a word link
        word_links = soup.find_all("a", class_="word")
        for link in word_links:
            if link.get("href", "").endswith("#de"):  # Check if it's a German word link
                word_url = f"https://forvo.com{link['href']}"
                response = requests.get(word_url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                play_elements = soup.find_all("div", class_="play", onclick=True)
                for element in play_elements:
                    onclick = element.get("onclick", "")
                    if "German" in onclick:
                        match = re.search(
                            r"Play\(\d+,'([^']+)','[^']+',false,'([^']+)','[^']+','h'",
                            onclick,
                        )
                        if match:
                            mp3_param1, mp3_param2 = match.groups()
                            mp3_param1 = base64.b64decode(mp3_param1).decode("utf-8")
                            mp3_param2 = base64.b64decode(mp3_param2).decode("utf-8")
                            return f"https://audio00.forvo.com/{mp3_param1}"

        return None
    except Exception as e:
        st.error(f"Error fetching pronunciation: {str(e)}")
        return None


# Create the search input
word = st.text_input("Enter a German word:", "")

if word:
    st.write(f"Searching pronunciation for: {word}")
    with st.spinner("Searching..."):
        audio_url = get_pronunciation_url(word)

        if audio_url:
            st.audio(audio_url, format="audio/mp3")
            st.success("✅ Pronunciation found!")
        else:
            st.error(
                "❌ No pronunciation found for this word. Please try another word."
            )
