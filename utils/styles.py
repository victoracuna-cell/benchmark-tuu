GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Inter', -apple-system, sans-serif !important; }

[data-testid="stAppViewContainer"] { background: #fafafa !important; }
[data-testid="stHeader"] { background: transparent !important; border-bottom: none !important; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1100px; }
[data-testid="stMainBlockContainer"] { background: #fafafa; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #ebebeb !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 1.75rem 0 1.5rem !important; }
[data-testid="stSidebarNav"] { display: none !important; }

/* ── Page header ── */
.page-header { margin-bottom: 1.75rem; display: flex; justify-content: space-between; align-items: flex-start; }
.page-title {
    font-size: 1.75rem;
    font-weight: 700;
    color: #0a0a0a;
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin-bottom: 0.35rem;
}
.page-title span { color: #0128c9; }
.page-sub { font-size: 0.7rem; color: #888; letter-spacing: 0.01em; display: flex; align-items: center; gap: 6px; }
.dot-cyan {
    display: inline-block; width: 7px; height: 7px; border-radius: 50%;
    background: #affffd; border: 1.5px solid #0128c9; flex-shrink: 0;
}
.page-date { font-size: 0.7rem; color: #888; text-align: right; line-height: 1.8; }

/* ── Metric cards (st.metric override) ── */
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1px solid #ebebeb !important;
    border-radius: 14px !important;
    padding: 1.1rem 1.25rem !important;
    box-shadow: none !important;
}
[data-testid="stMetricLabel"] > div {
    font-size: 0.62rem !important;
    color: #888 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
    font-weight: 500 !important;
}
[data-testid="stMetricValue"] > div {
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: #0a0a0a !important;
    letter-spacing: -0.04em !important;
}
[data-testid="stMetricDelta"] { font-size: 0.65rem !important; color: #666 !important; }

/* Metric hero — wrap in div.metric-hero para activar */
.metric-hero [data-testid="metric-container"] {
    background: #0128c9 !important;
    border-color: #0128c9 !important;
}
.metric-hero [data-testid="stMetricLabel"] > div { color: rgba(175,255,253,0.7) !important; }
.metric-hero [data-testid="stMetricValue"] > div { color: #affffd !important; }
.metric-hero [data-testid="stMetricDelta"] { color: rgba(175,255,253,0.55) !important; }

/* ── Cards ── */
.card {
    background: #ffffff;
    border: 1px solid #ebebeb;
    border-radius: 14px;
    padding: 1.375rem 1.5rem;
    margin-bottom: 0.75rem;
}
.card-label {
    font-size: 0.62rem;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 500;
    margin-bottom: 1rem;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #ebebeb !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    padding: 0.6rem 1.1rem !important;
    font-size: 0.78rem !important;
    color: #888 !important;
    font-weight: 400 !important;
    margin-bottom: -1px !important;
}
.stTabs [aria-selected="true"] {
    color: #0128c9 !important;
    border-bottom-color: #0128c9 !important;
    font-weight: 600 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 1.25rem 0 0 !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid #ebebeb !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    background: #ffffff !important;
}
[data-testid="stDataFrame"] th {
    background: #fafafa !important;
    color: #888 !important;
    font-size: 0.65rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    font-weight: 500 !important;
    border-bottom: 1px solid #ebebeb !important;
}
[data-testid="stDataFrame"] td { font-size: 0.78rem !important; color: #333 !important; }

/* ── Buttons ── */
.stButton > button {
    background: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    color: #333 !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1rem !important;
    box-shadow: none !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    border-color: #0128c9 !important;
    color: #0128c9 !important;
    background: #f5f7ff !important;
}
.stButton > button[kind="primary"] {
    background: #0128c9 !important;
    border-color: #0128c9 !important;
    color: #ffffff !important;
}
.stButton > button[kind="primary"]:hover {
    background: #0135e8 !important;
}

/* ── Inputs / selects ── */
[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
}
[data-baseweb="input"] > div {
    background: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
}
[data-testid="stMultiSelect"] [data-baseweb="tag"] {
    background: rgba(1,40,201,0.08) !important;
    color: #0128c9 !important;
    border-radius: 6px !important;
    font-size: 0.72rem !important;
}
textarea {
    background: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    font-family: 'Inter', monospace !important;
    color: #333 !important;
}

/* ── Sidebar nav items ── */
.sb-logo-row { display: flex; align-items: center; gap: 8px; padding: 0 1.25rem 1.5rem; }
.sb-dot { width: 8px; height: 8px; border-radius: 50%; background: #0128c9; flex-shrink: 0; }
.sb-brand { font-size: 0.82rem; font-weight: 600; color: #0128c9; letter-spacing: -0.01em; }
.sb-caption { font-size: 0.65rem; color: #888; padding: 0 1.25rem; margin-bottom: 1.25rem; }
.sb-section { font-size: 0.6rem; color: #bbb; text-transform: uppercase; letter-spacing: 0.1em; padding: 0 1.25rem; margin: 1rem 0 0.35rem; }
.sb-divider { height: 1px; background: #f0f0f0; margin: 0.75rem 1rem; }
.sb-footer { font-size: 0.62rem; color: #999; line-height: 1.9; padding: 0 1.25rem; border-top: 1px solid #f0f0f0; padding-top: 1rem; margin-top: 1rem; }

[data-testid="stSidebarNav"] a, .stPageLink a {
    font-size: 0.78rem !important;
    color: #555 !important;
    border-radius: 8px !important;
    padding: 0.5rem 0.75rem !important;
    font-weight: 400 !important;
}
[data-testid="stSidebarNav"] a:hover { color: #0128c9 !important; background: #f5f7ff !important; }
[data-testid="stSidebarNav"] [aria-current="page"] a {
    color: #0128c9 !important;
    background: #f5f7ff !important;
    font-weight: 500 !important;
}

/* ── Status / alerts ── */
[data-testid="stAlert"] {
    background: #ffffff !important;
    border: 1px solid #ebebeb !important;
    border-radius: 10px !important;
    font-size: 0.78rem !important;
    color: #333 !important;
}
[data-testid="stInfo"] { border-left: 3px solid #0128c9 !important; }
[data-testid="stSuccess"] { border-left: 3px solid #affffd !important; border-top-color: #0128c9 !important; }

/* ── Progress ── */
[data-testid="stProgress"] > div > div {
    background: #0128c9 !important;
    border-radius: 99px !important;
}
[data-testid="stProgress"] > div {
    background: #f0f0f0 !important;
    border-radius: 99px !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #ebebeb !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}
[data-testid="stExpander"] summary {
    font-size: 0.78rem !important;
    color: #333 !important;
    font-weight: 500 !important;
}

/* ── Divider ── */
hr { border: none !important; border-top: 1px solid #ebebeb !important; margin: 1rem 0 !important; }

/* ── Caption ── */
[data-testid="stCaptionContainer"] { color: #999 !important; font-size: 0.68rem !important; }

/* ── Slider ── */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] { background: #0128c9 !important; }
[data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stSliderTrackFill"] { background: #0128c9 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #e0e0e0; border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: #0128c9; }

/* ── Number input ── */
[data-testid="stNumberInput"] input {
    background: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    font-size: 0.78rem !important;
    color: #333 !important;
}

/* ── Form ── */
[data-testid="stForm"] {
    background: #ffffff;
    border: 1px solid #ebebeb;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
}
</style>
"""
