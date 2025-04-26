import time

import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def search_duckduckgo_image(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.images(query, max_results=1)
            for r in results:
                return r["image"]
    except Exception as e:
        st.error(f"Error fetching image: {e}")
        return None
    return None


def get_dictionary_content(word):
    url = f"https://www.collinsdictionary.com/dictionary/german-english/{word}"

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    try:
        # Initialize the Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        with st.spinner("Fetching translation..."):
            driver.get(url)

            # Wait for the page to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            time.sleep(3)

            # Get the page source and create BeautifulSoup object
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Find the translation content
            translation_items = soup.select("li.translation")
            data = []
            lang_selection = ["German", "American English", "Chinese", "Turkish"]
            for item in translation_items:
                lang_tag = item.find("span", class_="lang")
                lang = lang_tag.get_text(strip=True) if lang_tag else None
                if lang not in lang_selection:
                    continue
                orth_tag = item.find("span", class_="orth")
                if orth_tag:
                    translation = orth_tag.get_text(strip=True)
                else:
                    orth_tag = item.find("span", class_="lang").find_next_sibling(
                        text=True
                    )
                    translation = orth_tag.strip() if orth_tag else None
                mp3_tag = item.find("a", class_="hwd_sound")
                mp3_url = mp3_tag["data-src-mp3"] if mp3_tag else None
                if lang == "American English":
                    lang = "English"
                if lang and translation:
                    data.append(
                        {"Language": lang, "Translation": translation, "Audio": mp3_url}
                    )

            if data:
                return pd.DataFrame(data)
            else:
                st.error("No translations found")
                return None

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

    finally:
        try:
            driver.quit()
        except:
            pass


def main():
    st.title("German-multiple language Dictionary")

    # Input for the German word
    word = st.text_input("Enter a German word:", "huhn")

    if st.button("Search") or word:
        # Get translations
        df = get_dictionary_content(word)

        if df is not None and not df.empty:
            # Display translations as a table
            st.subheader("Translations")

            # Display table with audio play buttons if available
            def audio_html(url):
                if url:
                    return f'<audio controls src="{url}"></audio>'
                return ""

            df_display = df.copy()
            df_display["Audio"] = df_display["Audio"].apply(audio_html)
            st.write(
                df_display.to_html(escape=False, index=False), unsafe_allow_html=True
            )

            # Get and display image
            st.subheader("Image")
            with st.spinner("Fetching image..."):
                img_url = search_duckduckgo_image(f"{word} german word")
                if img_url:
                    st.image(img_url, caption=f"Image for '{word}'")
                else:
                    st.warning("No image found")


if __name__ == "__main__":
    main()
