import streamlit as st
import pandas as pd
import uuid

st.set_page_config(page_title="Bharat Kisan Notebook", page_icon="📓", layout="wide")

# ===== 3 LANGUAGES =====
LANG = {
    "English": {
        "title": "📓 Bharat Kisan NOTEBOOK", "new": "➕ Add New Crop", "crop": "Select Crop", "area": "Area (Guntha)",
        "bhav": "Market Rate Rs/Q", "kharch": "All Charges Per Acre", "beej": "Seed", "khat": "Fertilizer", "aushad": "Pesticide",
        "majdoor": "Labour", "pani": "Irrigation", "other": "Other", "weight": "Total Yield", "gram": "Gram", "kg": "KG",
        "quintal": "Quintal", "ton": "Ton", "profit": "Net Profit", "save": "💾 Save Page", "pages": "📚 My Pages"
    },
    "Marathi": {
        "title": "📓 Bharat Kisan NOTEBOOK", "new": "➕ नवीन पीक जोडा", "crop": "पीक निवडा", "area": "क्षेत्र (गुंठा)",
        "bhav": "बाजार भाव Rs/Q", "kharch": "सर्व खर्च प्रति एकर", "beej": "बीज", "khat": "खत", "aushad": "औषध",
        "majdoor": "मजूर", "pani": "पाणी", "other": "इतर", "weight": "एकूण उत्पादन", "gram": "ग्रॅम", "kg": "किलो",
        "quintal": "क्विंटल", "ton": "टन", "profit": "निव्वळ नफा", "save": "💾 जतन करा", "pages": "📚 माझी पाने"
    },
    "Hindi": {
        "title": "📓 Bharat Kisan NOTEBOOK", "new": "➕ नई फसल जोड़े", "crop": "फसल चुने", "area": "क्षेत्र (गुंठा)",
        "bhav": "बाजार भाव Rs/Q", "kharch": "सभी खर्च प्रति एकड़", "beej": "बीज", "khat": "खाद", "aushad": "दवा",
        "majdoor": "मजदूर", "pani": "पानी", "other": "अन्य", "weight": "कुल उपज", "gram": "ग्राम", "kg": "किलो",
        "quintal": "क्विंटल", "ton": "टन", "profit": "शुद्ध लाभ", "save": "💾 सेव करे", "pages": "📚 मेरे पेज"
    }
}

lang = st.sidebar.selectbox("🌐 Language", list(LANG.keys()))
T = LANG[lang]
st.title(T["title"])

# CROPS
CROPS = {
    "Tomato": {"yield": 150, "beej": 5000, "khat": 8000, "aushad": 7000, "majdoor": 10000, "pani": 3000, "other": 2000},
    "Onion": {"yield": 100, "beej": 6000, "khat": 7000, "aushad": 5000, "majdoor": 8000, "pani": 2500, "other": 1500},
    "Wheat": {"yield": 18, "beej": 2500, "khat": 4000, "aushad": 2000, "majdoor": 6000, "pani": 2000, "other": 1500},
    "Dalimb": {"yield": 60, "beej": 15000, "khat": 15000, "aushad": 12000, "majdoor": 10000, "pani": 5000, "other": 3000},
    "Soybean": {"yield": 10, "beej": 3000, "khat": 4000, "aushad": 3000, "majdoor": 5000, "pani": 1500, "other": 1500}
}

if 'pages' not in st.session_state:
    st.session_state.pages = []

st.sidebar.subheader(T["pages"])
if st.sidebar.button(T["new"]):
    st.session_state.pages.append({"id": str(uuid.uuid4()), "crop": "Tomato", "area": 10, "rate": 3500})

for i, p in enumerate(st.session_state.pages):
    st.sidebar.write(f"{i+1}. {p['crop']}")

# MAIN FORM
if len(st.session_state.pages) > 0:
    page = st.session_state.pages[-1]
    crop = st.selectbox(T["crop"], list(CROPS.keys()))
    area = st.number_input(T["area"], value=page["area"])
    rate = st.number_input(T["bhav"], value=page["rate"])
    data = CROPS[crop]

    st.subheader(T["kharch"])
    c1, c2, c3 = st.columns(3)
    beej = c1.number_input(T["beej"], value=data["beej"])
    khat = c2.number_input(T["khat"], value=data["khat"])
    aushad = c3.number_input(T["aushad"], value=data["aushad"])

    total_cost = (beej+khat+aushad+data["majdoor"]+data["pani"]+data["other"]) * (area/40)
    total_yield = data["yield"] * (area/40)
    profit = (total_yield * rate) - total_cost

    st.subheader(T["weight"])
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(T["gram"], f"{total_yield*100000:,.0f}")
    col2.metric(T["kg"], f"{total_yield*100:,.0f}")
    col3.metric(T["quintal"], f"{total_yield:.2f}")
    col4.metric(T["ton"], f"{total_yield/10:.2f}")

    st.metric(T["profit"], f"Rs {profit:,.0f}")

    if st.button(T["save"]):
        st.success("Saved!")
else:
    st.info("Click 'Add New Crop' from sidebar")