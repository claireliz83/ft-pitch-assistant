import streamlit as st
import pandas as pd
import openai
import os

def safe_display_text(text):
    try:
        return text.encode('utf-8', errors='replace').decode('utf-8')
    except Exception:
        return "⚠️ Error displaying text due to encoding issues."

try:
    # --- Configuration ---
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # --- Load Journalist Data ---
    @st.cache_data
    def load_journalists():
        return pd.read_csv("journalists.csv", encoding="utf-8", on_ba
