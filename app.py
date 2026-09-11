import streamlit as st
import pandas as pd
import os
from datetime import date

# --- CONFIG ---
st.set_page_config(page_title="Bharat Kisan NOTEBOOK", page_icon="📓", layout="centered")

# --- LANGUAGE DICTIONARY ---
LANG = {
    "English": {
        "title": "📓 Bharat Kisan NOTEBOOK",
        "new": "+ Add New Crop",
        "edit": "✏️ Edit",
        "delete": "🗑️ Delete",
        "crop": "Select Crop",
        "cat": "Category",
        "area": "Area (Guntha)",
        "bhav": "Market Rate Rs/Q",
        "kharch": "💸 All Charges Per Acre",
        "beej": "Seed",
        "khat": "Fertilizer",
        "aushad": "Pesticide",
        "majdoor": "Labour",
        "pani": "Irrigation",
        "other": "Other",
        "weight": "📦 Total Yield",
        "gram": "Gram",
        "kg": "KG",
        "quintal": "Quintal",
        "ton": "Ton",
        "profit": "✅ Net Profit",
        "total_cost": "💸 Total Cost",
        "total_income": "💰 Total Income",
        "save": "💾 Save Page",
        "pages": "📚 My Pages",
        "weather": "🌤️ Weather & Mandi",
        "loan": "🏦 Loan Calculator",
        "download": "📥 Download CSV"
    },
    "Marathi": {
        "title": "Bharat Kisan NOTEBOOK",
        "new": "+ नवीन पीक जोडा",
        "edit": "✏️ बदल करा",
        "delete": "🗑️ हटवा",
        "crop": "पीक निवडा",
        "cat": "प्रकार",
        "area": "क्षेत्र (गुंठा)",
        "bhav": "बाजार भाव Rs/Q",
        "kharch": "💸 सर्व खर्च प्रति एकर",
        "beej": "बीज",
        "khat": "खत",
        "aushad": "औषध",
        "majdoor": "मजूर",
        "pani": "पाणी",
        "other": "इतर",
        "weight": "📦 Total Yield",
        "gram": "Gram",
        "kg": "KG",
        "quintal": "Quintal",
        "ton": "Ton",
        "profit": "✅ शुद्ध लाभ",
        "total_cost": "💸 एकूण खर्च",
        "total_income": "💰 एकूण उत्पन्न",
        "save": "💾 सेव करे",
        "pages": "📚 मेरे पेज",
        "weather": "🌤️ Weather & Mandi",
        "loan": "🏦 Loan Calculator",
        "download": "📥 Download CSV"
    }
}

# --- SIDEBAR ---
lang_choice = st.sidebar.selectbox("Language / भाषा", ["English", "Marathi"])
T = LANG[lang_choice]

# --- MAIN APP ---
st.title(T["title"])
st.markdown("---")

# --- INPUTS ---
crop_name = st.text_input(T["crop"])
col_a1, col_a2 = st.columns(2)
with col_a1:
    area = st.number_input(T["area"], min_value=1.0, value=20.0)
with col_a2:
    rate = st.number_input(T["bhav"], min_value=0.0, value=4000.0)

st.subheader(T["kharch"])
c1, c2 = st.columns(2)
with c1:
    beej = st.number_input(T["beej"], min_value=0.0, value=0.0)
    khat = st.number_input(T["khat"], min_value=0.0, value=0.0)
    aushad = st.number_input(T["aushad"], min_value=0.0, value=0.0)
with c2:
    majdoor = st.number_input(T["majdoor"], min_value=0.0, value=0.0)
    pani = st.number_input(T["pani"], min_value=0.0, value=0.0)
    other = st.number_input(T["other"], min_value=0.0, value=0.0)

st.markdown("---")

# --- YIELD SECTION ---
st.subheader(T["weight"])
y1, y2 = st.columns(2)
with y1:
    yield_qty = st.number_input(T["weight"], min_value=0.0, value=0.0, label_visibility="collapsed")
with y2:
    yield_unit_name = st.selectbox("Unit", [T["gram"], T["kg"], T["quintal"], T["ton"]], label_visibility="collapsed")

# Unit conversion to Quintal
unit_map = {T["gram"]: 0.00001, T["kg"]: 0.01, T["quintal"]: 1.0, T["ton"]: 10.0, "Gram":0.00001, "KG":0.01, "Quintal":1.0, "Ton":10.0}
yield_unit = unit_map.get(yield_unit_name, 1.0)

# --- CALCULATION - FIXED INDENTATION ---
total_cost = beej + khat + aushad + majdoor + pani + other
total_yield = yield_qty * yield_unit
total_income = total_yield * rate
profit = total_income - total_cost

# --- 3 BOXES DISPLAY ---
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(T["total_cost"], f"Rs {total_cost:,.2f}")
with col2:
    st.metric(T["total_income"], f"Rs {total_income:,.2f}")
with col3:
    st.metric(T["profit"], f"Rs {profit:,.2f}")

# --- SAVE ---
st.markdown("---")
if st.button(T["save"]):
    data = {
        "Date": [str(date.today())],
        "Crop": [crop_name],
        "Area_Guntha": [area],
        "Rate": [rate],
        "Total_Cost": [total_cost],
        "Yield_Q": [total_yield],
        "Income": [total_income],
        "Profit": [profit]
    }
    df = pd.DataFrame(data)
    if not os.path.exists("kisan_data.csv"):
        df.to_csv("kisan_data.csv", index=False)
    else:
        df.to_csv("kisan_data.csv", mode='a', header=False, index=False)
    st.success("Saved Successfully!")

# --- SHOW DATA ---
if os.path.exists("kisan_data.csv"):
    st.subheader(T["pages"])
    df_show = pd.read_csv("kisan_data.csv")
    st.dataframe(df_show)
    st.download_button(T["download"], df_show.to_csv(index=False), "kisan_data.csv")