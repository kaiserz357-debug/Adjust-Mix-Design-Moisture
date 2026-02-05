import streamlit as st

# ตั้งค่าหน้าจอให้พอดีกับอุปกรณ์
st.set_page_config(page_title="Concrete Mix Mobile", layout="centered")

# ตกแต่ง CSS เล็กน้อยเพื่อให้ปุ่มและตารางดูใหญ่ขึ้นในมือถือ
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    div[data-testid="stMetricValue"] {
        font-size: 25px;
    }
    </style>
    """, unsafe_allow_input=True)

st.title("🏗️ Mix Design Adjuster")
st.write("เครื่องมือปรับสัดส่วนผสมคอนกรีตหน้างาน")

# --- ส่วนที่ 1: Input Original Design ---
with st.expander("📝 1. กำหนดสูตร Original Mix (Dry Base)", expanded=True):
    # ใช้ Columns ใน Expander เพื่อให้กรอกง่ายขึ้น
    col_a, col_b = st.columns(2)
    with col_a:
        c = st.number_input("Cement (kg)", value=300.0, step=1.0)
        s_dry = st.number_input("Sand Dry (kg)", value=800.0, step=1.0)
    with col_b:
        fa = st.number_input("Fly Ash (kg)", value=100.0, step=1.0)
        r_dry = st.number_input("Rock Dry (kg)", value=1100.0, step=1.0)
    
    w_design = st.number_input("Water (kg)", value=180.0, step=1.0)

# --- ส่วนที่ 2: Input Moisture ---
with st.expander("💧 2. ป้อนค่าความชื้น (%)", expanded=True):
    ms_pct = st.number_input("ทราย: Moisture in Sand (%)", value=3.0, step=0.1)
    mr_pct = st.number_input("หิน: Moisture in Rock (%)", value=1.0, step=0.1)

# --- ส่วนการคำนวณ (ใช้ Dry Base เป็นหลักเพราะเป็นสากลที่สุด) ---
# Dry Base Calculation
s_actual = s_dry * (1 + ms_pct / 100)
r_actual = r_dry * (1 + mr_pct / 100)
excess_w = (s_actual - s_dry) + (r_actual - r_dry)
w_net = w_design - excess_w

# --- ส่วนแสดงผลลัพธ์ (Output) ---
st.divider()
st.subheader("📊 ปริมาณที่ต้องชั่งจริง (Actual Weight)")

# แสดง Metric สำคัญ
m_col1, m_col2 = st.columns(2)
m_col1.metric("W/B Ratio", f"{w_design/(c+fa):.2f}")
m_col2.metric("Total Weight", f"{c+fa+s_actual+r_actual+w_net:,.0f} kg")

# ตารางสรุปผล
result_data = {
    "รายการวัสดุ": ["Cement (ปูน)", "Fly Ash (เถ้าลอย)", "Sand (ทรายเปียก)", "Rock (หินเปียก)", "Water (น้ำเติมจริง)"],
    "น้ำหนัก (kg)": [f"{c:,.1f}", f"{fa:,.1f}", f"{s_actual:,.1f}", f"{r_actual:,.1f}", f"{w_net:,.1f}"]
}
st.table(result_data)

# เปรียบเทียบ Wet Base สั้นๆ ด้านล่าง
with st.expander("🔍 ดูเปรียบเทียบแบบ Wet Base"):
    s_wet = s_dry / (1 - ms_pct / 100)
    r_wet = r_dry / (1 - mr_pct / 100)
    w_net_wet = w_design - ((s_wet - s_dry) + (r_wet - r_dry))
    st.write(f"**Sand:** {s_wet:.1f} kg | **Rock:** {r_wet:.1f} kg | **Water:** {w_net_wet:.1f} kg")

st.caption("หมายเหตุ: คำนวณตามมาตรฐานการปรับความชื้นหน้างาน (Field Adjustment)")
