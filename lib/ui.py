# lib/ui.py
import streamlit as st

def apply_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;800&display=swap');

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {
            background: #0D1117 !important;
            border-right: 1px solid #1E2A3A;
        }
        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 0 !important;
        }
        .sb-brand {
            font-family: 'Sora', sans-serif;
            font-size: 0.95rem;
            font-weight: 800;
            color: #4F8EF7;
            letter-spacing: -0.01em;
            padding: 1rem 0 1rem 0;
            border-bottom: 1px solid #1E2A3A;
            margin-bottom: 0;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
            padding-top: 0 !important;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"]::before {
            content: "MENU";
            display: block;
            font-size: 0.6rem;
            font-weight: 700;
            letter-spacing: 0.18em;
            color: #3A4A66;
            padding: 0.8rem 1.2rem 0.4rem;
        }
        section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"] {
            border-radius: 8px;
            margin: 2px 8px;
            padding: 0.5rem 0.75rem;
            font-size: 0.82rem;
            font-weight: 500;
            color: #6B7A99 !important;
            transition: all 0.15s;
        }
        section[data-testid="stSidebar"] a[data-testid="stSidebarNavLink"]:hover {
            background: #1C2333 !important;
            color: #C5CEDE !important;
        }
        section[data-testid="stSidebar"] a[aria-current="page"] {
            background: rgba(79,142,247,0.1) !important;
            color: #4F8EF7 !important;
            font-weight: 600 !important;
        }

        /* ── General ── */
        :root {
            --bg: var(--background-color);
            --card: var(--secondary-background-color);
            --text: var(--text-color);
            --muted: rgba(127,127,127,0.9);
            --border: rgba(127,127,127,0.25);
            --primary: var(--primary-color);
        }

        .block-container { padding-top: 1.1rem; padding-bottom: 2rem; }
        h1,h2,h3 { letter-spacing: -0.02em; }
        .subtle { color: var(--muted); font-size: 0.95rem; }

        .card {
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 16px 16px 10px 16px;
            background: var(--card);
        }
        .pill {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            border: 1px solid var(--border);
            font-size: 0.82rem;
            color: var(--muted);
            margin-right: 6px;
        }

        div[data-testid="metric-container"] {
            border: 1px solid var(--border);
            padding: 14px 14px 10px 14px;
            border-radius: 16px;
            background: var(--card);
        }

        .stDownloadButton button, .stButton button {
            border-radius: 12px;
            padding: 0.6rem 0.9rem;
        }

        #MainMenu, footer { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True
    )

def section_header(title: str, subtitle: str | None = None):
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f'<div class="subtle">{subtitle}</div>', unsafe_allow_html=True)