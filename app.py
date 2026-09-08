import streamlit as st

st.set_page_config(page_title="Bharat Kisan Calculator", page_icon="🌾", layout="centered")
st.title("🌾 Bharat Kisan Labh Calculator")
st.markdown("**1 Guntha pasun 100 Acre paryant - Sarva Shetkaryansathi**")
st.divider()

# Crop Database - You can edit rates as per Solapur Market
crops_data = {
    "Tomato": {"prod": 150, "rate": 2000, "cost": 40000, "days": 90, "unit": "Quintal"},
    "Onion (Kanda)": {"prod": 120, "rate": 2500, "cost": 35000, "days": 120, "unit": "Quintal"},
    "Soybean": {"prod": 12, "rate": 4800, "cost": 15000, "days": 110, "unit": "Quintal"},
    "Cotton (Kapus)": {"prod": 10, "rate": 7000, "cost": 20000, "days": 180, "unit": "Quintal"},
    "Brinjal (Vangi)": {"prod": 100, "rate": 2000, "cost": 30000, "days": 120, "unit": "Quintal"},
    "Pomegranate": {"prod": 80, "rate": 6000, "cost": 60000, "days": 240, "unit": "Quintal"},
    "Banana (Keli)": {"prod": 300, "rate": 1500, "cost": 50000, "days": 365, "unit": "Quintal"},
    "Wheat (Gahu)": {"prod": 18, "rate": 2200, "cost": 12000, "days": 120, "unit": "Quintal"},
}

col1, col2 = st.columns(2)
with col1:
    crop = st.selectbox("🌱 Pik Nivda / Select Crop", list(crops_data.keys()))
with col2:
    area = st.number_input("📏 Area in Acre", min_value=0.05, max_value=100.0, value=1.0, step=0.05, help="0.05 Acre = 2 Guntha, 0.25 Acre = 10 Guntha")

data = crops_data[crop]

st.divider()
st.subheader(f"📊 Andaj for {area} Acre - {crop}")

total_prod = data["prod"] * area
total_cost = data["cost"] * area
total_income = total_prod * data["rate"]
profit = total_income - total_cost
per_month_income = profit / (data["days"] / 30) if data["days"] > 0 else 0

m1, m2, m3 = st.columns(3)
m1.metric("💸 Total Kharch", f"₹ {total_cost:,.0f}")
m2.metric("💰 Total Vikri", f"₹ {total_income:,.0f}")
m3.metric("📈 Nafa/Tota", f"₹ {profit:,.0f}")

st.write("")
c1, c2 = st.columns(2)
c1.info(f"**Utpanna:** {total_prod:.1f} {data['unit']}")
c2.info(f"**Kalavadhi:** {data['days']} Divas | **Per Month:** ₹ {per_month_income:,.0f}")

if profit > 0:
    st.success(f"✅ FAIDA: {area} Acre madhe {crop} ne tumhala ₹ {profit:,.0f} nafa hoil!")
    st.balloons()
else:
    st.error(f"❌ TOTA: Kharch jast aahe. Bajar bhav check kara.")

st.divider()
st.caption("Note: He andaje aahet. Bajar bhav badaltil. Solapur Market pramane badla karu shakta.")
st.caption("Made with ❤️ by Sopan Pakani - For Indian Farmers")