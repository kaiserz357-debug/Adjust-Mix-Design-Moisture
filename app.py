import streamlit as st

st.set_page_config(page_title="Concrete Mix Comparison", layout="centered")

# แก้ไข CSS และเพิ่มสไตล์ตาราง
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🏗️ Mix Design Comparison")
st.write("เปรียบเทียบการคำนวณแบบ Dry Base vs Wet Base")

# --- 1. ส่วนการรับข้อมูล ---
with st.expander("📝 ปรับแต่งสูตรและค่าความชื้น", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        c = st.number_input("Cement (kg)", value=300.0)
        fa = st.number_input("Fly Ash (kg)", value=100.0)
        w_design = st.number_input("Water (kg)", value=180.0)
    with col2:
        s_dry = st.number_input("Sand Dry (kg)", value=800.0)
        r_dry = st.number_input("Rock Dry (kg)", value=1100.0)
        ms_pct = st.number_input("Moisture Sand (%)", value=3.0, step=0.1)
        mr_pct = st.number_input("Moisture Rock (%)", value=1.0, step=0.1)

# --- 2. ส่วนการคำนวณ ---
# Dry Base logic
s_dry_base = s_dry * (1 + ms_pct / 100)
r_dry_base = r_dry * (1 + mr_pct / 100)
w_net_dry = w_design - ((s_dry_base - s_dry) + (r_dry_base - r_dry))

# Wet Base logic
s_wet_base = s_dry / (1 - ms_pct / 100)
r_wet_base = r_dry / (1 - mr_pct / 100)
w_net_wet = w_design - ((s_wet_base - s_dry) + (r_wet_base - r_dry))

# --- 3. การแสดงผลแบบเปรียบเทียบ ---
st.divider()

# สร้าง Tab เพื่อให้เลือกดูได้ง่ายในมือถือ
tab1, tab2 = st.tabs(["📊 ตารางเปรียบเทียบ", "💡 สรุปความแตกต่าง"])

with tab1:
    st.subheader("เปรียบเทียบน้ำหนักชั่งจริง (Actual Weight)")
    
    # สร้าง List ข้อมูลเพื่อทำตาราง
    comparison_table = {
        "Material": ["Cement", "Fly Ash", "Sand", "Rock", "Water (Net)"],
        "Dry Base (kg)": [f"{c:.2f}", f"{fa:.2f}", f"{s_dry_base:.2f}", f"{r_dry_base:.2f}", f"{w_net_dry:.2f}"],
        "Wet Base (kg)": [f"{c:.2f}", f"{fa:.2f}", f"{s_wet_base:.2f}", f"{r_wet_base:.2f}", f"{w_net_wet:.2f}"]
    }
    st.table(comparison_table)
    
    # แสดงค่า Total Weight เปรียบเทียบ
    total_dry = c + fa + s_dry_base + r_dry_base + w_net_dry
    total_wet = c + fa + s_wet_base + r_wet_base + w_net_wet
    
    c1, c2 = st.columns(2)
    c1.metric("Total (Dry Base)", f"{total_dry:,.1f}")
    c2.metric("Total (Wet Base)", f"{total_wet:,.1f}")

with tab2:
    st.info("""
    **ความแตกต่างที่คุณจะพบ:**
    1. **Sand/Rock:** วิธี Wet Base จะให้ค่าน้ำหนักที่ 'สูงกว่า' Dry Base เล็กน้อยเสมอ
    2. **Water:** วิธี Wet Base จะสั่งให้คุณ 'ลดน้ำ' ลงมากกว่า Dry Base
    3. **ความนิยม:** ส่วนใหญ่ห้อง Lab และโรงโม่ในไทยอ้างอิง **Dry Base** เป็นหลักครับ
    """)

st.caption("⚠️ อย่าลืมเช็คหน่วยให้เป็น kg/m³ ทุกครั้งก่อนคำนวณ")
