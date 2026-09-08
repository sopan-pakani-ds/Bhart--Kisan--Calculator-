import streamlit as st

st.set_page_config(page_title="Bharat Kisan Pro", page_icon="🌾", layout="centered")
st.title("🌾 Bharat Kisan PRO Calculator")
st.markdown("**A to Z Pik + Beej, Khat, Majdoor Kharch Sahit**")
st.divider()

crops_db = {
    "Tomato": {"yield":150, "days":90, "beej":5000, "khat":15000, "majdoor":15000, "med":5000},
    "Onion (Kanda)": {"yield":120, "days":120, "beej":8000, "khat":12000, "majdoor":12000, "med":3000},
    "Brinjal (Vangi)": {"yield":100, "days":130, "beej":4000, "khat":10000, "majdoor":12000, "med":4000},
    "Chilli (Mirchi)": {"yield":40, "days":150, "beej":6000, "khat":12000, "majdoor":15000, "med":7000},
    "Okra (Bhendi)": {"yield":50, "days":90, "beej":3000, "khat":8000, "majdoor":10000, "med":3000},
    "Potato": {"yield":100, "days":90, "beej":15000, "khat":10000, "majdoor":8000, "med":2000},
    "Soybean": {"yield":12, "days":100, "beej":4000, "khat":5000, "majdoor":4000, "med":2000},
    "Cotton (Kapus)": {"yield":10, "days":180, "beej":3000, "khat":7000, "majdoor":8000, "med":2000},
    "Wheat (Gahu)": {"yield":18, "days":120, "beej":2500, "khat":4000, "majdoor":3000, "med":2500},
    "Jowar": {"yield":15, "days":110, "beej":1500, "khat":3000, "majdoor":3000, "med":1000},
    "Groundnut": {"yield":14, "days":110, "beej":5000, "khat":4000, "majdoor":4000, "med":2000},
    "Gram (Harbhara)": {"yield":10, "days":100, "beej":3000, "khat":3000, "majdoor":3000, "med":1000},
    "Sugarcane (Uus)": {"yield":400, "days":365, "beej":10000, "khat":20000, "majdoor":15000, "med":5000},
    "Pomegranate": {"yield":80, "days":240, "beej":20000, "khat":15000, "majdoor":15000, "med":10000},
    "Banana (Keli)": {"yield":300, "days":365, "beej":15000, "khat":15000, "majdoor":10000, "med":10000},
    "Grapes (Draksha)": {"yield":100, "days":180, "beej":25000, "khat":20000, "majdoor":15000, "med":10000},
    "Watermelon": {"yield":150, "days":80, "beej":5000, "khat":8000, "majdoor":7000, "med":2000},
    "Sunflower": {"yield":8, "days":90, "beej":2000, "khat":3000, "majdoor":3000, "med":1000},
}

col1, col2 = st.columns(2)
with col1:
    crop = st.selectbox("🌱 Pik Nivda (A to Z)", sorted(crops_db.keys()))
with col2:
    area = st.number_input("📏 Area Acre", 0.05, 100.0, 1.0, 0.05)

bhav = st.number_input(f"💰 {crop} Bhav Rs/Qtl", 500, 20000, 3000, 100)

with st.expander("⚙️ Kharch Details - Beej, Khat, Majdoor", expanded=True):
    d = crops_db[crop]
    beej = st.number_input("🌰 Beej Kharch/Acre", 0, 100000, d["beej"], 500)
    khat = st.number_input("🧪 Khat/Acre", 0, 100000, d["khat"], 500)
    majdoor = st.number_input("👷 Majdoor/Acre", 0, 100000, d["majdoor"], 500)
    med = st.number_input("💊 Aushad/Acre", 0, 100000, d["med"], 500)
    other = st.number_input("🚜 Other/Acre", 0, 100000, 5000, 500)

per_acre_cost = beej + khat + majdoor + med + other
total_cost = per_acre_cost * area
total_yield = d["yield"] * area
total_income = total_yield * bhav
profit = total_income - total_cost
per_month = profit / (d["days"]/30) if d["days"]>0 else 0

st.divider()
st.subheader(f"📊 {crop} - {area} Acre Report")
m1,m2,m3 = st.columns(3)
m1.metric("Kharch", f"₹{total_cost:,.0f}")
m2.metric("Income", f"₹{total_income:,.0f}")
m3.metric("NAFA", f"₹{profit:,.0f}")

st.info(f"Utpanna: {total_yield:.1f} Qtl | Per Month: ₹{per_month:,.0f} | Per Acre Kharch: ₹{per_acre_cost:,.0f}")
st.write(f"🌰 Beej: ₹{beej*area:,.0f} | 🧪 Khat: ₹{khat*area:,.0f} | 👷 Majdoor: ₹{majdoor*area:,.0f} | 💊 Med: ₹{med*area:,.0f} | 🚜 Other: ₹{other*area:,.0f}")

if profit>0:
    st.success(f"✅ Fayda: ₹{profit:,.0f} in {d['days']} days")
    st.balloons()
else:
    st.error("❌ Tota - Bhav check kara")

st.caption("Made by Sopan Pakani for Farmers")