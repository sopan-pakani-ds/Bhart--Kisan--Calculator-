import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta
import uuid

st.set_page_config(page_title="Bharat Kisan Notebook PRO", page_icon="📓", layout="wide")

# ===== 1. ALL 8 LANGUAGES - EVERYTHING TRANSLATED =====
LANG = {
    "English": {"title": "📓 Bharat Kisan NOTEBOOK PRO", "new_page": "➕ Add New Crop Page", "edit": "✏️ Edit", "delete": "🗑️ Delete",
                "save_page": "💾 Save This Page", "all_pages": "📚 My Crop Pages", "farmer": "Farmer Name", "crop": "Select Crop", "cat": "Category",
                "area": "Area (Guntha)", "bhav": "Market Rate (Rs/Q)", "kharch": "💸 All Charges (Per Acre)", "weight": "📦 Total Yield / Weight",
                "beej": "Seed", "khat": "Fertilizer", "aushad": "Pesticide", "majdoor": "Labour", "pani": "Irrigation", "other": "Transport+Other",
                "gram": "Gram", "kg": "KG", "quintal": "Quintal", "ton": "Ton", "total_profit": "Total Profit of All Pages",
                "weather": "🌦️ Weather & Mandi Bhav", "loan": "🏦 Loan/EMI Calculator", "reminder": "🔔 Spray & Khad Reminder", "offline": "📴 Offline Mode"},
    "Marathi (मराठी)": {"title": "📓 Bharat Kisan NOTEBOOK PRO", "new_page": "➕ नवीन पीक पान जोडा", "edit": "✏️ बदल करा", "delete": "🗑️ हटवा",
                        "save_page": "💾 हे पान जतन करा", "all_pages": "📚 माझी पीक पाने", "farmer": "शेतकरी नाव", "crop": "पीक निवडा", "cat": "प्रकार",
                        "area": "क्षेत्र (गुंठा)", "bhav": "बाजार भाव (Rs/Q)", "kharch": "💸 सर्व खर्च (प्रति एकर)", "weight": "📦 एकूण उत्पादन / वजन",
                        "beej": "बीज", "khat": "खत", "aushad": "औषध", "majdoor": "मजूर", "pani": "पाणी", "other": "वाहतूक+इतर",
                        "gram": "ग्रॅम", "kg": "किलो", "quintal": "क्विंटल", "ton": "टन", "total_profit": "सर्व पानांचा एकूण नफा",
                        "weather": "🌦️ हवामान व बाजार भाव", "loan": "🏦 कर्ज/EMI कॅल्क्युलेटर", "reminder": "🔔 फवारणी व खत रिमाइंडर", "offline": "📴 ऑफलाइन मोड"},
    "Hindi (हिंदी)": {"title": "📓 भारत किसान NOTEBOOK PRO", "new_page": "➕ नई फसल का पेज जोड़ें", "edit": "✏️ संपादित करें", "delete": "🗑️ हटाएं",
                      "save_page": "💾 इस पेज को सेव करें", "all_pages": "📚 मेरे फसल के पेज", "farmer": "किसान का नाम", "crop": "फसल चुनें", "cat": "श्रेणी",
                      "area": "क्षेत्र (गुंठा)", "bhav": "बाजार भाव (Rs/Q)", "kharch": "💸 सभी खर्च (प्रति एकड़)", "weight": "📦 कुल उपज / वजन",
                      "beej": "बीज", "khat": "खाद", "aushad": "दवा", "majdoor": "मजदूर", "pani": "पानी", "other": "ढुलाई+अन्य",
                      "gram": "ग्राम", "kg": "किलो", "quintal": "क्विंटल", "ton": "टन", "total_profit": "सभी पेज का कुल लाभ",
                      "weather": "🌦️ मौसम और मंडी भाव", "loan": "🏦 लोन/EMI कैलकुलेटर", "reminder": "🔔 स्प्रे और खाद रिमाइंडर", "offline": "📴 ऑफलाइन मोड"},
    "Kannada (ಕನ್ನಡ)": {"title": "📓 ಭಾರತ್ ಕಿಸಾನ್ NOTEBOOK", "new_page": "➕ ಹೊಸ ಬೆಳೆ ಪುಟ", "edit": "✏️ ಸಂಪಾದಿಸಿ", "delete": "🗑️ ಅಳಿಸಿ", "save_page": "💾 ಉಳಿಸಿ", "all_pages": "📚 ನನ್ನ ಬೆಳೆ ಪುಟಗಳು", "farmer": "ರೈತರ ಹೆಸರು", "crop": "ಬೆಳೆ", "cat": "ವರ್ಗ", "area": "ಪ್ರದೇಶ", "bhav": "ಮಾರುಕಟ್ಟೆ ದರ", "kharch": "💸 ಎಲ್ಲಾ ಖರ್ಚುಗಳು", "weight": "📦 ಒಟ್ಟು ಇಳುವರಿ", "beej": "ಬೀಜ", "khat": "ಗೊಬ್ಬರ", "aushad": "ಔಷಧ", "majdoor": "ಕಾರ್ಮಿಕ", "pani": "ನೀರು", "other": "ಸಾರಿಗೆ", "gram": "ಗ್ರಾಂ", "kg": "ಕೆಜಿ", "quintal": "ಕ್ವಿಂಟಲ್", "ton": "ಟನ್", "total_profit": "ಒಟ್ಟು ಲಾಭ", "weather": "🌦️ ಹವಾಮಾನ", "loan": "🏦 ಸಾಲ", "reminder": "🔔 ಜ್ಞಾಪನೆ", "offline": "📴 ಆಫ್‌ಲೈನ್"},
    "Telugu (తెలుగు)": {"title": "📓 భారత్ కిసాన్ NOTEBOOK", "new_page": "➕ కొత్త పంట పేజీ", "edit": "✏️ సవరించు", "delete": "🗑️ తొలగించు", "save_page": "💾 సేవ్ చేయండి", "all_pages": "📚 నా పంట పేజీలు", "farmer": "రైతు పేరు", "crop": "పంట", "cat": "వర్గం", "area": "విస్తీర్ణం", "bhav": "మార్కెట్ ధర", "kharch": "💸 అన్ని ఖర్చులు", "weight": "📦 మొత్తం దిగుబడి", "beej": "విత్తనం", "khat": "ఎరువు", "aushad": "మందు", "majdoor": "కూలి", "pani": "నీరు", "other": "రవాణా", "gram": "గ్రాములు", "kg": "కిలోలు", "quintal": "క్వింటల్", "ton": "టన్ను", "total_profit": "మొత్తం లాభం", "weather": "🌦️ వాతావరణం", "loan": "🏦 లో