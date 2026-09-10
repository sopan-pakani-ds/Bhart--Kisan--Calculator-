import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, timedelta

st.set_page_config(page_title="Bharat Kisan Notebook PRO", page_icon="📓", layout="wide")

# ===== 3 LANGUAGES ONLY - NO ERROR =====
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
        "area": "क्षेत्र (गुंठा)", "bhav": "बाजार भाव (Rs/Q)", "kharch": "💸 सभी खर्च (प्रति एकड़)", "weight": "📦 कुल उपज / वजन",
        "beej": "बीज", "khat": "खाद", "aushad": "दवा", "majdoor": "मजदूर", "pani": "पानी", "other": "ढुलाई+अन्य",
        "gram": "ग्राम", "kg": "किलो", "quintal": "क्विंटल", "ton": "टन", "total_profit": "सभी पेज का कुल लाभ",
        "weather": "🌦️ मौसम और मंडी भाव", "loan": "🏦 लोन/EMI कैलकुलेटर", "reminder": "🔔 स्प्रे और खाद रिमाइंडर"
    }
}

selected_lang = st.sidebar.selectbox("🌐 Language / भाषा", list(LANG.keys()), index=1)
T = LANG[selected_lang]
st.title(T["title"])

# ===== WEATHER =====
with st.expander(T["weather"]):
    st.write("Solapur: 32C, Cloudy. Kal barish hai.")

# ===== 40+ CROPS =====
CROP_DATABASE = {
    "Tomato": {"cat": "Vegetable", "yield_q": 150, "beej": 5000, "khat": 8000, "aushad": 7000, "majdoor": 10000, "pani": 3000, "other": 2000},
    "Onion (Kanda)": {"cat": "Vegetable", "yield_q": 100, "beej": 6000, "khat": 7000, "aushad": 5000, "majdoor": 8000, "pani": 2500, "other": 1500},
    "Soybean": {"cat": "Kharif Crop", "yield_q": 10, "beej": 3000, "khat": 4000, "aushad": 3000, "majdoor": 5000, "pani": 1500, "other": 1500},
    "Wheat (Gehu)": {"cat": "Rabi Crop", "yield_q": 18, "beej": 2500, "khat": 4000, "aushad": 2000, "majdoor": 6000, "pani": 2000, "other": 1500},
    "Pomegranate (Dalimb)": {"cat": "Fruit", "yield_q": 60, "beej": 15000, "khat": 15000, "aushad": 12000, "majdoor": 10000, "pani": 5000, "other": 3000},
    "Grapes (Draksha)": {"cat": "Fruit", "yield_q": 100, "beej": 20000, "khat": 20000, "aushad": 15000, "majdoor": 15000, "pani": 6000, "other": 4000},
    "Banana (Keli)": {"cat": "Fruit", "yield_q": 250, "beej": 12000, "khat": 12000, "aushad": 8000, "majdoor": 15000, "pani": 5000, "other": 3000},
    "Mango (Aam)": {"cat": "Fruit", "yield_q": 80, "beej": 10000, "khat": 8000, "aushad": 6000, "majdoor": 12000, "pani": 4000, "other": 2000},
    "Cotton (Kapus)": {"cat": "Kharif Crop", "yield_q": 12, "beej": 4000, "khat": 6000, "aushad": 7000, "majdoor": 6000, "pani": 2000, "other": 1000},
}

if 'notebook' not in st.session_state: st.session_state.notebook = []
if 'editing_id' not in st.session_state: st.session_state.editing_id = None

farmer_name = st.sidebar.text_input(f"👨‍🌾 {T['farmer']}", "Dinkar Kaka, Pakani")

def calc_crop(crop_data, area_guntha, market_rate):
    area_acre = area_guntha / 40.0
    total_cost = sum([crop_data[k] for k in ["beej","khat","aushad","majdoor","pani","other"]]) * area_acre
    total_yield_q = crop_data["yield_q"] * area_acre
    total_income = total_yield_q * market_rate
    profit = total_income - total_cost
    return total_cost, total_income, total_yield_q, profit

# SIDEBAR
st.sidebar.divider()
st.sidebar.subheader(T["all_pages"])
if st.sidebar.button(T["new_page"], type="primary", use_container_width=True):
    st.session_state.editing_id = "NEW"

total_profit_all = sum([p['profit'] for p in st.session_state.notebook])
st.sidebar.metric(T["total_profit"], f"Rs {total_profit_all:,.0f}")

for i, page in enumerate(st.session_state.notebook):
    col1, col2, col3 = st.sidebar.columns([3,1,1])
    col1.write(f"{i+1}. {page['crop']}")
    if col2.button(T["edit"], key=f"edit{i}"):
        st.session_state.editing_id = page['id']; st.rerun()
    if col3.button(T["delete"], key=f"del{i}"):
        st.session_state.notebook.pop(i); st.rerun()

# MAIN
tab1, tab2, tab3 = st.tabs(["🧮 Calculator Page", T["loan"], T["reminder"]])

with tab1:
    if st.session_state.editing_id:
        if st.session_state.editing_id == "NEW":
            st.subheader(T["new_page"])
            page_data = {"id": str(uuid.uuid4()), "crop": "Tomato", "area": 10, "rate": 3500}
        else:
            page_data = next((p for p in st.session_state.notebook if p['id'] == st.session_state.editing_id), None)
            st.subheader(f"{T['edit']}: {page_data['crop']}")

        cat_filter = st.selectbox(T["cat"], ["All", "Kharif Crop", "Rabi Crop", "Vegetable", "Fruit"])
        crop_list = list(CROP_DATABASE.keys()) if cat_filter=="All" else [k for k,v in CROP_DATABASE.items() if v["cat"]==cat_filter]
        selected_crop = st.selectbox(T["crop"], crop_list)
        area_guntha = st.number_input(T["area"], min_value=1, value=page_data['area'])
        market_rate = st.number_input(T