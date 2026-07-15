# Python — EDA & Machine Learning

One script, `EDA_and_ML.py`, run top to bottom: it loads and cleans the raw data, works through 9 phases of exploratory analysis, then trains and evaluates a fare-prediction model. Each phase is self-contained, prints its own findings to the console, and saves its own charts — so the script doubles as a readable analysis log, not just code.

---

## What's inside

| Phase | Covers | Charts saved |
|---|---|---|
| 1 | Data loading (8 tables), null/duplicate checks, feature engineering (hour, weekday, wait time, fare/km, surge tier) | — |
| 2 | Revenue & trip performance — monthly trend, surge tiers, fare distribution, revenue by hour, Pareto analysis, cancellation revenue loss | 01–06 |
| 3 | Driver analysis — top earners, rating distribution, vehicle make, tenure vs. rating | 07–13 |
| 4 | Rider behaviour & retention — lifetime spend, segmentation, acquisition trend, first-to-second-trip gap | 14–18 |
| 5 | Location & zone analysis — top pickup zones, zone type, trip corridors, cancellation rate by zone | 19–23 |
| 6 | Cancellation deep dive — driver vs. rider split, reasons, rating bucket, hourly pattern, repeat cancellers | 24–27 |
| 7 | Payments & financial ops — method split, failure rate, settlement time | 28–31 |
| 8 | Reviews & satisfaction — rating direction, bottom drivers, fare vs. rating, review submission rate | 32–35 |
| 9 | Correlation analysis — full correlation matrix, strongest predictors of fare, weekend vs. weekday comparison | 36–38 |
| 10 | **Machine learning** — fare prediction with Linear Regression + Random Forest, feature importance, actual vs. predicted | 39–41 |

**Total output:** 41 charts saved to `/images`, `trips_clean.csv` (the cleaned dataset used for modeling in Phase 10), and full CSV exports of all 8 tables for downstream tools like the dashboard.

---

## Machine Learning (Phase 10)

**Goal:** predict `total_fare` from features known at or before trip start — the kind of thing that would power an "upfront price estimate" at booking.

**Features:** `distance_km`, `duration_mins`, `surge_multiplier`, `hour`, `is_weekend`
**Models:** Linear Regression (baseline) → Random Forest Regressor (100 trees)

| Model | MAE | R² |
|---|---|---|
| Linear Regression | $5.34 | 0.8924 |
| **Random Forest** | **$0.32** | **0.9987** |

Feature importance confirms distance (0.581) and surge (0.405) drive nearly all of the model's predictive power. See the main [README](../README.md#-machine-learning--fare-prediction) for the full interpretation — including why the R² is this high (fare in this dataset is close to a deterministic function of distance and surge, so the model essentially reverse-engineered the underlying pricing formula rather than overfitting).

---

## Running this script

Update the hardcoded paths near the top before running — `conn = sqlite3.connect(...)` (your database), `IMAGES_PATH` (where charts get saved), and the `trips_clean.csv` path used in Phase 10.

```bash
python EDA_and_ML.py
```

Runs start to finish in one pass — cleaning → EDA (phases 1–9) → ML (phase 10) — no need to run anything separately.

**Dependencies:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`
