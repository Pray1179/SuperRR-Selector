"""
app.py
------
Interactive Streamlit Dashboard for Rajasthan Royals SupeRR Selector Season 2:
IPL 2027 Auction Analytics — Separate Batter and Bowler Ranking Systems.

Sections:
1. Judge Quick View (Executive Default Landing Page)
2. Top 10 Batters Leaderboard
3. Top 10 Bowlers Leaderboard
4. Individual Player Analysis
5. Pressure vs Baseline Comparison
6. Bootstrap Reliability & Rank Uncertainty
7. Weight Sensitivity Explorer
8. Match Consistency & LOMO Fragility
9. Methodology & Limitations
"""

import os
import inspect
import warnings
warnings.filterwarnings("ignore", message=".*use_container_width.*")
warnings.filterwarnings("ignore", category=DeprecationWarning)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Rajasthan Royals | Pressure Reliability Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cross-version layout parameter resolution (Streamlit >=1.40 prefers width='stretch')
_PLOTLY_WIDTH_KW = {"width": "stretch", "theme": None} if "width" in inspect.signature(st.plotly_chart).parameters else {"use_container_width": True, "theme": None}
_DATAFRAME_WIDTH_KW = {"width": "stretch"} if "width" in inspect.signature(st.dataframe).parameters else {"use_container_width": True}

# Relative Path Discovery — Bulletproof cross-directory search
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_data_file(filename):
    """
    Search for data files across all standard local and relative directory structures:
    package root, app subfolder, parent repo root, and direct evidence/leaderboard folders.
    """
    candidates = [
        # Relative to dashboard directory
        os.path.join(os.path.dirname(__file__), "data", filename),
        os.path.join(os.path.dirname(__file__), filename),
        # Relative to BASE_DIR (final_submission or parent)
        os.path.join(BASE_DIR, "leaderboards", filename),
        os.path.join(BASE_DIR, "evidence", filename),
        os.path.join(BASE_DIR, "results", filename),
        # Relative to current working directory (e.g. repo root)
        os.path.join(os.getcwd(), "final_submission", "leaderboards", filename),
        os.path.join(os.getcwd(), "final_submission", "evidence", filename),
        os.path.join(os.getcwd(), "final_submission", "results", filename),
        os.path.join(os.getcwd(), "submission", "final_submission", "leaderboards", filename),
        os.path.join(os.getcwd(), "submission", "final_submission", "evidence", filename),
        os.path.join(os.getcwd(), "submission", "final_submission", "results", filename),
        os.path.join(os.getcwd(), "leaderboards", filename),
        os.path.join(os.getcwd(), "evidence", filename),
        os.path.join(os.getcwd(), "results", filename),
        os.path.join(os.getcwd(), "RR_IPL_2027_ANALYTICS_LOGS", "results", filename),
        os.path.join(os.path.dirname(__file__), "..", "leaderboards", filename),
        os.path.join(os.path.dirname(__file__), "..", "evidence", filename),
        os.path.join(os.path.dirname(__file__), "..", "results", filename)
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
            
    # Upward recursive search fallback (up to 3 levels)
    curr = os.path.abspath(os.path.dirname(__file__))
    for _ in range(3):
        for sub in ["leaderboards", "evidence", "results", "final_submission"]:
            candidate = os.path.join(curr, sub, filename)
            if os.path.exists(candidate):
                return candidate
            if os.path.isdir(os.path.join(curr, sub)):
                for deep_sub in ["leaderboards", "evidence", "results"]:
                    deep_candidate = os.path.join(curr, sub, deep_sub, filename)
                    if os.path.exists(deep_candidate):
                        return deep_candidate
        curr = os.path.dirname(curr)
        
    raise FileNotFoundError(
        f"Data file '{filename}' could not be located in any standard search directory.\n"
        f"Checked primary paths:\n" + "\n".join(candidates[:6])
    )

# Theme State Resolution: System Mode by default with optional query override (?theme=light or ?theme=dark)
query_theme = st.query_params.get("theme", None)
if query_theme:
    is_dark = (str(query_theme).lower() != "light")
else:
    # Check Streamlit runtime context if available, otherwise default to Dark Mode benchmark
    ctx_theme = getattr(st.context, "theme", None)
    if ctx_theme and isinstance(ctx_theme, dict) and ctx_theme.get("type"):
        is_dark = (ctx_theme.get("type") == "dark")
    else:
        is_dark = True

def apply_theme_to_fig(fig, is_dark_mode: bool = True):
    """
    Complete, rigorous theme adapter for Plotly figures. Ensures all titles,
    tick labels, axis titles, legends, colorbars, and gridlines have accessible
    contrast in both Dark and Light modes.
    """
    if is_dark_mode:
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#F8FAFC", family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"),
            title=dict(font=dict(color="#F8FAFC", size=15)),
            xaxis=dict(
                title_font=dict(color="#CBD5E1", size=13),
                tickfont=dict(color="#CBD5E1", size=11),
                gridcolor="#334155",
                zerolinecolor="#475569",
                linecolor="#334155"
            ),
            yaxis=dict(
                title_font=dict(color="#CBD5E1", size=13),
                tickfont=dict(color="#CBD5E1", size=11),
                gridcolor="#334155",
                zerolinecolor="#475569",
                linecolor="#334155"
            ),
            legend=dict(
                font=dict(color="#CBD5E1", size=11),
                title_font=dict(color="#F8FAFC", size=12)
            ),
            coloraxis_colorbar=dict(
                title_font=dict(color="#CBD5E1", size=12),
                tickfont=dict(color="#CBD5E1", size=10)
            ),
            margin=dict(l=10, r=10, t=35, b=10)
        )
    else:
        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="#F1F5F9",
            plot_bgcolor="#F1F5F9",
            font=dict(color="#14213D", family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif"),
            title=dict(font=dict(color="#14213D", size=15)),
            xaxis=dict(
                title_font=dict(color="#14213D", size=13),
                tickfont=dict(color="#52627A", size=11),
                gridcolor="#D7DFEA",
                zerolinecolor="#CBD5E1",
                linecolor="#D7DFEA"
            ),
            yaxis=dict(
                title_font=dict(color="#14213D", size=13),
                tickfont=dict(color="#52627A", size=11),
                gridcolor="#D7DFEA",
                zerolinecolor="#CBD5E1",
                linecolor="#D7DFEA"
            ),
            legend=dict(
                font=dict(color="#14213D", size=11),
                title_font=dict(color="#14213D", size=12)
            ),
            coloraxis_colorbar=dict(
                title_font=dict(color="#14213D", size=12),
                tickfont=dict(color="#52627A", size=10)
            ),
            margin=dict(l=10, r=10, t=35, b=10)
        )
    return fig

# Load data strictly from verified results with safe error handling
@st.cache_data
def load_all_results():
    bat_top10 = pd.read_csv(get_data_file("final_batter_leaderboard.csv"))
    bw_top10 = pd.read_csv(get_data_file("final_bowler_leaderboard.csv"))
    recon_20 = pd.read_csv(get_data_file("reconciled_20_players_phase_stats.csv"))
    bat_boot = pd.read_csv(get_data_file("batter_bootstrap_summary.csv"))
    bw_boot = pd.read_csv(get_data_file("bowler_bootstrap_summary.csv"))
    bat_sens = pd.read_csv(get_data_file("batter_sensitivity_analysis.csv"))
    bw_sens = pd.read_csv(get_data_file("bowler_sensitivity_analysis.csv"))
    bat_consist = pd.read_csv(get_data_file("batter_match_consistency.csv"))
    bw_consist = pd.read_csv(get_data_file("bowler_match_consistency.csv"))
    return bat_top10, bw_top10, recon_20, bat_boot, bw_boot, bat_sens, bw_sens, bat_consist, bw_consist

try:
    bat_top10, bw_top10, recon_20, bat_boot, bw_boot, bat_sens, bw_sens, bat_consist, bw_consist = load_all_results()
except Exception as e:
    st.error(f"Error loading canonical datasets: {e}")
    st.stop()

# Comprehensive Dynamic CSS Injection
if is_dark:
    theme_css = """
    <style>
        :root {
            --bg-main: #111827;
            --bg-sidebar: #0B1220;
            --bg-card: #1E293B;
            --bg-card-sec: #263449;
            --text-primary: #F8FAFC;
            --text-secondary: #CBD5E1;
            --text-muted: #94A3B8;
            --border-color: #334155;
            --color-pink: #F472B6;
            --color-gold: #F5C451;
            --color-green: #34D399;
            --color-red: #F87171;
            --table-header-bg: #263449;
            --table-row-alt: #1A2436;
            --card-shadow: 0 2px 4px rgba(0,0,0,0.25);
            --badge-bg: #1E293B;
            --badge-text: #F8FAFC;
            --badge-bw-bg: #BE185D;
            --badge-bw-text: #FFFFFF;
            --caveat-bg: #2D1525;
            --caveat-border: #F472B6;
            --disclaimer-bg: #2D1525;
            --disclaimer-border: #F472B6;
            --sidebar-active-bg: #263449;
            --sidebar-active-border: #F472B6;
        }

        html, body, .stApp, .stAppViewContainer, [data-testid="stAppViewContainer"], section.main, [data-testid="stMain"] {
            background-color: var(--bg-main) !important;
            color: var(--text-primary) !important;
        }

        /* Top header bar and toolbar in Dark Mode */
        header[data-testid="stHeader"],
        .stAppHeader,
        [data-testid="stToolbar"] {
            background-color: var(--bg-main) !important;
        }
        header[data-testid="stHeader"] *,
        .stAppHeader *,
        [data-testid="stToolbar"] * {
            color: var(--text-primary) !important;
        }

        /* Suppress unwanted Streamlit nudge banners */
        .stSkillsNudge, [data-testid="stSkillsNudge"] {
            display: none !important;
        }

        /* Sidebar container */
        [data-testid="stSidebar"] {
            background-color: var(--bg-sidebar) !important;
            border-right: 1px solid var(--border-color) !important;
        }
        [data-testid="stSidebar"] * {
            color: var(--text-primary);
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: var(--text-secondary);
        }
        [data-testid="stSidebar"] a {
            text-decoration: none !important;
        }

        /* Streamlit Native Controls Contrast Enforcement */
        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] span {
            color: #F8FAFC !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
        }

        div[data-testid="stRadio"] label p,
        div[data-testid="stRadio"] label div {
            color: #CBD5E1 !important;
            font-weight: 500 !important;
        }

        [data-testid="stSlider"] [data-testid="stWidgetLabel"] p {
            color: #F8FAFC !important;
            font-weight: 600 !important;
        }
        [data-testid="stSlider"] div[data-testid="stThumbValue"] {
            color: #F472B6 !important;
            font-weight: 700 !important;
        }
        [data-testid="stSlider"] [data-testid="stTickBarMin"],
        [data-testid="stSlider"] [data-testid="stTickBarMax"] {
            color: #94A3B8 !important;
        }

        [data-testid="stSelectbox"] [data-testid="stWidgetLabel"] p {
            color: #F8FAFC !important;
            font-weight: 600 !important;
        }

        button[data-baseweb="tab"] p {
            color: #CBD5E1 !important;
            font-weight: 600 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] p {
            color: #F472B6 !important;
            font-weight: 700 !important;
        }

        h2, h3, h4 {
            color: #F8FAFC !important;
        }

        /* Sidebar active navigation indicator */
        [data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] {
            background-color: var(--sidebar-active-bg) !important;
            border-left: 3px solid var(--sidebar-active-border);
            font-weight: 700 !important;
        }

        .metric-card {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px;
            padding: 1rem 1.15rem;
            box-shadow: var(--card-shadow);
            margin-bottom: 0.6rem;
        }
        .metric-title {
            color: var(--text-muted) !important;
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 0.25rem;
        }
        .metric-val {
            color: var(--text-primary) !important;
            font-size: 1.45rem;
            font-weight: 800;
            margin: 0.15rem 0 0.35rem 0;
            line-height: 1.2;
        }
        .metric-delta {
            font-size: 0.82rem;
            font-weight: 600;
        }
        .delta-pos { color: var(--color-green) !important; }
        .delta-neg { color: var(--color-red) !important; }
        .delta-gold { color: var(--color-gold) !important; }

        .caveat-box {
            background-color: var(--caveat-bg) !important;
            border-left: 4px solid var(--caveat-border) !important;
            border-top: 1px solid var(--border-color);
            border-right: 1px solid var(--border-color);
            border-bottom: 1px solid var(--border-color);
            padding: 0.9rem 1.1rem;
            border-radius: 6px;
            margin: 0.8rem 0;
            font-size: 0.86rem;
            color: var(--text-primary) !important;
            line-height: 1.5;
        }
        .meth-strip {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px;
            padding: 1.1rem 1.25rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
            box-shadow: var(--card-shadow);
        }
        .disclaimer-box {
            background-color: var(--disclaimer-bg) !important;
            border-left: 4px solid var(--disclaimer-border) !important;
            border-top: 1px solid var(--border-color);
            border-right: 1px solid var(--border-color);
            border-bottom: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 0.9rem 1.1rem;
            margin: 1rem 0;
            font-size: 0.84rem;
            color: var(--text-primary) !important;
            line-height: 1.5;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
        }
    </style>
    """
else:
    theme_css = """
    <style>
        :root {
            --bg-main: #F1F5F9;
            --bg-sidebar: #FFFFFF;
            --bg-card: #FFFFFF;
            --bg-card-sec: #E8EDF5;
            --text-primary: #14213D;
            --text-secondary: #52627A;
            --text-muted: #52627A;
            --border-color: #D7DFEA;
            --color-pink: #C21870;
            --color-gold: #A87913;
            --color-green: #059669;
            --color-red: #DC2626;
            --table-header-bg: #E2E8F0;
            --table-row-alt: #F8FAFC;
            --card-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
            --badge-bg: #E8EDF5;
            --badge-text: #14213D;
            --badge-bw-bg: #FCE7F3;
            --badge-bw-text: #C21870;
            --caveat-bg: #FFF1F5;
            --caveat-border: #C21870;
            --disclaimer-bg: #FFF1F5;
            --disclaimer-border: #C21870;
            --sidebar-active-bg: #E8EDF5;
            --sidebar-active-border: #C21870;
        }

        html, body, .stApp, .stAppViewContainer, [data-testid="stAppViewContainer"], section.main, [data-testid="stMain"] {
            background-color: var(--bg-main) !important;
            color: var(--text-primary) !important;
        }

        /* Top header bar and toolbar in Light Mode */
        header[data-testid="stHeader"],
        .stAppHeader,
        [data-testid="stToolbar"] {
            background-color: var(--bg-main) !important;
        }
        header[data-testid="stHeader"] *,
        .stAppHeader *,
        [data-testid="stToolbar"] * {
            color: var(--text-primary) !important;
        }

        /* Suppress unwanted Streamlit nudge banners */
        .stSkillsNudge, [data-testid="stSkillsNudge"] {
            display: none !important;
        }

        /* Sidebar container */
        [data-testid="stSidebar"] {
            background-color: var(--bg-sidebar) !important;
            border-right: 1px solid var(--border-color) !important;
        }
        [data-testid="stSidebar"] * {
            color: var(--text-primary);
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: var(--text-secondary);
        }
        [data-testid="stSidebar"] a {
            text-decoration: none !important;
        }

        /* Streamlit Native Controls Contrast Enforcement */
        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] span {
            color: #14213D !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
        }

        div[data-testid="stRadio"] label p,
        div[data-testid="stRadio"] label div {
            color: #14213D !important;
            font-weight: 500 !important;
        }

        [data-testid="stSlider"] [data-testid="stWidgetLabel"] p {
            color: #14213D !important;
            font-weight: 600 !important;
        }
        [data-testid="stSlider"] div[data-testid="stThumbValue"] {
            color: #C21870 !important;
            font-weight: 700 !important;
        }
        [data-testid="stSlider"] [data-testid="stTickBarMin"],
        [data-testid="stSlider"] [data-testid="stTickBarMax"] {
            color: #52627A !important;
        }

        [data-testid="stSelectbox"] [data-testid="stWidgetLabel"] p {
            color: #14213D !important;
            font-weight: 600 !important;
        }

        button[data-baseweb="tab"] p {
            color: #52627A !important;
            font-weight: 600 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] p {
            color: #C21870 !important;
            font-weight: 700 !important;
        }

        h2, h3, h4 {
            color: #14213D !important;
        }

        /* Sidebar active navigation indicator */
        [data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] {
            background-color: var(--sidebar-active-bg) !important;
            border-left: 3px solid var(--sidebar-active-border);
            font-weight: 700 !important;
        }

        .metric-card {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px;
            padding: 1rem 1.15rem;
            box-shadow: var(--card-shadow);
            margin-bottom: 0.6rem;
        }
        .metric-title {
            color: var(--text-secondary) !important;
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 0.25rem;
        }
        .metric-val {
            color: var(--text-primary) !important;
            font-size: 1.45rem;
            font-weight: 800;
            margin: 0.15rem 0 0.35rem 0;
            line-height: 1.2;
        }
        .metric-delta {
            font-size: 0.82rem;
            font-weight: 600;
        }
        .delta-pos { color: var(--color-green) !important; }
        .delta-neg { color: var(--color-red) !important; }
        .delta-gold { color: var(--color-gold) !important; }

        .caveat-box {
            background-color: var(--caveat-bg) !important;
            border-left: 4px solid var(--caveat-border) !important;
            border-top: 1px solid var(--border-color);
            border-right: 1px solid var(--border-color);
            border-bottom: 1px solid var(--border-color);
            padding: 0.9rem 1.1rem;
            border-radius: 6px;
            margin: 0.8rem 0;
            font-size: 0.86rem;
            color: var(--text-primary) !important;
            line-height: 1.5;
        }
        .meth-strip {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px;
            padding: 1.1rem 1.25rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
            box-shadow: var(--card-shadow);
        }
        .disclaimer-box {
            background-color: var(--disclaimer-bg) !important;
            border-left: 4px solid var(--disclaimer-border) !important;
            border-top: 1px solid var(--border-color);
            border-right: 1px solid var(--border-color);
            border-bottom: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 0.9rem 1.1rem;
            margin: 1rem 0;
            font-size: 0.84rem;
            color: var(--text-primary) !important;
            line-height: 1.5;
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
        }
    </style>
    """

st.markdown(theme_css, unsafe_allow_html=True)

# Sidebar Branding & Navigation (Synchronized with active system theme)
with st.sidebar:
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "rr_logo.svg")
    logo_rendered = False
    if os.path.exists(logo_path):
        try:
            st.image(logo_path, width=110)
            logo_rendered = True
        except Exception:
            logo_rendered = False
            
    if not logo_rendered:
        st.markdown("""
        <div style='display:inline-block; padding: 6px 14px; background: #0B1B3D; border: 2px solid var(--color-pink); border-radius: 6px; color: #FFFFFF; font-weight: 800; font-size: 1.05rem; letter-spacing: 0.5px; margin-bottom: 0.5rem;'>
            🏏 RAJASTHAN ROYALS
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("""
    <div style='font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 1.35rem; font-weight: 800; color: var(--text-primary); margin-top: 0.3rem; margin-bottom: 0.15rem; line-height: 1.2;'>
        RR SupeRR Selector
    </div>
    <div style='color: var(--color-pink); font-weight: 700; font-size: 0.88rem; margin-bottom: 0.6rem; letter-spacing: 0.3px;'>
        Season 2 — Round 1 Technical System
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    nav_options = [
        "Judge Quick View",
        "Top 10 Batters Leaderboard",
        "Top 10 Bowlers Leaderboard",
        "Individual Player Analysis",
        "Pressure vs Baseline Comparison",
        "Bootstrap Reliability & Rank Uncertainty",
        "Weight Sensitivity Explorer",
        "Match Consistency & LOMO Fragility",
        "Methodology & Limitations"
    ]
    default_idx = 0
    query_sec = st.query_params.get("section", None)
    if query_sec:
        for i, opt in enumerate(nav_options):
            if str(query_sec).lower() in opt.lower():
                default_idx = i
                break

    selected_section = st.radio(
        "Navigation Menu:",
        nav_options,
        index=default_idx
    )
    
    st.markdown("---")
    # Verified canonical specs: 78 Batters (≥60b) | 68 Bowlers (≥75b)
    st.markdown("""
    <div style='font-size:0.78rem; color:var(--text-secondary); line-height: 1.5; background:var(--bg-card-sec); padding:0.75rem 0.85rem; border-radius:6px; border:1px solid var(--border-color);'>
        <b style='color:var(--text-primary);'>System Specs:</b><br/>
        • 367 Played IPL Matches<br/>
        • <b>14,475</b> High-Pressure Legal Balls<br/>
        <span style='font-size:0.73rem; opacity:0.85;'>&nbsp;&nbsp;(15,318 Total HP Deliveries)</span><br/>
        • <b>78 Batters</b> (≥60b) | <b>68 Bowlers</b> (≥75b)<br/>
        • 146 Qualified Role Instances<br/>
        • 1,000 Match-Cluster Bootstraps<br/>
        • Status: Verified Production
    </div>
    """, unsafe_allow_html=True)

# Dashboard Title & One-Line Description
st.markdown("<h1 class='rr-header'>Rajasthan Royals | Pressure Reliability Analytics</h1>", unsafe_allow_html=True)
st.markdown("<div class='rr-sub'>SupeRR Selector Season 2: Round 1 Technical Submission</div>", unsafe_allow_html=True)
st.markdown("<div style='color: var(--text-secondary); font-size: 0.95rem; margin-top: -0.4rem; margin-bottom: 1.2rem; font-weight: 500;'>An independent, data-driven evaluation of batter and bowler reliability under high-pressure IPL situations.</div>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. JUDGE QUICK VIEW (EXECUTIVE DEFAULT LANDING SCREEN)
# -------------------------------------------------------------
if selected_section == "Judge Quick View":
    # 1. Four Highlight Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-title'>#1 Ranked Batter</div>
            <div class='metric-val'>S. Rutherford</div>
            <div class='metric-delta delta-pos'>PRI: +2.615 | 84.5% Boot</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-title'>#1 Ranked Bowler</div>
            <div class='metric-val'>Sunil Narine</div>
            <div class='metric-delta delta-pos'>PRI: +2.506 | 98.3% Boot</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-title'>Top RR Asset</div>
            <div class='metric-val'>Dhruv Jurel</div>
            <div class='metric-delta delta-pos'>Batter #6 (+1.400) | Lift +17.9</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class='metric-card'>
            <div class='metric-title'>Frontline Pace Weapon</div>
            <div class='metric-val'>Jasprit Bumrah</div>
            <div class='metric-delta delta-pos'>Bowler #3 (+1.654) | 70.9% Boot</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)

    # 2. Side-by-Side Canonical Top 10 Leaderboards
    col_bat, col_bw = st.columns(2)
    with col_bat:
        st.markdown("""
        <div style='display:flex; align-items:center; justify-content:space-between; margin-bottom:0.35rem;'>
            <h3 style='color:var(--text-primary); margin:0; font-size:1.15rem;'>🏏 Top 10 Batters Under Pressure</h3>
            <span style='background:var(--badge-bg); color:var(--badge-text); border:1px solid var(--border-color); font-size:0.72rem; font-weight:700; padding:2px 8px; border-radius:4px;'>PRI Standardised</span>
        </div>
        <div style='font-size:0.8rem; color:var(--text-secondary); margin-bottom:0.5rem;'>
            Primary Finishing Assets | <b>60% Shrunk SR | 20% SR Lift | 20% Shrunk Avg</b>
        </div>
        """, unsafe_allow_html=True)
        
        bat_quick_df = bat_top10[[
            'rank', 'player_name', 'pri_score', 'shrunk_high_sr', 'situational_lift_sr', 'bootstrap_top10_inclusion'
        ]].copy()
        
        st.dataframe(
            bat_quick_df,
            column_config={
                "rank": st.column_config.NumberColumn("Rank", format="%d"),
                "player_name": st.column_config.TextColumn("Player"),
                "pri_score": st.column_config.NumberColumn("PRI Score", format="+%.3f", help="Intra-role standardized pressure reliability index"),
                "shrunk_high_sr": st.column_config.NumberColumn("Shrunk Pressure SR", format="%.1f", help="Empirical Bayes shrunk strike rate under high pressure"),
                "situational_lift_sr": st.column_config.NumberColumn("SR Lift", format="%+.1f", help="Situational strike rate lift above regular baseline (High SR − Base SR)"),
                "bootstrap_top10_inclusion": st.column_config.NumberColumn("Bootstrap %", format="%.1f%%", help="Inclusion probability across 1,000 match-cluster bootstraps")
            },
            hide_index=True,
            **_DATAFRAME_WIDTH_KW
        )

    with col_bw:
        st.markdown("""
        <div style='display:flex; align-items:center; justify-content:space-between; margin-bottom:0.35rem;'>
            <h3 style='color:var(--text-primary); margin:0; font-size:1.15rem;'>🎯 Top 10 Bowlers Under Pressure</h3>
            <span style='background:var(--badge-bw-bg); color:var(--badge-bw-text); border:1px solid var(--border-color); font-size:0.72rem; font-weight:700; padding:2px 8px; border-radius:4px;'>PRI Standardised</span>
        </div>
        <div style='font-size:0.8rem; color:var(--text-secondary); margin-bottom:0.5rem;'>
            Primary Clutch Bowlers | <b>60% Shrunk Econ | 20% Econ Lift | 20% Shrunk Wkt Rate</b>
        </div>
        """, unsafe_allow_html=True)
        
        bw_quick_df = bw_top10[[
            'rank', 'player_name', 'pri_score', 'shrunk_high_econ', 'situational_lift_econ', 'bootstrap_top10_inclusion'
        ]].copy()
        
        st.dataframe(
            bw_quick_df,
            column_config={
                "rank": st.column_config.NumberColumn("Rank", format="%d"),
                "player_name": st.column_config.TextColumn("Player"),
                "pri_score": st.column_config.NumberColumn("PRI Score", format="+%.3f", help="Intra-role standardized pressure reliability index"),
                "shrunk_high_econ": st.column_config.NumberColumn("Shrunk Pressure Econ", format="%.2f", help="Empirical Bayes shrunk economy rate under high pressure"),
                "situational_lift_econ": st.column_config.NumberColumn("Economy Lift", format="%+.2f", help="Situational economy lift (Baseline Econ − High Econ; positive = suppression)"),
                "bootstrap_top10_inclusion": st.column_config.NumberColumn("Bootstrap %", format="%.1f%%", help="Inclusion probability across 1,000 match-cluster bootstraps")
            },
            hide_index=True,
            **_DATAFRAME_WIDTH_KW
        )

    # 3. Compact Methodology Strip
    st.markdown("""
    <div class='meth-strip'>
        <div style='font-size:0.92rem; font-weight:700; color:var(--text-primary); margin-bottom:0.4rem;'>
            📐 Evaluation Architecture & Governance Summary
        </div>
        <div style='font-size:0.82rem; color:var(--text-secondary); line-height:1.6;'>
            • <b>Separate Evaluation Pipelines:</b> 78 qualified batters (≥60 HP legal balls) and 68 qualified bowlers (≥75 HP legal balls) are standard-scaled strictly against intra-role peers, satisfying the Unstop two-list mandate.<br/>
            • <b>60/20/20 Constituent PRI:</b> Batters = 60% Shrunk SR + 20% SR Lift (High − Base) + 20% Shrunk Average. Bowlers = 60% Shrunk Suppression (−Econ) + 20% Economy Lift (Base − High) + 20% Shrunk Breakthrough (Wkt Rate).<br/>
            • <b>Empirical Bayes Shrinkage:</b> Batting SR (Prior 140.0, <i>M</i>=50b), Batting Avg (Prior 22.0, <i>M</i>=5 dismissals); Bowling Econ (Prior 8.60, <i>M</i>=60b), Bowling Wicket Rate (Prior 5.50%, <i>M</i>=60b).<br/>
            • <b>Match-Cluster Bootstrap (B=1,000):</b> Resamples 367 full-match clusters with replacement to quantify empirical rank confidence intervals without breaking delivery autocorrelations.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Short Historical-Performance Disclaimer
    st.markdown("""
    <div class='disclaimer-box'>
        <b>⚠️ IMPORTANT ANALYTICAL DISCLAIMER:</b> PRI measures historical performance and reliability under high-pressure conditions across 367 IPL fixtures. Bootstrap inclusion probabilities describe historical ranking stability, not future success probabilities. The analysis does not establish auction prices, player availability, or guaranteed future performance.
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# 2. BATTER LEADERBOARD
# -------------------------------------------------------------
elif selected_section == "Top 10 Batters Leaderboard":
    st.subheader("Top 10 Batters Pressure Reliability Leaderboard")
    
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        view_mode = st.radio("Display Scope:", ["Top 10 Qualifiers (Submission Roster)", "Complete Universe (78 Qualified Batters)"], horizontal=True)
    with col_f2:
        min_balls = st.slider("Minimum High-Pressure Balls Faced:", min_value=60, max_value=250, value=60, step=10)

    df_b_view = bat_boot[bat_boot['high_balls'] >= min_balls].copy()
    if view_mode.startswith("Top 10"):
        df_b_view = df_b_view.head(10)

    if df_b_view.empty:
        st.info("No batter candidates meet the selected exposure threshold.")
    else:
        dynamic_h = max(450, len(df_b_view) * 24)
        fig = px.bar(
            df_b_view.iloc[::-1],
            x="point_pri",
            y="player_name",
            orientation="h",
            color="point_pri",
            color_continuous_scale="Purp",
            title="Batters Ranked by Intra-Role Standardised PRI Score (Z-Score)",
            labels={"point_pri": "Role-Standardised PRI", "player_name": "Batter"}
        )
        fig.update_layout(height=dynamic_h)
        fig = apply_theme_to_fig(fig, is_dark)
        st.plotly_chart(fig, **_PLOTLY_WIDTH_KW)

        st.dataframe(
            df_b_view[['rank', 'player_name', 'high_balls', 'point_pri', 'top10_inclusion_prob', 'median_rank', 'p5_rank', 'p95_rank', 'ci95_sr_shrunk']],
            column_config={
                "rank": "Role Rank",
                "player_name": "Player",
                "high_balls": "HP Balls",
                "point_pri": st.column_config.NumberColumn("PRI Score", format="+%.3f"),
                "top10_inclusion_prob": st.column_config.NumberColumn("Bootstrap Inc %", format="%.1f%%"),
                "median_rank": "Median Rank",
                "p5_rank": "5th Pct Rank",
                "p95_rank": "95th Pct Rank",
                "ci95_sr_shrunk": "95% Shrunk SR CI"
            },
            hide_index=True,
            **_DATAFRAME_WIDTH_KW
        )

# -------------------------------------------------------------
# 3. BOWLER LEADERBOARD
# -------------------------------------------------------------
elif selected_section == "Top 10 Bowlers Leaderboard":
    st.subheader("Top 10 Bowlers Pressure Reliability Leaderboard")

    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        view_mode_bw = st.radio("Display Scope:", ["Top 10 Qualifiers (Submission Roster)", "Complete Universe (68 Qualified Bowlers)"], horizontal=True)
    with col_f2:
        min_balls_bw = st.slider("Minimum High-Pressure Balls Bowled:", min_value=75, max_value=250, value=75, step=10)

    df_bw_view = bw_boot[bw_boot['high_balls'] >= min_balls_bw].copy()
    if view_mode_bw.startswith("Top 10"):
        df_bw_view = df_bw_view.head(10)

    if df_bw_view.empty:
        st.info("No bowler candidates meet the selected exposure threshold.")
    else:
        dynamic_h = max(450, len(df_bw_view) * 24)
        fig = px.bar(
            df_bw_view.iloc[::-1],
            x="point_pri",
            y="player_name",
            orientation="h",
            color="point_pri",
            color_continuous_scale="Blues",
            title="Bowlers Ranked by Intra-Role Standardised PRI Score (Z-Score)",
            labels={"point_pri": "Role-Standardised PRI", "player_name": "Bowler"}
        )
        fig.update_layout(height=dynamic_h)
        fig = apply_theme_to_fig(fig, is_dark)
        st.plotly_chart(fig, **_PLOTLY_WIDTH_KW)

        st.dataframe(
            df_bw_view[['rank', 'player_name', 'high_balls', 'point_pri', 'top10_inclusion_prob', 'median_rank', 'p5_rank', 'p95_rank', 'ci95_econ_shrunk']],
            column_config={
                "rank": "Role Rank",
                "player_name": "Player",
                "high_balls": "HP Balls",
                "point_pri": st.column_config.NumberColumn("PRI Score", format="+%.3f"),
                "top10_inclusion_prob": st.column_config.NumberColumn("Bootstrap Inc %", format="%.1f%%"),
                "median_rank": "Median Rank",
                "p5_rank": "5th Pct Rank",
                "p95_rank": "95th Pct Rank",
                "ci95_econ_shrunk": "95% Shrunk Econ CI"
            },
            hide_index=True,
            **_DATAFRAME_WIDTH_KW
        )

# -------------------------------------------------------------
# 4. INDIVIDUAL PLAYER ANALYSIS
# -------------------------------------------------------------
elif selected_section == "Individual Player Analysis":
    st.subheader("Individual Player Dossiers (All 20 Clutch Performers)")
    
    col_sel1, col_sel2 = st.columns([1, 2])
    with col_sel1:
        sel_role = st.selectbox("Select Role Discipline:", ["Batter", "Bowler"], key="sel_discipline")
        player_pool = bat_top10['player_name'].tolist() if sel_role == "Batter" else bw_top10['player_name'].tolist()
        sel_player = st.selectbox("Select Player Profile:", player_pool, key=f"sel_player_{sel_role}")

    # Extract player details safely with fallback handling
    p_rec_df = recon_20[recon_20['player_name'] == sel_player]
    if p_rec_df.empty:
        sel_player = player_pool[0]
        p_rec_df = recon_20[recon_20['player_name'] == sel_player]
    p_rec = p_rec_df.iloc[0]

    curr_boot = bat_boot if sel_role == "Batter" else bw_boot
    p_boot_df = curr_boot[curr_boot['player_name'] == sel_player]
    p_boot = p_boot_df.iloc[0] if not p_boot_df.empty else curr_boot[curr_boot['player_name'] == player_pool[0]].iloc[0]

    curr_cons = bat_consist if sel_role == "Batter" else bw_consist
    p_cons_df = curr_cons[curr_cons['player_name'] == sel_player]
    p_cons = p_cons_df.iloc[0] if not p_cons_df.empty else curr_cons[curr_cons['player_name'] == player_pool[0]].iloc[0]

    st.markdown(f"### Player Dossier: **{sel_player}** ({sel_role} #{int(p_rec['role_rank'])})")

    # True Canonical Metrics Display
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(
            "Role PRI Score",
            f"+{p_boot['point_pri']:.3f}",
            f"Shrunk: {p_rec['shrunk_execution']:.1f} SR" if sel_role == "Batter" else f"Shrunk: {p_rec['shrunk_execution']:.2f} RPO"
        )
    with kpi2:
        st.metric(
            "Situational Lift",
            f"{p_rec['situational_lift']:+.1f} SR" if sel_role == "Batter" else f"{p_rec['situational_lift']:+.2f} RPO"
        )
    with kpi3:
        st.metric(
            "Bootstrap Inclusion",
            f"{p_boot['top10_inclusion_prob']:.1f}%",
            f"Med Rank: #{p_boot['median_rank']:.0f}"
        )
    with kpi4:
        st.metric(
            "LOMO Max Drop",
            f"-{int(p_cons['lomo_max_rank_drop'])} Ranks",
            f"Worst: #{int(p_cons['lomo_worst_rank'])}"
        )

    # Comprehensive 4-Phase Breakdown Chart (Powerplay, Middle, Death, Super Over)
    phases = ['Powerplay (1-6)', 'Middle (7-15)', 'Death (16-20)', 'Super Over']
    p_balls = [
        int(p_rec['powerplay_balls']) if not pd.isna(p_rec['powerplay_balls']) else 0,
        int(p_rec['middle_balls']) if not pd.isna(p_rec['middle_balls']) else 0,
        int(p_rec['death_balls']) if not pd.isna(p_rec['death_balls']) else 0,
        int(p_rec['superover_balls']) if not pd.isna(p_rec['superover_balls']) else 0
    ]
    p_execs = [
        p_rec['powerplay_exec'],
        p_rec['middle_exec'],
        p_rec['death_exec'],
        p_rec['superover_exec']
    ]

    exec_texts = []
    for b, v in zip(p_balls, p_execs):
        if b == 0 or pd.isna(v):
            exec_texts.append("N/A (0b)")
        elif sel_role == "Batter":
            exec_texts.append(f"{v:.1f} SR")
        else:
            exec_texts.append(f"{v:.2f} Econ")

    fig_phase = go.Figure()
    bar_color = "#3B82F6" if is_dark else "#1D4ED8"
    scatter_color = ("#F472B6" if is_dark else "#C21870") if sel_role == "Batter" else ("#60A5FA" if is_dark else "#0284C7")
    
    fig_phase.add_trace(go.Bar(
        x=phases,
        y=p_balls,
        name="Legal Balls",
        marker_color=bar_color,
        text=[f"{b}b" for b in p_balls],
        textposition="auto"
    ))
    fig_phase.add_trace(go.Scatter(
        x=phases,
        y=[v if b > 0 and not pd.isna(v) else None for b, v in zip(p_balls, p_execs)],
        name="Execution Metric" + (" (SR)" if sel_role == "Batter" else " (Econ)"),
        yaxis="y2",
        mode="lines+markers+text",
        text=exec_texts,
        textposition="top center",
        marker=dict(size=10, color=scatter_color),
        line=dict(width=2)
    ))
    fig_phase.update_layout(
        title=f"Reconciled Phase Execution & Exposure for {sel_player}",
        yaxis=dict(title="Legal Deliveries"),
        yaxis2=dict(
            title="Execution Metric" + (" (SR)" if sel_role == "Batter" else " (Economy)"),
            overlaying="y",
            side="right"
        ),
        height=400,
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_phase = apply_theme_to_fig(fig_phase, is_dark)
    st.plotly_chart(fig_phase, **_PLOTLY_WIDTH_KW)

# -------------------------------------------------------------
# 5. PRESSURE VS BASELINE COMPARISON
# -------------------------------------------------------------
elif selected_section == "Pressure vs Baseline Comparison":
    st.subheader("Pressure vs Baseline Lift Dynamics")
    
    tab_b, tab_bw = st.tabs(["Batters: High SR vs Baseline SR", "Bowlers: High Econ vs Baseline Econ"])
    with tab_b:
        fig_b = px.scatter(
            bat_top10,
            x="baseline_sr",
            y="shrunk_high_sr",
            size="high_legal_balls",
            color="situational_lift_sr",
            hover_name="player_name",
            text="player_name",
            color_continuous_scale="Viridis",
            labels={
                "baseline_sr": "Tournament Baseline SR",
                "shrunk_high_sr": "Shrunk High-Pressure SR",
                "situational_lift_sr": "Situational Lift (SR)",
                "high_legal_balls": "HP Legal Balls"
            },
            title="Batters: Elevating Beyond Baseline (Above Diagonal = Positive Lift)"
        )
        fig_b.add_shape(type="line", x0=130, y0=130, x1=195, y1=195, line=dict(color="#EF4444" if is_dark else "#DC2626", dash="dash"))
        fig_b.update_traces(textposition='top right')
        fig_b.update_layout(height=500)
        fig_b = apply_theme_to_fig(fig_b, is_dark)
        st.plotly_chart(fig_b, **_PLOTLY_WIDTH_KW)

    with tab_bw:
        fig_bw = px.scatter(
            bw_top10,
            x="baseline_econ",
            y="shrunk_high_econ",
            size="high_legal_balls",
            color="situational_lift_econ",
            hover_name="player_name",
            text="player_name",
            color_continuous_scale="Teal",
            labels={
                "baseline_econ": "Tournament Baseline Econ",
                "shrunk_high_econ": "Shrunk High-Pressure Econ",
                "situational_lift_econ": "Containment Lift (RPO)",
                "high_legal_balls": "HP Legal Balls"
            },
            title="Bowlers: Run Suppression Under Leverage (Below Diagonal = Improved Econ)"
        )
        fig_bw.add_shape(type="line", x0=6.0, y0=6.0, x1=10.0, y1=10.0, line=dict(color="#EF4444" if is_dark else "#DC2626", dash="dash"))
        fig_bw.update_traces(textposition='bottom right')
        fig_bw.update_layout(height=500)
        fig_bw = apply_theme_to_fig(fig_bw, is_dark)
        st.plotly_chart(fig_bw, **_PLOTLY_WIDTH_KW)

# -------------------------------------------------------------
# 6. BOOTSTRAP RELIABILITY & RANK UNCERTAINTY
# -------------------------------------------------------------
elif selected_section == "Bootstrap Reliability & Rank Uncertainty":
    st.subheader("Bootstrap Stability & 90% Rank Intervals")
    st.markdown("""
    Evaluated across **1,000 match-cluster bootstrap replicates** with replacement ($K_m$ draw multiplicity).
    Tracking within-role rankings resolves the cross-role crowding artifact.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Batters Rank Intervals (5th to 95th Percentile)")
        fig_r_b = go.Figure()
        diamond_color = "#F5C451" if is_dark else "#A87913"
        line_color = "#F472B6" if is_dark else "#C21870"
        for idx, r in bat_top10.iloc[::-1].iterrows():
            fig_r_b.add_trace(go.Scatter(
                x=[r['bootstrap_p5_rank'], r['bootstrap_p95_rank']],
                y=[r['player_name'], r['player_name']],
                mode="lines+markers",
                line=dict(color=line_color, width=3),
                marker=dict(size=8),
                name=r['player_name'],
                showlegend=False
            ))
            fig_r_b.add_trace(go.Scatter(
                x=[r['bootstrap_median_rank']],
                y=[r['player_name']],
                mode="markers",
                marker=dict(color=diamond_color, size=10, symbol="diamond"),
                showlegend=False
            ))
        fig_r_b.update_layout(
            xaxis=dict(title="Rank (Lower is Better)", autorange="reversed"),
            height=450,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        fig_r_b = apply_theme_to_fig(fig_r_b, is_dark)
        st.plotly_chart(fig_r_b, **_PLOTLY_WIDTH_KW)

    with col2:
        st.markdown("### Bowlers Rank Intervals (5th to 95th Percentile)")
        fig_r_bw = go.Figure()
        line_bw_color = "#60A5FA" if is_dark else "#0284C7"
        for idx, r in bw_top10.iloc[::-1].iterrows():
            fig_r_bw.add_trace(go.Scatter(
                x=[r['bootstrap_p5_rank'], r['bootstrap_p95_rank']],
                y=[r['player_name'], r['player_name']],
                mode="lines+markers",
                line=dict(color=line_bw_color, width=3),
                marker=dict(size=8),
                name=r['player_name'],
                showlegend=False
            ))
            fig_r_bw.add_trace(go.Scatter(
                x=[r['bootstrap_median_rank']],
                y=[r['player_name']],
                mode="markers",
                marker=dict(color=diamond_color, size=10, symbol="diamond"),
                showlegend=False
            ))
        fig_r_bw.update_layout(
            xaxis=dict(title="Rank (Lower is Better)", autorange="reversed"),
            height=450,
            margin=dict(l=0, r=0, t=20, b=0)
        )
        fig_r_bw = apply_theme_to_fig(fig_r_bw, is_dark)
        st.plotly_chart(fig_r_bw, **_PLOTLY_WIDTH_KW)

# -------------------------------------------------------------
# 7. WEIGHT SENSITIVITY EXPLORER
# -------------------------------------------------------------
elif selected_section == "Weight Sensitivity Explorer":
    st.subheader("Intra-Role Weight Sensitivity Matrix")
    st.markdown(r"""
    Sweeps across 5 execution-weight regimes ($50\%$ to $70\%$) confirm that core anchors remain stable,
    while boundary positions respond logically to lift vs execution trade-offs.
    """)

    tab_s_b, tab_s_bw = st.tabs(["Batters Sensitivity (Top 12)", "Bowlers Sensitivity (Top 12)"])
    cols_s = ['primary_rank_60_20_20', 'player_name', 'rank_50/30/20', 'rank_55/25/20', 'rank_60/20/20', 'rank_65/15/20', 'rank_70/10/20']
    
    with tab_s_b:
        st.dataframe(
            bat_sens.head(12)[cols_s],
            column_config={
                "primary_rank_60_20_20": "Canonical Rank",
                "player_name": "Player Name",
                "rank_50/30/20": "50/30/20",
                "rank_55/25/20": "55/25/20",
                "rank_60/20/20": "60/20/20 (Canonical)",
                "rank_65/15/20": "65/15/20",
                "rank_70/10/20": "70/10/20"
            },
            hide_index=True,
            **_DATAFRAME_WIDTH_KW
        )
    with tab_s_bw:
        st.dataframe(
            bw_sens.head(12)[cols_s],
            column_config={
                "primary_rank_60_20_20": "Canonical Rank",
                "player_name": "Player Name",
                "rank_50/30/20": "50/30/20",
                "rank_55/25/20": "55/25/20",
                "rank_60/20/20": "60/20/20 (Canonical)",
                "rank_65/15/20": "65/15/20",
                "rank_70/10/20": "70/10/20"
            },
            hide_index=True,
            **_DATAFRAME_WIDTH_KW
        )

# -------------------------------------------------------------
# 8. MATCH CONSISTENCY & LOMO FRAGILITY
# -------------------------------------------------------------
elif selected_section == "Match Consistency & LOMO Fragility":
    st.subheader("Match-to-Match Consistency & Single-Match Dependence")
    st.markdown("""
    Leave-one-match-out (LOMO) tests drop each played fixture and recompute the entire leaderboard to isolate single-match dependencies.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Batters LOMO Maximum Rank Drops")
        st.dataframe(
            bat_consist.head(10)[['role_rank', 'player_name', 'hp_matches', 'max_match_runs_pct', 'lomo_worst_rank', 'lomo_max_rank_drop']],
            column_config={
                "role_rank": "Rank",
                "player_name": "Player",
                "hp_matches": "HP Matches",
                "max_match_runs_pct": st.column_config.NumberColumn("Top Knock %", format="%.1f%%"),
                "lomo_worst_rank": "LOMO Worst Rank",
                "lomo_max_rank_drop": "Max Rank Drop"
            },
            hide_index=True,
            **_DATAFRAME_WIDTH_KW
        )
    with col2:
        st.markdown("### Bowlers LOMO Maximum Rank Drops")
        st.dataframe(
            bw_consist.head(10)[['role_rank', 'player_name', 'hp_matches', 'max_match_balls_pct', 'lomo_worst_rank', 'lomo_max_rank_drop']],
            column_config={
                "role_rank": "Rank",
                "player_name": "Player",
                "hp_matches": "HP Matches",
                "max_match_balls_pct": st.column_config.NumberColumn("Top Game %", format="%.1f%%"),
                "lomo_worst_rank": "LOMO Worst Rank",
                "lomo_max_rank_drop": "Max Rank Drop"
            },
            hide_index=True,
            **_DATAFRAME_WIDTH_KW
        )

# -------------------------------------------------------------
# 9. METHODOLOGY & LIMITATIONS
# -------------------------------------------------------------
elif selected_section == "Methodology & Limitations":
    st.subheader("Methodology Documentation & Governance Limitations")
    
    st.markdown(r"""
    ### Mathematical Model Summary
    - **Continuous Leverage ($S_t$)**: Continuous function $S_t \in [0.05, 1.00]$ combining chasing leverage (RRR par, resource scarcity, time amplification) and target-setting par deficits evaluated via 5-fold cross-fitting.
    - **Eligibility Thresholds**:
      - Batters: $\ge 60$ High-Pressure Legal Balls ($N = 78$ qualified candidates).
      - Bowlers: $\ge 75$ High-Pressure Legal Balls ($N = 68$ qualified candidates).
    - **Empirical Bayes Shrinkage**: Regresses observed rates to tournament empirical priors:
      - Batting SR: Prior $140.0$, Weight $M = 50$ legal balls.
      - Batting Average: Prior $22.0$, Weight $M = 5$ dismissals.
      - Bowling Economy: Prior $8.60$, Weight $M = 60$ legal balls.
      - Bowling Wicket Rate: Prior $5.50\%$, Weight $M = 60$ legal balls.
    - **60/20/20 Weighting Architecture**:
      - $\text{PRI}_{\text{bat}} = 0.60 Z(\text{SR}_{\text{shrunk}}) + 0.20 Z(\Delta\text{SR}) + 0.20 Z(\text{Avg}_{\text{shrunk}})$
      - $\text{PRI}_{\text{bowl}} = 0.60 Z(-\text{Econ}_{\text{shrunk}}) + 0.20 Z(-\Delta\text{Econ}) + 0.20 Z(\text{WktRate}_{\text{shrunk}})$

    ### Governance & Analytical Caveats
    1. **Historical Stability vs Future Prediction**: Bootstrap inclusion probabilities reflect historical resampling stability across 367 matches; they do NOT predict future match outcomes.
    2. **Auction Independence**: This statistical index measures delivery-level execution. It does not establish contract prices, retention slabs, or auction valuations.
    3. **Official Neutrality**: Prepared strictly as an independent analytical submission for SupeRR Selector Season 2; does not imply official endorsement by Rajasthan Royals franchise leadership.
    4. **Prior-Inflation Stress Testing**: Under a $+25\%$ prior inflation stress test, bowling ranks exhibit movement (including Narine shifting from #1 to #4) while retaining 9/10 cohort membership. The canonical ranking remains based on the pre-specified empirical Bayes priors.
    """)
