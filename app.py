import streamlit as st

st.set_page_config(page_title="Concrete Mix Comparison", layout="centered")

# --- ส่วนกำหนดสไตล์ ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .developer-text {
        color: #6c757d;
        font-size: 14px;
        margin-top: -15px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ส่วนหัวข้อและเครดิต ---
st.title("🏗️ Mix Design Comparison")
st.markdown('<p class="developer-text">Develop By Ardharn 2026</p>', unsafe_allow_html=True)

# --- 1. ส่วนการรับข้อมูล ---
with st.expander("📝 ปรับแต่งสูตรและค่าความชื้น", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        c = st.number_input("Cement (kg)", value=300.0, step=1.0)
        fa = st.number_input("Fly Ash (kg)", value=100.0, step=1.0)
        w_design = st.number_input("Water (kg)", value=180.0, step=1.0)
    with col2:
        s_dry = st.number_input("Sand Dry (kg)", value=800.0, step=1.0)
        r_dry = st.number_input("Rock Dry (kg)", value=1100.0, step=1.0)
        ms_pct = st.number_input("Moisture Sand (%)", value=3.0, step=0.1)
        mr_pct = st.number_input("Moisture Rock (%)", value=0.0, step=0.1)

# --- 2. ส่วนการคำนวณ ---
# Dry Base logic
s_dry_base = s_dry * (1 + ms_pct / 100)
r_dry_base = r_dry * (1 + mr_pct / 100)
w_net_dry = w_design - ((s_dry_base - s_dry) + (r_dry_base - r_dry))

# Wet Base logic
s_wet_base = s_dry / (1 - ms_pct / 100) if ms_pct < 100 else 0
r_wet_base = r_dry / (1 - mr_pct / 100) if mr_pct < 100 else 0
w_net_wet = w_design - ((s_wet_base - s_dry) + (r_wet_base - r_dry))

# --- 3. การแสดงผล ---
st.divider()

tab1, tab2 = st.tabs(["📊 ตารางเปรียบเทียบ", "💡 สรุปความแตกต่าง"])

with tab1:
    st.subheader("น้ำหนักที่ต้องชั่งจริง (Actual Weight)")
    
    # ตารางแสดงผลเปรียบเทียบ
    comparison_table = {
        "Material": ["Cement (ปูน)", "Fly Ash (เถ้าลอย)", "Sand (ทรายเปียก)", "Rock (หินเปียก)", "Water (น้ำเติมจริง)"],
        "Dry Base (kg)": [f"{c:,.1f}", f"{fa:,.1f}", f"{s_dry_base:,.1f}", f"{r_dry_base:,.1f}", f"{w_net_dry:,.1f}"],
        "Wet Base (kg)": [f"{c:,.1f}", f"{fa:,.1f}", f"{s_wet_base:,.1f}", f"{r_wet_base:,.1f}", f"{w_net_wet:,.1f}"]
    }
    st.table(comparison_table)
