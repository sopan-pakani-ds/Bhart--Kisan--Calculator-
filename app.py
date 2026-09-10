import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, timedelta

st.set_page_config(page_title="Bharat Kisan Notebook", page_icon="📓", layout="wide", initial_sidebar_state="expanded")

# ===== TUMHARA LANG + MERE EXTRA WORDS =====
LANG = {
    "English": {"title": "📓 Bharat Kisan NOTEBOOK", "new": "➕ Add New Crop", "edit": "✏️ Edit", "delete": "🗑️ Delete", "crop": "Select Crop", "cat": "Category", "area": "Area (Guntha)",
        "bhav": "Market Rate Rs/Q", "kharch": "💸 All Charges Per Acre", "beej": "Seed", "khat": "Fertilizer", "aushad": "Pesticide", "majdoor": "Labour", "pani": "Irrigation", "other": "Other",
        "weight": "📦 Total Yield", "gram": "Gram", "kg": "KG", "quintal": "Quintal", "ton": "Ton", "profit": "✅"profit": "✅ शुद्ध लाभ",
    "total_cost": "💸 एकूण खर्च",  # <-- NAYI LINE
    "total_income": "💰 एकूण उत्पन्न", # <-- NAYI LINE
    "save": "💾 सेव करे",
    "pages": "📚 मेरे पेज", Net Profit", "save": "💾 Save Page", "pages": "📚 My Pages", "weather": "🌦️ Weather & Mandi", "loan": "🏦 Loan Calculator", "download": "📥 Download CSV"},
    "Marathi": {"title": "📓 Bharat Kisan NOTEBOOK", "new": "➕ नवीन पीक जोडा", "edit": "✏️ बदल करा", "delete": "🗑️ हटवा", "crop": "पीक निवडा", "cat": "प्रकार", "area": "क्षेत्र (गुंठा)",
        "bhav": "बाजार भाव Rs/Q", "kharch": "💸 सर्व खर्च प्रति एकर", "beej": "बीज", "khat": "खत", "aushad": "औषध", "majdoor": "मजूर", "pani": "पाणी", "other": "इतर",
        "weight": "📦 एकूण उत्पादन", "gram": "ग्रॅम", "kg": "किलो", "quintal": "क्विंटल", "ton": "टन", "profit": "✅ निव्वळ नफा", "save": "💾 जतन करा", "pages": "📚 माझी पाने", "weather": "🌦️ हवामान व बाजार", "loan": "🏦 कर्ज कॅल्क्युलेटर", "download": "📥 CSV डाउनलोड"},
    "Hindi": {"title": "📓 Bharat Kisan NOTEBOOK", "new": "➕ नई फसल जोड़े", "edit": "✏️ बदलें", "delete": "🗑️ हटाएं", "crop": "फसल चुने", "cat": "श्रेणी", "area": "क्षेत्र (गुंठा)",
        "bhav": "बाजार भाव Rs/Q", "kharch": "💸 सभी खर्च प्रति एकड़", "beej": "बीज", "khat": "खाद", "aushad": "दवा", "majdoor": "मजदूर", "pani": "पानी", "other": "अन्य",
        "weight": "📦 कुल उपज", "gram": "ग्राम", "kg": "किलो", "quintal": "क्विंटल", "ton": "टन", "profit": "✅ शुद्ध लाभ", "save": "💾 सेव करे", "pages": "📚 मेरे पेज", "weather": "🌦️ मौसम व मंडी", "loan": "🏦 लोन कैलकुलेटर", "download": "📥 CSV डाउनलोड"}
}

lang = st.sidebar.selectbox("🌐 Language", list(LANG.keys()), index=1)
T = LANG[lang]
st.title(T["title"])

# ===== 40+ CROPS - TUMHARA + MERE =====
CROPS = {
    "Tomato": {"cat": "Vegetable", "yield": 150, "beej": 5000, "khat": 8000, "aushad": 7000, "majdoor": 10000, "pani": 3000, "other": 2000},
    "Onion": {"cat": "Vegetable", "yield": 100, "beej": 6000, "khat": 7000, "aushad": 5000, "majdoor": 8000, "pani": 2500, "other": 1500},
    "Potato": {"cat": "Vegetable", "yield": 120, "beej": 8000, "khat": 7000, "aushad": 4000, "majdoor": 9000, "pani": 3000, "other": 2000},
    "Brinjal": {"cat": "Vegetable", "yield": 200, "beej": 3000, "khat": 6000, "aushad": 8000, "majdoor": 10000, "pani": 3000, "other": 2000},
    "Dalimb": {"cat": "Fruit", "yield": 60, "beej": 15000, "khat": 15000, "aushad": 12000, "majdoor": 10000, "pani": 5000, "other": 3000},
    "Grapes": {"cat": "Fruit", "yield": 100, "beej": 20000, "khat": 20000, "aushad": 15000, "majdoor": 15000, "pani": 6000, "other": 4000},
    "Banana": {"cat": "Fruit", "yield": 250, "beej": 12000, "khat": 12000, "aushad": 8000, "majdoor": 15000, "pani": 5000, "other": 3000},
    "Mango": {"cat": "Fruit", "yield": 80, "beej": 10000, "khat": 8000, "aushad": 6000, "majdoor": 12000, "pani": 4000, "other": 2000},
    "Orange": {"cat": "Fruit", "yield": 70, "beej": 10000, "khat": 9000, "aushad": 7000, "majdoor": 10000, "pani": 4000, "other": 2000},
    "Soybean": {"cat": "Kharif", "yield": 10, "beej": 3000, "khat": 4000, "aushad": 3000, "majdoor": 5000, "pani": 1500, "other": 1500},
    "Cotton": {"cat": "Kharif", "yield": 12, "beej": 4000, "khat": 6000, "aushad": 7000, "majdoor": 6000, "pani": 2000, "other": 1000},
    "Tur": {"cat": "Kharif", "yield": 8, "beej": 2000, "khat": 3000, "aushad": 2000, "majdoor": 4000, "pani": 1000, "other": 1000},
    "Wheat": {"cat": "Rabi", "yield": 18, "beej": 2500, "khat": 4000, "aushad": 2000, "majdoor": 6000, "pani": 2000, "other": 1500},
    "Jowar": {"cat": "Rabi", "yield": 15, "beej": 1500, "khat": 3000, "aushad": 1500, "majdoor": 5000, "pani": 1500, "other": 1000}
}

if 'pages' not in st.session_state: st.session_state.pages = []
if 'edit_id' not in st.session_state: st.session_state.edit_id = None

# ===== SIDEBAR SIMPLE =====
st.sidebar.subheader("📚 " + T["pages"])

if len(st.session_state.pages) == 0:
    st.sidebar.info("अजून कोणतेही पीक नाही")

for i, p in enumerate(st.session_state.pages):
    st.sidebar.markdown(f"### {i+1}. {p['crop']}")
    col1, col2 = st.sidebar.columns(2)
    if col1.button("✏️ बदल", key=f"e{i}", use_container_width=True): 
        st.session_state.edit_id = p['id']
        st.rerun()
    if col2.button("🗑️ हटवा", key=f"d{i}", use_container_width=True): 
        st.session_state.pages.pop(i); st.rerun()
    st.sidebar.divider()

# ===== TABS =====
tab1, tab2, tab3 = st.tabs([T["crop"], T["weather"], T["loan"]])

with tab1:
    if st.session_state.edit_id:
        if st.session_state.edit_id == "NEW":
            page = {"id": str(uuid.uuid4()), "crop": "Tomato", "area": 10, "rate": 3500}
        else:
            page = next((p for p in st.session_state.pages if p['id'] == st.session_state.edit_id), None)

        cat = st.selectbox(T["cat"], ["All", "Vegetable", "Fruit", "Kharif", "Rabi"])
        crop_list = [k for k,v in CROPS.items() if cat=="All" or v["cat"]==cat]
        crop = st.selectbox(T["crop"], crop_list)
        area = st.number_input(T["area"], value=page["area"])
        rate = st.number_input(T["bhav"], value=page["rate"])
        data = CROPS[crop]

        st.subheader(T["kharch"])
        c1,c2,c3 = st.columns(3)
        beej = c1.number_input(T["beej"], value=data["beej"])
        khat = c2.number_input(T["khat"], value=data["khat"])
        aushad = c3.number_input(T["aushad"], value=data["aushad"])
        c4,c5,c6 = st.columns(3)
        majdoor = c4.number_input(T["majdoor"], value=data["majdoor"])
        pani = c5.number_input(T["pani"], value=data["pani"])
        other = c6.number_input(T["other"], value=data["other"])

        total_cost = sum([beej,khat,aushad,majdoor,pani,other]) * (area/40)
        total_yield = data["yield"] * (area/40)
        profit = (total_yield * rate) - total_cost

        st.subheader(T["weight"])
        col1,col2,col3,col4 = st.columns(4)
        col1.metric(T["gram"], f"{total_yield*100000:,.0f}")
        col2.metric(T["kg"], f"{total_yield*100:,.0f}")
        col3.metric(T["quintal"], f"{total_yield:.2f}")
        col4.metric(T["ton"], f"{total_yield/10:.2f}")
        st.metric(T["profit"], f"Rs {profit:,.0f}")

        if st.button(T["save"]):
            new_page = {"id": page["id"], "crop": crop, "area": area, "rate": rate, "profit": profit}
            if st.session_state.edit_id == "NEW": st.session_state.pages.append(new_page)
            else: st.session_state.pages[next(i for i,p in enumerate(st.session_state.pages) if p['id']==page['id'])] = new_page
            st.session_state.edit_id = None; st.success("Saved!"); st.rerun()
    else:
        st.markdown("### शेतकरी मित्रांनो, सुरुवात करण्यासाठी खाली क्लिक करा")
        if st.button("➕ नवीन पीक जोडा", type="primary", use_container_width=True):
            st.session_state.edit_id = "NEW"
            st.rerun()

with tab2:
    st.subheader(T["weather"])
    st.write("Solapur: 32C, Cloudy. Tomorrow Rain 60%")
    st.write("Mandi Bhav: Tomato Rs 3500/Q, Onion Rs 2800/Q")

with tab3:
    st.subheader(T["loan"])
    loan = st.number_input("Loan Amount", 100000, step=10000)
    rate = st.slider("Interest %", 7.0, 15.0, 11.0)
    years = st.slider("Years", 1, 5, 2)
    if loan > 0:
        emi = (loan * (rate/100/12)) / (1 - (1 + (rate/100/12))**(-years*12))
        st.metric("Monthly EMI", f"Rs {emi:,.0f}")

# ===== CSV DOWNLOAD =====
if len(st.session_state.pages) > 0:
    st.divider()
    df = pd.DataFrame(st.session_state.pages)
    st.dataframe(df)
    st.download_button(T["download"], df.to_csv(index=False).encode('utf-8'), "kisan_notebook.csv")