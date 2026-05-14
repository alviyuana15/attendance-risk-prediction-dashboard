# Home.py — landing page, otomatis jadi halaman pertama di navbar Streamlit
import streamlit as st
from lib.ui import apply_theme

# ✅ 1. Google Analytics 
st.components.v1.html("""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-802MRDWF01"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

gtag('config', 'G-802MRDWF01');
</script>
""", height=0)

st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@700;800&family=DM+Sans:wght@400;500&display=swap');
.page-title {
    font-family: 'Sora', sans-serif; font-size: 2.6rem; font-weight: 800;
    color: #FFFFFF; letter-spacing: -0.03em; line-height: 1.25; margin-bottom: 0.4rem;
}
.page-subtitle {
    font-size: 0.85rem; color: #6B7A99; letter-spacing: 0.12em;
    text-transform: uppercase; margin-bottom: 3rem;
}
.nav-card {
    background: #161D2E; border: 1px solid #2A3347; border-radius: 16px;
    padding: 2rem 2rem; margin-bottom: 1rem; position: relative; overflow: hidden;
}
.nav-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px; border-radius: 16px 16px 0 0;
}
.nav-card.blue::before { background: #4F8EF7; }
.nav-card.purple::before { background: #A78BFA; }
.nav-card .nc-icon { font-size: 2.2rem; margin-bottom: 1rem; }
.nav-card .nc-title {
    font-family: 'Sora', sans-serif; font-size: 1.15rem; font-weight: 700;
    color: #E5EAF5; margin-bottom: 0.5rem;
}
.nav-card .nc-desc { font-size: 0.83rem; color: #6B7A99; line-height: 1.6; }
.nc-hint { font-size: 0.72rem; color: #4F8EF7; margin-top: 0.8rem; }
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 📊 HR Analytics")
    st.markdown("---")
    st.caption("Dashboard v2.0 · C-Level View")

st.markdown("""
<div class="page-title">HR Analytics Dashboard</div>
<div class="page-subtitle">Sistem Analisis Kehadiran & Keterlambatan Karyawan</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")
with col1:
    with st.container(border=False):
        st.markdown("""
        <div class="nav-card blue">
            <div class="nc-icon">📈</div>
            <div class="nc-title">Attendance Forecast</div>
            <div class="nc-desc">
                Prakiraan tingkat kehadiran 30 hari kerja ke depan menggunakan model ML.
                Identifikasi hari berisiko rendah, kalender visual, dan tren mingguan.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Buka Attendance Forecast", use_container_width=True):
            print("User clicked Attendance Forecast")
            st.session_state["last_click"] = "attendance_forecast"
            st.switch_page("pages/1_Attendance_Forecast.py")

with col2:
    with st.container(border=False):
        st.markdown("""
        <div class="nav-card purple">
            <div class="nc-icon">🕐</div>
            <div class="nc-title">Late Analisis Karyawan</div>
            <div class="nc-desc">
                Ranking karyawan berdasarkan risk score keterlambatan. Tren per divisi,
                heatmap bulanan, dan forecast probabilitas terlambat per individu.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Buka Late Analisis Karyawan", use_container_width=True):
            print("User clicked Late Analysis")
            st.session_state["last_click"] = "late_analysis"
            st.switch_page("pages/2_Late_Analisis_Karyawan.py")