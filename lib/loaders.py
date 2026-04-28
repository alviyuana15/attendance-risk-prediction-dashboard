from pathlib import Path
import pandas as pd
import streamlit as st
from .utils import clip01

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

@st.cache_data
def load_attendance():
    daily_att = pd.read_csv(DATA_DIR / "daily_full_weekday.csv")
    fc_att = pd.read_csv(DATA_DIR / "attendance_forecast_result.csv")

    daily_att["date"] = pd.to_datetime(daily_att["date"], errors="coerce")
    fc_att["date"] = pd.to_datetime(fc_att["date"], errors="coerce")

    if "attendance_rate" in daily_att.columns:
        daily_att["attendance_rate"] = pd.to_numeric(daily_att["attendance_rate"], errors="coerce").clip(0,1)
    if "prediction" in fc_att.columns:
        fc_att["prediction"] = pd.to_numeric(fc_att["prediction"], errors="coerce").clip(0,1)

    # optional importance
    try:
        att_imp = pd.read_csv(DATA_DIR / "attendance_feature_importance.csv")
    except Exception:
        att_imp = None

    daily_att = daily_att.dropna(subset=["date"]).sort_values("date")
    fc_att = fc_att.dropna(subset=["date"]).sort_values("date")
    return daily_att, fc_att, att_imp

@st.cache_data
def load_late():
    ts_div = pd.read_csv(DATA_DIR / "ts_division_monthly.csv")
    fc_div = pd.read_csv(DATA_DIR / "division_forecast.csv")
    met_div = pd.read_csv(DATA_DIR / "division_model_metrics.csv")
    emp_sum = pd.read_csv(DATA_DIR / "employee_risk_summary.csv")
    emp_mon = pd.read_csv(DATA_DIR / "employee_risk_monthly.csv")

    for d in (ts_div, fc_div, emp_mon):
        d["month"] = pd.to_datetime(d["month"], errors="coerce")

    ts_div["late_rate"] = pd.to_numeric(ts_div.get("late_rate"), errors="coerce")
    ts_div["late_rate"] = clip01(ts_div["late_rate"])

    fc_div["yhat"] = pd.to_numeric(fc_div.get("yhat"), errors="coerce")
    fc_div["yhat"] = clip01(fc_div["yhat"])

    for c in ["yhat_lower","yhat_upper"]:
        if c in fc_div.columns:
            fc_div[c] = pd.to_numeric(fc_div[c], errors="coerce")
            fc_div[c] = clip01(fc_div[c])

    for c in ["mae","rmse","mape","smape"]:
        if c in met_div.columns:
            met_div[c] = pd.to_numeric(met_div[c], errors="coerce")

    # employee clean
    emp_sum["employee_id"] = emp_sum["employee_id"].astype(str).str.strip()
    emp_sum["employee_name"] = emp_sum["employee_name"].astype(str).str.strip()
    emp_sum["division"] = emp_sum["division"].astype(str).str.strip()
    if "department_clean" in emp_sum.columns:
        emp_sum["department_clean"] = emp_sum["department_clean"].astype(str).str.strip()

    for c in ["risk_score","late_rate_recent3","late_rate_overall","trend_late"]:
        if c in emp_sum.columns:
            emp_sum[c] = pd.to_numeric(emp_sum[c], errors="coerce")

    emp_mon["employee_id"] = emp_mon["employee_id"].astype(str).str.strip()
    for c in ["late_rate","ewma"]:
        if c in emp_mon.columns:
            emp_mon[c] = pd.to_numeric(emp_mon[c], errors="coerce")
            emp_mon[c] = clip01(emp_mon[c])

    ts_div = ts_div.dropna(subset=["month","division","late_rate"]).sort_values(["division","month"])
    fc_div = fc_div.dropna(subset=["month","division","yhat"]).sort_values(["division","month"])
    emp_mon = emp_mon.dropna(subset=["month","employee_id"]).sort_values(["employee_id","month"])

    return ts_div, fc_div, met_div, emp_sum, emp_mon