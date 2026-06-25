GLOBAL_CSS = """
<style>
/* ── Reset & base ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #dde4f0 0%, #e8edf4 50%, #d8e2f0 100%);
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.45) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.6) !important;
    box-shadow: 4px 0 24px rgba(30,58,95,0.06);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
.block-container {
    padding: 1.5rem 2rem 3rem 2rem !important;
    max-width: 1200px;
}

/* ── Glass card ── */
.glass-card {
    background: rgba(255,255,255,0.72);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.85);
    border-radius: 18px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 24px rgba(30,58,95,0.07), 0 1px 4px rgba(30,58,95,0.04);
}
.glass-card-sm {
    background: rgba(255,255,255,0.72);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.85);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    box-shadow: 0 2px 12px rgba(30,58,95,0.06);
}

/* ── KPI tiles ── */
.kpi-tile {
    background: rgba(255,255,255,0.75);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 16px rgba(30,58,95,0.07);
    text-align: center;
}
.kpi-tile .kpi-value {
    font-size: 2rem;
    font-weight: 600;
    color: #1E3A5F;
    line-height: 1.1;
    letter-spacing: -0.03em;
}
.kpi-tile .kpi-label {
    font-size: 0.72rem;
    color: #6b7a99;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}

/* ── Page title ── */
.page-title {
    font-size: 1.6rem;
    font-weight: 600;
    color: #1E3A5F;
    letter-spacing: -0.02em;
    margin-bottom: 0.25rem;
}
.page-subtitle {
    font-size: 0.82rem;
    color: #8292b0;
    margin-bottom: 1.5rem;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.5);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(255,255,255,0.8);
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    padding: 6px 16px !important;
    font-size: 13px !important;
    color: #6b7a99 !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(255,255,255,0.9) !important;
    color: #1E3A5F !important;
    font-weight: 500 !important;
    box-shadow: 0 1px 6px rgba(30,58,95,0.10) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ── Sidebar nav ── */
[data-testid="stSidebarNav"] { display: none; }
.sidebar-logo {
    font-size: 1rem;
    font-weight: 600;
    color: #1E3A5F;
    margin-bottom: 0.25rem;
}
.sidebar-caption {
    font-size: 0.72rem;
    color: #8292b0;
    margin-bottom: 1.5rem;
}
.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    border-radius: 10px;
    font-size: 13px;
    color: #3d5278;
    cursor: pointer;
    transition: background 0.15s;
    text-decoration: none;
    margin-bottom: 2px;
}
.nav-item:hover { background: rgba(30,58,95,0.07); }
.nav-item.active {
    background: rgba(255,255,255,0.75);
    color: #1E3A5F;
    font-weight: 500;
    box-shadow: 0 1px 6px rgba(30,58,95,0.08);
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.8) !important;
    background: rgba(255,255,255,0.6) !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.72);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 16px;
    padding: 1rem 1.25rem;
    box-shadow: 0 2px 12px rgba(30,58,95,0.06);
}
[data-testid="stMetricValue"] { color: #1E3A5F !important; font-weight: 600 !important; }
[data-testid="stMetricLabel"] { color: #8292b0 !important; font-size: 12px !important; }

/* ── Buttons ── */
.stButton > button {
    background: rgba(255,255,255,0.75) !important;
    border: 1px solid rgba(30,58,95,0.15) !important;
    border-radius: 10px !important;
    color: #1E3A5F !important;
    font-weight: 500 !important;
    box-shadow: 0 1px 4px rgba(30,58,95,0.06) !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: rgba(255,255,255,0.95) !important;
    box-shadow: 0 2px 10px rgba(30,58,95,0.12) !important;
}
.stButton > button[kind="primary"] {
    background: #1E3A5F !important;
    color: white !important;
    border-color: #1E3A5F !important;
}
.stButton > button[kind="primary"]:hover {
    background: #26487a !important;
}

/* ── Selectbox / inputs ── */
[data-baseweb="select"] > div,
[data-baseweb="input"] > div {
    background: rgba(255,255,255,0.7) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(30,58,95,0.12) !important;
}
[data-testid="stMultiSelect"] [data-baseweb="tag"] {
    background: rgba(30,58,95,0.10) !important;
    border-radius: 6px !important;
}

/* ── Divider ── */
hr { border-color: rgba(30,58,95,0.08) !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.55) !important;
    border: 1px solid rgba(255,255,255,0.8) !important;
    border-radius: 12px !important;
}

/* ── Progress bar ── */
[data-testid="stProgress"] > div > div {
    background: #1E3A5F !important;
    border-radius: 99px !important;
}

/* ── Caption / info ── */
[data-testid="stCaptionContainer"] { color: #8292b0 !important; }
.stAlert {
    background: rgba(255,255,255,0.65) !important;
    border: 1px solid rgba(30,58,95,0.10) !important;
    border-radius: 12px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(30,58,95,0.18); border-radius: 99px; }
</style>
"""
