# pages/1_Attendance_Forecast.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from lib.ui import apply_theme, section_header
from lib.loaders import load_attendance
from lib.utils import download_csv_button

# =========================
# Setup & Theme Injection
# =========================
st.set_page_config(
    page_title="Attendance Forecast",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()

# ── Premium C-Level CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Root palette */
:root {
    --ink:       #0D1117;
    --slate:     #1C2333;
    --border:    #2A3347;
    --muted:     #6B7A99;
    --accent:    #4F8EF7;
    --accent2:   #F7A24F;
    --danger:    #F75B5B;
    --success:   #4FC98E;
    --surface:   #161D2E;
    --glass:     rgba(79,142,247,0.07);
}

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* Kill default Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.block-container { padding-top: 1.8rem !important; padding-bottom: 2rem; }

/* ── Page header ── */
.page-title {
    font-family: 'Sora', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    font-style: normal;
    color: #FFFFFF;
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 0.2rem;
}
.page-subtitle {
    font-size: 0.85rem;
    font-weight: 400;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* ── KPI Cards ── */
.kpi-wrap { display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }

.kpi-card {
    flex: 1;
    min-width: 160px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem 1.2rem;
    position: relative;
    overflow: hidden;
    transition: border-color .2s;
}
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.kpi-card.blue::before  { background: var(--accent); }
.kpi-card.amber::before { background: var(--accent2); }
.kpi-card.red::before   { background: var(--danger); }
.kpi-card.green::before { background: var(--success); }
.kpi-card.purple::before{ background: #A78BFA; }

.kpi-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.6rem;
}
.kpi-value {
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    font-size: 2.2rem;
    color: #FFFFFF;
    line-height: 1;
    margin-bottom: 0.35rem;
}
.kpi-delta {
    font-size: 0.78rem;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 99px;
    display: inline-block;
}
.kpi-delta.pos { background: rgba(79,201,142,0.15); color: var(--success); }
.kpi-delta.neg { background: rgba(247,91,91,0.15);  color: var(--danger); }
.kpi-delta.neu { background: rgba(107,122,153,0.15); color: var(--muted); }
.kpi-sub {
    font-size: 0.72rem;
    color: var(--muted);
    margin-top: 0.3rem;
}

/* ── Section headers ── */
.sec-head {
    display: flex; align-items: center; gap: .75rem;
    margin: 2rem 0 1rem;
}
.sec-head .bar {
    width: 4px; height: 22px;
    border-radius: 4px;
    background: var(--accent);
    flex-shrink: 0;
}
.sec-head h3 {
    font-family: 'Sora', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    font-style: normal;
    color: #E5EAF5;
    margin: 0;
}
.sec-head .badge {
    margin-left: auto;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--muted);
    border: 1px solid var(--border);
    padding: 3px 10px;
    border-radius: 99px;
}

/* ── Insight boxes ── */
.insight-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.insight-box {
    flex: 1; min-width: 200px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
}
.insight-box .i-title {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .5rem;
}
.insight-box .i-body {
    font-size: 0.88rem;
    color: #C5CEDE;
    line-height: 1.5;
}
.insight-box .i-body strong { color: #FFFFFF; }

/* ── Risk table ── */
.risk-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
}
.risk-table th {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--muted);
    padding: 8px 12px;
    border-bottom: 1px solid var(--border);
    text-align: left;
}
.risk-table td {
    padding: 10px 12px;
    border-bottom: 1px solid rgba(42,51,71,0.5);
    color: #C5CEDE;
}
.risk-table tr:last-child td { border-bottom: none; }
.risk-pill {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 99px;
    font-size: 0.7rem;
    font-weight: 700;
}
.risk-high   { background: rgba(247,91,91,.18);  color: var(--danger); }
.risk-medium { background: rgba(247,162,79,.18); color: var(--accent2); }
.risk-low    { background: rgba(79,201,142,.18); color: var(--success); }

/* ── Divider ── */
.h-line {
    height: 1px;
    background: var(--border);
    margin: 2rem 0;
    border: none;
}

/* ── Tabs override ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: var(--surface);
    border-radius: 10px;
    border: 1px solid var(--border);
    padding: 4px;
    width: fit-content;
}
.stTabs [data-baseweb="tab"] {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: .06em;
    padding: 6px 18px;
    border-radius: 7px;
    color: var(--muted);
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: white !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--ink); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
daily_att, fc_att, att_imp = load_attendance()

# =========================
# Sidebar Controls
# =========================
with st.sidebar:
    st.markdown("### ⚙️ Controls")
    hist_days = st.slider("Historical window (workdays)", 10, 90, 22, 1)

    threshold_warn  = st.slider("Warning threshold (%)", 50, 95, 75) / 100
    threshold_crit  = st.slider("Critical threshold (%)", 30, 75, 60) / 100

    st.markdown("---")
    st.caption("Dashboard v2.0 · C-Level View")

# =========================
# Data Prep
# =========================
daily_att = daily_att.sort_values("date").copy()
fc = fc_att.sort_values("date").copy()
hist = daily_att.tail(hist_days).copy()

# Derive emp_ref otomatis dari kolom 'employee' di data, fallback ke kolom 'total' atau median attendance
if "employee" in daily_att.columns:
    emp_ref = int(round(pd.to_numeric(daily_att["employee"], errors="coerce").dropna().iloc[-1]))
elif "total" in daily_att.columns:
    emp_ref = int(round(pd.to_numeric(daily_att["total"], errors="coerce").dropna().iloc[-1]))
else:
    # fallback: estimasi dari max actual hadir (attendance_rate * inferred headcount)
    emp_ref = 300  # default aman jika kolom tidak tersedia

# Guard
for required, df_name, df_obj in [
    ("attendance_rate", "daily_full_weekday.csv", hist),
    ("prediction", "attendance_forecast_result.csv", fc),
]:
    if required not in df_obj.columns:
        st.error(f"Kolom '{required}' tidak ditemukan di {df_name}")
        st.stop()

# Holiday normalisation
for df in (hist, fc):
    if "is_holiday" not in df.columns: df["is_holiday"] = 0
    if "holiday_name" not in df.columns: df["holiday_name"] = ""
    if "holiday_type" not in df.columns: df["holiday_type"] = "None"
    df["holiday_name"]  = df["holiday_name"].fillna("")
    df["holiday_type"]  = df["holiday_type"].fillna("None")
    df["is_holiday"]    = pd.to_numeric(df["is_holiday"], errors="coerce").fillna(0).astype(int)

fc["expected_present"] = (fc["prediction"] * emp_ref).round().astype(int)

# Risk flags
fc["risk"] = "Normal"
fc.loc[fc["prediction"] < threshold_warn, "risk"] = "Warning"
fc.loc[fc["prediction"] < threshold_crit, "risk"] = "Critical"

# Hover labels
def make_hover(row, is_weekend=False):
    if int(row["is_holiday"]) == 1:
        nm = row["holiday_name"] if str(row["holiday_name"]).strip() else "Hari Libur"
        tp = row["holiday_type"] if str(row["holiday_type"]).strip() else "Holiday"
        return f"🎌 {nm} ({tp})"
    return "🏖 Weekend" if is_weekend else "💼 Workday"

hist["hover_label"] = hist.apply(make_hover, axis=1)
fc["hover_label"]   = fc.apply(make_hover, axis=1)

# Bridge line historical → forecast
fc_line = fc.copy()
if len(hist) and len(fc):
    bridge = pd.DataFrame({
        "date":             [hist["date"].iloc[-1]],
        "prediction":       [hist["attendance_rate"].iloc[-1]],
        "expected_present": [int(round(hist["attendance_rate"].iloc[-1] * emp_ref))],
        "is_holiday":       [int(hist["is_holiday"].iloc[-1])],
        "holiday_name":     [hist["holiday_name"].iloc[-1]],
        "holiday_type":     [hist["holiday_type"].iloc[-1]],
        "hover_label":      [hist["hover_label"].iloc[-1]],
        "risk":             ["Normal"],
    })
    fc_line = pd.concat([bridge, fc_line], ignore_index=True).sort_values("date")

# =========================
# Derived Metrics
# =========================
avg_pred       = float(fc["prediction"].mean())
avg_hist       = float(hist["attendance_rate"].mean()) if "attendance_rate" in hist.columns else avg_pred
delta_vs_hist  = avg_pred - avg_hist

min_row  = fc.loc[fc["prediction"].idxmin()]
max_row  = fc.loc[fc["prediction"].idxmax()]

crit_days  = int((fc["risk"] == "Critical").sum())
warn_days  = int((fc["risk"] == "Warning").sum())
hol_days   = int((fc["is_holiday"] == 1).sum())
total_wdays= len(fc)

# Trend: simple linear slope over forecast window
slope = 0.0
if len(fc) >= 3:
    xs = np.arange(len(fc))
    slope = float(np.polyfit(xs, fc["prediction"].values, 1)[0])

trend_label = "▲ Naik"   if slope >  0.001 else (
              "▼ Turun"  if slope < -0.001 else "→ Stabil")
trend_cls   = "pos" if slope > 0.001 else ("neg" if slope < -0.001 else "neu")

# Expected absent on lowest day
absent_min = emp_ref - int(min_row["expected_present"])

# =========================
# Page Header
# =========================
st.markdown("""
<div class="page-title">Dashboard Kehadiran</div>
<div class="page-subtitle">Prakiraan 30 Hari Kerja · Ringkasan Eksekutif</div>
""", unsafe_allow_html=True)

# =========================
# KPI Strip
# =========================
delta_sign  = "+" if delta_vs_hist >= 0 else ""
delta_cls   = "pos" if delta_vs_hist >= 0 else "neg"

hol_rate_txt = f"{hol_days} hari libur"

st.markdown(f"""
<div class="kpi-wrap">
  <div class="kpi-card blue">
    <div class="kpi-label">Rata-rata Tingkat Kehadiran</div>
    <div class="kpi-value">{avg_pred*100:.1f}%</div>
    <div class="kpi-delta {delta_cls}">{delta_sign}{delta_vs_hist*100:.1f}% vs periode lalu</div>
    <div class="kpi-sub">{total_wdays} hari kerja ke depan</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-label">Hari Puncak Kehadiran</div>
    <div class="kpi-value">{max_row['prediction']*100:.1f}%</div>
    <div class="kpi-delta pos">↑ Hari terbaik</div>
    <div class="kpi-sub">{max_row['date'].date()}</div>
  </div>
  <div class="kpi-card {'red' if min_row['prediction'] < threshold_crit else 'amber'}">
    <div class="kpi-label">Hari Terendah</div>
    <div class="kpi-value">{min_row['prediction']*100:.1f}%</div>
    <div class="kpi-delta neg">~{absent_min} tidak hadir</div>
    <div class="kpi-sub">{min_row['date'].date()}</div>
  </div>
  <div class="kpi-card {'red' if crit_days > 0 else 'amber' if warn_days > 0 else 'green'}">
    <div class="kpi-label">Hari Berisiko</div>
    <div class="kpi-value">{crit_days + warn_days}</div>
    <div class="kpi-delta {'neg' if crit_days > 0 else 'neu'}">{crit_days} kritis · {warn_days} waspada</div>
    <div class="kpi-sub">dari {total_wdays} total hari kerja</div>
  </div>
  <div class="kpi-card purple">
    <div class="kpi-label">Tren Prakiraan</div>
    <div class="kpi-value" style="font-size:1.8rem">{trend_label}</div>
    <div class="kpi-delta {trend_cls}">{slope*100:+.3f}%/hari</div>
    <div class="kpi-sub">{hol_rate_txt} dalam periode ini</div>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================
# Insight Boxes
# =========================
# Build narrative
risk_narrative = "Tidak ada hari dengan risiko kehadiran kritis — perencanaan tenaga kerja dapat berjalan normal." \
    if crit_days == 0 else \
    f"<strong>{crit_days} hari kritis</strong> diprakirakan di bawah {threshold_crit*100:.0f}% — rekomendasikan tindakan proaktif SDM."

trend_narrative = (
    f"Kehadiran berada dalam <strong>tren naik</strong> (+{slope*100:.3f}%/hari). "
    "Sinyal positif untuk kelangsungan operasional." if slope > 0.001
    else f"Kehadiran menunjukkan <strong>tren menurun</strong> ({slope*100:.3f}%/hari). "
    "Pantau secara berkala untuk intervensi dini." if slope < -0.001
    else "Prakiraan kehadiran <strong>stabil</strong> — variasi minimal diperkirakan dalam periode ini."
)

holiday_narrative = (
    f"<strong>{hol_days} hari libur nasional</strong> jatuh dalam jendela prakiraan. "
    "Kehadiran pada hari-hari sekitarnya berpotensi turun akibat pola libur panjang."
    if hol_days > 0 else
    "Tidak ada hari libur nasional dalam jendela prakiraan. Ketersediaan tenaga kerja penuh diperkirakan."
)

st.markdown(f"""
<div class="insight-row">
  <div class="insight-box">
    <div class="i-title">Penilaian Risiko 🔴</div>
    <div class="i-body">{risk_narrative}</div>
  </div>
  <div class="insight-box">
    <div class="i-title">Sinyal Tren 📈</div>
    <div class="i-body">{trend_narrative}</div>
  </div>
  <div class="insight-box">
    <div class="i-title">Dampak Hari Libur 🎌</div>
    <div class="i-body">{holiday_narrative}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================
# Main Tabs
# =========================
tab1, tab2, tab3 = st.tabs(["  Grafik Prakiraan  ", "  Tampilan Kalender  ", "  Rincian Risiko  "])

# ─────────────────────────────────────────────────────────────────
# TAB 1 – Forecast Chart (enhanced)
# ─────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="sec-head"><div class="bar"></div><h3>Historis vs Prakiraan</h3><span class="badge">Model Aktif</span></div>', unsafe_allow_html=True)

    fig = go.Figure()

    # Confidence band (±1.5% simulated around forecast)
    if len(fc_line) > 1:
        fig.add_trace(go.Scatter(
            x=pd.concat([fc_line["date"], fc_line["date"][::-1]]),
            y=pd.concat([fc_line["prediction"] + 0.015, (fc_line["prediction"] - 0.015)[::-1]]),
            fill="toself",
            fillcolor="rgba(79,142,247,0.10)",
            line=dict(color="rgba(0,0,0,0)"),
            name="Rentang Kepercayaan",
            hoverinfo="skip",
            showlegend=True,
        ))

    # Historical line
    fig.add_trace(go.Scatter(
        x=hist["date"],
        y=hist["attendance_rate"],
        mode="lines",
        name="Historis",
        line=dict(width=2.5, color="#6B7A99"),
        customdata=hist[["hover_label"]].values,
        hovertemplate="%{x|%Y-%m-%d}<br>Aktual: <b>%{y:.1%}</b><br>%{customdata[0]}<extra></extra>",
    ))

    # Forecast line
    fig.add_trace(go.Scatter(
        x=fc_line["date"],
        y=fc_line["prediction"],
        mode="lines",
        name="Prakiraan",
        line=dict(width=3, color="#4F8EF7", dash="dot"),
        customdata=fc_line[["expected_present", "hover_label"]].fillna("").values,
        hovertemplate="%{x|%Y-%m-%d}<br>Prakiraan: <b>%{y:.1%}</b><br>Perkiraan hadir: %{customdata[0]} org<br>%{customdata[1]}<extra></extra>",
    ))

    risk_id_map = {"Critical": "Kritis", "Warning": "Waspada"}
    for risk_val, color in [("Critical", "#F75B5B"), ("Warning", "#F7A24F")]:
        sub = fc[fc["risk"] == risk_val]
        if len(sub):
            fig.add_trace(go.Scatter(
                x=sub["date"], y=sub["prediction"],
                mode="markers",
                name=f"Hari {risk_id_map[risk_val]}",
                marker=dict(size=10, color=color, symbol="circle",
                            line=dict(color="white", width=1.5)),
                customdata=sub[["expected_present", "hover_label"]].values,
                hovertemplate=f"<b>{risk_id_map[risk_val]}</b><br>%{{x|%Y-%m-%d}}<br>%{{y:.1%}} · %{{customdata[0]}} org<extra></extra>",
            ))

    # Threshold lines
    for thr, label, color in [
        (threshold_warn, f"Waspada ({threshold_warn:.0%})", "#F7A24F"),
        (threshold_crit, f"Kritis ({threshold_crit:.0%})", "#F75B5B"),
    ]:
        fig.add_hline(
            y=thr, line_dash="dash", line_color=color, line_width=1.2,
            annotation_text=label,
            annotation_font_color=color,
            annotation_font_size=11,
        )

    # Forecast zone
    if len(fc):
        fig.add_vrect(x0=fc["date"].min(), x1=fc["date"].max(),
                      fillcolor="rgba(79,142,247,0.05)", line_width=0)

    # Holiday shading
    for _, r in fc[fc["is_holiday"] == 1].iterrows():
        fig.add_vrect(
            x0=r["date"], x1=r["date"] + pd.Timedelta(days=1),
            fillcolor="rgba(247,162,79,0.12)", line_width=0,
        )

    # Trend line
    if len(fc) >= 3:
        xs = np.arange(len(fc))
        m, b = np.polyfit(xs, fc["prediction"].values, 1)
        trend_y = m * xs + b
        fig.add_trace(go.Scatter(
            x=fc["date"], y=trend_y,
            mode="lines", name="Garis Tren",
            line=dict(width=1.5, color="#A78BFA", dash="longdash"),
            hoverinfo="skip",
        ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(22,29,46,0)",
        plot_bgcolor ="rgba(22,29,46,0)",
        height=480,
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis=dict(title="Tingkat Kehadiran", tickformat=".0%",
                   gridcolor="rgba(42,51,71,0.5)", zeroline=False),
        xaxis=dict(title="Tanggal", gridcolor="rgba(42,51,71,0.4)", zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                    bgcolor="rgba(0,0,0,0)", font_size=12),
        hovermode="x unified",
        font=dict(family="DM Sans"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Weekly average bar chart
    st.markdown('<div class="sec-head"><div class="bar" style="background:#A78BFA"></div><h3>Rata-rata Kehadiran per Minggu</h3><span class="badge">Agregasi Mingguan</span></div>', unsafe_allow_html=True)

    fc_weekly = fc.copy()
    fc_weekly["week"] = fc_weekly["date"].dt.to_period("W-SUN").apply(lambda p: p.start_time)
    wk_agg = fc_weekly.groupby("week").agg(
        avg_rate=("prediction", "mean"),
        min_rate=("prediction", "min"),
        max_rate=("prediction", "max"),
        expected=("expected_present", "mean"),
        n=("prediction", "count"),
    ).reset_index()
    wk_agg["week_label"] = wk_agg["week"].dt.strftime("Wk %d %b")

    bar_colors = []
    for r in wk_agg["avg_rate"]:
        if r < threshold_crit:   bar_colors.append("#F75B5B")
        elif r < threshold_warn: bar_colors.append("#F7A24F")
        else:                    bar_colors.append("#4F8EF7")

    wk_fig = go.Figure()
    wk_fig.add_trace(go.Bar(
        x=wk_agg["week_label"],
        y=wk_agg["avg_rate"],
        marker_color=bar_colors,
        marker_line_width=0,
        text=[f"{v:.1%}" for v in wk_agg["avg_rate"]],
        textposition="outside",
        textfont=dict(size=11, color="white"),
        customdata=wk_agg[["min_rate", "max_rate", "expected"]].values,
        hovertemplate=(
            "<b>%{x}</b><br>Rata-rata: %{y:.1%}<br>"
            "Min: %{customdata[0]:.1%}  Maks: %{customdata[1]:.1%}<br>"
            "Perkiraan hadir: %{customdata[2]:.0f} org<extra></extra>"
        ),
    ))
    wk_fig.add_hline(y=threshold_warn, line_dash="dash", line_color="#F7A24F", line_width=1)
    wk_fig.add_hline(y=threshold_crit, line_dash="dash", line_color="#F75B5B", line_width=1)
    wk_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(22,29,46,0)",
        plot_bgcolor ="rgba(22,29,46,0)",
        height=280,
        margin=dict(l=10, r=10, t=20, b=10),
        yaxis=dict(tickformat=".0%", gridcolor="rgba(42,51,71,0.4)", zeroline=False, range=[0, 1.08]),
        xaxis=dict(gridcolor="rgba(0,0,0,0)"),
        font=dict(family="DM Sans"),
        showlegend=False,
    )
    st.plotly_chart(wk_fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────────
# TAB 2 – Calendar View
# ─────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="sec-head"><div class="bar" style="background:#4FC98E"></div><h3>Heatmap Kalender — 30 Hari ke Depan</h3><span class="badge">Warna = Tingkat Kehadiran</span></div>', unsafe_allow_html=True)

    forecast_start = fc["date"].min()
    calendar_start = forecast_start.to_period("W-SUN").start_time
    calendar_end   = forecast_start + pd.Timedelta(days=29)

    cal = pd.DataFrame({"date": pd.date_range(start=calendar_start, end=calendar_end, freq="D")})
    cal["dow"]        = cal["date"].dt.dayofweek
    cal["is_weekend"] = (cal["dow"] >= 5).astype(int)

    need_cols = ["date", "prediction", "expected_present", "is_holiday", "holiday_name", "holiday_type", "risk"]
    fc_merge  = fc.copy()
    for c in need_cols:
        if c not in fc_merge.columns: fc_merge[c] = np.nan
    fc_merge = fc_merge[need_cols].copy()
    cal = cal.merge(fc_merge, on="date", how="left")

    for col in ["is_holiday", "is_weekend"]:
        cal[col] = pd.to_numeric(cal[col], errors="coerce").fillna(0).astype(int)
    cal["holiday_name"] = cal["holiday_name"].fillna("")
    cal["holiday_type"] = cal["holiday_type"].fillna("None")
    cal["expected_present"] = pd.to_numeric(cal["expected_present"], errors="coerce")
    cal.loc[(cal["is_weekend"] == 1) & cal["expected_present"].isna(), "expected_present"] = 0
    cal.loc[(cal["date"] < forecast_start) & (cal["is_weekend"] == 0), "expected_present"] = np.nan
    cal["risk"] = cal["risk"].fillna("Weekend")

    cal["week_start"] = cal["date"].dt.to_period("W-SUN").apply(lambda p: p.start_time)
    week_starts  = sorted(cal["week_start"].unique())
    week_to_row  = {ws: i for i, ws in enumerate(week_starts)}
    cal["week_row"] = cal["week_start"].map(week_to_row)

    rows, cols_n = len(week_starts), 7
    Z     = np.full((rows, cols_n), np.nan, dtype=float)
    TEXT  = np.full((rows, cols_n), "", dtype=object)
    HOVER = np.full((rows, cols_n), "", dtype=object)
    RISK  = np.full((rows, cols_n), "", dtype=object)

    dow_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    for _, r in cal.iterrows():
        i = int(r["week_row"]); j = int(r["dow"])
        pred = r["prediction"] if pd.notna(r["prediction"]) else np.nan
        Z[i, j] = float(pred) if pd.notna(pred) else np.nan

        day_txt = r["date"].strftime("%d")
        ep      = r["expected_present"]
        sub_txt = "" if pd.isna(ep) else f"\n{int(ep)}p"
        TEXT[i, j] = f"{day_txt}{sub_txt}"

        ep_txt = "N/A" if pd.isna(ep) else str(int(ep))
        rate_txt = f"{pred:.1%}" if pd.notna(pred) else "N/A"

        hname = r["holiday_name"] if str(r["holiday_name"]).strip() else "Holiday"
        if r["is_holiday"] == 1:
            label = f"🎌 {hname}"
        elif r["is_weekend"] == 1:
            label = "🏖 Akhir Pekan"
        else:
            label = "💼 Hari Kerja"

        HOVER[i, j] = (
            f"<b>{r['date'].strftime('%A, %d %b %Y')}</b><br>"
            f"Kehadiran: {rate_txt}<br>"
            f"Perkiraan hadir: {ep_txt} org<br>"
            f"{label}"
        )
        RISK[i, j] = str(r["risk"])

    cal_fig = go.Figure()
    cal_fig.add_trace(go.Heatmap(
        z=Z, x=list(range(7)), y=list(range(rows)),
        hoverinfo="text", hovertext=HOVER,
        text=TEXT, texttemplate="%{text}",
        textfont={"size": 11, "family": "DM Sans"},
        showscale=True,
        colorscale=[
            [0.0, "#F75B5B"],
            [float(threshold_crit), "#F7A24F"],
            [float(threshold_warn), "#F7E94F"],
            [1.0, "#4FC98E"],
        ],
        zmin=0, zmax=1,
        colorbar=dict(
            title=dict(text="Tingkat", font=dict(size=11, family="DM Sans")),
            tickformat=".0%",
            len=0.6,
        ),
    ))

    shapes = []
    for i in range(rows):
        for j in [5, 6]:
            shapes.append(dict(
                type="rect", xref="x", yref="y",
                x0=j-.5, x1=j+.5, y0=i-.5, y1=i+.5,
                fillcolor="rgba(30,30,40,0.55)", line_width=0, layer="above",
            ))
    for _, r in cal[cal["is_holiday"] == 1].iterrows():
        i = int(r["week_row"]); j = int(r["dow"])
        shapes.append(dict(
            type="rect", xref="x", yref="y",
            x0=j-.5, x1=j+.5, y0=i-.5, y1=i+.5,
            fillcolor="rgba(0,0,0,0)",
            line=dict(color="#F7A24F", width=3), layer="above",
        ))
    # Critical: thick red border
    for _, r in cal[(cal["risk"] == "Critical") & (cal["is_weekend"] == 0)].iterrows():
        i = int(r["week_row"]); j = int(r["dow"])
        shapes.append(dict(
            type="rect", xref="x", yref="y",
            x0=j-.5, x1=j+.5, y0=i-.5, y1=i+.5,
            fillcolor="rgba(0,0,0,0)",
            line=dict(color="#F75B5B", width=3), layer="above",
        ))

    week_labels = [ws.strftime("Wk %d %b") for ws in week_starts]
    cal_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(22,29,46,0)",
        plot_bgcolor ="rgba(22,29,46,0)",
        height=260 + rows * 60,
        margin=dict(l=10, r=10, t=10, b=10),
        shapes=shapes,
        xaxis=dict(tickmode="array", tickvals=list(range(7)), ticktext=dow_names,
                   side="top", showgrid=False, zeroline=False,
                   tickfont=dict(size=12, family="DM Sans")),
        yaxis=dict(tickmode="array", tickvals=list(range(rows)), ticktext=week_labels,
                   autorange="reversed", showgrid=False, zeroline=False,
                   tickfont=dict(size=11, family="DM Sans")),
        font=dict(family="DM Sans"),
    )
    st.plotly_chart(cal_fig, use_container_width=True)

    # Legend
    st.markdown("""
    <div style="display:flex;gap:1.5rem;font-size:0.75rem;color:#6B7A99;margin-top:-.5rem">
      <span><b style="color:#F75B5B">■</b> Kritis (&lt;60%)</span>
      <span><b style="color:#F7A24F">■</b> Waspada (&lt;75%)</span>
      <span><b style="color:#F7E94F">■</b> Sedang</span>
      <span><b style="color:#4FC98E">■</b> Baik</span>
      <span><b style="color:#F7A24F">▣</b> Hari Libur</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# TAB 3 – Risk Breakdown
# ─────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="sec-head"><div class="bar" style="background:#F75B5B"></div><h3>Detail Hari Berisiko</h3><span class="badge">Perlu Tindakan</span></div>', unsafe_allow_html=True)

    risk_days = fc[fc["risk"].isin(["Critical", "Warning"])].copy()

    if len(risk_days) == 0:
        st.success("✅ Tidak ada hari berisiko dalam jendela prakiraan. Kehadiran diperkirakan tetap di atas ambang batas.")
    else:
        rows_html = ""
        risk_id_map = {"Critical": "Kritis", "Warning": "Waspada"}
        for _, r in risk_days.sort_values("date").iterrows():
            cls  = "risk-high" if r["risk"] == "Critical" else "risk-medium"
            hol  = f"<br><span style='font-size:.7rem;color:#6B7A99'>{r['holiday_name']} ({r['holiday_type']})</span>" \
                   if int(r["is_holiday"]) == 1 else ""
            gap  = emp_ref - int(r["expected_present"])
            rows_html += f"""
            <tr>
              <td>{r['date'].strftime('%A, %d %b %Y')}{hol}</td>
              <td><b>{r['prediction']*100:.1f}%</b></td>
              <td>{int(r['expected_present'])} / {emp_ref}</td>
              <td><b style="color:#F75B5B">~{gap} tidak hadir</b></td>
              <td><span class="risk-pill {cls}">{risk_id_map[r['risk']]}</span></td>
            </tr>"""

        st.markdown(f"""
        <table class="risk-table">
          <thead>
            <tr>
              <th>Tanggal</th><th>Tingkat Prakiraan</th><th>Perkiraan Hadir</th>
              <th>Estimasi Tidak Hadir</th><th>Level Risiko</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)

    # Distribution gauge
    st.markdown('<div class="sec-head"><div class="bar" style="background:#A78BFA"></div><h3>Distribusi Prakiraan 30 Hari</h3><span class="badge">Analisis Sebaran</span></div>', unsafe_allow_html=True)

    dist_fig = go.Figure()
    dist_fig.add_trace(go.Histogram(
        x=fc["prediction"],
        nbinsx=20,
        marker_color="#4F8EF7",
        marker_line_color="#1C2333",
        marker_line_width=1,
        opacity=0.85,
        name="Days",
        hovertemplate="Tingkat: %{x:.1%}<br>Jumlah Hari: %{y}<extra></extra>",
    ))
    for thr, color, label in [
        (threshold_crit, "#F75B5B", "Kritis"),
        (threshold_warn, "#F7A24F", "Waspada"),
    ]:
        dist_fig.add_vline(x=thr, line_dash="dash", line_color=color, line_width=1.5,
                           annotation_text=label, annotation_font_color=color, annotation_font_size=11)

    dist_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(22,29,46,0)",
        plot_bgcolor ="rgba(22,29,46,0)",
        height=260,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(tickformat=".0%", gridcolor="rgba(42,51,71,0.4)", title="Tingkat Kehadiran"),
        yaxis=dict(title="Jumlah Hari", gridcolor="rgba(42,51,71,0.4)"),
        font=dict(family="DM Sans"),
        showlegend=False,
    )
    st.plotly_chart(dist_fig, use_container_width=True)

# =========================
# Footer + Export
# =========================
st.markdown('<hr class="h-line">', unsafe_allow_html=True)

col_exp, col_note = st.columns([1, 3])
with col_exp:
    export_df = fc[["date", "prediction", "expected_present", "risk", "is_holiday", "holiday_name"]].copy()
    export_df["date"] = export_df["date"].dt.strftime("%Y-%m-%d")
    export_df.columns = ["Tanggal", "Tingkat Prakiraan", "Perkiraan Hadir", "Risiko", "Hari Libur", "Nama Libur"]
    download_csv_button(export_df, filename="prakiraan_kehadiran.csv", label="⬇ Ekspor CSV Prakiraan")
with col_note:
    st.caption(
        f"Output model · {total_wdays} hari kerja diprakirakan · "
        f"Ambang batas: Waspada {threshold_warn:.0%} / Kritis {threshold_crit:.0%} · "
        f"Referensi jumlah karyawan: {emp_ref} orang"
    )