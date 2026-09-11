import streamlit as st
import pandas as pd
import uuid

st.set_page_config(page_title="Bharat Kisan Notebook", page_icon="📓", layout="wide", initial_sidebar_state="expanded")

LANG = {
    "English": {"title": "📓 Bharat Kisan NOTEBOOK", "new": "➕ Add New Crop", "edit": "✏️ Edit", "delete": "🗑️ Delete", "crop": "Select Crop", "cat": "Category", "area": "Area (Guntha)",
        "bhav": "Market Rate Rs/Q", "kharch": "💸 All Charges Per Acre", "beej": "Seed", "khat": "Fertilizer", "aushad": "Pesticide", "majdoor": "Labour", "pani": "Irrigation", "other": "Other",
        "weight": "📦 Total Yield", "gram": "Gram", "kg": "KG", "quintal": "Quintal", "ton": "Ton", "profit": "✅ Net Profit", "total_cost": "💸 Total Cost", "total_income": "💰 Total Income", "save": "💾 Save Page", "pages": "📚 My Pages", "weather": "🌦️ Weather & Mandi", "loan": "🏦 Loan Calculator", "download": "📥 Download CSV"},
    "Marathi": {"title": "📓 Bharat Kisan NOTEBOOK", "new": "➕ नवीन पीक जोडा", "edit": "✏️ बदल करा", "delete": "🗑️ हटवा", "crop": "पीक निवडा", "cat": "प्रकार", "area": "क्षेत्र (गुंठा)",
        "bhav": "बाजार भाव Rs/Q", "kharch": "💸 सर्व खर्च प्रति एकर", "beej": "बीज", "khat": "खत", "aushad": "औषध", "majdoor": "मजूर", "pani": "पाणी", "other": "इतर",
        "weight": "📦 एकूण उत्पादन", "gram": "ग्रॅम", "kg": "किलो", "quintal": "क्विंटल", "ton": "टन", "profit": "✅ निव्वळ नफा", "total_cost": "💸 एकूण खर्च", "total_income": "💰 एकूण उत्पन्न", "save": "💾 जतन करा", "pages": "📚 माझी पाने", "weather": "🌦️ हवामान व बाजार", "loan": "🏦 कर्ज कॅल्क्युलेटर", "download": "📥 CSV डाउनलोड"},
    "Hindi": {"title": "📓 Bharat Kisan NOTEBOOK", "new": "➕ नई फसल जोड़े", "edit": "✏️ बदलें", "delete": "🗑️ हटाएं", "crop": "फसल चुने", "cat": "श्रेणी", "area": "क्षेत्र (गुंठा)",
        "bhav": "बाजार भाव Rs/Q", "kharch": "💸 सभी खर्च प्रति एकड़", "beej": "बीज", "khat": "खाद", "aushad": "दवा", "majdoor": "मजदूर", "pani": "पानी", "other": "अन्य",
        "weight": "📦 कुल उपज", "gram": "ग्राम", "kg": "किलो", "quintal": "क्विंटल", "ton": "टन", "profit": "✅ शुद्ध लाभ", "total_cost": "💸 कुल खर्च", "total_income": "💰 कुल आमदनी", "save": "💾 सेव करे", "pages": "📚 मेरे पेज", "weather": "🌦️ मौसम व मंडी", "loan": "🏦 लोन कैलकुलेटर", "download": "📥 CSV डाउनलोड"}
}

lang = st.sidebar.selectbox("🌐 Language", list(LANG.keys()), index=1)
T = LANG[lang]
st.title(T["title"])

CROPS = {
    "Tomato": {"cat": "Vegetable", "yield": 150, "beej": 5000, "khat": 8000, "aushad": 7000, "majdoor": 10000, "pani": 3000, "other": 2000},
    "Onion": {"cat": "Vegetable", "yield": 100, "beej": 6000, "khat": 7000, "aushad": 5000, "majdoor": 8000, "pani": 2500, "other": 1500},
    "Potato": {"cat": "Vegetable", "yield": 120, "beej": 8000, "khat": 7000, "aushad": 4000, "majdoor": 9000, "pani": 3000, "other": 2000},
    "Brinjal": {"cat": "Vegetable", "yield": 200, "beej": 3000, "khat": 6000, "aushad": 8000, "majdoor": 10000, "pani": 3000, "other": 2000},
    "Dalimb": {"cat": "Fruit", "yield": 60, "beej": 15000, "khat": 15000, "aushad": 12000, "majdoor": 10000, "pani": 5000, "other": 3000},
    "Grapes": {"cat": "Fruit", "yield": 100, "beej": 20000, "khat": 20000, "aushad": 15000, "majdoor": 15000, "pani": 6000, "other": 4000},
    "Banana": {"cat": "Fruit", "yield": 250, "beej": 12000, "khat": 12000, "aushad": 8000, "majdoor": 15000, "pani": 5000, "other": 3000},
    "Mango": {"cat": "Fruit", "yield": 80, "beej": 10000, "khat": 8000, "aushad": 6000, "majdoor": 12000, "pani": 4000, "other": 2000},
    "Soybean": {"cat": "Kharif", "yield": 10, "beej": 3000, "khat": 4000, "aushad": 3000, "majdoor": 5000, "pani": 1500, "other": 1500},
    "Cotton": {"cat": "Kharif", "yield": 12, "beej": 4000, "khat": 6000, "aushad": 7000, "majdoor": 6000, "pani": 2000, "other": 1000},
    "Wheat": {"cat": "Rabi", "yield": 18, "beej": 2500, "khat": 4000, "aushad": 2000, "majdoor": 6000, "pani": 2000, "other": 1500},
    "Jowar": {"cat": "Rabi", "yield": 15, "beej": 1500, "khat": 3000, "aushad": 1500, "majdoor": 5000, "pani": 1500, "other": 1000}
}

if 'pages' not in st.session_state:
    st.session_state.pages = []
if 'edit_id' not in st.session_state:
    st.session_state.edit_id = None

st.sidebar.subheader(T["pages"])
for i, p in enumerate(st.session_state.pages):
    col1, col2, col3 = st.sidebar.columns([4, 1, 1])
    col1.write(f"{i+1}. {p['crop']}")
    if col2.button(T["edit"], key=f"e{i}"):
        st.session_state.edit_id = p['id']
        st.rerun()
    if col3.button(T["delete"], key=f"d{i}"):
        st.session_state.pages.pop(i)
        st.rerun()

tab1, tab2, tab3 = st.tabs([T["crop"], T["weather"], T["loan"]])

with tab1:
    if not st.session_state.edit_id:
        st.markdown("### 👇 नयी फसल जोड़ने के लिए नीचे दबाएं")
        if st.button(T["new"], type="primary", use_container_width=True):
            st.session_state.edit_id = "NEW"
            st.rerun()
        st.info("💡 Tip: ऊपर वाले नीले बटन पर क्लिक करो")
    else:
        if st.session_state.edit_id == "NEW":
            page = {"id": str(uuid.uuid4()), "crop": "Tomato", "area": 10, "rate": 3500}
        else:
            page = next((p for p in st.session_state.pages if p['id'] == st.session_state.edit_id), None)
            if page is None:
                st.session_state.edit_id = None
                st.rerun()

        cat = st.selectbox(T["cat"], ["All", "Vegetable", "Fruit", "Kharif", "Rabi"])
        crop_list = [k for k, v in CROPS.items() if cat == "All" or v["cat"] == cat]
        crop = st.selectbox(T["crop"], crop_list)
        area = st.number_input(T["area"], value=float(page.get("area", 10)))
        rate = st.number_input(T["bhav"], value=float(page.get("rate", 3500)))
        data = CROPS[crop]

        st.subheader(T["kharch"])
        c1, c2, c3 = st.columns(3)
        beej = c1.number_input(T["beej"], value=float(data["beej"]))
        khat = c2.number_input(T["khat"], value=float(data["khat"]))
        aushad = c3.number_input(T["aushad"], value=float(data["aushad"]))
        c4, c5, c6 = st.columns(3)
        majdoor = c4.number_input(T["majdoor"], value=float(data["majdoor"]))
        pani = c5.number_input(T["pani"], value=float(data["pani"]))
        other = c6.number_input(T["other"], value=float(data["other"]))

        st.subheader(T["weight"])
        y1, y2 = st.columns([2, 1])
        with y1:
            yield_input = st.number_input("Total Yield Quantity", value=float(data["yield"]), min_value=0.0)
        with y2:
            unit_choice = st.selectbox("Unit", [T["gram"], T["kg"], T["quintal"], T["ton"]])

        unit_map = {
            T["gram"]: 0.00001, T["kg"]: 0.01, T["quintal"]: 1.0, T["ton"]: 10.0,
            "Gram": 0.00001, "KG": 0.01, "Quintal": 1.0, "Ton": 10.0,
            "ग्रॅम": 0.00001, "किलो": 0.01, "क्विंटल": 1.0, "टन": 10.0, "ग्राम": 0.00001
        }
        conv = unit_map.get(unit_choice, 1.0)
        total_yield_user = yield_input * conv

        col1, col2, col3, col4 = st.columns(4)
        col1.metric(T["gram"], f"{total_yield_user*100000:,.0f}")
        col2.metric(T["kg"], f"{total_yield_user*100:,.0f}")
        col3.metric(T["quintal"], f"{total_yield_user:.2f}")
        col4.metric(T["ton"], f"{total_yield_user/10:.2f}")

        total_cost_per_acre = beej + khat + aushad + majdoor + pani + other
        total_cost = (total_cost_per_acre * area) / 40
        total_yield = total_yield_user * (area / 40)
        total_income = total_yield * rate
        profit = total_income - total_cost

        st.divider()
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(T["total_cost"], f"Rs {total_cost:,.0f}")
        with m2:
            st.metric(T["total_income"], f"Rs {total_income:,.0f}")
        with m3:
            st.metric(T["profit"], f"Rs {profit:,.0f}")

        c_save, c_cancel = st.columns(2)
        with c_save:
            if st.button(T["save"], use_container_width=True, type="primary"):
                new_page = {
                    "id": page["id"], "crop": crop, "area": area, "rate": rate,
                    "beej": beej, "khat": khat, "aushad": aushad, "majdoor": majdoor, "pani": pani, "other": other,
                    "total_cost": total_cost, "total_yield_q": total_yield, "total_income": total_income, "profit": profit
                }
                if st.session_state.edit_id == "NEW":
                    st.session_state.pages.append(new_page)
                else:
                    idx = next((i for i, p in enumerate(st.session_state.pages) if p['id'] == page['id']), 0)
                    st.session_state.pages[idx] = new_page
                st.session_state.edit_id = None
                st.success("Saved!")
                st.rerun()
        with c_cancel:
            if st.button("⬅️ Back / मागे", use_container_width=True):
                st.session_state.edit_id = None
                st.rerun()

with tab2:
    st.subheader(T["weather"])
    loc = st.text_input("📍 Tumcha Gaav / Village", "Sindkhed, Maharashtra")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("🌡️ Temperature", "32°C", "2°C")
    with c2:
        st.metric("💧 Humidity", "65%")
    with c3:
        st.metric("🌧️ Rain Chance", "60%", "-10%")
    st.info(f"📍 {loc} - Aaj: Thoda Dhund, Kal: Halki Baarish ki sambhavna")
    st.divider()
    st.subheader("🧅 Mandi Bhav - Aaj ka Bhav")
    mandi_data = {
        "Crop": ["Tomato", "Onion", "Potato", "Soybean", "Cotton"],
        "Bhav (Rs/Q)": [3500, 2800, 2200, 4800, 7200],
        "Kal ka Bhav": [3400, 2700, 2100, 4750, 7100]
    }
    st.table(pd.DataFrame(mandi_data))

with tab3:
    st.subheader(T["loan"])
    loan = st.number_input("Loan Amount", 100000, step=10000)
    rate_l = st.slider("Interest %", 7.0, 15.0, 11.0)
    years = st.slider("Years", 1, 5, 2)
    emi = (loan * (rate_l/100/12)) / (1 - (1 + (rate_l/100/12))**(-years*12))
    st.metric("Monthly EMI", f"Rs {emi:,.0f}")

if len(st.session_state.pages) > 0:
    st.divider()
    df = pd.DataFrame(st.session_state.pages)
    st.dataframe(df, use_container_width=True)
    st.download_button(T["download"], df.to_csv(index=False).encode('utf-8'), "kisan_notebook.csv", use_container_width=True)