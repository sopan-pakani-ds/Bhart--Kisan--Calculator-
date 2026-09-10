import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bharat Kisan", page_icon="🇮🇳", layout="wide")

# 3 LANGUAGES
LANG = {
    "English": {"title": "Bharat Kisan PRO", "crop": "Select Crop", "area": "Area Guntha", "save": "Save"},
    "Marathi": {"title": "Bharat Kisan PRO", "crop": "पीक निवडा", "area": "क्षेत्र गुंठा", "save": "जतन करा"},
    "Hindi": {"title": "Bharat Kisan PRO", "crop": "फसल चुने", "area": "क्षेत्र गुंठा", "save": "सेव करे"}
}

lang = st.sidebar.selectbox("Language", list(LANG.keys()))
T = LANG[lang]
st.title(T["title"])

CROPS = ["Tomato", "Onion", "Wheat", "Dalimb", "Soybean"]

crop = st.selectbox(T["crop"], CROPS)
area = st.number_input(T["area"], 10)

if st.button(T["save"]):
    st.success(f"{crop} saved for {area} guntha!")

st.write("This is working version. Now we will add Notebook + Weight + All Fruits step by step")