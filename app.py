import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="Bharat Kisan PRO", page_icon="🇮🇳", layout="centered")

# ===== 8 LANGUAGES DICTIONARY =====
LANG = {
    "English": {"title": "🇮🇳 Bharat Kisan PRO - Pakani", "farmer": "Farmer Name", "cat": "Category", "crop": "Select Crop", "area": "Area (Guntha)", "bhav": "Market Rate (Rs/Q)", "kharch": "All Charges (Per Acre)", "save": "💾 Save Hisab - Old Hisab", "profit": "Net Profit", "old": "My Old Hisab", "no_hisab": "No hisab saved yet.", "share": "WhatsApp Share", "kharch_l": "Total Cost", "income_l": "Total Income"},
    "Marathi (मराठी)": {"title": "🇮🇳 Bharat Kisan PRO - पाकणी", "farmer": "शेतकरी नाव", "cat": "प्रकार", "crop": "पीक निवडा", "area": "क्षेत्र (गुंठा)", "bhav": "बाजार भाव (Rs/Q)", "kharch": "सर्व खर्च (प्रति एकर)", "save": "💾 हिशोब जतन करा", "profit": "निव्वळ नफा", "old": "माझा जुना हिशोब", "no_hisab": "अजून हिशोब नाही.", "share": "WhatsApp वर शेअर करा", "kharch_l": "एकूण खर्च", "income_l": "एकूण उत्पन्न"},
    "Hindi (हिंदी)": {"title": "🇮🇳 भारत किसान PRO", "farmer": "किसान का नाम", "cat": "श्रेणी", "crop": "फसल चुनें", "area": "क्षेत्र (गुंठा)", "bhav": "बाजार भाव", "kharch": "सभी खर्च", "save": "💾 हिसाब सेव करें", "profit": "शुद्ध लाभ", "old": "मेरा पुराना हिसाब", "no_hisab": "अभी कोई हिसाब नहीं।", "share": "WhatsApp पर शेयर करें", "kharch_l": "कुल खर्च", "income_l": "कुल आय"},
    "Kannada (ಕನ್ನಡ)": {"title": "🇮🇳 ಭಾರತ್ ಕಿಸಾನ್ PRO", "farmer": "ರೈತರ ಹೆಸರು", "cat": "ವರ್ಗ", "crop": "ಬೆಳೆ ಆಯ್ಕೆ", "area": "ಪ್ರದೇಶ (ಗುಂಠಾ)", "bhav": "ಮಾರುಕಟ್ಟೆ ದರ", "kharch": "ಎಲ್ಲಾ ಖರ್ಚುಗಳು", "save": "💾 ಲೆಕ್ಕ ಉಳಿಸಿ", "profit": "ನಿವ್ವಳ ಲಾಭ", "old": "ನನ್ನ ಹಳೆಯ ಲೆಕ್ಕ", "no_hisab": "ಇನ್ನೂ ಲೆಕ್ಕವಿಲ್ಲ.", "share": "WhatsApp ನಲ್ಲಿ ಹಂಚಿಕೊಳ್ಳಿ", "kharch_l": "ಒಟ್ಟು ವೆಚ್ಚ", "income_l": "ಒಟ್ಟು ಆದಾಯ"},
    "Telugu (తెలుగు)": {"title": "🇮🇳 భారత్ కిసాన్ PRO", "farmer": "రైతు పేరు", "cat": "వర్గం", "crop": "పంట ఎంచుకోండి", "area": "విస్తీర్ణం (గుంటా)", "bhav": "మార్కెట్ ధర", "kharch": "అన్ని ఖర్చులు", "save": "💾 లెక్క సేవ్ చేయండి", "profit": "నికర లాభం", "old": "నా పాత లెక్కలు", "no_hisab": "ఇంకా లెక్క లేదు.", "share": "WhatsApp లో షేర్", "kharch_l": "మొత్తం ఖర్చు", "income_l": "మొత్తం ఆదాయం"},
    "Tamil (தமிழ்)": {"title": "🇮🇳 பாரத் கிசான் PRO", "farmer": "விவசாயி பெயர்", "cat": "வகை", "crop": "பயிர்", "area": "பரப்பு", "bhav": "சந்தை விலை", "kharch": "செலவுகள்", "save": "💾 சேமிக்கவும்", "profit": "லாபம்", "old": "பழைய கணக்கு", "no_hisab": "கணக்கு இல்லை.", "share": "WhatsApp பகிரவும்", "kharch_l": "செலவு", "income_l": "வருமானம்"},
    "Gujarati (ગુજરાતી)": {"title": "🇮🇳 ભારત કિસાન PRO", "farmer": "ખેડૂતનું નામ", "cat": "શ્રેણી", "crop": "પાક", "area": "વિસ્તાર", "bhav": "બજાર ભાવ", "kharch": "બધા ખર્ચા", "save": "💾 હિસાબ સેવ કરો", "profit": "નફો", "old": "જૂનો હિસાબ", "no_hisab": "કોઈ હિસાબ નથી.", "share": "WhatsApp શેર", "kharch_l": "કુલ ખર્ચ", "income_l": "કુલ આવક"},
    "Punjabi (ਪੰਜਾਬੀ)": {"title": "🇮🇳 ਭਾਰਤ ਕਿਸਾਨ PRO", "farmer": "ਕਿਸਾਨ ਦਾ ਨਾਮ", "cat": "ਸ਼੍ਰੇਣੀ", "crop": "ਫਸਲ", "area": "ਖੇਤਰ", "bhav": "ਮੰਡੀ ਭਾਅ", "kharch": "ਖਰਚੇ", "save": "💾 ਹਿਸਾਬ ਸੇਵ ਕਰੋ", "profit": "ਲਾਭ", "old": "ਪੁਰਾਣਾ ਹਿਸਾਬ", "no_hisab": "ਕੋਈ ਹਿਸਾਬ ਨਹੀਂ।", "share": "WhatsApp ਸਾਂਝਾ", "kharch_l": "ਕੁੱਲ ਖਰਚ", "income_l": "ਕੁੱਲ ਆਮਦਨ"},
}

# LANGUAGE BUTTON
selected_lang = st.selectbox("🌐 Language / भाषा / భాష / ಭಾಷೆ", list(LANG.keys()), index=1)
T = LANG[selected_lang]

st.title(T["title"])
st.caption("PAH Solapur University | Pakani, Solapur | All India Languages")
st.divider()

# CROP DB 50+
CROP_DATABASE = {
    "Tomato": {"cat": "Vegetable", "yield_q": 150, "beej": 5000, "khat": 8000, "aushad": 7000, "majdoor": 10000, "pani": 3000, "other": 2000},
    "Onion (Kanda)": {"cat": "Vegetable", "yield_q": 100, "beej": 6000, "khat": 7000, "aushad": 5000, "majdoor": 8000, "pani": 2500, "other": 1500},
    "Soybean": {"cat": "Kharif Crop", "yield_q": 10, "beej": 3000, "khat": 4000, "aushad": 3000, "majdoor": 5000, "pani": 1500, "other": 1500},
    "Cotton": {"cat": "Kharif Crop", "yield_q": 12, "beej": 4000, "khat": 6000, "aushad": 7000, "majdoor": 6000, "pani": 2000, "other": 1000},
    "Wheat": {"cat": "Rabi Crop", "yield_q": 18, "beej": 2500, "khat": 4000, "aushad": 2000, "majdoor": 6000, "pani": 2000, "other": 1500},
    "Pomegranate (Dalimb)": {"cat": "Fruit", "yield_q": 60, "beej": 15000, "khat": 15000, "aushad": 12000, "majdoor": 10000, "pani": 5000, "other": 3000},
    "Grapes": {"cat": "Fruit", "yield_q": 100, "beej": 20000, "khat": 20000, "aushad": 15000, "majdoor": 15000, "pani": 6000, "other": 4000},
    "Banana": {"cat": "Fruit", "yield_q": 250, "beej": 12000, "khat": 12000, "aushad": 8000, "majdoor": 15000, "pani": 5000, "other": 3000},
}
for c in ["Tur","Moong","Jowar","Brinjal","Chilli","Potato","Watermelon","Fig - Solapur Special","Mango","Papaya"]:
    if c not in CROP_DATABASE:
        CROP_DATABASE[c] = {"cat": "Other", "yield_q": 50, "beej": 4000, "khat": 5000, "aushad": 4000, "majdoor": 6000, "pani": 2000, "other": 1500}

if 'history' not in st.session_state:
    st.session_state.history = []

# INPUTS
farmer_name = st.text_input(f"👨‍🌾 {T['farmer']}", "Dinkar Kaka, Pakani")
cat_filter = st.selectbox(f"📂 {T['cat']}", ["All"] + sorted(list(set([v["cat"] for v in CROP_DATABASE.values()]))))
crop_list = list(CROP_DATABASE.keys()) if cat_filter=="All" else [k for k,v in CROP_DATABASE.items() if v["cat"]==cat_filter]
selected_crop = st.selectbox(f"🌱 {T['crop']}", crop_list)
crop = CROP_DATABASE[selected_crop]

area_guntha = st.number_input(f"📏 {T['area']}", min_value=1, value=10)
area_acre = area_guntha / 40.0
market_rate = st.number_input(f"💰 {T['bhav']} - Solapur APMC", value=3500, step=100)

st.subheader(f"💸 {T['kharch']}")
c1, c2, c3 = st.columns(3)
beej = c1.number_input("Beej", value=crop["beej"])
khat = c2.number_input("Khat", value=crop["khat"])
aushad = c3.number_input("Aushad", value=crop["aushad"])
c4, c5, c6 = st.columns(3)
majdoor = c4.number_input("Majdoor", value=crop["majdoor"])
pani = c5.number_input("Pani", value=crop["pani"])
other = c6.number_input("Transport+Other", value=crop["other"])

cost_per_acre = beej+khat+aushad+majdoor+pani+other
total_cost = cost_per_acre * area_acre
total_yield = crop["yield_q"] * area_acre
total_income = total_yield * market_rate
profit = total_income - total_cost
roi = (profit/total_cost*100) if total_cost>0 else 0

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric(T["kharch_l"], f"Rs {total_cost:,.0f}")
m2.metric(T["income_l"], f"Rs {total_income:,.0f}")
m3.metric(f"✅ {T['profit']}", f"Rs {profit:,.0f}", delta=f"{roi:.1f}%")

# OLD HISAB BUTTON - MAIN FEATURE
if st.button(T["save"], type="primary", use_container_width=True):
    record = {"Date": datetime.now().strftime("%d-%m-%Y"), "Language": selected_lang, "Farmer": farmer_name, "Crop": selected_crop, "Guntha": area_guntha, "Profit": round(profit), "ROI%": round(roi,1)}
    st.session_state.history.append(record)
    st.success(f"✅ Saved in {T['old']}!")
    st.balloons()

# WHATSAPP SHARE
wa_text = f"{T['title']}\nFarmer: {farmer_name}\nCrop: {selected_crop} {area_guntha}G\nProfit: Rs {profit:.0f} ({roi:.1f}% ROI)\nLang: {selected_lang}\nPAH Solapur University"
st.link_button(f"💬 {T['share']}", f"https://wa.me/?text={urllib.parse.quote(wa_text)}", use_container_width=True)

# OLD HISAB TABLE
st.divider()
st.subheader(f"📚 {T['old']} ({len(st.session_state.history)})")
if len(st.session_state.history) > 0:
    df_hist = pd.DataFrame(st.session_state.history)
    st.dataframe(df_hist, use_container_width=True)
    st.download_button("📥 Download All Hisab CSV", df_hist.to_csv(index=False).encode('utf-8'), "kisan_hisab.csv", "text/csv", use_container_width=True)
    if st.button("🗑️ Clear All Hisab"):
        st.session_state.history = []
        st.rerun()
else:
    st.info(T["no_hisab"])

# CHART - No external library needed
st.bar_chart(pd.DataFrame({"Kharch": [beej, khat, aushad, majdoor, pani, other]}, index=["Beej","Khat","Aushad","Majdoor","Pani","Other"]))