
# ============================================================
# PHASE 10 -- MACHINE LEARNING: FARE PREDICTION MODEL

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# ============================================================
# STEP 1 — CONNECT TO DATABASE & LOAD ALL 8 TABLES
# ============================================================
#  FILL IN YOUR PATH BELOW (use r"..." to avoid backslash errors)
conn = sqlite3.connect(r"C:\Users\vrutupatel\OneDrive\Desktop\uber project\UBER-DATA-ANALYSIS\DATA\uber_data.db3")

# Load all 8 tables
trips         = pd.read_sql("SELECT * FROM trips",         conn)
drivers       = pd.read_sql("SELECT * FROM drivers",       conn)
riders        = pd.read_sql("SELECT * FROM riders",        conn)
users         = pd.read_sql("SELECT * FROM users",         conn)
locations     = pd.read_sql("SELECT * FROM locations",     conn)
payments      = pd.read_sql("SELECT * FROM payments",      conn)
reviews       = pd.read_sql("SELECT * FROM reviews",       conn)
cancels       = pd.read_sql("SELECT * FROM cancellations", conn)

print(" All 8 tables loaded successfully!")


# ============================================================
print("\n" + "="*60)
print("PHASE 10 -- MACHINE LEARNING: FARE PREDICTION MODEL")
print("="*60)

from sklearn.model_selection import train_test_split
from sklearn.linear_model  import LinearRegression
from sklearn.ensemble      import RandomForestRegressor
from sklearn.metrics       import mean_absolute_error, r2_score

# ------------------------------------------------------------
# STEP 1 -- LOAD DATA
# ------------------------------------------------------------
print("\nStep 1 -- Loading trips_clean.csv")
print("-"*40)

# Load from the CSV saved in Phase 1
# FILL IN YOUR PATH if needed -- same as CSV_PATH at the top
df_ml = pd.read_csv("C:\\Users\\vrutupatel\\OneDrive\\Desktop\\uber project\\UBER-DATA-ANALYSIS\\DATA\\trips_clean.csv")
print(f"Rows loaded : {len(df_ml):,}")
print(f"Columns     : {list(df_ml.columns)}")

# ------------------------------------------------------------
# STEP 2 -- DEFINE FEATURES AND TARGET
# ------------------------------------------------------------
print("\nStep 2 -- Defining features (X) and target (y)")
print("-"*40)

features = ['distance_km', 'duration_mins', 'surge_multiplier',
            'hour', 'is_weekend']
target   = 'total_fare'

# Convert is_weekend to int (True/False -> 1/0) if needed
df_ml['is_weekend'] = df_ml['is_weekend'].astype(int)

# Drop rows with nulls in feature or target columns
df_ml = df_ml.dropna(subset=features + [target])

X = df_ml[features]
y = df_ml[target]

print(f"Features shape : {X.shape}")
print(f"Target shape   : {y.shape}")
print(f"Features used  : {features}")

# ------------------------------------------------------------
# STEP 3 -- TRAIN / TEST SPLIT
# ------------------------------------------------------------
print("\nStep 3 -- Train/Test Split (80/20)")
print("-"*40)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training rows : {len(X_train):,}")
print(f"Testing rows  : {len(X_test):,}")

# ------------------------------------------------------------
# STEP 4+5+6 -- LINEAR REGRESSION (BASELINE)
# ------------------------------------------------------------
print("\nStep 4-6 -- Linear Regression (Baseline Model)")
print("-"*40)

lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

mae_lr = round(mean_absolute_error(y_test, y_pred_lr), 2)
r2_lr  = round(r2_score(y_test, y_pred_lr), 4)

print(f"LINEAR REGRESSION RESULTS:")
print(f"   MAE (Mean Absolute Error) : ${mae_lr}")
print(f"   R2 Score                  : {r2_lr}")
print(f"   Interpretation: On average, predictions are off by ${mae_lr}")

# ------------------------------------------------------------
# STEP 7+8 -- RANDOM FOREST (MAIN MODEL)
# ------------------------------------------------------------
print("\nStep 7-8 -- Random Forest (Main Model)")
print("-"*40)

rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

mae_rf = round(mean_absolute_error(y_test, y_pred_rf), 2)
r2_rf  = round(r2_score(y_test, y_pred_rf), 4)

print(f"RANDOM FOREST RESULTS:")
print(f"   MAE (Mean Absolute Error) : ${mae_rf}")
print(f"   R2 Score                  : {r2_rf}")
print(f"   Interpretation: Model explains {round(r2_rf*100, 1)}% of fare variation")

# Model comparison
print(f"\nMODEL COMPARISON:")
print(f"   Linear Regression -- MAE: ${mae_lr}  R2: {r2_lr}")
print(f"   Random Forest     -- MAE: ${mae_rf}  R2: {r2_rf}")
winner = "Random Forest" if r2_rf > r2_lr else "Linear Regression"
print(f"   Winner: {winner}")

# Chart 1 -- Model comparison bar chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

models = ['Linear Regression', 'Random Forest']
maes   = [mae_lr, mae_rf]
r2s    = [r2_lr, r2_rf]

ax1.bar(models, maes, color=['#60a5fa', '#4ade80'], edgecolor='white', width=0.4)
ax1.set_title('MAE Comparison (lower is better)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Mean Absolute Error ($)', fontsize=10)
for bar, val in zip(ax1.patches, maes):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'${val}', ha='center', va='bottom', fontweight='bold', fontsize=11)

ax2.bar(models, r2s, color=['#60a5fa', '#4ade80'], edgecolor='white', width=0.4)
ax2.set_title('R2 Score Comparison (higher is better)', fontsize=12, fontweight='bold')
ax2.set_ylabel('R2 Score', fontsize=10)
ax2.set_ylim(0, 1.1)
for bar, val in zip(ax2.patches, r2s):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
             str(val), ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.suptitle('Linear Regression vs Random Forest', fontsize=14, fontweight='bold')
plt.tight_layout()
save("39_model_comparison.png")
plt.close()

# ------------------------------------------------------------
# STEP 9 -- FEATURE IMPORTANCE
# ------------------------------------------------------------
print("\nStep 9 -- Feature Importance")
print("-"*40)

importance = (
    pd.Series(rf.feature_importances_, index=features)
    .sort_values(ascending=True)
)
print(importance)

# Chart 2 -- Feature importance horizontal bar
plt.figure(figsize=(9, 5))
colors = ['#93c5fd', '#60a5fa', '#3b82f6', '#1d4ed8', '#1e3a8a']
bars = plt.barh(importance.index, importance.values,
                color=colors, edgecolor='white')
for bar, val in zip(bars, importance.values):
    plt.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height()/2,
             f'{val:.3f}', va='center', fontsize=10, fontweight='bold')
plt.title('Feature Importance -- What Drives Fare Prediction?',
          fontsize=14, fontweight='bold')
plt.xlabel('Importance Score', fontsize=11)
plt.ylabel('Feature', fontsize=11)
plt.tight_layout()
save("40_feature_importance.png")
plt.close()

# ------------------------------------------------------------
# STEP 10 -- ACTUAL VS PREDICTED SCATTER PLOT
# ------------------------------------------------------------
print("\nStep 10 -- Actual vs Predicted Chart")
print("-"*40)

plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_rf, alpha=0.25, color='steelblue', s=20)

# Perfect prediction diagonal line
min_val = min(y_test.min(), y_pred_rf.min())
max_val = max(y_test.max(), y_pred_rf.max())
plt.plot([min_val, max_val], [min_val, max_val],
         color='red', linestyle='dashed', linewidth=2,
         label='Perfect prediction line')

plt.title('Actual vs Predicted Fare -- Random Forest',
          fontsize=14, fontweight='bold')
plt.xlabel('Actual Fare ($)', fontsize=11)
plt.ylabel('Predicted Fare ($)', fontsize=11)
plt.legend(fontsize=10)
plt.tight_layout()
save("41_actual_vs_predicted.png")
plt.close()

# ------------------------------------------------------------
# FINAL SUMMARY
# ------------------------------------------------------------
print("\n" + "="*60)
print("PHASE 10 COMPLETE")
print("="*60)
print(f"\nFINAL MODEL RESULTS:")
print(f"   Best Model : Random Forest (100 trees)")
print(f"   MAE        : ${mae_rf}  (predictions off by ${mae_rf} on average)")
print(f"   R2 Score   : {r2_rf}  (model explains {round(r2_rf*100,1)}% of fare variation)")
print(f"   Top Feature: {importance.idxmax()}")
print(f"\nAll 41 charts saved to your images folder")
print("\n" + "="*60)
print("ALL PHASES COMPLETE -- EDA + ML DONE")
print("="*60)
print("""
BUSINESS INTERPRETATION (paste into Markdown cell):

The Random Forest model achieves an R2 score of {r2_rf}, meaning it
explains {pct}% of the variation in Uber fares. With a Mean Absolute
Error of ${mae_rf}, predictions are accurate to within a few dollars.

The most important predictor is distance_km, followed by
duration_mins and surge_multiplier. Hour and is_weekend have
smaller but meaningful effects on fare.

Business use case: This model could power Uber's upfront fare
estimate feature -- showing riders an accurate price before they
book. Accurate estimates reduce fare surprise at payment,
which is one of the top reasons riders cancel or leave bad reviews.
""".format(r2_rf=r2_rf, pct=round(r2_rf*100,1), mae_rf=mae_rf))









# ----------------------------------------------------------------------------------------------------------------------------------------------------
#
#  Export all tables to CSV for Power BI
import os

PROCESSED = r"C:\Users\vrutupatel\OneDrive\Desktop\uber project\UBER-DATA-ANALYSIS\DATA"
os.makedirs(PROCESSED, exist_ok=True)

completed.to_csv(f"{PROCESSED}\\trips_clean.csv",     index=False)
drivers.to_csv(  f"{PROCESSED}\\drivers.csv",          index=False)
riders.to_csv(   f"{PROCESSED}\\riders.csv",           index=False)
users.to_csv(    f"{PROCESSED}\\users.csv",             index=False)
locations.to_csv(f"{PROCESSED}\\locations.csv",        index=False)
payments.to_csv( f"{PROCESSED}\\payments.csv",          index=False)
reviews.to_csv(  f"{PROCESSED}\\reviews.csv",           index=False)
cancels.to_csv(  f"{PROCESSED}\\cancellations.csv",    index=False)

print("All 8 CSVs exported successfully!")

