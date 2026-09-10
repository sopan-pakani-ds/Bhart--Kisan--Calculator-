import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, timedelta

st.set_page_config(page_title="Bharat Kisan Notebook PRO", page_icon="📓", layout="wide")

# ===== 3 LANGUAGES ONLY =====
LANG = {
    "English": {
        "title": "📓 Bharat Kisan NOTEBOOK PRO", "new_page": "➕ Add New Crop Page", "edit": "✏️ Edit", "delete": "🗑️ Delete",
        "save_page": "💾 Save This Page", "all_pages": "📚 My Crop Pages", "farmer": "Farmer Name", "crop": "Select Crop", "cat": "Category",
        "area": "Area (Guntha)", "bhav": "Market Rate (Rs/Q)", "kharch": "💸 All Charges (Per Acre)", "weight": "📦 Total Yield / Weight",
        "beej": "Seed", "khat": "Fertilizer", "aushad": "Pesticide", "majdoor": "Labour", "pani": "Irrigation", "other": "Transport+Other",
        "gram": "Gram", "kg": "KG", "quintal": "Quintal", "ton": "Ton", "total_profit": "Total Profit of All Pages",
        "weather": "🌦️ Weather & Mandi Bhav", "loan": "🏦 Loan/EMI Calculator", "reminder": "🔔 Spray & Khad Reminder"
    },
    "Marathi (Marathi)": {
        "title": "📓 Bharat Kisan NOTEBOOK PRO", "new_page": "➕ नवीन पीक पान जोडा", "edit": "✏️ बदल करा", "delete": "🗑️ हटवा",
        "save_page": "💾 हे पान जतन करा", "all_pages": "📚 माझी पीक पाने", "farmer": "शेतकरी नाव", "crop": "पीक निवडा", "cat": "प्रकार",
        "area": "क्षेत्र (गुंठा)", "bhav": "बाजार भाव (Rs/Q)", "kharch": "💸 सर्व खर्च (प्रति एकर)", "weight": "📦 एकूण उत्पादन / वजन",
        "beej": "बीज", "khat": "खत", "aushad": "औषध", "majdoor": "मजूर", "pani": "पाणी", "other": "वाहतूक+इतर",
        "gram": "ग्रॅम", "kg": "किलो", "quintal": "क्विंटल", "ton": "टन", "total_profit": "सर्व पानांचा एकूण नफा",
        "weather": "🌦️ हवामान व बाजार भाव", "loan": "🏦 कर्ज/EMI कॅल्क्युलेटर", "reminder": "🔔 फवारणी व खत रिमाइंडर"
    },
    "Hindi (Hindi)": {
        "title": "📓 Bharat Kisan NOTEBOOK PRO", "new_page": "➕ नई फसल का पेज जोड़ें", "edit": "✏️ संपादित करें", "delete": "🗑️ हटाएं",
        "save_page": "💾 इस पेज को सेव करें", "all_pages": "📚 मेरे फसल के पेज", "farmer": "किसान का नाम", "crop": "फसल चुनें", "cat": "श्रेणी",
        "area": "क्षेत्र (गुंठा)", "bhav": "बाजार भाव (Rs/Q)", "kharch": "💸 सभी खर्च (प्रति एकड़)",