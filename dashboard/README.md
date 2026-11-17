# Rajasthan Royals SupeRR Selector — Interactive Analytics Dashboard

Interactive Streamlit decision-support dashboard for the **Rajasthan Royals SupeRR Selector Season 2 (Round 1)** auction analytics system.

---

## 1. Environment Setup & Installation

Ensure Python 3.10+ is installed. It is recommended to use an isolated virtual environment:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

### Dependencies:
- `streamlit>=1.30.0`: Web application framework
- `pandas>=2.0.0`: Data loading and manipulation
- `numpy>=1.24.0`: Array and numerical calculations
- `plotly>=5.18.0`: Interactive charts and visualizations
- `watchdog>=3.0.0`: Fast filesystem watcher for smooth local live-reloading

---

## 2. Launching the Application

The dashboard contains robust relative-path discovery and can be launched from either the project repository root or directly from inside the `dashboard/` directory:

### Option A: From Repository Root
```bash
streamlit run final_submission/dashboard/app.py
```

### Option B: From Dashboard Directory
```bash
cd final_submission/dashboard
streamlit run app.py
```

The application will launch locally at `http://localhost:8501`.

---

## 3. Included Dashboard Modules

The dashboard features 9 fully interactive analytical sections accessible via the sidebar navigation:

1. **Judge Quick View**: Executive default landing page featuring 4 key performer spotlight cards (#1 Rutherford, #1 Narine, RR asset Jurel, pace weapon Bumrah), side-by-side Top 10 Batters & Bowlers leaderboards, compact evaluation architecture & governance summary, and analytical disclaimer. Both Dark Mode (default) and Light Mode are supported via the sidebar appearance toggle.
2. **Top 10 Batters Leaderboard**: Interactive horizontal bar charts and data tables with exposure filtering and complete 78-player universe expansion.
3. **Top 10 Bowlers Leaderboard**: Interactive horizontal bar charts and data tables with exposure filtering and complete 68-player universe expansion.
4. **Individual Player Analysis**: Comprehensive player dossier for all 20 clutch performers with KPI metrics, role PRI score, and 4-phase breakdown (Powerplay, Middle, Death, Super Over).
5. **Pressure vs Baseline Comparison**: Scatter plots illustrating situational strike rate and economy rate lift above baseline.
6. **Bootstrap Reliability & Rank Uncertainty**: Visualizing 90% rank intervals across 1,000 match-cluster bootstrap replicates.
7. **Weight Sensitivity Explorer**: Intra-role sensitivity sweeps across 5 execution-weight regimes ($50\%$ to $70\%$).
8. **Match Consistency & LOMO Fragility**: Leave-one-match-out maximum rank drops and single-fixture dependence diagnostics.
9. **Methodology & Limitations**: Mathematical specifications, Empirical Bayes shrinkage parameters, and governance disclosures.

---

## 4. Cloud Deployment Notes (e.g. Streamlit Community Cloud)

If deploying to a cloud hosting platform such as Streamlit Community Cloud:
1. Ensure the parent directory containing the `leaderboards/` and `evidence/` CSV folders is included in the deployment repository.
2. The entry point file is `final_submission/dashboard/app.py` (or `app.py` if the repository root is `dashboard/` with CSVs located in a `data/` or relative path).
