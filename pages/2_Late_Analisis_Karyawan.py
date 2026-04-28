# pages/2_Late_Analisis_Karyawan.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from lib.ui import apply_theme
from lib.loaders import load_late
from lib.utils import download_csv_button, fmt_pct

st.set_page_config(
    page_title="Late Analisis Karyawan",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()

# ── CSS — konsisten dengan page 1 ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --ink:     #0D1117;
    --slate:   #1C2333;
    --border:  #2A3347;
    --muted:   #6B7A99;
    --accent:  #4F8EF7;
    --accent2: #F7A24F;
    --danger:  #F75B5B;
    --success: #4FC98E;
    --surface: #161D2E;
    --purple:  #A78BFA;
}

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
.block-container { padding-top: 1.8rem !important; padding-bottom: 2rem; }

/* ── Page header ── */
.page-title {
    font-family: 'Sora', sans-serif;
    font-size: 2.4rem; font-weight: 800;
    color: #FFFFFF; letter-spacing: -0.03em;
    line-height: 1; margin-bottom: 0.2rem;
}
.page-subtitle {
    font-size: 0.85rem; font-weight: 400;
    color: var(--muted); letter-spacing: 0.12em;
    text-transform: uppercase; margin-bottom: 2rem;
}

/* ── KPI Cards ── */
.kpi-wrap { display:flex; gap:1rem; margin-bottom:2rem; flex-wrap:wrap; }
.kpi-card {
    flex:1; min-width:160px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.4rem 1.6rem 1.2rem;
    position: relative; overflow: hidden;
}
.kpi-card::before {
    content:''; position:absolute; top:0; left:0; right:0;
    height:3px; border-radius:16px 16px 0 0;
}
.kpi-card.blue::before   { background: var(--accent); }
.kpi-card.amber::before  { background: var(--accent2); }
.kpi-card.red::before    { background: var(--danger); }
.kpi-card.green::before  { background: var(--success); }
.kpi-card.purple::before { background: var(--purple); }

.kpi-label {
    font-size:0.7rem; font-weight:600;
    letter-spacing:0.14em; text-transform:uppercase;
    color:var(--muted); margin-bottom:0.6rem;
}
.kpi-value {
    font-family:'Sora', sans-serif; font-weight:700;
    font-size:2.2rem; color:#FFFFFF;
    line-height:1; margin-bottom:0.35rem;
}
.kpi-delta {
    font-size:0.78rem; font-weight:500;
    padding:2px 8px; border-radius:99px; display:inline-block;
}
.kpi-delta.neg { background:rgba(247,91,91,0.15);  color:var(--danger); }
.kpi-delta.pos { background:rgba(79,201,142,0.15); color:var(--success); }
.kpi-delta.neu { background:rgba(107,122,153,0.15);color:var(--muted); }
.kpi-sub { font-size:0.72rem; color:var(--muted); margin-top:0.3rem; }

/* ── Section headers ── */
.sec-head { display:flex; align-items:center; gap:.75rem; margin:2rem 0 1rem; }
.sec-head .bar { width:4px; height:22px; border-radius:4px; background:var(--accent); flex-shrink:0; }
.sec-head h3 {
    font-family:'Sora', sans-serif; font-size:1.1rem;
    font-weight:700; color:#E5EAF5; margin:0;
}
.sec-head .badge {
    margin-left:auto; font-size:0.65rem; font-weight:600;
    letter-spacing:.1em; text-transform:uppercase; color:var(--muted);
    border:1px solid var(--border); padding:3px 10px; border-radius:99px;
}

/* ── Risk pills ── */
.risk-pill { display:inline-block; padding:2px 10px; border-radius:99px; font-size:0.7rem; font-weight:700; }
.risk-high   { background:rgba(247,91,91,.18);  color:var(--danger); }
.risk-medium { background:rgba(247,162,79,.18); color:var(--accent2); }
.risk-low    { background:rgba(79,201,142,.18); color:var(--success); }

/* ── Risk table ── */
.risk-table { width:100%; border-collapse:collapse; font-size:0.82rem; }
.risk-table th {
    font-size:0.65rem; font-weight:700; letter-spacing:.12em;
    text-transform:uppercase; color:var(--muted);
    padding:8px 12px; border-bottom:1px solid var(--border); text-align:left;
}
.risk-table td {
    padding:10px 12px;
    border-bottom:1px solid rgba(42,51,71,0.5);
    color:#C5CEDE;
}
.risk-table tr:last-child td { border-bottom:none; }
.risk-table tr:hover td { background:rgba(79,142,247,0.04); }

/* ── Insight boxes ── */
.insight-row { display:flex; gap:1rem; margin-bottom:1.5rem; flex-wrap:wrap; }
.insight-box {
    flex:1; min-width:200px;
    background:var(--surface); border:1px solid var(--border);
    border-radius:12px; padding:1rem 1.2rem;
}
.insight-box .i-title {
    font-size:0.68rem; font-weight:700; letter-spacing:.12em;
    text-transform:uppercase; color:var(--muted); margin-bottom:.5rem;
}
.insight-box .i-body { font-size:0.88rem; color:#C5CEDE; line-height:1.5; }
.insight-box .i-body strong { color:#FFFFFF; }

/* ── Tabs override ── */
.stTabs [data-baseweb="tab-list"] {
    gap:0; background:var(--surface);
    border-radius:10px; border:1px solid var(--border);
    padding:4px; width:fit-content;
}
.stTabs [data-baseweb="tab"] {
    font-size:0.78rem; font-weight:600;
    letter-spacing:.06em; padding:6px 18px;
    border-radius:7px; color:var(--muted);
}
.stTabs [aria-selected="true"] { background:var(--accent) !important; color:white !important; }

.h-line { height:1px; background:var(--border); margin:2rem 0; border:none; }

::-webkit-scrollbar { width:6px; }
::-webkit-scrollbar-track { background:var(--ink); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
ts_div, fc_div, met_div, emp_sum, emp_mon = load_late()

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown("### ⚙️ Controls")

    all_divisions = sorted(emp_sum["division"].dropna().unique().tolist())
    sel_divisions = st.multiselect("Filter Divisi", all_divisions, default=all_divisions)

    if "department_clean" in emp_sum.columns:
        all_depts = sorted(emp_sum["department_clean"].dropna().unique().tolist())
        sel_depts = st.multiselect("Filter Departemen", all_depts, default=all_depts)
    else:
        sel_depts = None

    top_n = st.slider("Tampilkan Top-N Karyawan Berisiko", 5, 50, 20, 5)
    risk_threshold_high   = st.slider("Threshold High Risk (%)",   30, 80, 50) / 100
    risk_threshold_medium = st.slider("Threshold Medium Risk (%)", 10, 50, 25) / 100

    st.markdown("---")
    st.caption("Dashboard v2.0 · C-Level View")

# =========================
# Filter data
# =========================
emp_f = emp_sum[emp_sum["division"].isin(sel_divisions)].copy()
if sel_depts is not None and "department_clean" in emp_f.columns:
    emp_f = emp_f[emp_f["department_clean"].isin(sel_depts)]

ts_f  = ts_div[ts_div["division"].isin(sel_divisions)].copy()
fc_f  = fc_div[fc_div["division"].isin(sel_divisions)].copy()

# Assign risk tier
def assign_tier(score):
    if pd.isna(score): return "Unknown"
    if score >= risk_threshold_high:   return "High"
    if score >= risk_threshold_medium: return "Medium"
    return "Low"

emp_f["risk_tier"] = emp_f["risk_score"].apply(assign_tier)

# =========================
# Derived KPI metrics
# =========================
total_emp       = len(emp_f)
high_risk_count = int((emp_f["risk_tier"] == "High").sum())
med_risk_count  = int((emp_f["risk_tier"] == "Medium").sum())
low_risk_count  = int((emp_f["risk_tier"] == "Low").sum())

avg_late_overall = float(emp_f["late_rate_overall"].mean()) if "late_rate_overall" in emp_f.columns else 0.0
avg_late_recent  = float(emp_f["late_rate_recent3"].mean()) if "late_rate_recent3" in emp_f.columns else 0.0
delta_late       = avg_late_recent - avg_late_overall

# Trend direction overall
trending_worse = 0
if "trend_late" in emp_f.columns:
    trending_worse = int((emp_f["trend_late"] > 0).sum())

# =========================
# Page Header
# =========================
st.markdown("""
<div class="page-title">Analisis Keterlambatan</div>
<div class="page-subtitle">Risiko Per Karyawan · Tren Divisi · Forecast Ke Depan</div>
""", unsafe_allow_html=True)

# =========================
# KPI Strip
# =========================
delta_cls  = "neg" if delta_late > 0 else "pos"
delta_sign = "+" if delta_late > 0 else ""
trend_icon = f"↑ {trending_worse} karyawan memburuk" if trending_worse > 0 else "→ Tren stabil"
trend_cls  = "neg" if trending_worse > 0 else "pos"

st.markdown(f"""
<div class="kpi-wrap">
  <div class="kpi-card blue">
    <div class="kpi-label">Total Karyawan</div>
    <div class="kpi-value">{total_emp:,}</div>
    <div class="kpi-delta neu">{len(sel_divisions)} divisi</div>
    <div class="kpi-sub">dalam filter aktif</div>
  </div>
  <div class="kpi-card red">
    <div class="kpi-label">Risiko Tinggi</div>
    <div class="kpi-value">{high_risk_count}</div>
    <div class="kpi-delta neg">{high_risk_count/max(total_emp,1):.1%} dari total</div>
    <div class="kpi-sub">risk score ≥ {risk_threshold_high:.0%}</div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-label">Risiko Sedang</div>
    <div class="kpi-value">{med_risk_count}</div>
    <div class="kpi-delta neu">{med_risk_count/max(total_emp,1):.1%} dari total</div>
    <div class="kpi-sub">risk score {risk_threshold_medium:.0%}–{risk_threshold_high:.0%}</div>
  </div>
  <div class="kpi-card {'red' if delta_late > 0.01 else 'green'}">
    <div class="kpi-label">Rata-rata Late Rate</div>
    <div class="kpi-value">{avg_late_recent:.1%}</div>
    <div class="kpi-delta {delta_cls}">{delta_sign}{delta_late:.1%} vs keseluruhan</div>
    <div class="kpi-sub">3 bulan terakhir</div>
  </div>
  <div class="kpi-card purple">
    <div class="kpi-label">Tren Keterlambatan</div>
    <div class="kpi-value" style="font-size:1.8rem">{'↑ Naik' if trending_worse > total_emp*0.3 else ('→ Stabil')}</div>
    <div class="kpi-delta {trend_cls}">{trend_icon}</div>
    <div class="kpi-sub">berdasarkan trend_late score</div>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================
# Insight Boxes
# =========================
top1 = emp_f.sort_values("risk_score", ascending=False).iloc[0] if len(emp_f) else None
worst_div = emp_f.groupby("division")["late_rate_overall"].mean().idxmax() if len(emp_f) else "-"
worst_div_rate = emp_f.groupby("division")["late_rate_overall"].mean().max() if len(emp_f) else 0

st.markdown(f"""
<div class="insight-row">
  <div class="insight-box">
    <div class="i-title">🔴 Karyawan Paling Berisiko</div>
    <div class="i-body">
      {"<strong>" + str(top1['employee_name']) + "</strong> memiliki risk score tertinggi " +
       f"(<strong>{top1['risk_score']:.2f}</strong>) dengan late rate overall " +
       f"<strong>{top1.get('late_rate_overall', 0):.1%}</strong>." if top1 is not None else "Tidak ada data."}
    </div>
  </div>
  <div class="insight-box">
    <div class="i-title">🏢 Divisi Paling Terdampak</div>
    <div class="i-body">
      Divisi <strong>{worst_div}</strong> mencatat rata-rata late rate tertinggi sebesar
      <strong>{worst_div_rate:.1%}</strong> — memerlukan perhatian manajerial segera.
    </div>
  </div>
  <div class="insight-box">
    <div class="i-title">📊 Distribusi Risiko</div>
    <div class="i-body">
      <strong>{high_risk_count}</strong> karyawan High Risk,
      <strong>{med_risk_count}</strong> Medium Risk,
      <strong>{low_risk_count}</strong> Low Risk.
      {"Perlu intervensi segera untuk karyawan berisiko tinggi." if high_risk_count > 0
       else "Tidak ada karyawan dalam kategori risiko tinggi saat ini."}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# =========================
# Global Helpers
# =========================
def hex_to_rgba(hex_color, alpha=0.33):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

# =========================
# Main Tabs
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "  Ranking Karyawan  ",
    "  Tren & Forecast Divisi  ",
    "  Heatmap Hari  ",
    "  Forecast Per Karyawan  ",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — Ranking Karyawan Berisiko
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="sec-head"><div class="bar"></div><h3>Ranking Karyawan Berisiko</h3><span class="badge">Sorted by Risk Score</span></div>', unsafe_allow_html=True)

    # Sort descending by risk_score, reset index for proper rank numbering
    top_emp = emp_f.sort_values("risk_score", ascending=False).head(top_n).reset_index(drop=True)

    # ── Horizontal bar chart — Risk Score per karyawan ──
    # Sort ascending → rank #1 muncul di atas (Plotly bar horizontal render dari bawah ke atas)
    top_emp_chart = top_emp.sort_values("risk_score", ascending=True).copy()
    color_map_tier = {"High": "#F75B5B", "Medium": "#F7A24F", "Low": "#6B7A99", "Unknown": "#6B7A99"}
    bar_colors_chart = [color_map_tier.get(t, "#6B7A99") for t in top_emp_chart["risk_tier"]]

    # Satu bar = risk_score, hover tampilkan late rate detail
    hover_texts = []
    for _, r in top_emp_chart.iterrows():
        lr_o = f"{r.get('late_rate_overall', 0):.1%}" if pd.notna(r.get('late_rate_overall')) else "-"
        lr_r = f"{r.get('late_rate_recent3', 0):.1%}" if pd.notna(r.get('late_rate_recent3')) else "-"
        hover_texts.append(
            f"<b>{r['employee_name']}</b><br>"
            f"Risk Score: {r.get('risk_score',0):.3f}<br>"
            f"Late Rate Overall: {lr_o}<br>"
            f"Late Rate 3 Bln: {lr_r}<br>"
            f"Divisi: {r['division']}"
        )

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        y=top_emp_chart["employee_name"],
        x=top_emp_chart["risk_score"],
        orientation="h",
        marker_color=bar_colors_chart,
        marker_line_width=0,
        text=[f"{v:.3f}" for v in top_emp_chart["risk_score"]],
        textposition="outside",
        textfont=dict(size=10, color="white"),
        hovertext=hover_texts,
        hoverinfo="text",
        showlegend=False,
    ))

    # Legend manual
    for tier, clr in [("High Risk","#F75B5B"),("Medium Risk","#F7A24F"),("Low Risk","#6B7A99")]:
        fig_bar.add_trace(go.Bar(
            x=[None], y=[None], orientation="h",
            name=tier, marker_color=clr, showlegend=True,
        ))

    fig_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(22,29,46,0)",
        plot_bgcolor ="rgba(22,29,46,0)",
        height=max(400, top_n * 28),
        margin=dict(l=10, r=80, t=20, b=10),
        xaxis=dict(title="Risk Score (0–1)", gridcolor="rgba(42,51,71,0.4)", zeroline=False,
                   tickformat=".2f"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10)),
        legend=dict(orientation="h", y=1.05, x=0, bgcolor="rgba(0,0,0,0)", font_size=11),
        font=dict(family="DM Sans"),
        barmode="group",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ── Penjelasan Risk Score ──
    st.markdown("""
    <div style="background:#161D2E;border:1px solid #2A3347;border-radius:12px;padding:1rem 1.2rem;margin-bottom:1rem;font-size:0.82rem;color:#6B7A99;line-height:1.7">
      <b style="color:#C5CEDE">📐 Formula Risk Score:</b><br>
      <code style="color:#4F8EF7">Risk Score = (Late Rate 3 Bln × 55%) + (Near-Late Rate × 30%) + (Trend Naik × 15%)</code><br>
      Semakin tinggi skor → semakin sering terlambat belakangan ini & tren memburuk.
      <span style="color:#F75B5B">■ Tinggi ≥ threshold</span> &nbsp;
      <span style="color:#F7A24F">■ Sedang</span> &nbsp;
      <span style="color:#6B7A99">■ Rendah</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Detail Table ──
    st.markdown('<div class="sec-head"><div class="bar" style="background:#A78BFA"></div><h3>Detail Tabel</h3><span class="badge">Top ' + str(top_n) + '</span></div>', unsafe_allow_html=True)

    show_cols = ["employee_name", "division"]
    if "department_clean" in top_emp.columns: show_cols.append("department_clean")
    if "late_rate_overall"  in top_emp.columns: show_cols.append("late_rate_overall")
    if "late_rate_recent3"  in top_emp.columns: show_cols.append("late_rate_recent3")
    if "trend_late"         in top_emp.columns: show_cols.append("trend_late")
    show_cols += ["risk_score", "risk_tier"]

    col_labels = {
        "employee_name":    "Nama",
        "division":         "Divisi",
        "department_clean": "Departemen",
        "late_rate_overall":"Late Rate (Overall)",
        "late_rate_recent3":"Late Rate (3 Bln)",
        "trend_late":       "Trend",
        "risk_score":       "Risk Score",
        "risk_tier":        "Tier",
    }

    rows_html = ""
    for rank, (_, r) in enumerate(top_emp[show_cols].iterrows(), 1):
        tier = r.get("risk_tier", "Unknown")
        pill_cls = {"High":"risk-high","Medium":"risk-medium","Low":"risk-low"}.get(tier,"")
        tier_id  = {"High":"Tinggi","Medium":"Sedang","Low":"Rendah"}.get(tier, tier)

        trend_val = r.get("trend_late", np.nan)
        trend_disp = (
            f'<span style="color:#F75B5B">↑ Naik</span>'  if pd.notna(trend_val) and trend_val > 0.001 else
            f'<span style="color:#4FC98E">↓ Turun</span>' if pd.notna(trend_val) and trend_val < -0.001 else
            f'<span style="color:#6B7A99">→ Stabil</span>'
        )

        dept_cell = f"<td>{r.get('department_clean','-')}</td>" if "department_clean" in show_cols else ""

        rows_html += f"""
        <tr>
          <td style="color:#6B7A99;font-size:0.7rem">#{rank}</td>
          <td><b style="color:#E5EAF5">{r['employee_name']}</b></td>
          <td>{r['division']}</td>
          {dept_cell}
          <td>{r.get('late_rate_overall', 0):.1%}</td>
          <td><b>{r.get('late_rate_recent3', 0):.1%}</b></td>
          <td>{trend_disp}</td>
          <td><b>{r.get('risk_score', 0):.3f}</b></td>
          <td><span class="risk-pill {pill_cls}">{tier_id}</span></td>
        </tr>"""

    dept_th = "<th>Departemen</th>" if "department_clean" in show_cols else ""
    st.markdown(f"""
    <table class="risk-table">
      <thead>
        <tr>
          <th>#</th><th>Nama</th><th>Divisi</th>{dept_th}
          <th>Late Rate (Overall)</th><th>Late Rate (3 Bln)</th>
          <th>Tren</th><th>Risk Score</th><th>Tier</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    """, unsafe_allow_html=True)



# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — Tren Historis & Forecast Per Divisi
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="sec-head"><div class="bar" style="background:#4FC98E"></div><h3>Tren & Forecast Late Rate per Divisi</h3><span class="badge">Prophet Model</span></div>', unsafe_allow_html=True)

    divisions_plot = sorted(ts_f["division"].unique().tolist())
    if not divisions_plot:
        st.info("Tidak ada data divisi untuk filter yang dipilih.")
    else:
        # Color palette per division
        palette = ["#4F8EF7","#4FC98E","#F7A24F","#F75B5B","#A78BFA",
                   "#38BDF8","#FB923C","#34D399","#F472B6","#FACC15"]
        div_colors = {d: palette[i % len(palette)] for i, d in enumerate(divisions_plot)}

        fig_div = go.Figure()

        for div in divisions_plot:
            clr  = div_colors[div]
            ts_d = ts_f[ts_f["division"] == div].sort_values("month")
            fc_d = fc_f[fc_f["division"] == div].sort_values("month")

            # Historical
            fig_div.add_trace(go.Scatter(
                x=ts_d["month"], y=ts_d["late_rate"],
                mode="lines+markers",
                name=f"{div} (Historis)",
                line=dict(color=clr, width=2),
                marker=dict(size=5),
                legendgroup=div,
                hovertemplate=f"<b>{div}</b><br>%{{x|%b %Y}}<br>Late Rate: %{{y:.1%}}<extra></extra>",
            ))

            # Forecast with confidence band
            if len(fc_d):
                # Band
                if "yhat_lower" in fc_d.columns and "yhat_upper" in fc_d.columns:
                    fig_div.add_trace(go.Scatter(
                        x=pd.concat([fc_d["month"], fc_d["month"][::-1]]),
                        y=pd.concat([fc_d["yhat_upper"], fc_d["yhat_lower"][::-1]]),
                        fill="toself",
                        fillcolor=hex_to_rgba(clr, 0.13),
                        line=dict(color="rgba(0,0,0,0)"),
                        name=f"{div} (CI)",
                        legendgroup=div,
                        showlegend=False,
                        hoverinfo="skip",
                    ))
                # Bridge last historical → first forecast
                if len(ts_d):
                    bridge_x = [ts_d["month"].iloc[-1], fc_d["month"].iloc[0]]
                    bridge_y = [ts_d["late_rate"].iloc[-1], fc_d["yhat"].iloc[0]]
                    fig_div.add_trace(go.Scatter(
                        x=bridge_x, y=bridge_y,
                        mode="lines",
                        line=dict(color=clr, width=2, dash="dot"),
                        legendgroup=div, showlegend=False, hoverinfo="skip",
                    ))
                # Forecast line
                fig_div.add_trace(go.Scatter(
                    x=fc_d["month"], y=fc_d["yhat"],
                    mode="lines+markers",
                    name=f"{div} (Forecast)",
                    line=dict(color=clr, width=2.5, dash="dash"),
                    marker=dict(size=7, symbol="diamond"),
                    legendgroup=div,
                    hovertemplate=f"<b>{div} Forecast</b><br>%{{x|%b %Y}}<br>Prakiraan: %{{y:.1%}}<extra></extra>",
                ))

        # Forecast zone shading
        if len(fc_f):
            fig_div.add_vrect(
                x0=fc_f["month"].min(), x1=fc_f["month"].max(),
                fillcolor="rgba(79,142,247,0.04)", line_width=0,
                annotation_text="Forecast Zone", annotation_position="top left",
                annotation_font_color="#6B7A99", annotation_font_size=10,
            )

        fig_div.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(22,29,46,0)",
            plot_bgcolor ="rgba(22,29,46,0)",
            height=480,
            margin=dict(l=10, r=10, t=30, b=10),
            yaxis=dict(title="Late Rate", tickformat=".0%",
                       gridcolor="rgba(42,51,71,0.4)", zeroline=False),
            xaxis=dict(title="Bulan", gridcolor="rgba(42,51,71,0.3)", zeroline=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0,
                        bgcolor="rgba(0,0,0,0)", font_size=11),
            hovermode="x unified",
            font=dict(family="DM Sans"),
        )
        st.plotly_chart(fig_div, use_container_width=True)

        # ── Model metrics table ──
        if len(met_div):
            st.markdown('<div class="sec-head"><div class="bar" style="background:#A78BFA"></div><h3>Model Metrics per Divisi</h3><span class="badge">Evaluasi Akurasi</span></div>', unsafe_allow_html=True)
            met_show = met_div[met_div["division"].isin(sel_divisions)].copy() if "division" in met_div.columns else met_div.copy()

            # Format manual tanpa style (hindari matplotlib dependency)
            met_display = met_show.copy()
            for c in ["mae","rmse"]:
                if c in met_display.columns:
                    met_display[c] = met_display[c].apply(lambda x: f"{x:.4f}" if pd.notna(x) else "-")
            for c in ["mape","smape"]:
                if c in met_display.columns:
                    met_display[c] = met_display[c].apply(lambda x: f"{x:.1%}" if pd.notna(x) else "-")
            met_display = met_display.rename(columns={
                "division":"Divisi","mae":"MAE","rmse":"RMSE",
                "mape":"MAPE","smape":"SMAPE","n_train":"N Train","n_test":"N Test"
            })
            st.dataframe(met_display, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — Heatmap Per Hari dalam Seminggu
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="sec-head"><div class="bar" style="background:#F7A24F"></div><h3>Heatmap Late Rate per Hari & Divisi</h3><span class="badge">Warna = Late Rate</span></div>', unsafe_allow_html=True)

    # Gunakan emp_mon untuk heatmap hari dalam seminggu
    # emp_mon punya kolom: employee_id, month, late_rate, ewma, dll
    # Kita derive day-of-week dari emp_mon jika ada kolom day_of_week
    # Fallback: gunakan ts_div per bulan → pivot per divisi x bulan

    if "day_of_week" in emp_mon.columns and "late_rate" in emp_mon.columns:
        # Heatmap: divisi x day_of_week
        emp_mon_f = emp_mon[emp_mon["employee_id"].isin(emp_f["employee_id"])].copy()
        pivot_dow = emp_mon_f.pivot_table(
            values="late_rate",
            index="employee_id",
            columns="day_of_week",
            aggfunc="mean"
        )
        # Map ke nama hari
        day_map = {0:"Sen",1:"Sel",2:"Rab",3:"Kam",4:"Jum",5:"Sab",6:"Min"}
        pivot_dow.columns = [day_map.get(c, str(c)) for c in pivot_dow.columns]
        # Join nama karyawan
        pivot_dow = pivot_dow.join(
            emp_f.set_index("employee_id")[["employee_name"]]
        ).set_index("employee_name")

        fig_hw = px.imshow(
            pivot_dow.fillna(0).head(30),
            color_continuous_scale=[[0,"#0D1117"],[0.25,"#1C3A6B"],[0.5,"#F7A24F"],[1,"#F75B5B"]],
            aspect="auto",
            labels={"color":"Late Rate"},
        )
        fig_hw.update_coloraxes(colorbar_tickformat=".0%")
        fig_hw.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(22,29,46,0)",
            plot_bgcolor ="rgba(22,29,46,0)",
            height=max(400, min(30,len(pivot_dow)) * 22 + 80),
            margin=dict(l=10, r=10, t=20, b=10),
            font=dict(family="DM Sans"),
            xaxis=dict(title="Hari", side="top"),
            yaxis=dict(title=""),
        )
        st.plotly_chart(fig_hw, use_container_width=True)

    else:
        # Fallback: Heatmap divisi x bulan
        st.caption("ℹ️ Kolom day_of_week tidak tersedia di employee_risk_monthly.csv — menampilkan heatmap per bulan.")
        pivot_month = ts_f.pivot_table(
            values="late_rate", index="division", columns="month", aggfunc="mean"
        )
        pivot_month.columns = [str(c)[:7] for c in pivot_month.columns]

        fig_hm = px.imshow(
            pivot_month.fillna(0),
            color_continuous_scale=[[0,"#0D1117"],[0.25,"#1C3A6B"],[0.5,"#F7A24F"],[1,"#F75B5B"]],
            aspect="auto",
            labels={"color":"Late Rate"},
        )
        fig_hm.update_coloraxes(colorbar_tickformat=".0%")
        fig_hm.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(22,29,46,0)",
            plot_bgcolor ="rgba(22,29,46,0)",
            height=max(300, len(pivot_month) * 50 + 80),
            margin=dict(l=10, r=10, t=20, b=10),
            font=dict(family="DM Sans"),
            xaxis=dict(title="Bulan", tickangle=-45, side="top"),
            yaxis=dict(title=""),
        )
        st.plotly_chart(fig_hm, use_container_width=True)

    # ── Heatmap late rate per divisi x bulan (selalu tampil) ──
    st.markdown('<div class="sec-head"><div class="bar" style="background:#4FC98E"></div><h3>Tren Bulanan Late Rate per Divisi</h3><span class="badge">Time Series Heatmap</span></div>', unsafe_allow_html=True)

    pivot_div_month = ts_f.pivot_table(
        values="late_rate", index="division", columns="month", aggfunc="mean"
    )
    pivot_div_month.columns = pd.to_datetime(pivot_div_month.columns).strftime("%b %Y")

    fig_dm = px.imshow(
        pivot_div_month.fillna(0),
        color_continuous_scale=[[0,"#0F2B1E"],[0.3,"#1C5E3A"],[0.6,"#F7A24F"],[1,"#F75B5B"]],
        text_auto=".0%",
        aspect="auto",
        labels={"color":"Late Rate"},
    )
    fig_dm.update_coloraxes(colorbar_tickformat=".0%")
    fig_dm.update_traces(textfont_size=10)
    fig_dm.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(22,29,46,0)",
        plot_bgcolor ="rgba(22,29,46,0)",
        height=max(200, len(pivot_div_month) * 55 + 80),
        margin=dict(l=10, r=10, t=20, b=10),
        font=dict(family="DM Sans"),
        xaxis=dict(title="", tickangle=-30, side="top"),
        yaxis=dict(title=""),
    )
    st.plotly_chart(fig_dm, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — Forecast Probabilitas Per Karyawan
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="sec-head"><div class="bar" style="background:#A78BFA"></div><h3>Forecast Probabilitas Per Karyawan</h3><span class="badge">EWMA Trend</span></div>', unsafe_allow_html=True)

    # Pilih karyawan
    emp_options = emp_f.sort_values("risk_score", ascending=False)[["employee_id","employee_name","division","risk_score"]].copy()
    emp_options["label"] = emp_options.apply(
        lambda r: f"{r['employee_name']} ({r['division']}) — Score: {r['risk_score']:.3f}", axis=1
    )

    selected_label = st.selectbox(
        "Pilih Karyawan",
        options=emp_options["label"].tolist(),
        index=0,
    )
    sel_row  = emp_options[emp_options["label"] == selected_label].iloc[0]
    sel_id   = sel_row["employee_id"]
    sel_name = sel_row["employee_name"]

    # Data historis per karyawan
    emp_hist = emp_mon[emp_mon["employee_id"] == sel_id].sort_values("month").copy()

    if emp_hist.empty:
        st.warning(f"Tidak ada data historis untuk {sel_name}.")
    else:
        # ── Summary card karyawan ──
        emp_detail = emp_f[emp_f["employee_id"] == sel_id].iloc[0]
        tier_id    = {"High":"Tinggi","Medium":"Sedang","Low":"Rendah"}.get(emp_detail["risk_tier"], emp_detail["risk_tier"])
        pill_cls   = {"High":"risk-high","Medium":"risk-medium","Low":"risk-low"}.get(emp_detail["risk_tier"],"")

        st.markdown(f"""
        <div style="background:var(--surface);border:1px solid var(--border);border-radius:16px;
                    padding:1.2rem 1.6rem;margin-bottom:1.5rem;display:flex;gap:2rem;flex-wrap:wrap;">
          <div>
            <div class="kpi-label">Nama</div>
            <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:1.2rem;color:#FFF">{sel_name}</div>
          </div>
          <div>
            <div class="kpi-label">Divisi</div>
            <div style="color:#C5CEDE;font-size:0.9rem">{emp_detail['division']}</div>
          </div>
          <div>
            <div class="kpi-label">Risk Score</div>
            <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:1.2rem;color:#FFF">{emp_detail['risk_score']:.3f}</div>
          </div>
          <div>
            <div class="kpi-label">Late Rate Overall</div>
            <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:1.2rem;color:#FFF">{emp_detail.get('late_rate_overall',0):.1%}</div>
          </div>
          <div>
            <div class="kpi-label">Late Rate 3 Bln</div>
            <div style="font-family:'Sora',sans-serif;font-weight:700;font-size:1.2rem;color:#FFF">{emp_detail.get('late_rate_recent3',0):.1%}</div>
          </div>
          <div>
            <div class="kpi-label">Risk Tier</div>
            <div><span class="risk-pill {pill_cls}">{tier_id}</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Time series chart ──
        fig_emp = go.Figure()

        # Confidence band dari EWMA std (simulated ±1 std)
        if "ewma" in emp_hist.columns:
            std_val = float(emp_hist["late_rate"].std()) if "late_rate" in emp_hist.columns else 0.05
            std_val = max(std_val, 0.02)
            fig_emp.add_trace(go.Scatter(
                x=pd.concat([emp_hist["month"], emp_hist["month"][::-1]]),
                y=pd.concat([
                    (emp_hist["ewma"] + std_val).clip(0,1),
                    (emp_hist["ewma"] - std_val).clip(0,1)[::-1]
                ]),
                fill="toself",
                fillcolor="rgba(167,139,250,0.12)",
                line=dict(color="rgba(0,0,0,0)"),
                name="Rentang EWMA ±1σ",
                hoverinfo="skip",
            ))

        # Actual late rate
        if "late_rate" in emp_hist.columns:
            fig_emp.add_trace(go.Scatter(
                x=emp_hist["month"], y=emp_hist["late_rate"],
                mode="lines+markers",
                name="Late Rate Aktual",
                line=dict(color="#4F8EF7", width=2.5),
                marker=dict(size=7, color="#4F8EF7"),
                hovertemplate="%{x|%b %Y}<br>Late Rate: <b>%{y:.1%}</b><extra></extra>",
            ))

        # EWMA smoothed
        if "ewma" in emp_hist.columns:
            fig_emp.add_trace(go.Scatter(
                x=emp_hist["month"], y=emp_hist["ewma"],
                mode="lines",
                name="EWMA (Smoothed Trend)",
                line=dict(color="#A78BFA", width=2, dash="dot"),
                hovertemplate="%{x|%b %Y}<br>EWMA: <b>%{y:.1%}</b><extra></extra>",
            ))

        # Simple linear forecast 3 bulan ke depan dari EWMA
        if "ewma" in emp_hist.columns and len(emp_hist) >= 3:
            xs   = np.arange(len(emp_hist))
            m, b = np.polyfit(xs, emp_hist["ewma"].ffill().values, 1)
            last_month = emp_hist["month"].max()
            future_months = [last_month + pd.DateOffset(months=i) for i in range(1, 4)]
            future_y = [float(np.clip(m*(len(emp_hist)+i-1)+b, 0, 1)) for i in range(1, 4)]

            # Bridge
            bridge_x = [emp_hist["month"].iloc[-1]] + future_months
            bridge_y = [float(emp_hist["ewma"].iloc[-1])] + future_y

            fig_emp.add_trace(go.Scatter(
                x=bridge_x, y=bridge_y,
                mode="lines+markers",
                name="Forecast 3 Bulan",
                line=dict(color="#F7A24F", width=2.5, dash="dash"),
                marker=dict(size=9, symbol="diamond",
                            color=["#F7A24F" if v < risk_threshold_high else "#F75B5B" for v in bridge_y]),
                hovertemplate="%{x|%b %Y}<br>Forecast: <b>%{y:.1%}</b><extra></extra>",
            ))

            fig_emp.add_vrect(
                x0=future_months[0], x1=future_months[-1],
                fillcolor="rgba(247,162,79,0.06)", line_width=0,
                annotation_text="Forecast Zone",
                annotation_font_color="#6B7A99", annotation_font_size=10,
            )

        # Threshold line
        fig_emp.add_hline(
            y=risk_threshold_high, line_dash="dash", line_color="#F75B5B",
            annotation_text=f"High Risk ({risk_threshold_high:.0%})",
            annotation_font_color="#F75B5B", annotation_font_size=11,
        )
        fig_emp.add_hline(
            y=risk_threshold_medium, line_dash="dot", line_color="#F7A24F",
            annotation_text=f"Med Risk ({risk_threshold_medium:.0%})",
            annotation_font_color="#F7A24F", annotation_font_size=11,
        )

        fig_emp.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(22,29,46,0)",
            plot_bgcolor ="rgba(22,29,46,0)",
            height=420,
            margin=dict(l=10, r=10, t=20, b=10),
            yaxis=dict(title="Late Rate / Probabilitas", tickformat=".0%",
                       gridcolor="rgba(42,51,71,0.4)", zeroline=False, range=[-0.02, 1.05]),
            xaxis=dict(title="Bulan", gridcolor="rgba(42,51,71,0.3)", zeroline=False),
            legend=dict(orientation="h", y=1.05, x=0, bgcolor="rgba(0,0,0,0)", font_size=11),
            hovermode="x unified",
            font=dict(family="DM Sans"),
        )
        st.plotly_chart(fig_emp, use_container_width=True)

        # ── Monthly detail table ──
        st.markdown('<div class="sec-head"><div class="bar" style="background:#4F8EF7"></div><h3>Riwayat Bulanan</h3><span class="badge">Detail Data</span></div>', unsafe_allow_html=True)

        display_cols = ["month"] + [c for c in ["late_rate","ewma"] if c in emp_hist.columns]
        fmt_emp = {}
        for c in ["late_rate","ewma"]: fmt_emp[c] = "{:.1%}"
        fmt_emp["month"] = lambda x: x.strftime("%b %Y") if pd.notna(x) else "-"

        # Format manual tanpa style
        emp_display = emp_hist[display_cols].sort_values("month", ascending=False).copy()
        if "month" in emp_display.columns:
            emp_display["month"] = emp_display["month"].apply(
                lambda x: x.strftime("%b %Y") if pd.notna(x) else "-"
            )
        for c in ["late_rate","ewma"]:
            if c in emp_display.columns:
                emp_display[c] = emp_display[c].apply(lambda x: f"{x:.1%}" if pd.notna(x) else "-")
        emp_display = emp_display.rename(columns={
            "month":"Bulan","late_rate":"Late Rate","ewma":"EWMA (Trend)"
        })
        st.dataframe(emp_display, use_container_width=True, hide_index=True)



# =========================
# Footer
# =========================
st.markdown('<hr class="h-line">', unsafe_allow_html=True)
st.caption(
    f"Dashboard v2.0 · {total_emp} karyawan · "
    f"{len(sel_divisions)} divisi aktif · "
    f"Threshold: High ≥{risk_threshold_high:.0%} / Medium ≥{risk_threshold_medium:.0%}"
)