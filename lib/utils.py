import numpy as np
import streamlit as st

def clip01(s):
    return s.clip(lower=0, upper=1)

def fmt_pct(x, decimals=2):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "-"
    return f"{x*100:.{decimals}f}%"

def fmt_num(x, decimals=4):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "-"
    return f"{x:.{decimals}f}"

def download_csv_button(df, filename: str, label: str):
    st.download_button(
        label=label,
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
    )