# ============================================================
# UBER DATA ANALYSIS — Phase 1: Data Loading & Cleaning
# ============================================================

import sqlite3
import pandas as pd
import numpy as np

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
print(f"   Trips     : {len(trips):,} rows")
print(f"   Drivers   : {len(drivers):,} rows")
print(f"   Riders    : {len(riders):,} rows")
print(f"   Users     : {len(users):,} rows")
print(f"   Locations : {len(locations):,} rows")
print(f"   Payments  : {len(payments):,} rows")
print(f"   Reviews   : {len(reviews):,} rows")
print(f"   Cancels   : {len(cancels):,} rows")

# ============================================================
# STEP 2 — EXPLORE EACH TABLE
# ============================================================

all_tables = {
    "trips"     : trips,
    "drivers"   : drivers,
    "riders"    : riders,
    "users"     : users,
    "locations" : locations,
    "payments"  : payments,
    "reviews"   : reviews,
    "cancels"   : cancels,
}

print("\n" + "="*60)
print("TABLE SHAPES & COLUMN NAMES")
print("="*60)
for name, df in all_tables.items():
    print(f"\n {name.upper()} — {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"   Columns: {list(df.columns)}")

print("\n" + "="*60)
print("FIRST 5 ROWS — TRIPS TABLE")
print("="*60)
print(trips.head())

print("\n" + "="*60)
print("DATA TYPES — TRIPS TABLE")
print("="*60)
print(trips.dtypes)

# ============================================================
# STEP 3 — NULL VALUE CHECK ACROSS ALL TABLES
# ============================================================

print("\n" + "="*60)
print("NULL VALUES PER COLUMN")
print("="*60)
for name, df in all_tables.items():
    nulls = df.isnull().sum()
    null_pct = (df.isnull().mean() * 100).round(2)
    if nulls.sum() > 0:
        print(f"\n {name.upper()} — has nulls:")
        for col in df.columns:
            if nulls[col] > 0:
                print(f"   {col}: {nulls[col]} nulls ({null_pct[col]}%)")
    else:
        print(f"\n {name.upper()} — no nulls")

# ============================================================
# STEP 4 — DUPLICATE CHECK IN TRIPS TABLE
# ============================================================

print("\n" + "="*60)
print("DUPLICATE ROWS CHECK — TRIPS TABLE")
print("="*60)
dup_count = trips.duplicated().sum()
print(f"Duplicate rows in trips: {dup_count}")

if dup_count > 0:
    trips = trips.drop_duplicates()
    print(f" Duplicates removed. New shape: {trips.shape}")
else:
    print(" No duplicates found.")

# ============================================================
# STEP 5 — SUMMARY STATISTICS — TRIPS TABLE
# ============================================================

print("\n" + "="*60)
print("SUMMARY STATISTICS — TRIPS TABLE (numeric columns)")
print("="*60)
print(trips.describe().round(2))

# ============================================================
# STEP 6 — CONVERT DATE COLUMNS TO DATETIME
# ============================================================

trips['requested_at']  = pd.to_datetime(trips['requested_at'])
trips['started_at']    = pd.to_datetime(trips['started_at'])
trips['completed_at']  = pd.to_datetime(trips['completed_at'])

print("\n Date columns converted to datetime")
print(trips[['requested_at', 'started_at', 'completed_at']].dtypes)

# ============================================================
# STEP 7 — EXTRACT TIME FEATURES FROM requested_at
# ============================================================

trips['hour']        = trips['requested_at'].dt.hour
trips['day_of_week'] = trips['requested_at'].dt.day_name()
trips['month']       = trips['requested_at'].dt.to_period('M').astype(str)
trips['year']        = trips['requested_at'].dt.year
trips['is_weekend']  = trips['requested_at'].dt.dayofweek >= 5  # 5=Sat, 6=Sun

print("\n Time features created:")
print(trips[['requested_at', 'hour', 'day_of_week', 'month', 'is_weekend']].head())

# ============================================================
# STEP 8 — CALCULATE WAIT TIME IN MINUTES
# ============================================================

trips['wait_time_mins'] = (
    (trips['started_at'] - trips['requested_at'])
    .dt.total_seconds() / 60
)

print(f"\n wait_time_mins created")
print(f"   Average wait time: {trips['wait_time_mins'].mean():.1f} mins")
print(f"   Max wait time    : {trips['wait_time_mins'].max():.1f} mins")

# ============================================================
# STEP 9 — CALCULATE FARE PER KM
# ============================================================

# Replace 0 with NaN first to avoid division by zero
trips['fare_per_km'] = trips['total_fare'] / trips['distance_km'].replace(0, np.nan)

print(f"\n fare_per_km created")
print(f"   Average fare per km: ${trips['fare_per_km'].mean():.2f}")

# ============================================================
# STEP 10 — CREATE SURGE TIER COLUMN
# ============================================================

trips['surge_tier'] = pd.cut(
    trips['surge_multiplier'],
    bins=[0, 1.0, 1.5, 99],
    labels=['No Surge', 'Low Surge', 'High Surge'],
    include_lowest=True
)

print(f"\n surge_tier created")
print(trips['surge_tier'].value_counts())

# ============================================================
# STEP 11 — FILTER COMPLETED TRIPS ONLY
# ============================================================

completed = trips[trips['status'] == 'completed'].copy()

print(f"\n 'completed' DataFrame created")
print(f"   Total trips    : {len(trips):,}")
print(f"   Completed trips: {len(completed):,}")
print(f"   Cancelled trips: {len(trips[trips['status'] == 'cancelled']):,}")
print(f"   In-progress    : {len(trips[trips['status'] == 'in_progress']):,}")

# ============================================================
# STEP 12 — SAVE CLEANED DATA TO CSV
# ============================================================
# FILL IN YOUR SAVE PATH BELOW
completed.to_csv(r"C:\Users\vrutupatel\OneDrive\Desktop\uber project\UBER-DATA-ANALYSIS\NOTEBOOKS\trips_clean.csv", index=False)

print(f"\ntrips_clean.csv saved successfully!")
print(f"   Rows saved: {len(completed):,}")
print(f"   Columns   : {completed.shape[1]}")
print(f"\n{'='*60}")
print("PHASE 1 COMPLETE")
print("All 8 tables loaded, cleaned, and ready for analysis.")
print(f"{'='*60}")







#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------




# ============================================================
# UBER DATA ANALYSIS — Phase 2: Revenue & Trip Analysis
# ============================================================
#  Run Phase 1 code FIRST before running this file
# This file assumes: completed, trips, cancels are already loaded

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# FILL IN YOUR IMAGES FOLDER PATH
IMAGES_PATH = r"C:\Users\vrutupatel\OneDrive\Desktop\uber project\UBER-DATA-ANALYSIS\images"

# Helper: save chart
def save(filename):
    plt.savefig(f"{IMAGES_PATH}\\{filename}", dpi=150, bbox_inches='tight')
    print(f"    Saved: {filename}")

# ============================================================
# Q1 — CORE FINANCIAL KPIs
# ============================================================
print("=" * 60)
print("Q1 — CORE FINANCIAL KPIs")
print("=" * 60)

total_revenue   = completed['total_fare'].sum().round(2)
avg_fare        = completed['total_fare'].mean().round(2)
avg_rev_per_km  = (completed['total_fare'] / completed['distance_km'].replace(0, np.nan)).mean().round(2)

print(f"   Total Revenue      : ${total_revenue:,.2f}")
print(f"   Avg Fare per Trip  : ${avg_fare:,.2f}")
print(f"   Avg Revenue per KM : ${avg_rev_per_km:,.2f}")

# ============================================================
# Q2 — MONTHLY REVENUE & TRIP COUNT TREND
# ============================================================
print("\n" + "=" * 60)
print("Q2 — MONTHLY REVENUE & TRIP COUNT TREND")
print("=" * 60)

monthly = (
    completed
    .groupby('month')
    .agg(total_revenue=('total_fare', 'sum'),
         trip_count=('trip_id', 'count'))
    .reset_index()
)

print(monthly.head(10))

# --- CHART 1: Monthly Revenue Line Chart ---
fig, ax1 = plt.subplots(figsize=(14, 5))

ax1.plot(monthly['month'], monthly['total_revenue'],
         color='steelblue', linewidth=2.5, marker='o', markersize=5, label='Total Revenue')
ax1.set_xlabel('Month', fontsize=11)
ax1.set_ylabel('Total Revenue ($)', color='steelblue', fontsize=11)
ax1.tick_params(axis='x', rotation=45)
ax1.tick_params(axis='y', labelcolor='steelblue')

ax2 = ax1.twinx()
ax2.plot(monthly['month'], monthly['trip_count'],
         color='coral', linewidth=2, linestyle='--', marker='s', markersize=4, label='Trip Count')
ax2.set_ylabel('Trip Count', color='coral', fontsize=11)
ax2.tick_params(axis='y', labelcolor='coral')

plt.title('Monthly Revenue & Trip Count Trend (2019–2024)', fontsize=14, fontweight='bold', pad=15)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
plt.tight_layout()
save("01_monthly_revenue_trend.png")
plt.show()

# ============================================================
# Q3 — SURGE TIER ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("Q3 — SURGE TIER ANALYSIS")
print("=" * 60)

surge = (
    completed
    .groupby('surge_tier', observed=True)
    .agg(avg_fare=('total_fare', 'mean'),
         trip_count=('trip_id', 'count'))
    .reset_index()
)
surge['avg_fare'] = surge['avg_fare'].round(2)

print(surge)

# --- CHART 2: Surge Tier — Avg Fare Bar Chart ---
fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#4ade80', '#facc15', '#f87171']
bars = ax.bar(surge['surge_tier'], surge['avg_fare'], color=colors, edgecolor='white', width=0.5)

for bar, val in zip(bars, surge['avg_fare']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'${val:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_title('Average Fare by Surge Tier', fontsize=14, fontweight='bold')
ax.set_xlabel('Surge Tier', fontsize=11)
ax.set_ylabel('Average Fare ($)', fontsize=11)
ax.set_ylim(0, surge['avg_fare'].max() * 1.2)
plt.tight_layout()
save("02_surge_tier_avg_fare.png")
plt.show()

# --- CHART 3: Surge Tier — Box Plot (fare spread) ---
plt.figure(figsize=(8, 5))
sns.boxplot(data=completed, x='surge_tier', y='total_fare',
            order=['No Surge', 'Low Surge', 'High Surge'],
            palette=['#4ade80', '#facc15', '#f87171'])
plt.title('Fare Distribution by Surge Tier', fontsize=14, fontweight='bold')
plt.xlabel('Surge Tier', fontsize=11)
plt.ylabel('Total Fare ($)', fontsize=11)
plt.tight_layout()
save("03_surge_tier_boxplot.png")
plt.show()

# ============================================================
# Q4 — FARE DISTRIBUTION (5 BUCKETS)
# ============================================================
print("\n" + "=" * 60)
print("Q4 — FARE DISTRIBUTION BY BUCKET")
print("=" * 60)

completed['fare_bucket'] = pd.cut(
    completed['total_fare'],
    bins=[0, 10, 25, 50, 100, 99999],
    labels=['Under $10', '$10–$25', '$25–$50', '$50–$100', 'Over $100'],
    include_lowest=True
)

fare_dist = completed['fare_bucket'].value_counts().sort_index()
print(fare_dist)

# --- CHART 4: Fare Distribution Bar Chart ---
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(fare_dist.index, fare_dist.values,
              color='steelblue', edgecolor='white')

for bar, val in zip(bars, fare_dist.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
            f'{val:,}', ha='center', va='bottom', fontsize=10)

ax.set_title('Trip Count by Fare Bucket', fontsize=14, fontweight='bold')
ax.set_xlabel('Fare Range', fontsize=11)
ax.set_ylabel('Number of Trips', fontsize=11)
plt.tight_layout()
save("04_fare_bucket_distribution.png")
plt.show()

# --- CHART 5: Fare Histogram with Mean Line ---
plt.figure(figsize=(10, 5))
plt.hist(completed['total_fare'], bins=40, color='steelblue',
         edgecolor='white', alpha=0.85)
mean_fare = completed['total_fare'].mean()
plt.axvline(mean_fare, color='red', linestyle='dashed',
            linewidth=2, label=f'Mean: ${mean_fare:.2f}')
plt.title('Distribution of Trip Fares', fontsize=14, fontweight='bold')
plt.xlabel('Total Fare ($)', fontsize=11)
plt.ylabel('Number of Trips', fontsize=11)
plt.legend(fontsize=11)
plt.tight_layout()
save("05_fare_histogram.png")
plt.show()

# ============================================================
# Q5 — REVENUE & FARE BY HOUR (SIDE BY SIDE)
# ============================================================
print("\n" + "=" * 60)
print("Q5 — REVENUE & AVG FARE BY HOUR")
print("=" * 60)

hourly = (
    completed
    .groupby('hour')
    .agg(total_revenue=('total_fare', 'sum'),
         avg_fare=('total_fare', 'mean'))
    .reset_index()
)

# --- CHART 6: Two Side-by-Side Bar Charts ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

# Left: Total Revenue by Hour
ax1.bar(hourly['hour'], hourly['total_revenue'],
        color='steelblue', edgecolor='white')
ax1.set_title('Total Revenue by Hour of Day', fontsize=13, fontweight='bold')
ax1.set_xlabel('Hour (0 = Midnight, 12 = Noon)', fontsize=10)
ax1.set_ylabel('Total Revenue ($)', fontsize=10)
ax1.set_xticks(range(0, 24, 2))

# Right: Avg Fare by Hour
ax2.bar(hourly['hour'], hourly['avg_fare'],
        color='coral', edgecolor='white')
ax2.set_title('Average Fare by Hour of Day', fontsize=13, fontweight='bold')
ax2.set_xlabel('Hour (0 = Midnight, 12 = Noon)', fontsize=10)
ax2.set_ylabel('Average Fare ($)', fontsize=10)
ax2.set_xticks(range(0, 24, 2))

plt.suptitle('Revenue vs Average Fare by Hour', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
save("06_revenue_by_hour.png")
plt.show()

# ============================================================
# Q6 — TOP 10% TRIPS PARETO ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("Q6 — TOP 10% TRIPS — PARETO ANALYSIS")
print("=" * 60)
total_rev      = completed['total_fare'].sum()
threshold_90   = completed['total_fare'].quantile(0.9)
top10_rev      = completed[completed['total_fare'] >= threshold_90]['total_fare'].sum()
top10_pct      = (top10_rev / total_rev * 100).round(1)
top10_trip_pct = round(len(completed[completed['total_fare'] >= threshold_90]) / len(completed) * 100, 1)

print(f"   90th percentile fare threshold : ${threshold_90:.2f}")
print(f"   Top 10% trips revenue          : ${top10_rev:,.2f}")
print(f"   % of total revenue from top 10%: {top10_pct}%")
print(f"   (These {top10_trip_pct}% of trips generate {top10_pct}% of revenue)")

# ============================================================
# Q7 — REVENUE LOST FROM CANCELLATIONS
# ============================================================
print("\n" + "=" * 60)
print("Q7 — REVENUE LOST FROM CANCELLATIONS")
print("=" * 60)

 

cancelled_trips   = trips[trips['status'] == 'cancelled']
revenue_lost      = cancelled_trips['base_fare'].fillna(0).sum().round(2)
cancellation_rate = round(len(cancelled_trips) / len(trips) * 100, 1)

print(f"   Total cancelled trips    : {len(cancelled_trips):,}")
print(f"   Cancellation rate        : {cancellation_rate}%")
print(f"   Estimated revenue lost   : ${revenue_lost:,.2f}")

# Cancellation reasons breakdown (using cancels table)
cancel_reasons = cancels['reason'].value_counts().head(5)
print(f"\n   Top 5 cancellation reasons:")
print(cancel_reasons)

print("\n" + "=" * 60)
print("PHASE 2 COMPLETE ")
print(f"   6 charts saved to: {IMAGES_PATH}")
print("=" * 60)











#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------







# ============================================================
# PHASE 3 -- DRIVER ANALYSIS
# ============================================================
print("\n" + "="*60)
print("PHASE 3 -- DRIVER ANALYSIS")
print("="*60)

# ------------------------------------------------------------
# Q1 -- TOP 10 DRIVERS BY EARNINGS & TRIPS
# ------------------------------------------------------------
print("\nQ1 -- TOP 10 DRIVERS BY EARNINGS")
print("-"*40)

# Merge completed trips with drivers to get driver info
trips_drivers = completed.merge(drivers, on='driver_id', how='left')

# Merge with users to get driver names
trips_drivers = trips_drivers.merge(
    users[['user_id', 'name']],
    on='user_id',
    how='left'
)

# Group by driver
top_drivers = (
    trips_drivers
    .groupby(['driver_id', 'name'])
    .agg(total_earnings=('total_fare', 'sum'),
         total_trips=('trip_id', 'count'))
    .reset_index()
    .nlargest(10, 'total_earnings')
)
top_drivers['total_earnings'] = top_drivers['total_earnings'].round(2)
print(top_drivers[['name', 'total_earnings', 'total_trips']])

# Chart 1 -- Top 10 drivers horizontal bar
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top_drivers['name'], top_drivers['total_earnings'],
               color='steelblue', edgecolor='white')
for bar, val in zip(bars, top_drivers['total_earnings']):
    ax.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2,
            f'${val:,.0f}', va='center', fontsize=9)
ax.set_title('Top 10 Drivers by Total Earnings', fontsize=14, fontweight='bold')
ax.set_xlabel('Total Earnings ($)', fontsize=11)
ax.set_ylabel('Driver Name', fontsize=11)
ax.invert_yaxis()
plt.tight_layout()
save("07_top10_drivers_earnings.png")
plt.close()

# ------------------------------------------------------------
# Q2 -- DRIVER RATING DISTRIBUTION
# ------------------------------------------------------------
print("\nQ2 -- DRIVER RATING DISTRIBUTION")
print("-"*40)

drivers['rating_bucket'] = pd.cut(
    drivers['rating'],
    bins=[0, 3.5, 4.0, 4.5, 5.01],
    labels=['Below 3.5', '3.5 - 4.0', '4.0 - 4.5', '4.5 - 5.0'],
    include_lowest=True
)

rating_dist = drivers['rating_bucket'].value_counts().sort_index()
print(rating_dist)

# Chart 2 -- Driver rating distribution bar chart
fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#f87171', '#facc15', '#4ade80', '#22c55e']
bars = ax.bar(rating_dist.index, rating_dist.values,
              color=colors, edgecolor='white')
for bar, val in zip(bars, rating_dist.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            str(val), ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.set_title('Driver Rating Distribution', fontsize=14, fontweight='bold')
ax.set_xlabel('Rating Bucket', fontsize=11)
ax.set_ylabel('Number of Drivers', fontsize=11)
plt.tight_layout()
save("08_driver_rating_distribution.png")
plt.close()

# ------------------------------------------------------------
# Q3 -- DO HIGHER RATED DRIVERS EARN MORE?
# ------------------------------------------------------------
print("\nQ3 -- AVG FARE BY DRIVER RATING BUCKET")
print("-"*40)

# Merge completed trips with drivers rating bucket
trips_rating = completed.merge(
    drivers[['driver_id', 'rating', 'rating_bucket']],
    on='driver_id',
    how='left'
)

avg_fare_by_rating = (
    trips_rating
    .groupby('rating_bucket', observed=True)['total_fare']
    .mean()
    .round(2)
    .reset_index()
)
print(avg_fare_by_rating)

# Chart 3 -- Avg fare by rating bucket
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(avg_fare_by_rating['rating_bucket'],
              avg_fare_by_rating['total_fare'],
              color=['#f87171', '#facc15', '#4ade80', '#22c55e'],
              edgecolor='white')
for bar, val in zip(bars, avg_fare_by_rating['total_fare']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f'${val:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.set_title('Average Fare per Trip by Driver Rating', fontsize=14, fontweight='bold')
ax.set_xlabel('Driver Rating Bucket', fontsize=11)
ax.set_ylabel('Average Fare ($)', fontsize=11)
ax.set_ylim(0, avg_fare_by_rating['total_fare'].max() * 1.2)
plt.tight_layout()
save("09_avg_fare_by_driver_rating.png")
plt.close()

# ------------------------------------------------------------
# Q4 -- ACTIVE VS INACTIVE DRIVERS
# ------------------------------------------------------------
print("\nQ4 -- ACTIVE VS INACTIVE DRIVERS")
print("-"*40)

active_counts = drivers['is_active'].value_counts()
active_pct    = drivers['is_active'].value_counts(normalize=True).mul(100).round(1)

print(f"Active drivers   (1): {active_counts.get(1, 0)} ({active_pct.get(1, 0)}%)")
print(f"Inactive drivers (0): {active_counts.get(0, 0)} ({active_pct.get(0, 0)}%)")

# Chart 4 -- Pie chart
labels = ['Active', 'Inactive']
sizes  = [active_counts.get(1, 0), active_counts.get(0, 0)]
colors = ['#4ade80', '#f87171']

fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    sizes,
    labels=labels,
    colors=colors,
    autopct='%1.1f%%',
    startangle=90,
    textprops={'fontsize': 12}
)
for t in autotexts:
    t.set_fontweight('bold')
ax.set_title('Active vs Inactive Drivers', fontsize=14, fontweight='bold')
plt.tight_layout()
save("10_active_vs_inactive_drivers.png")
plt.close()

# ------------------------------------------------------------
# Q5 -- VEHICLE MAKE ANALYSIS
# ------------------------------------------------------------
print("\nQ5 -- VEHICLE MAKE ANALYSIS")
print("-"*40)

# Most common vehicle makes
vehicle_counts = drivers['vehicle_make'].value_counts()
print("Most common vehicle makes:")
print(vehicle_counts)

# Avg fare by vehicle make
trips_vehicle = completed.merge(
    drivers[['driver_id', 'vehicle_make']],
    on='driver_id',
    how='left'
)

avg_fare_vehicle = (
    trips_vehicle
    .groupby('vehicle_make')['total_fare']
    .mean()
    .round(2)
    .sort_values(ascending=False)
)
print("\nAvg fare by vehicle make:")
print(avg_fare_vehicle)

# Chart 5 -- Vehicle make frequency bar chart
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

# Left: vehicle count
ax1.bar(vehicle_counts.index, vehicle_counts.values,
        color='steelblue', edgecolor='white')
ax1.set_title('Number of Drivers by Vehicle Make', fontsize=13, fontweight='bold')
ax1.set_xlabel('Vehicle Make', fontsize=10)
ax1.set_ylabel('Number of Drivers', fontsize=10)
ax1.tick_params(axis='x', rotation=45)

# Right: avg fare by vehicle make
ax2.bar(avg_fare_vehicle.index, avg_fare_vehicle.values,
        color='coral', edgecolor='white')
ax2.set_title('Average Fare by Vehicle Make', fontsize=13, fontweight='bold')
ax2.set_xlabel('Vehicle Make', fontsize=10)
ax2.set_ylabel('Average Fare ($)', fontsize=10)
ax2.tick_params(axis='x', rotation=45)

plt.suptitle('Vehicle Make Analysis', fontsize=15, fontweight='bold')
plt.tight_layout()
save("11_vehicle_make_analysis.png")
plt.close()

# ------------------------------------------------------------
# Q6 -- TRIPS PER DRIVER PER MONTH
# ------------------------------------------------------------
print("\nQ6 -- TRIPS PER DRIVER PER MONTH")
print("-"*40)

trips_per_month = (
    completed
    .groupby(['driver_id', 'month'])['trip_id']
    .count()
    .reset_index()
    .rename(columns={'trip_id': 'monthly_trips'})
)

avg_monthly  = round(trips_per_month['monthly_trips'].mean(), 1)
min_monthly  = trips_per_month['monthly_trips'].min()
max_monthly  = trips_per_month['monthly_trips'].max()
med_monthly  = trips_per_month['monthly_trips'].median()

print(f"Average trips per driver per month : {avg_monthly}")
print(f"Minimum                            : {min_monthly}")
print(f"Maximum                            : {max_monthly}")
print(f"Median                             : {med_monthly}")

# Chart 6 -- Histogram of monthly trips per driver
plt.figure(figsize=(10, 5))
plt.hist(trips_per_month['monthly_trips'], bins=30,
         color='steelblue', edgecolor='white', alpha=0.85)
plt.axvline(avg_monthly, color='red', linestyle='dashed',
            linewidth=2, label=f'Mean: {avg_monthly}')
plt.title('Distribution of Monthly Trips per Driver', fontsize=14, fontweight='bold')
plt.xlabel('Trips per Month', fontsize=11)
plt.ylabel('Frequency', fontsize=11)
plt.legend(fontsize=11)
plt.tight_layout()
save("12_trips_per_driver_per_month.png")
plt.close()

# ------------------------------------------------------------
# Q7 -- DRIVER TENURE VS RATING
# ------------------------------------------------------------
print("\nQ7 -- DRIVER TENURE VS RATING")
print("-"*40)

drivers['join_date'] = pd.to_datetime(drivers['join_date'])
reference_date       = pd.Timestamp('2024-06-30')
drivers['tenure_days'] = (reference_date - drivers['join_date']).dt.days

print(f"Average driver tenure : {round(drivers['tenure_days'].mean())} days")
print(f"Longest tenure        : {drivers['tenure_days'].max()} days")
print(f"Shortest tenure       : {drivers['tenure_days'].min()} days")

# Chart 7 -- Scatter plot: tenure vs rating
plt.figure(figsize=(9, 5))
plt.scatter(drivers['tenure_days'], drivers['rating'],
            alpha=0.4, color='steelblue', s=40)
plt.title('Driver Tenure vs Rating', fontsize=14, fontweight='bold')
plt.xlabel('Days on Platform', fontsize=11)
plt.ylabel('Driver Rating', fontsize=11)
plt.tight_layout()
save("13_driver_tenure_vs_rating.png")
plt.close()

print("\n" + "="*60)
print("PHASE 3 COMPLETE")
print("7 charts saved to your images folder")
print("="*60)








#------------------------------------------------------------------------------------------------------------------------------------------------------------------------






















