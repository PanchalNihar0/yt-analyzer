import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import predict


def app():
    def get_youtube_comments(video_url, max_comments=1000):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        st.info("🚀 Opening video...")
        driver.get(video_url)
        time.sleep(5)

        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height or len(driver.find_elements(By.XPATH, '//*[@id="content-text"]')) >= max_comments:
                break
            last_height = new_height

        comments_elements = driver.find_elements(By.XPATH, '//*[@id="content-text"]')
        comments = [elem.text for elem in comments_elements[:max_comments]]

        driver.quit()
        return comments

    st.set_page_config(page_title="YouTube Sentiment Analysis", layout="wide", page_icon="📺",initial_sidebar_state="collapsed")

    st.markdown("""
        <style>
            .stApp {
                background-color: #3A2726;
                color: #eee;
            }
            h1, h2, h3, h4 {
                text-align: center;
                color: #F72585;
            }
            .stButton>button {
                background-color: #7209b7;
                color: white;
                font-size: 16px;
                padding: 10px 24px;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)
    st.title("📺 YouTube Comments Sentiment Analysis")
    st.markdown("## 🎯 Extract YouTube comments, analyze sentiment, and visualize results beautifully!")
    st.markdown("### ✨ Powered by: **Sahil Mera Beta** 🤖")

    col1,col2=st.columns([2,2])
    with col1:
        video_url=st.text_input("🔗Enter URL Here")
    with col2:
        max_comments=st.slider("choose the number of comments",10,1000,200) 

    if st.button("🔍 Extract and Analyze"):
        if not video_url:
            st.error("🚨 Please enter a valid YouTube video URL.")
        else:
            with st.spinner("🕵️ Extracting comments..."):
                comments = get_youtube_comments(video_url, max_comments)
            
            if comments:
                st.success(f"✅ Extracted {len(comments)} comments.")

                with st.expander("📜 Show Extracted Comments"):
                    results = predict.predict_sentiments(comments)
                    for comment, sentiment in results[:50]:
                        if sentiment.lower() == "positive":
                            st.markdown(f"<span style='color:lightgreen'>👍 {comment}</span>", unsafe_allow_html=True)
                        elif sentiment.lower() == "negative":
                            st.markdown(f"<span style='color:salmon'>👎 {comment}</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<span style='color:orange'>😐 {comment}</span>", unsafe_allow_html=True)
