# Rajasthan Royals IPL 2027 Analytics | Data Dictionary

This document provides a comprehensive specification of all tables, fields, data types, constraints, operational cricket rules, and derived analytical variables used across the official proprietary dataset.

---

## 1. Table Inventory

| Table Name | File Name | Row Count | Column Count | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Competitions** | `competitions.csv` | 141 | 4 | Metadata for tournaments and series across IPL and T20Is (2022–2026). |
| **Matches** | `matches.csv` | 883 | 22 | Match-level metadata including dates, venues, toss, DLS targets, knockouts, and results. |
| **Teams** | `teams.csv` | 353 | 3 | Tournament-to-team identity mappings. |
| **Playing XI** | `playing_eleven.csv` | 28,381 | 9 | Match-level player rosters, batting orders, captaincy, wicketkeepers, and impact player tags. |
| **Player Mapping** | `competition_team_player_mapping.csv` | 6,413 | 6 | Tournament rosters mapping player IDs to names, teams, and competitions. |
| **Ball by Ball** | `ball_by_ball.csv` | 200,999 | 33 | Delivery-level tracking including speeds, styles, strokes, pitch zones, runs, dismissals, and extras. |

---

## 2. Table Schemas & Column Definitions

### 2.1 `competitions.csv`

| Column | Type | Null Count | Description & Units |
| :--- | :--- | :--- | :--- |
| `comp_id` | Integer | 0 | Unique integer identifier for the competition/tournament. Primary Key. |
| `comp_name` | String | 0 | Full name of the tournament (e.g., `IPL 2022`, `IPL 2026`, `Asia Cup 2025`). |
| `match_format` | String | 0 | Format of the competition: `T20` (domestic leagues like IPL) or `T20I` (international). |
| `season` | String | 0 | Season label (e.g., `2022`, `2022/23`, `2024`, `2026`). |

---

### 2.2 `matches.csv`

| Column | Type | Null Count | Description & Units |
| :--- | :--- | :--- | :--- |
| `match_id` | Integer | 0 | Unique integer identifier for each match. Primary Key. |
| `comp_id` | Integer | 0 | Foreign key referencing `competitions.comp_id`. |
| `match_number` | Integer | 0 | Sequence number of the match within the competition. |
| `match_date` | Date (YYYY-MM-DD) | 0 | Date the match took place. Range: `2022-01-22` to `2026-11-01`. |
| `stage` | String | 0 | Tournament phase: `League`, `Final`, `Qualifier`, `Super 4`, `Eliminator`, `Semi Final`, `Others`. |
| `venue_id` | Integer | 0 | Identifier for the cricket stadium/ground. |
| `venue_country` | String | 0 | Host country of the venue (e.g., `India`, `Australia`, `UAE`, `West Indies`). |
| `home_team_id` | Integer | 0 | Team ID of the designated home team. |
| `home_team` | String | 0 | Full name of the home team. |
| `away_team_id` | Integer | 0 | Team ID of the designated away team. |
| `away_team` | String | 0 | Full name of the away team. |
| `home_team_captain_id` | Integer | 0 | Player ID of the home team captain. |
| `away_team_captain_id` | Integer | 0 | Player ID of the away team captain. |
| `toss_win_team_id` | Integer | 0 | Team ID of the team that won the coin toss. |
| `toss_decision` | String | 0 | Decision made by toss winner: `field` or `bat`. |
| `knock_out` | Integer | 0 | Indicator for knockout fixture: `1` if playoff/knockout, `0` if league/group stage. |
| `revised_target` | Float | 851 | Revised target score if DLS method applied (null for standard matches). |
| `first_inn_revised_overs` | Float | 857 | Revised scheduled overs for innings 1 (null if standard 20 overs). |
| `second_inn_revised_overs` | Float | 851 | Revised scheduled overs for innings 2 (null if standard 20 overs). |
| `win_team_id` | Float | 16 | Team ID of match winner (null for 16 abandoned/no-result fixtures). |
| `win_margin` | Float | 16 | Margin of victory in runs or wickets. |
| `result` | String | 0 | Result description (e.g., `Won by 5 wickets`, `Won by 14 runs`, `Tie`, `No result`). |

---

### 2.3 `teams.csv`

| Column | Type | Null Count | Description & Units |
| :--- | :--- | :--- | :--- |
| `comp_id` | Integer | 0 | Foreign key referencing `competitions.comp_id`. |
| `team_id` | Integer | 0 | Unique integer identifier for the franchise or national team. |
| `team_name` | String | 0 | Official full team name (e.g., `Rajasthan Royals`, `Mumbai Indians`). |

---

### 2.4 `playing_eleven.csv`

| Column | Type | Null Count | Description & Units |
| :--- | :--- | :--- | :--- |
| `match_id` | Integer | 0 | Foreign key referencing `matches.match_id`. |
| `team_id` | Integer | 0 | Foreign key referencing `teams.team_id`. |
| `player_id` | Integer | 0 | Unique player identifier. |
| `player_name` | String | 0 | Official player name. |
| `batting_order` | Integer | 0 | Designated batting order slot (1 through 11). |
| `is_captain` | Boolean | 0 | Team captain flag (`True` / `False`). |
| `is_keeper` | Boolean | 0 | Wicketkeeper flag (`True` / `False`). |
| `playing_role` | String | 1,023 | Roster role: `Batter`, `Bowler`, `Allrounder`, `Wicketkeeper`. |
| `is_impact` | Boolean | 0 | IPL Impact Player substitution flag (`True` / `False`). |

---

### 2.5 `competition_team_player_mapping.csv`

| Column | Type | Null Count | Description & Units |
| :--- | :--- | :--- | :--- |
| `comp_id` | Integer | 0 | Foreign key referencing `competitions.comp_id`. |
| `comp_name` | String | 0 | Tournament name. |
| `team_id` | Integer | 0 | Foreign key referencing `teams.team_id`. |
| `team_name` | String | 0 | Team name. |
| `player_id` | Integer | 0 | Player identifier. |
| `player_name` | String | 0 | Player name. |

---

### 2.6 `ball_by_ball.csv`

| Column | Type | Null Count | Description & Detailed Cricket Nuances |
| :--- | :--- | :--- | :--- |
| `match_id` | Integer | 0 | Foreign key referencing `matches.match_id`. |
| `innings` | Integer | 0 | Innings index: `1` (First innings), `2` (Second innings), `3` & `4` (Super Overs). |
| `overid` | Integer | 0 | Over number: 1-indexed from `1` to `20`. |
| `over_ball_num` | Integer | 0 | Ball sequence within the over (1 to 13, including re-bowled extras). |
| `innings_ball_num` | Integer | 0 | Cumulative ball sequence within the innings. |
| `batting_team_id` | Integer | 0 | Team ID of the batting team. |
| `bowling_team_id` | Integer | 0 | Team ID of the bowling team. |
| `striker_id` | Integer | 0 | Player ID of the batter facing the delivery. |
| `striker_name` | String | 0 | Batter name. |
| `non_striker_id` | Integer | 0 | Player ID of the batter at the non-striker's end. |
| `non_striker_name`| String | 0 | Non-striker name. |
| `bowler_id` | Integer | 0 | Player ID of the bowler delivering the ball. |
| `bowler_name` | String | 0 | Bowler name. |
| `batting_type` | String | 0 | Batter stance: `Right Hand Bat` or `Left Hand Bat`. |
| `bowling_type` | String | 0 | Detailed bowling action (e.g., `Right-arm fast-medium`, `Left-arm orthodox`). |
| `batting_order` | Integer | 0 | Batter's actual entry slot in the innings. |
| `runs` | Integer | 0 | Runs scored off the bat. Credited to batter. Overstep runs off bat are here. |
| `is_four` | Boolean | 0 | Delivery resulted in a boundary four off the bat. |
| `is_six` | Boolean | 0 | Delivery resulted in a six over the boundary off the bat. |
| `is_wicket` | Boolean | 0 | A dismissal occurred on this delivery. |
| `dismissal_type_id` | Float | 190,118 | Identifier code for dismissal. |
| `dismissal_type` | String | 190,118 | Dismissal mode: `Caught`, `Bowled`, `LBW`, `RunOut`, `Stump`, `Hit Wicket`, `Retire Out`, `Obstructing the field`. |
| `dismissed_player_id` | Float | 190,118 | Player ID of the batter dismissed on the delivery. |
| `extras_type` | String | 189,167 | Extra category: `wide`, `legbyes`, `Overstep` (no-ball), `byes`, `other`, `Penalty`. |
| `extras1_runs` | Integer | 0 | Penalty/extra runs conceded: 1 for wide/no-ball, or bye/legbye count. |
| `extras_2_runs` | Integer | 0 | Additional physical runs taken during an extra event (e.g. bye off no-ball). |
| `pace_or_spin` | String | 0 | High-level categorization: `Pace` or `Spin`. |
| `bowl_speed` | Integer | 0 | Delivery release speed in km/h (0 if unmeasured or spin). |
| `stroke` | String | 37 | Batting shot type (e.g., `Pull`, `Cover Drive`, `Defensive`, `Cut`, `Flick`, `Scoop`). |
| `delivery_style`| String | 2 | Pitch movement / seam trajectory (e.g., `Seamed In`, `Orthodox`, `Googly`, `Inswing`, `Off Cutter`). |
| `over_or_around`| String | 0 | Bowler delivery angle relative to stumps: `Over` or `Around`. |
| `on_or_off` | String | 0 | Pitch line: `Off-side` or `On-side`. |
| `delivery_ist_time`| Timestamp | 0 | Delivery timestamp in IST (`YYYY-MM-DD HH:MM:SS UTC`). |

---

## 3. Standard Cricket Calculation Rules Implemented

1. **Batter Runs (`runs`) & Balls Faced (`tot_balls`, `high_balls`)**:
   - `runs` represents physical runs struck off the bat, credited to the striker.
   - Strike Rate = `(Total Batter Runs / Legal Balls Faced) * 100`.
   - **Wide Deliveries**: A wide (`extras_type == 'wide'`) is NOT a legal delivery and does **NOT** count as a ball faced.
   - **No-Balls / Oversteps (Analytical Convention vs. Conventional Scorekeeping)**:
     - *Project Analytical Implementation*: In this codebase (`01_build_match_context.py` and `run_independent_ranking_engines.py`), batter balls faced is calculated strictly as the sum of **legal deliveries faced** (`is_legal_ball`), where `is_legal_ball = ~(is_wide | is_overstep)`. Consequently, overstep no-balls are **excluded from the balls-faced denominator**. Any runs struck off the bat on an overstep are credited to the batter's run tally, but the delivery itself does not increment balls faced.
     - *Conventional Cricket Scorekeeping Difference*: In standard cricket scorekeeping (e.g., Wisden, ESPNcricinfo), a no-ball bowled to a batter is conventionally recorded as a ball faced. The project's pipeline deliberately evaluates strike rate per *legal delivery faced* to preserve dimensional symmetry with bowling over progression and economy calculations.
     - *MCC Law 21 Distinction*: MCC Law 21 defines what constitutes a no-ball and specifies that it does not count as one of the 6 valid balls of an over for over progression; it does not govern batting strike-rate conventions. Excluded no-balls from balls faced is strictly an internal analytical convention of this project, not an MCC Law 21 requirement.

2. **Bowler Runs Conceded (`bowler_runs_conceded`) & Bowler Legal Balls**:
   - Conceded = `runs` + `extras1_runs` + `extras_2_runs` (only when `extras_type` is `wide` or `overstep`).
   - Byes (`byes`) and leg-byes (`legbyes`) are team extras; they are **never** charged to the bowler.
   - Bowler Economy Rate = `(Bowler Runs Conceded / Bowler Legal Balls) * 6.0`.
   - Bowler Legal Balls = sum of `is_legal_ball` bowled by the bowler (excludes wides and no-balls).

3. **Bowler Wickets (`is_bowler_wicket`)**:
   - A bowler is credited with a wicket only for: `Bowled`, `Caught`, `LBW`, `Stump`, and `Hit Wicket`.
   - A bowler is **strictly not credited** with wickets for: `RunOut`, `Retire Out`, or `Obstructing the field`.

4. **Legal Deliveries (`is_legal_ball`)**:
   - Deliveries where `extras_type` is NOT in `['wide', 'overstep']`.
   - Each completed over has exactly 6 legal deliveries.

---

## 4. Derived Match-Context & PRI Variables

In `match_context_ball_by_ball.parquet` and production scripts:

| Variable Name | Type | Value Range | Definition & Implementation Details |
| :--- | :--- | :--- | :--- |
| `is_legal_ball` | Boolean | `True` / `False` | `~(is_wide | is_overstep)`. Indicates an official legal delivery counting toward the 6-ball over. |
| `team_runs_on_ball` | Integer | $\ge 0$ | Total runs added to team score on delivery (`runs + extras1_runs + extras_2_runs`). |
| `cum_team_runs_before` | Integer | $\ge 0$ | Cumulative innings score before the current delivery. |
| `cum_wickets_before` | Integer | 0 to 10 | Cumulative wickets lost before the current delivery. |
| `wickets_in_hand` | Integer | 0 to 10 | Wickets remaining before delivery: $10 - \text{cum\_wickets\_before}$. |
| `legal_balls_remaining` | Integer | 0 to 120 | Scheduled legal balls minus legal balls bowled before delivery. |
| `crr_before` | Float | $\ge 0.0$ | Current Run Rate before delivery: $(\text{runs} / \text{legal balls}) \times 6.0$. |
| `target` | Float | $\ge 0.0$ | Target runs to win in innings 2 (revised target if DLS, else innings 1 total + 1). |
| `runs_needed_before` | Float | $\ge 0.0$ | Runs required to win before delivery in innings 2 ($\max(0, \text{target} - \text{score})$). |
| `rrr_before` | Float | $\ge 0.0$ | Required Run Rate before delivery: $(\text{runs needed} / \text{balls remaining}) \times 6.0$. |
| `match_phase` | String | Categorical | `Powerplay` (overs 1–6), `Middle` (overs 7–15), `Death` (overs 16–20), `SuperOver` (innings 3 & 4). |
| `comp_par_total` | Float | $\approx 165–185$ | Macro seasonal average 1st-innings score across completed 20-over matches in that competition/season. |
| `cross_exp_runs_rem` | Float | $\ge 0.0$ | Expected runs remaining in innings 1 from (over, wickets lost) grid via 5-fold match cross-fitting. |
| `situational_pressure` | Float | $[0.05, 1.00]$ | Continuous situational leverage score $S_t$. Bounded continuous logistic formulation. |
| `is_high_pressure` | Boolean | `True` / `False` | High-pressure classification indicator: $S_t \ge 0.65$. |
| `match_stakes` | Float | $1.00$ to $1.25$ | Upstream tournament importance factor. **Experimental only; unused in production rankings.** |

---

## 5. Dataset Populations & Eligibility Discipline

### 5.1 Dataset Population Totals
- **Combined Dataset Universe**:
  - `matches.csv`: **883 scheduled matches** (482 T20I, 401 T20 of which 371 are IPL).
  - `ball_by_ball.csv`: **867 played matches** with delivery data (16 matches abandoned without a ball bowled: $883 - 16 = 867$), containing **200,999 delivery records**.
- **IPL Production Universe (2022–2026)**:
  - **371 scheduled IPL matches**.
  - **4 rain-abandoned matches** with no balls bowled.
  - **367 played IPL matches** with ball-by-ball delivery records.
  - **87,687 IPL delivery records**.
  - **83,878 IPL legal deliveries** (`is_legal_ball == True`).
- **IPL High-Pressure Population ($S_t \ge 0.65$)**:
  - **15,318 high-pressure delivery records** ($17.47\%$ of IPL delivery records).
  - **14,475 high-pressure legal deliveries** ($17.26\%$ of IPL legal deliveries).

### 5.2 Eligibility Cutoffs vs. Shrinkage Parameters
- **Batter Eligibility Threshold**: Minimum **60 high-pressure legal balls faced** in IPL 2022–2026 ($\rightarrow$ **78 qualified batters**).
- **Bowler Eligibility Threshold**: Minimum **75 high-pressure legal balls bowled** in IPL 2022–2026 ($\rightarrow$ **68 qualified bowlers**).
- **Shrinkage Parameters (Empirical Bayes Weighting)**:
  - Batter Strike Rate: Empirical Prior = **140.0 SR**, Shrinkage Weight $M = 50.0$ legal balls.
  - Batting Average: Empirical Prior = **22.0 runs/out**, Shrinkage Weight $M = 5.0$ dismissals.
  - Bowling Economy: Empirical Prior = **8.60 RPO**, Shrinkage Weight $M = 60.0$ legal balls.
  - Bowling Wicket Rate: Empirical Prior = **5.50%**, Shrinkage Weight $M = 60.0$ legal balls.
