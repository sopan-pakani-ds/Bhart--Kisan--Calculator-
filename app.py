import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

st.set_page_config(page_title="Bharat Kisan Notebook", page_icon="Notebook", layout="wide")

LANG = {
    "Marathi": {"title": "Bharat Kisan NOTEBOOK", "new": "नवीन पीक जोडा", "cat": "प्रकार", "crop": "पीक निवडा", "custom": "तुमचे पीक नाव लिहा", "farmer": "शेतकऱ्याचे नाव", "area": "क्षेत्र (गुंठा)", "bhav": "बाजार भाव Rs/Q", "kharch": "सर्व खर्च प्रति एकर", "beej": "बीज", "khat": "खत", "aushad": "औषध", "majdoor": "मजूर", "pani": "पाणी", "other": "इतर", "weight": "एकूण उत्पादन", "gram": "ग्रॅम", "kg": "किलो", "quintal": "क्विंटल", "ton": "टन", "profit": "निव्वळ नफा", "total_cost": "एकूण खर्च", "total_income": "एकूण उत्पन्न", "save": "फाईल जतन करा", "pages": "माझ्या फाईल्स", "edit": "उघडा / बदला", "delete": "हटवा", "download": "CSV डाउनलोड", "file_name": "फाईलचे नाव", "weather": "हवामान व बाजार", "loan": "कर्ज कॅल्क्युलेटर"},
    "Hindi": {"title": "Bharat Kisan NOTEBOOK", "new": "नई फसल जोड़ें", "cat": "श्रेणी", "crop": "फसल चुनें", "custom": "अपनी फसल का नाम लिखें", "farmer": "किसान का नाम", "area": "क्षेत्र (गुंठा)", "bhav": "बाजार भाव Rs/Q", "kharch": "सभी खर्च प्रति एकड़", "beej": "बीज", "khat": "खाद", "aushad": "दवा", "majdoor": "मजदूर", "pani": "पानी", "other": "अन्य", "weight": "कुल उपज", "gram": "ग्राम", "kg": "किलो", "quintal": "क्विंटल", "ton": "टन", "profit": "शुद्ध लाभ", "total_cost": "कुल खर्च", "total_income": "कुल आमदनी", "save": "फाइल सेव करें", "pages": "मेरी फाइलें", "edit": "खोलें / बदलें", "delete": "हटाएं", "download": "CSV डाउनलोड", "file_name": "फाइल का नाम", "weather": "मौसम व मंडी", "loan": "लोन कैलकुलेटर"},
    "English": {"title": "Bharat Kisan NOTEBOOK", "new": "Add New Farm File", "cat": "Category", "crop": "Select Crop", "custom": "Add Your Own Crop Name", "farmer": "Farmer Name", "area": "Area (Guntha)", "bhav": "Market Rate Rs/Q", "kharch": "All Charges Per Acre", "beej": "Seed", "khat": "Fertilizer", "aushad": "Pesticide", "majdoor": "Labour", "pani": "Irrigation", "other": "Other", "weight": "Total Yield", "gram": "Gram", "kg": "KG", "quintal": "Quintal", "ton": "Ton", "profit": "Net Profit", "total_cost": "Total Cost", "total_income": "Total Income", "save": "Save File", "pages": "My Files", "edit": "Open / Edit", "delete": "Delete", "download": "Download CSV", "file_name": "File Name", "weather": "Weather & Mandi", "loan": "Loan Calculator"}
}

lang = st.sidebar.selectbox("Language / भाषा", list(LANG.keys()), index=0)
T = LANG[lang]

CAT_TRANS = {
    "English": ["All", "Vegetable", "Fruit", "Kharif", "Rabi", "Other"],
    "Marathi": ["सर्व", "भाजीपाला", "फळे", "खरीप", "रब्बी", "इतर"],
    "Hindi": ["सभी", "सब्जी", "फल", "खरीफ", "रबी", "अन्य"]
}
CAT_MAP = {"सर्व":"All", "भाजीपाला":"Vegetable", "फळे":"Fruit", "खरीप":"Kharif", "रब्बी":"Rabi", "इतर":"Other", "सभी":"All", "सब्जी":"Vegetable", "फल":"Fruit", "अन्य":"Other"}

CROPS_DB = {
    "Tomato": {"cat": "Vegetable", "mr": "टोमॅटो", "hi": "टमाटर", "yield": 150, "beej": 5000, "khat": 8000, "aushad": 7000, "majdoor": 10000, "pani": 3000, "other": 2000},
    "Onion": {"cat": "Vegetable", "mr": "कांदा", "hi": "प्याज", "yield": 100, "beej": 6000, "khat": 7000, "aushad": 5000, "majdoor": 8000, "pani": 2500, "other": 1500},
    "Dalimb": {"cat": "Fruit", "mr": "डाळिंब", "hi": "अनार", "yield": 60, "beej": 15000, "khat": 15000, "aushad": 12000, "majdoor": 10000, "pani": 5000, "other": 3000},
    "Grapes": {"cat": "Fruit", "mr": "द्राक्ष", "hi": "अंगूर", "yield": 100, "beej": 20000, "khat": 20000, "aushad": 15000, "majdoor": 15000, "pani": 6000, "other": 4000},
    "Banana": {"cat": "Fruit", "mr": "केळी", "hi": "केला", "yield": 250, "beej": 12000, "khat": 12000, "aushad": 8000, "majdoor": 15000, "pani": 5000, "other": 3000},
    "Mango": {"cat": "Fruit", "mr": "आंबा", "hi": "आम", "yield": 80, "beej": 10000, "khat": 8000, "aushad": 6000, "majdoor": 12000, "pani": 4000, "other": 2000},
    "Orange": {"cat": "Fruit", "mr": "संत्रा", "hi": "संतरा", "yield": 90, "beej": 12000, "khat": 10000, "aushad": 8000, "majdoor": 10000, "pani": 4000, "other": 2000},
    "Guava": {"cat": "Fruit", "mr": "पेरू", "hi": "अमरूद", "yield": 70, "beej": 8000, "khat": 7000, "aushad": 5000, "majdoor": 8000, "pani": 3000, "other": 1500},
    "Papaya": {"cat": "Fruit", "mr": "पपई", "hi": "पपीता", "yield": 120, "beej": 6000, "khat": 6000, "aushad": 5000, "majdoor": 7000, "pani": 3000, "other": 1500},
    "Watermelon": {"cat": "Fruit", "mr": "कलिंगड", "hi": "तरबूज", "yield": 180, "beej": 5000, "khat": 6000, "aushad": 4000, "majdoor": 7000, "pani": 3000, "other": 1500},
    "Apple": {"cat": "Fruit", "mr": "सफरचंद", "hi": "सेब", "yield": 80, "beej": 20000, "khat": 15000, "aushad": 10000, "majdoor": 12000, "pani": 5000, "other": 3000},
    "Soybean": {"cat": "Kharif", "mr": "सोयाबीन", "hi": "सोयाबीन", "yield": 10, "beej": 3000, "khat": 4000, "aushad": 3000, "majdoor": 5000, "pani": 1500, "other": 1500},
    "Cotton": {"cat": "Kharif", "mr": "कापूस", "hi": "कपास", "yield": 12, "beej": 4000, "khat": 6000, "aushad": 7000, "majdoor": 6000, "pani": 2000, "other": 1000},
}

st.title(T["title"])
if 'pages' not in st.session_state: st.session_state.pages = []
if 'edit_id' not in st.session_state: st.session_state.edit_id = None

st.sidebar.subheader(T["pages"])
for i, p in enumerate(st.session_state.pages):
    fname = f"{p.get('farmer_name','')} - {p.get('file_name', p['crop'])}"
    if st.sidebar.button(f"{fname}", key=f"side_{i}", use_container_width=True):
        st.session_state.edit_id = p['id']
        st.rerun()

tab1, tab2, tab3 = st.tabs([T["crop"], T["weather"], T["loan"]])

with tab1:
    if not st.session_state.edit_id:
        st.markdown(f"### {T['pages']} ({len(st.session_state.pages)})")
        if len(st.session_state.pages) == 0:
            st.info("अजून एकही फाईल नाही. नवीन फाईल जोडा.")
        else:
            for i, p in enumerate(st.session_state.pages):
                with st.container(border=True):
                    c1, c2, c3 = st.columns([3, 1, 1])
                    with c1:
                        st.write(f"**{p.get('file_name', p['crop'])}**")
                        st.caption(f"शेतकरी: {p.get('farmer_name','-')} | {p['crop']} | {p['area']} गुंठा | नफा: Rs {p['profit']:,.0f} | {p.get('date','')}")
                    with c2:
                        if st.button(T["edit"], key=f"open_{i}", use_container_width=True, type="primary"):
                            st.session_state.edit_id = p['id']
                            st.rerun()
                    with c3:
                        if st.button(T["delete"], key=f"del_{i}", use_container_width=True):
                            st.session_state.pages.pop(i)
                            st.rerun()
        st.divider()
        if st.button(T["new"], type="primary", use_container_width=True):
            st.session_state.edit_id="NEW"; st.rerun()

        if len(st.session_state.pages)>0:
            st.divider()
            display_data = []
            for p in st.session_state.pages:
                display_data.append({
                    "फाईल": p.get('file_name',''),
                    "शेतकऱ्याचे नाव": p.get('farmer_name',''),
                    "पीक": p.get('crop',''),
                    "क्षेत्र (गुंठा)": p.get('area',''),
                    "एकूण खर्च": f"Rs {p.get('total_cost',0):,.0f}",
                    "एकूण उत्पन्न": f"Rs {p.get('total_income',0):,.0f}",
                    "निव्वळ नफा": f"Rs {p.get('profit',0):,.0f}"
                })
            df_display = pd.DataFrame(display_data)
            st.dataframe(df_display, use_container_width=True)
            st.download_button(T["download"], df_display.to_csv(index=False).encode('utf-8'), "kisan.csv", use_container_width=True)
    else:
        is_new = st.session_state.edit_id == "NEW"
        if is_new:
            page = {"id": str(uuid.uuid4()), "crop": "टोमॅटो", "area": 10, "rate": 3500, "file_name": "", "farmer_name": ""}
        else:
            page = next((p for p in st.session_state.pages if p['id']==st.session_state.edit_id), None)
            if page is None:
                st.session_state.edit_id=None; st.rerun()

        c_f1, c_f2 = st.columns(2)
        farmer_name_input = c_f1.text_input(T["farmer"], value=page.get("farmer_name", ""), placeholder="उदा. राम पाटील")
        file_name_input = c_f2.text_input(T["file_name"], value=page.get("file_name", ""), placeholder="उदा. टोमॅटो - शेत 1")

        cat_display = st.selectbox(T["cat"], CAT_TRANS[lang])
        cat_eng = CAT_MAP.get(cat_display, cat_display)
        if cat_display in ["All","सर्व","सभी"]: cat_eng="All"

        def get_crop_name(k):
            d=CROPS_DB[k]
            if lang=="Marathi": return d["mr"]
            if lang=="Hindi": return d["hi"]
            return k

        filtered = [k for k,v in CROPS_DB.items() if cat_eng=="All" or v["cat"]==cat_eng]
        crop_options = [get_crop_name(k) for k in filtered] + [T["custom"]]
        try:
            default_idx = crop_options.index(page.get("crop", "टोमॅटो")) if page.get("crop") in crop_options else 0
        except:
            default_idx = 0
        crop_sel = st.selectbox(T["crop"], crop_options, index=default_idx)

        if crop_sel == T["custom"]:
            custom_crop = st.text_input(T["custom"], value=page.get("crop","") if page.get("crop") not in [get_crop_name(k) for k in CROPS_DB.keys()] else "")
            data = {"yield": 50, "beej": 5000, "khat": 5000, "aushad": 5000, "majdoor": 8000, "pani": 2000, "other": 1000}
            final_crop_name = custom_crop if custom_crop else page.get("crop","My Crop")
        else:
            crop_key = None
            for k,v in CROPS_DB.items():
                if get_crop_name(k)==crop_sel:
                    crop_key=k; break
            if crop_key is None: crop_key="Tomato"
            data = CROPS_DB.get(crop_key, {"yield": 50, "beej": 5000, "khat": 5000, "aushad": 5000, "majdoor": 8000, "pani": 2000, "other": 1000})
            final_crop_name = crop_sel

        area = st.number_input(T["area"], value=float(page.get("area",10)))
        rate = st.number_input(T["bhav"], value=float(page.get("rate",3500)))
        st.subheader(T["kharch"])
        c1,c2,c3 = st.columns(3)
        beej=c1.number_input(T["beej"], value=float(page.get("beej", data["beej"])))
        khat=c2.number_input(T["khat"], value=float(page.get("khat", data["khat"])))
        aushad=c3.number_input(T["aushad"], value=float(page.get("aushad", data["aushad"])))
        c4,c5,c6=st.columns(3)
        majdoor=c4.number_input(T["majdoor"], value=float(page.get("majdoor", data["majdoor"])))
        pani=c5.number_input(T["pani"], value=float(page.get("pani", data["pani"])))
        other=c6.number_input(T["other"], value=float(page.get("other", data["other"])))
        st.subheader(T["weight"])
        y1,y2 = st.columns([2,1])
        with y1:
            yield_input = st.number_input("Quantity", value=float(page.get("yield_qty", data["yield"])), min_value=0.0)
        with y2:
            unit_choice = st.selectbox("Unit", [T["gram"], T["kg"], T["quintal"], T["ton"]])
        unit_map = {T["gram"]:0.00001, T["kg"]:0.01, T["quintal"]:1.0, T["ton"]:10.0}
        conv = unit_map.get(unit_choice, 1.0)
        total_yield_user = yield_input * conv
        col1,col2,col3,col4 = st.columns(4)
        col1.metric(T["gram"], f"{total_yield_user*100000:,.0f}")
        col2.metric(T["kg"], f"{total_yield_user*100:,.0f}")
        col3.metric(T["quintal"], f"{total_yield_user:.2f}")
        col4.metric(T["ton"], f"{total_yield_user/10:.2f}")
        total_cost_per_acre = beej+khat+aushad+majdoor+pani+other
        total_cost = (total_cost_per_acre * area)/40
        total_yield = total_yield_user * (area/40)
        total_income = total_yield * rate
        profit = total_income - total_cost
        st.divider()
        m1,m2,m3=st.columns(3)
        m1.metric(T["total_cost"], f"Rs {total_cost:,.0f}")
        m2.metric(T["total_income"], f"Rs {total_income:,.0f}")
        m3.metric(T["profit"], f"Rs {profit:,.0f}")
        c_save,c_cancel=st.columns(2)
        with c_save:
            if st.button(T["save"], type="primary", use_container_width=True):
                final_file_name = file_name_input if file_name_input else f"{final_crop_name} - {area} Guntha"
                new_page={"id":page["id"], "file_name": final_file_name, "farmer_name": farmer_name_input, "crop":final_crop_name, "area":area, "rate":rate, "beej":beej, "khat":khat, "aushad":aushad, "majdoor":majdoor, "pani":pani, "other":other, "yield_qty": yield_input, "total_cost":total_cost, "total_yield_q":total_yield, "total_income":total_income, "profit":profit, "date": datetime.now().strftime("%d-%m-%Y")}
                if is_new: st.session_state.pages.append(new_page)
                else:
                    idx=next((i for i,p in enumerate(st.session_state.pages) if p['id']==page['id']),0)
                    st.session_state.pages[idx]=new_page
                st.session_state.edit_id=None; st.rerun()
        with c_cancel:
            if st.button("Back", use_container_width=True): st.session_state.edit_id=None; st.rerun()

with tab2:
    st.subheader(T["weather"])
    loc=st.text_input("गाव", "सिंदखेड, महाराष्ट्र")
    c1,c2,c3=st.columns(3)
    c1.metric("Temp", "32 C"); c2.metric("Humidity", "65%"); c3.metric("Rain", "60%")
    st.info(f"{loc} - आज धुके, उद्या पाऊस")
    mandi_df = pd.DataFrame({"Crop":["टोमॅटो","कांदा","डाळिंब","संत्रा"], "Bhav":[3500,2800,5000,4000]})
    st.table(mandi_df)

with tab3:
    st.subheader(T["loan"])
    loan=st.number_input("Loan",100000,step=10000)
    rate_l=st.slider("Interest %",7.0,15.0,11.0)
    years=st.slider("Years",1,5,2)
    emi=(loan*(rate_l/100/12))/(1-(1+(rate_l/100/12))**(-years*12))
    st.metric("EMI", f"Rs {emi:,.0f}")