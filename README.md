# Rajasthan Royals | SupeRR Selector Season 2 (Round 1)
## Pressure Reliability Index (PRI) Analytics System & IPL 2027 Auction Analytics

**Submission Track**: Round 1 — Independent Batter & Bowler Pressure Reliability Ranking Systems  
**Project Root**: `.` (RR_IPL_2027_ANALYTICS)  
**Production Status**: **FROZEN & AUTHORITATIVELY RECONCILED (GATE 3)**  

---

## 1. Executive Summary & Purpose

Ahead of the **IPL 2027 Mega-Auction**, this project addresses a foundational challenge in modern T20 cricket analytics: **Which players consistently and reliably execute under extreme match pressure relative to their baseline output?**

Traditional cricket metrics (such as aggregate strike rates, batting averages, and economy rates) evaluate performance across all game situations, blending low-stakes accumulation with crisis execution. Conversely, naive "clutch" analyses rely on arbitrary over filters (e.g., classifying all deliveries in overs 16–20 as high-pressure, regardless of whether a match is tightly contested or effectively decided).

This project establishes the **Pressure Reliability Index (PRI)**: a continuous, empirically calibrated leverage framework evaluated on delivery-level match states across **IPL 2022–2026**. 

### Core Analytical Tenets:
1. **Independent Dual Pipelines**: In strict accordance with the competition brief, batters and bowlers are evaluated in separate, non-overlapping scoring pipelines. No cross-role composite ranking is created.
2. **Dynamic Continuous Pressure ($S_t \in [0.05, 1.00]$)**: High pressure is defined dynamically by match context—incorporating required run rate elevation against seasonal par, resource scarcity (wickets in hand), innings progression (time leverage), and target-setting par deficits—thresholded at **$S_t \ge 0.65$**.
3. **Empirical Bayes Shrinkage**: Low-exposure estimates are regressed toward empirical population priors, preventing small-sample artifacts from dominating rankings.
4. **Holistic 60/20/20 Architecture**: Evaluates crisis execution (60%), situational lift relative to baseline (20%), and survival/breakthrough capacity (20%).
5. **Rigorous Uncertainty Disclosures**: Validated via 1,000-replicate match-cluster bootstrap simulations and Leave-One-Match-Out (LOMO) diagnostics.

---

## 2. Authoritative Canonical Leaderboards

The canonical production leaderboards are evaluated strictly within the qualified IPL universes: **78 Batters** ($\ge 60$ high-pressure legal balls faced) and **68 Bowlers** ($\ge 75$ high-pressure legal balls bowled).

### Top 10 Batters Under Pressure (Ranks 1–10)
Standardized strictly within the universe of 78 qualified IPL batters ($\mu = 0, \sigma = 1$):

| Rank | Player Name | HP Balls | Raw HP SR | Shrunk HP SR | Baseline SR | Situational Lift ($\Delta\text{SR}$) | Shrunk HP Avg | PRI Score | Bootstrap Top 10 Inc % | Median Rank | 90% Empirical Rank Interval |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **Sherfane Rutherford** | 87 | 220.69 | 191.24 | 145.13 | +46.11 | 27.45 | **+2.615** | 84.5% | 3.0 | [1.0, 26.0] |
| **#2** | **Namboori Tilak Varma** | 241 | 186.31 | 178.35 | 144.89 | +33.46 | 31.06 | **+2.011** | 75.7% | 5.0 | [1.0, 33.0] |
| **#3** | **David Miller** | 192 | 179.69 | 171.49 | 144.24 | +27.25 | 35.00 | **+1.783** | 63.6% | 7.0 | [1.0, 34.0] |
| **#4** | **Rinku Singh** | 313 | 173.48 | 168.87 | 150.97 | +17.90 | 40.81 | **+1.746** | 62.6% | 7.0 | [1.0, 35.0] |
| **#5** | **Tim David** | 293 | 183.62 | 177.26 | 178.57 | -1.31 | 34.11 | **+1.454** | 52.2% | 10.0 | [2.0, 40.0] |
| **#6** | **Dhruv Jurel** | 165 | 181.82 | 172.09 | 154.19 | +17.90 | 29.29 | **+1.400** | 48.0% | 11.0 | [3.0, 31.0] |
| **#7** | **Liam Livingstone** | 116 | 181.03 | 168.67 | 160.61 | +8.07 | 35.56 | **+1.340** | 40.2% | 14.0 | [2.0, 55.0] |
| **#8** | **Ashutosh Sharma** | 182 | 186.81 | 176.72 | 170.91 | +5.82 | 28.12 | **+1.316** | 46.9% | 11.0 | [2.0, 34.0] |
| **#9** | **Tristan Stubbs** | 241 | 170.95 | 165.64 | 152.40 | +13.24 | 32.62 | **+1.192** | 37.5% | 15.0 | [2.0, 45.0] |
| **#10** | **Dinesh Karthik** | 186 | 184.95 | 175.42 | 174.56 | +0.86 | 28.38 | **+1.183** | 43.2% | 13.0 | [2.0, 51.0] |

---

### Top 10 Bowlers Under Pressure (Ranks 1–10)
Standardized strictly within the universe of 68 qualified IPL bowlers ($\mu = 0, \sigma = 1$):

| Rank | Player Name | HP Balls | Raw HP Econ | Shrunk HP Econ | Baseline Econ | Situational Lift ($-\Delta\text{Econ}$) | Shrunk HP Wkt% | PRI Score | Bootstrap Top 10 Inc % | Median Rank | 90% Empirical Rank Interval |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **#1** | **Sunil Narine** | 272 | 5.45 | 6.02 | 6.86 | +0.85 | 7.32% | **+2.506** | 98.3% | 1.0 | [1.0, 7.0] |
| **#2** | **Sai Kishore** | 92 | 6.85 | 7.54 | 8.99 | +1.45 | 8.75% | **+1.798** | 84.4% | 6.0 | [2.0, 15.0] |
| **#3** | **Jasprit Bumrah** | 232 | 6.57 | 6.99 | 7.17 | +0.18 | 7.98% | **+1.654** | 70.9% | 6.0 | [1.0, 25.0] |
| **#4** | **Noor Ahmad** | 226 | 6.90 | 7.26 | 8.17 | +0.91 | 6.75% | **+1.509** | 63.0% | 7.5 | [1.0, 33.0] |
| **#5** | **Mitchell Santner** | 76 | 5.61 | 6.93 | 7.63 | +0.70 | 5.37% | **+1.471** | 61.2% | 8.0 | [2.0, 34.0] |
| **#6** | **Rahul Chahar** | 106 | 6.91 | 7.52 | 8.15 | +0.64 | 8.01% | **+1.416** | 54.1% | 10.0 | [2.0, 32.0] |
| **#7** | **Yuzvendra Chahal** | 301 | 8.03 | 8.13 | 8.76 | +0.63 | 10.06% | **+1.276** | 47.0% | 12.0 | [2.0, 37.0] |
| **#8** | **Suyash Sharma** | 209 | 7.29 | 7.58 | 8.89 | +1.31 | 4.94% | **+1.123** | 40.7% | 13.0 | [2.0, 40.0] |
| **#9** | **Matheesha Pathirana** | 268 | 7.86 | 7.99 | 8.62 | +0.63 | 8.02% | **+1.058** | 28.1% | 15.0 | [5.0, 30.0] |
| **#10** | **Mohit Sharma** | 229 | 8.67 | 8.66 | 9.59 | +0.94 | 10.48% | **+1.051** | 26.2% | 16.5 | [4.0, 35.0] |

---

## 3. Dataset Populations & Provenance

To maintain absolute transparency, all populations are rigorously reconciled against underlying match logs:

- **IPL Production Universe (IPL 2022–2026)**:
  - **371 scheduled IPL matches**.
  - **4 rain-abandoned matches** without delivery records.
  - **367 played IPL matches** with delivery logs.
  - **87,687 ball-by-ball delivery records**.
  - **83,878 legal deliveries** (`is_legal_ball == True`).
- **IPL High-Pressure Substrate ($S_t \ge 0.65$)**:
  - **15,318 delivery records** ($17.47\%$ of IPL delivery records).
  - **14,475 legal deliveries** ($17.26\%$ of IPL legal deliveries).
- **Broader Raw Dataset Context**:
  - `matches.csv`: 883 scheduled matches across all formats (482 T20I, 401 T20 of which 371 are IPL).
  - `ball_by_ball.csv`: 867 played matches (16 abandoned matches: $883 - 16 = 867$), containing 200,999 delivery records.
  - *Boundary Rule*: International T20 data is used strictly for macroscopic context calibration; the canonical candidate leaderboards are **100% IPL-only**.

---

## 4. Methodology Summary & Equations

### 4.1 Production PRI Equations (60 / 20 / 20 Architecture)
The production PRI model balances absolute execution under pressure with situational elevation over baseline:

$$\text{Raw PRI}_{\text{bat}} = 0.60 \cdot z(\text{SR}_{\text{shrunk}}) + 0.20 \cdot z(\Delta\text{SR}) + 0.20 \cdot z(\text{Avg}_{\text{shrunk}})$$

$$\text{Raw PRI}_{\text{bowl}} = 0.60 \cdot z(-\text{Econ}_{\text{shrunk}}) + 0.20 \cdot z(-\Delta\text{Econ}) + 0.20 \cdot z(\text{WktRate}_{\text{shrunk}})$$

Standardization is performed strictly within role ($\mu=0, \sigma=1$ across the 78 batters and 68 bowlers).

### 4.2 Eligibility Cutoffs vs. Empirical Bayes Priors
- **Batter Qualification**: Minimum **60 high-pressure legal balls faced** ($\rightarrow$ **78 candidates**).
  - Strike Rate: Prior = **140.0 SR**, Shrinkage Weight $M = 50.0$ legal balls.
  - Batting Average: Prior = **22.0 runs/out**, Shrinkage Weight $M = 5.0$ dismissals.
- **Bowler Qualification**: Minimum **75 high-pressure legal balls bowled** ($\rightarrow$ **68 candidates**).
  - Economy Rate: Prior = **8.60 RPO**, Shrinkage Weight $M = 60.0$ legal balls.
  - Wicket Rate: Prior = **5.50%**, Shrinkage Weight $M = 60.0$ legal balls.

### 4.3 Cricket Metric Accounting & Analytical Conventions
- **Batter Balls Faced (Analytical Modeling Convention vs. Conventional Scorekeeping)**: In this project's codebase, balls faced is calculated strictly as the sum of legal deliveries faced (`is_legal_ball`), excluding both wides and overstep no-balls. While conventional scorekeeping counts no-balls as balls faced by the batter, this pipeline measures batting strike rate strictly per *legal delivery faced* to maintain dimensional symmetry with bowling over progression and economy calculations. Runs scored off the bat on an overstep are credited to the batter's runs. This is an internal analytical modeling choice, not an MCC Law 21 statutory mandate.
- **Bowler Economy Rate**: Includes runs off the bat, wides, and overstep no-balls. Excludes byes and leg-byes. Calculated per 6 legal deliveries.
- **Bowler Wickets**: Strictly credited for bowler dismissals (`Bowled`, `Caught`, `LBW`, `Stumped`, and `Hit Wicket`). Run-outs, retired out, and obstructing the field are excluded.

---

## 5. Statistical Uncertainty & Temporal Disclosures

1. **Bootstrap Selection Frequency**:
   - Evaluated across 1,000 match-cluster resamples ($B=1,000$).
   - Bootstrap inclusion percentage measures historical selection stability across tournament resamples; it is **not** an individual probability of future match success.
2. **Rank Intervals**:
   - Reported as 90% empirical rank intervals $[P_5, P_{95}]$, encompassing the 5th to 95th percentiles of resampled ranks.
   - Intervals reflect genuine cricket variance (e.g., Dhruv Jurel $[3, 31]$; Liam Livingstone $[2, 55]$). They are not "narrow confidence bands".
3. **Disaggregated LOMO Diagnostics**:
   - **Pressure-Benchmark LOMO**: Omits 1 match when calculating tournament par. Batter Top 10 ranks are 10/10 identical; Bowler Top 10 membership is 10/10 identical (1 rank swap: Chahar/Chahal). Confirms par benchmark stability.
   - **Player-Match Influence**: Omits an individual player's best match. Highlights outlier-dependent players (e.g., Liam Livingstone drops 30 positions from #7 to #37; Dinesh Karthik drops 14 positions from #10 to #24).
4. **Retrospective Calibration Disclosure**:
   - 5-fold cross-fitting for innings 1 expected runs uses randomized match assignment rather than chronological partitioning.
   - The tournament par benchmark (`comp_par_total`) is calibrated retrospectively from completed matches across the full season. PRI is an objective retrospective performance evaluation, not a strict real-time predictive forecasting model.

---

## 6. Player Availability & Strategic Scouting Context

The PRI rankings represent delivery-level performance signals, not an econometric auction price or valuation model. Franchise acquisition decisions must integrate availability, auction pool status, and squad construction constraints:

- **Dinesh Karthik (#10 Batter)**: Officially retired from all formats of professional cricket on June 1, 2024, and was appointed Batting Coach and Mentor of Royal Challengers Bengaluru (RCB). He is **ineligible and unavailable for the IPL 2027 auction**. His #10 ranking reflects historical 2022–2024 performance and stands as an analytical validation of late-innings finishing, not an active acquisition recommendation.
- **Dhruv Jurel (#6 Batter)**: Retained by Rajasthan Royals for INR 14 Crore ahead of the IPL 2025 mega-auction. While his #6 ranking reflects elite finishing capability, his 48.0% bootstrap inclusion rate, median rank 11, and 90% rank interval [3, 31] reflect material variance across match contexts. His ranking provides a strong scouting indicator, but should not be framed as an indisputable guarantee of unpriced surplus.

---

## 7. Submission Package Structure & Navigation

The submission deliverables are structured into modular directories:

```
final_submission/
├── README.md                                      # Primary package overview & documentation
├── dashboard/                                     # Interactive decision-support application
│   ├── app.py                                     # Streamlit dashboard script (9 interactive modules)
│   ├── requirements.txt                           # Dashboard Python dependencies
│   ├── README.md                                  # Dashboard launch & installation guide
│   └── assets/                                    # Local branding assets (vector RR crest)
├── documentation/                                 # Authoritative methodology & dictionaries
│   ├── SEPARATE_RANKING_METHODOLOGY.md            # Complete mathematical specifications
│   ├── data_dictionary.md                         # Field schemas & operational cricket rules
│   ├── FINAL_FORENSIC_ISSUE_REGISTER.md           # Register of all 18 audited issues
│   ├── FINAL_METHODOLOGY_CORRECTIONS.md           # Record of methodological corrections
│   └── FINAL_SUBMISSION_QA_REPORT.md              # Quality assurance & sign-off report
├── evidence/                                      # Diagnostic matrices & bootstrap tables
│   ├── batter_bootstrap_summary.csv               # 78 Batters cluster-bootstrap distributions
│   ├── bowler_bootstrap_summary.csv               # 68 Bowlers cluster-bootstrap distributions
│   ├── batter_match_consistency.csv               # Batters LOMO player-match influence
│   ├── bowler_match_consistency.csv               # Bowlers LOMO player-match influence
│   ├── batter_sensitivity_analysis.csv            # Batters weight sensitivity sweeps
│   └── bowler_sensitivity_analysis.csv            # Bowlers weight sensitivity sweeps
├── leaderboards/                                  # Canonical Top 10 CSV outputs
│   ├── final_batter_leaderboard.csv               # Canonical Top 10 Batters Leaderboard
│   ├── final_bowler_leaderboard.csv               # Canonical Top 10 Bowlers Leaderboard
│   └── reconciled_20_players_phase_stats.csv      # Phase breakdown for all 20 players
├── presentations/                                 # Executive presentation deliverable
│   └── RR_2027_Auction_Presentation_Gate5_2.pptx  # 16-slide 16:9 widescreen presentation deck (Gate 5.2 Authoritative)
├── reports/                                       # Executive strategy report deliverable
│   ├── RR_2027_Auction_Strategy.pdf               # 9-page executive strategy PDF report
│   └── figures/                                   # High-resolution analytical figures
└── submission_manifest.csv                        # Cryptographic SHA-256 checksum manifest
```

### Interactive Dashboard Execution
To launch the interactive decision-support tool:
```bash
pip install -r final_submission/dashboard/requirements.txt
streamlit run final_submission/dashboard/app.py
```
*(The dashboard is supporting exploratory software; official competition judging is anchored in the canonical CSVs, PDF report, and PPTX presentation).*
