import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Bharat Kisan NOTEBOOK", page_icon="📓", layout="centered")

LANG = {
    "English": {
        "title": "📓 Bharat Kisan NOTEBOOK", "new": "+ Add New Crop", "edit": "✏️ Edit", "delete": "🗑️ Delete",
        "crop": "Select Crop", "cat": "Category", "area": "Area (Guntha)", "bhav": "Market Rate Rs/Q",
        "kharch": "💸 All Charges Per Acre", "beej": "Seed", "khat": "Fertilizer", "aushad": "Pesticide",
        "majdoor": "Labour", "pani": "Irrigation", "other": "Other", "weight": "📦 Total Yield",
        "gram": "Gram", "kg": "KG", "quintal": "Quintal", "ton": "Ton",
        "profit": "✅ Net Profit", "total_cost": "💸 Total Cost", "total_income": "💰 Total Income",
        "save": "💾 Save Page", "pages": "📚 My Pages", "weather": "🌤️ Weather & Mandi", "loan": "🏦 Loan Calculator", "download": "📥 Download CSV"
    },
    "Marathi": {
        "title": "Bharat Kisan NOTEBOOK", "new": "+ नवीन पीक जोडा", "edit": "✏️ बदल करा", "delete": "🗑️ हटवा",
        "crop": "पीक निवडा", "cat": "प्रकार", "area": "क्षेत्र (गुंठा)", "bhav": "बाजार भाव Rs/Q",
        "kharch": "💸 सर्व खर्च प्रति एकर", "beej": "बीज", "khat": "खत", "aushad": "औषध",
        "majdoor": "मजूर", "pani": "पाणी", "other": "इतर", "weight": "📦 Total Yield",
        "gram": "Gram", "kg": "KG", "quintal": "Quintal", "ton": "Ton",
        "profit": "✅ शुद्ध लाभ", "total_cost": "💸 एकूण खर्च", "total_income": "💰 एकूण उत्पन्न",
        "save": "💾 सेव करे", "pages": "📚 मेरे पेज", "weather": "🌤️ Weather & Mandi", "loan": "🏦 Loan Calculator", "download": "📥 Download CSV"
    }
}

lang = st.sidebar.selectbox("Language / भाषा", ["English", "Marathi"])
T = LANG[lang]

st.title(T["title"])
tab1, tab2, tab3 = st.tabs([T["new"], T["pages"], T["weather"]])

with tab1:
    crop = st.selectbox(T["crop"], ["Cotton", "Soybean", "Wheat", "Chana", "Other"])
    if crop == "Other":
        crop = st.text_input("Enter Crop Name")

    category = st.selectbox(T["cat"], ["Kharif", "Rabi", "Summer"])

    col1, col2 = st.columns(2)
    with col1:
        area = st.number_input(T["area"], 1.0, 1000.0, 20.0)
    with col2:
        rate = st.number_input(T["bhav"], 0.0, 20000.0, 5000.0)

    st.subheader(T["kharch"])
    c1, c2, c3 = st.columns(3)
    with c1:
        beej = st.number_input(T["beej"] + " (Rs)", 0.0, value=0.0)
        khat = st.number_input(T["khat"] + " (Rs)", 0.0, value=0.0)
    with c2:
        aushad = st.number_input(T["aushad"] + " (Rs)", 0.0, value=0.0)
        majdoor = st.number_input(T["majdoor"] + " (Rs)", 0.0, value=0.0)
    with c3:
        pani = st.number_input(T["pani"] + " (Rs)", 0.0, value=0.0)
        other = st.number_input(T["other"] + " (Rs)", 0.0, value=0.0)

    st.divider()
    st.subheader(T["weight"])
    y1, y2 = st.columns([2,1])
    with y1:
        yield_qty = st.number_input("Yield Quantity", 0.0, value=0.0)
    with y2:
        yield_unit_name = st.selectbox("Unit", [T["gram"], T["kg"], T["quintal"], T["ton"]])

    # Calculation with correct indentation
    unit_map = {T["gram"]: 0.00001, T["kg"]: 0.01, T["quintal"]: 1.0, T["ton"]: 10.0, "Gram":0.00001, "KG":0.01, "Quintal":1.0, "Ton":10.0, "gram":0.00001, "kg":0.01, "quintal":1.0, "ton":10.0}
    conv = unit_map.get(yield_unit_name, 1.0)

    total_cost_per_acre = beej + khat + aushad + majdoor + pani + other
    total_cost = (total_cost_per_acre * area) / 40 # Guntha to Acre
    total_yield = yield_qty * conv
    total_income = total_yield * rate
    profit = total_income - total_cost

    # 3 BOXES - FINAL FIX
    st.divider()
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(T["total_cost"], f"Rs {total_cost:,.0f}")
    with m2:
        st.metric(T["total_income"], f"Rs {total_income:,.0f}")
    with m3:
        st.metric(T["profit"], f"Rs {profit:,.0f}", delta=f"{profit:,.0f}")

    if st.button(T["save"], use_container_width=True):
        new_data = {"Date": str(date.today()), "Crop": crop, "Area": area, "Cost": total_cost, "Yield": total_yield, "Income": total_income, "Profit": profit}
        df_new = pd.DataFrame([new_data])
        if os.path.exists("data.csv"):
            df_old = pd.read_csv("data.csv")
            df_all = pd.concat([df_old, df_new], ignore_index=True)
            df_all.to_csv("data.csv", index=False)
        else:
            df_new.to_csv("data.csv", index=False)
        st.success("Saved!")

with tab2:
    st.subheader(T["pages"])
    if os.path.exists("data.csv"):
        df = pd.read_csv("data.csv")
        st.dataframe(df, use_container_width=True)
        st.download_button(T["download"], df.to_csv(index=False), "kisan_data.csv", use_container_width=True)
    else:
        st.info("No data yet")

with tab3:
    st.subheader(T["weather"])
    st.write("Coming Soon: Weather API & Mandi Bhav")
    st.subheader(T["loan"])
    loan_amt = st.number_input("Loan Amount", 0.0, value=100000.0)
    interest = st.number_input("Interest %", 0.0, value=7.0)
    years = st.number_input("Years", 1, 10, 3)
    if st.button("Calculate Loan"):
        emi = (loan_amt * (interest/100) * (1 + interest/100)**years) / (((1 + interest/100)**years)-1) if interest>0 else loan_amt/12/years
        st.write(f"Approx EMI: Rs {emi:,.0f}")