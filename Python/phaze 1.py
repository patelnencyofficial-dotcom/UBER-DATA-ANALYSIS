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











# ============================================================
# PHASE 4 -- RIDER BEHAVIOUR & RETENTION
# ============================================================
print("\n" + "="*60)
print("PHASE 4 -- RIDER BEHAVIOUR & RETENTION")
print("="*60)

# ------------------------------------------------------------
# Q1 -- TOP 10 RIDERS BY LIFETIME SPEND
# ------------------------------------------------------------
print("\nQ1 -- TOP 10 RIDERS BY LIFETIME SPEND")
print("-"*40)

trips_riders = completed.merge(riders, on='rider_id', how='left')
trips_riders = trips_riders.merge(
    users[['user_id', 'name', 'city']],
    on='user_id',
    how='left'
)

top_riders = (
    trips_riders
    .groupby(['rider_id', 'name'])
    .agg(total_spend=('total_fare', 'sum'),
         total_trips=('trip_id', 'count'))
    .reset_index()
    .nlargest(10, 'total_spend')
)
top_riders['total_spend'] = top_riders['total_spend'].round(2)
print(top_riders[['name', 'total_spend', 'total_trips']])

# Chart 1 -- Top 10 riders horizontal bar
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top_riders['name'], top_riders['total_spend'],
               color='steelblue', edgecolor='white')
for bar, val in zip(bars, top_riders['total_spend']):
    ax.text(bar.get_width() + 20, bar.get_y() + bar.get_height()/2,
            f'${val:,.0f}', va='center', fontsize=9)
ax.set_title('Top 10 Riders by Lifetime Spend', fontsize=14, fontweight='bold')
ax.set_xlabel('Total Spend ($)', fontsize=11)
ax.set_ylabel('Rider Name', fontsize=11)
ax.invert_yaxis()
plt.tight_layout()
save("14_top10_riders_spend.png")
plt.close()

# ------------------------------------------------------------
# Q2 -- RIDER SEGMENTATION BY TRIP COUNT
# ------------------------------------------------------------
print("\nQ2 -- RIDER SEGMENTATION")
print("-"*40)

rider_trip_counts = (
    completed
    .groupby('rider_id')['trip_id']
    .count()
    .reset_index()
    .rename(columns={'trip_id': 'trip_count'})
)

rider_trip_counts['segment'] = pd.cut(
    rider_trip_counts['trip_count'],
    bins=[0, 5, 20, 99999],
    labels=['Low (1-5)', 'Medium (6-20)', 'High (20+)'],
    include_lowest=True
)

rider_revenue = (
    completed
    .groupby('rider_id')['total_fare']
    .sum()
    .reset_index()
    .rename(columns={'total_fare': 'total_spend'})
)

rider_segments = rider_trip_counts.merge(rider_revenue, on='rider_id', how='left')

total_rev   = rider_segments['total_spend'].sum()
segment_rev = (
    rider_segments
    .groupby('segment', observed=True)['total_spend']
    .sum()
    .reset_index()
)
segment_rev['revenue_pct'] = (segment_rev['total_spend'] / total_rev * 100).round(1)
segment_rev['rider_count'] = (
    rider_segments
    .groupby('segment', observed=True)['rider_id']
    .count()
    .values
)
print(segment_rev)

# Chart 2 -- Revenue % by segment
fig, ax = plt.subplots(figsize=(8, 5))
colors = ['#93c5fd', '#3b82f6', '#1d4ed8']
bars = ax.bar(segment_rev['segment'], segment_rev['revenue_pct'],
              color=colors, edgecolor='white')
for bar, val in zip(bars, segment_rev['revenue_pct']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{val}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
ax.set_title('Revenue Contribution by Rider Segment', fontsize=14, fontweight='bold')
ax.set_xlabel('Rider Segment', fontsize=11)
ax.set_ylabel('% of Total Revenue', fontsize=11)
ax.set_ylim(0, segment_rev['revenue_pct'].max() * 1.2)
plt.tight_layout()
save("15_revenue_by_rider_segment.png")
plt.close()

# ------------------------------------------------------------
# Q3 -- RIDER RATING DISTRIBUTION
# ------------------------------------------------------------
print("\nQ3 -- RIDER RATING DISTRIBUTION")
print("-"*40)

below_4     = (riders['rating'] < 4.0).sum()
below_4_pct = round(below_4 / len(riders) * 100, 1)

print(f"Riders with rating below 4.0 : {below_4} ({below_4_pct}%)")
print(f"Average rider rating         : {riders['rating'].mean():.2f}")

# Chart 3 -- Rider rating histogram
plt.figure(figsize=(9, 5))
plt.hist(riders['rating'], bins=20, color='steelblue',
         edgecolor='white', alpha=0.85)
plt.axvline(4.0, color='red', linestyle='dashed',
            linewidth=2, label='Rating = 4.0 threshold')
plt.axvline(riders['rating'].mean(), color='orange', linestyle='dashed',
            linewidth=2, label=f"Mean: {riders['rating'].mean():.2f}")
plt.title('Rider Rating Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Rating', fontsize=11)
plt.ylabel('Number of Riders', fontsize=11)
plt.legend(fontsize=10)
plt.tight_layout()
save("16_rider_rating_distribution.png")
plt.close()

# ------------------------------------------------------------
# Q4 -- NEW RIDER ACQUISITION TREND
# ------------------------------------------------------------
print("\nQ4 -- NEW RIDER ACQUISITION TREND")
print("-"*40)

riders_users = riders.merge(
    users[['user_id', 'date_joined', 'city']],
    on='user_id',
    how='left'
)
riders_users['date_joined'] = pd.to_datetime(riders_users['date_joined'])
riders_users['join_month']  = riders_users['date_joined'].dt.to_period('M').astype(str)

monthly_new_riders = (
    riders_users
    .groupby('join_month')['rider_id']
    .count()
    .reset_index()
    .rename(columns={'rider_id': 'new_riders'})
)
print(monthly_new_riders.head(10))

# Chart 4 -- New rider acquisition line chart
plt.figure(figsize=(14, 5))
plt.plot(monthly_new_riders['join_month'], monthly_new_riders['new_riders'],
         color='steelblue', linewidth=2.5, marker='o', markersize=5)
plt.title('New Rider Acquisitions by Month', fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=11)
plt.ylabel('New Riders Joined', fontsize=11)
plt.xticks(rotation=45)
plt.tight_layout()
save("17_new_rider_acquisition.png")
plt.close()

# ------------------------------------------------------------
# Q5 -- FIRST TO SECOND TRIP GAP
# ------------------------------------------------------------
print("\nQ5 -- FIRST TO SECOND TRIP GAP")
print("-"*40)

sorted_trips = completed[['rider_id', 'requested_at']].sort_values(
    ['rider_id', 'requested_at']
)

first_trip = (
    sorted_trips
    .groupby('rider_id')
    .nth(0)
    .reset_index()
    .rename(columns={'requested_at': 'first_trip'})
)

second_trip = (
    sorted_trips
    .groupby('rider_id')
    .nth(1)
    .reset_index()
    .rename(columns={'requested_at': 'second_trip'})
)

retention    = first_trip.merge(second_trip, on='rider_id', how='inner')
retention['gap_days'] = (retention['second_trip'] - retention['first_trip']).dt.days

avg_gap    = round(retention['gap_days'].mean(), 1)
median_gap = round(retention['gap_days'].median(), 1)

print(f"Riders who took a 2nd trip : {len(retention):,}")
print(f"Riders with only 1 trip    : {len(first_trip) - len(retention):,}")
print(f"Average gap (days)         : {avg_gap}")
print(f"Median gap (days)          : {median_gap}")

# ------------------------------------------------------------
# Q6 -- AVG SPEND PER TRIP BY CITY
# ------------------------------------------------------------
print("\nQ6 -- AVG SPEND PER TRIP BY CITY")
print("-"*40)

trips_city = completed.merge(riders, on='rider_id', how='left')
trips_city = trips_city.merge(
    users[['user_id', 'city']],
    on='user_id',
    how='left'
)

avg_spend_city = (
    trips_city
    .groupby('city')['total_fare']
    .mean()
    .round(2)
    .sort_values(ascending=True)
    .reset_index()
)
print(avg_spend_city)

# Chart 5 -- Avg spend by city horizontal bar
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(avg_spend_city['city'], avg_spend_city['total_fare'],
               color='steelblue', edgecolor='white')
for bar, val in zip(bars, avg_spend_city['total_fare']):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
            f'${val:.2f}', va='center', fontsize=10, fontweight='bold')
ax.set_title('Average Fare per Trip by City', fontsize=14, fontweight='bold')
ax.set_xlabel('Average Fare ($)', fontsize=11)
ax.set_ylabel('City', fontsize=11)
ax.set_xlim(0, avg_spend_city['total_fare'].max() * 1.15)
plt.tight_layout()
save("18_avg_fare_by_city.png")
plt.close()

print("\n" + "="*60)
print("PHASE 4 COMPLETE")
print("5 charts saved to your images folder")
print("="*60)






#----------------------------------------------------------------------------------------------------------------------------------------------------------------------










# ============================================================
# PHASE 5 -- LOCATION & ZONE ANALYSIS
# ============================================================
print("\n" + "="*60)
print("PHASE 5 -- LOCATION & ZONE ANALYSIS")
print("="*60)

# ------------------------------------------------------------
# Q1 -- TOP PICKUP ZONES BY REVENUE
# ------------------------------------------------------------
print("\nQ1 -- TOP PICKUP ZONES BY REVENUE")
print("-"*40)

trips_zones = completed.merge(
    locations[['location_id', 'zone_name', 'city', 'zone_type']],
    left_on='pickup_location_id',
    right_on='location_id',
    how='left'
)

top_pickup_zones = (
    trips_zones
    .groupby('zone_name')
    .agg(total_revenue=('total_fare', 'sum'),
         trip_count=('trip_id', 'count'))
    .reset_index()
    .nlargest(10, 'total_revenue')
    .sort_values('total_revenue', ascending=True)
)
print(top_pickup_zones)

# Chart 1 -- Top 10 pickup zones horizontal bar
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top_pickup_zones['zone_name'], top_pickup_zones['total_revenue'],
               color='steelblue', edgecolor='white')
for bar, val in zip(bars, top_pickup_zones['total_revenue']):
    ax.text(bar.get_width() + 100, bar.get_y() + bar.get_height()/2,
            f'${val:,.0f}', va='center', fontsize=9)
ax.set_title('Top 10 Pickup Zones by Total Revenue', fontsize=14, fontweight='bold')
ax.set_xlabel('Total Revenue ($)', fontsize=11)
ax.set_ylabel('Zone', fontsize=11)
plt.tight_layout()
save("19_top_pickup_zones_revenue.png")
plt.close()

# ------------------------------------------------------------
# Q2 -- AVG FARE BY ZONE TYPE
# ------------------------------------------------------------
print("\nQ2 -- AVG FARE BY ZONE TYPE")
print("-"*40)

avg_fare_zone = (
    trips_zones
    .groupby('zone_type')['total_fare']
    .mean()
    .round(2)
    .reset_index()
    .sort_values('total_fare', ascending=False)
)
print(avg_fare_zone)

# Chart 2 -- Avg fare by zone type (seaborn)
plt.figure(figsize=(8, 5))
sns.barplot(data=avg_fare_zone, x='zone_type', y='total_fare',
            palette='Blues_d')
plt.title('Average Fare by Zone Type', fontsize=14, fontweight='bold')
plt.xlabel('Zone Type', fontsize=11)
plt.ylabel('Average Fare ($)', fontsize=11)
plt.tight_layout()
save("20_avg_fare_by_zone_type.png")
plt.close()

# ------------------------------------------------------------
# Q3 -- TOP 10 TRIP CORRIDORS
# ------------------------------------------------------------
print("\nQ3 -- TOP 10 TRIP CORRIDORS")
print("-"*40)

# Merge for pickup zone name
corridors = completed.merge(
    locations[['location_id', 'zone_name']].rename(
        columns={'location_id': 'pickup_location_id', 'zone_name': 'pickup_zone'}),
    on='pickup_location_id', how='left'
)

# Merge for dropoff zone name
corridors = corridors.merge(
    locations[['location_id', 'zone_name']].rename(
        columns={'location_id': 'dropoff_location_id', 'zone_name': 'dropoff_zone'}),
    on='dropoff_location_id', how='left'
)

top_corridors = (
    corridors
    .groupby(['pickup_zone', 'dropoff_zone'])['trip_id']
    .count()
    .reset_index()
    .rename(columns={'trip_id': 'trip_count'})
    .nlargest(10, 'trip_count')
    .sort_values('trip_count', ascending=True)
)
top_corridors['corridor'] = top_corridors['pickup_zone'] + ' --> ' + top_corridors['dropoff_zone']
print(top_corridors[['corridor', 'trip_count']])

# Chart 3 -- Top corridors horizontal bar
fig, ax = plt.subplots(figsize=(12, 6))
ax.barh(top_corridors['corridor'], top_corridors['trip_count'],
        color='steelblue', edgecolor='white')
ax.set_title('Top 10 Most Common Trip Corridors', fontsize=14, fontweight='bold')
ax.set_xlabel('Number of Trips', fontsize=11)
ax.set_ylabel('Corridor (Pickup --> Dropoff)', fontsize=11)
plt.tight_layout()
save("21_top_corridors.png")
plt.close()

# ------------------------------------------------------------
# Q4 -- DROPOFF ZONES WITH LONGEST AVG DISTANCE
# ------------------------------------------------------------
print("\nQ4 -- DROPOFF ZONES BY AVG TRIP DISTANCE")
print("-"*40)

trips_dropoff = completed.merge(
    locations[['location_id', 'zone_name']],
    left_on='dropoff_location_id',
    right_on='location_id',
    how='left'
)

avg_dist_dropoff = (
    trips_dropoff
    .groupby('zone_name')['distance_km']
    .mean()
    .round(2)
    .reset_index()
    .nlargest(10, 'distance_km')
    .sort_values('distance_km', ascending=True)
)
print(avg_dist_dropoff)

# Chart 4 -- Dropoff zones by avg distance
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(avg_dist_dropoff['zone_name'], avg_dist_dropoff['distance_km'],
               color='coral', edgecolor='white')
for bar, val in zip(bars, avg_dist_dropoff['distance_km']):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
            f'{val:.1f} km', va='center', fontsize=9)
ax.set_title('Top 10 Dropoff Zones by Avg Trip Distance', fontsize=14, fontweight='bold')
ax.set_xlabel('Average Distance (km)', fontsize=11)
ax.set_ylabel('Dropoff Zone', fontsize=11)
plt.tight_layout()
save("22_dropoff_zones_avg_distance.png")
plt.close()

# ------------------------------------------------------------
# Q5 -- ZONES WITH HIGHEST CANCELLATION RATE
# ------------------------------------------------------------
print("\nQ5 -- ZONES WITH HIGHEST CANCELLATION RATE")
print("-"*40)

# All trips with pickup zone
all_trips_zones = trips.merge(
    locations[['location_id', 'zone_name']],
    left_on='pickup_location_id',
    right_on='location_id',
    how='left'
)

total_by_zone = (
    all_trips_zones
    .groupby('zone_name')['trip_id']
    .count()
    .reset_index()
    .rename(columns={'trip_id': 'total_trips'})
)

cancelled_by_zone = (
    all_trips_zones[all_trips_zones['status'] == 'cancelled']
    .groupby('zone_name')['trip_id']
    .count()
    .reset_index()
    .rename(columns={'trip_id': 'cancelled_trips'})
)

zone_cancel_rate = total_by_zone.merge(cancelled_by_zone, on='zone_name', how='left')
zone_cancel_rate['cancelled_trips'] = zone_cancel_rate['cancelled_trips'].fillna(0)
zone_cancel_rate['cancel_rate']     = (
    zone_cancel_rate['cancelled_trips'] / zone_cancel_rate['total_trips'] * 100
).round(1)

top_cancel_zones = (
    zone_cancel_rate
    .nlargest(10, 'cancel_rate')
    .sort_values('cancel_rate', ascending=False)
)
print(top_cancel_zones[['zone_name', 'total_trips', 'cancelled_trips', 'cancel_rate']])

# Chart 5 -- Cancellation rate by zone
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(top_cancel_zones['zone_name'], top_cancel_zones['cancel_rate'],
              color='#f87171', edgecolor='white')
for bar, val in zip(bars, top_cancel_zones['cancel_rate']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f'{val}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.set_title('Top 10 Zones by Cancellation Rate', fontsize=14, fontweight='bold')
ax.set_xlabel('Zone', fontsize=11)
ax.set_ylabel('Cancellation Rate (%)', fontsize=11)
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
save("23_zone_cancellation_rate.png")
plt.close()

print("\nPHASE 5 COMPLETE -- 5 charts saved")

# ============================================================
# PHASE 6 -- CANCELLATION DEEP DIVE
# ============================================================
print("\n" + "="*60)
print("PHASE 6 -- CANCELLATION DEEP DIVE")
print("="*60)

# ------------------------------------------------------------
# Q1 -- OVERALL CANCELLATION RATE + DRIVER VS RIDER SPLIT
# ------------------------------------------------------------
print("\nQ1 -- CANCELLATION RATE & WHO CANCELS MORE")
print("-"*40)

total_trips      = len(trips)
total_cancelled  = len(trips[trips['status'] == 'cancelled'])
cancel_rate      = round(total_cancelled / total_trips * 100, 1)

print(f"Total trips        : {total_trips:,}")
print(f"Cancelled trips    : {total_cancelled:,}")
print(f"Cancellation rate  : {cancel_rate}%")

cancelled_by = cancels['cancelled_by'].value_counts()
print(f"\nCancelled by driver: {cancelled_by.get('driver', 0)}")
print(f"Cancelled by rider : {cancelled_by.get('rider', 0)}")

# Chart 1 -- Pie chart driver vs rider
labels = ['Cancelled by Driver', 'Cancelled by Rider']
sizes  = [cancelled_by.get('driver', 0), cancelled_by.get('rider', 0)]
colors = ['#f87171', '#60a5fa']

fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, colors=colors,
    autopct='%1.1f%%', startangle=90,
    textprops={'fontsize': 12}
)
for t in autotexts:
    t.set_fontweight('bold')
ax.set_title('Who Cancels More -- Driver vs Rider', fontsize=14, fontweight='bold')
plt.tight_layout()
save("24_cancellation_driver_vs_rider.png")
plt.close()

# ------------------------------------------------------------
# Q2 -- TOP 5 CANCELLATION REASONS (DRIVER VS RIDER)
# ------------------------------------------------------------
print("\nQ2 -- TOP 5 CANCELLATION REASONS")
print("-"*40)

driver_reasons = (
    cancels[cancels['cancelled_by'] == 'driver']['reason']
    .value_counts()
    .head(5)
)
rider_reasons = (
    cancels[cancels['cancelled_by'] == 'rider']['reason']
    .value_counts()
    .head(5)
)

print("Driver reasons:")
print(driver_reasons)
print("\nRider reasons:")
print(rider_reasons)

# Chart 2 -- Side by side bar charts
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

ax1.barh(driver_reasons.index[::-1], driver_reasons.values[::-1],
         color='#f87171', edgecolor='white')
ax1.set_title('Top 5 Driver Cancellation Reasons', fontsize=12, fontweight='bold')
ax1.set_xlabel('Number of Cancellations', fontsize=10)

ax2.barh(rider_reasons.index[::-1], rider_reasons.values[::-1],
         color='#60a5fa', edgecolor='white')
ax2.set_title('Top 5 Rider Cancellation Reasons', fontsize=12, fontweight='bold')
ax2.set_xlabel('Number of Cancellations', fontsize=10)

plt.suptitle('Cancellation Reasons -- Driver vs Rider', fontsize=14, fontweight='bold')
plt.tight_layout()
save("25_cancellation_reasons.png")
plt.close()

# ------------------------------------------------------------
# Q3 -- CANCELLATION RATE BY DRIVER RATING BUCKET
# ------------------------------------------------------------
print("\nQ3 -- CANCELLATION RATE BY DRIVER RATING")
print("-"*40)

# All trips merged with drivers
trips_drivers_all = trips.merge(
    drivers[['driver_id', 'rating']],
    on='driver_id', how='left'
)
trips_drivers_all['rating_bucket'] = pd.cut(
    trips_drivers_all['rating'],
    bins=[0, 3.5, 4.0, 4.5, 5.01],
    labels=['Below 3.5', '3.5-4.0', '4.0-4.5', '4.5-5.0'],
    include_lowest=True
)

total_by_bucket = (
    trips_drivers_all
    .groupby('rating_bucket', observed=True)['trip_id']
    .count()
    .reset_index()
    .rename(columns={'trip_id': 'total'})
)

cancel_by_bucket = (
    trips_drivers_all[trips_drivers_all['status'] == 'cancelled']
    .groupby('rating_bucket', observed=True)['trip_id']
    .count()
    .reset_index()
    .rename(columns={'trip_id': 'cancelled'})
)

cancel_rate_bucket = total_by_bucket.merge(cancel_by_bucket, on='rating_bucket', how='left')
cancel_rate_bucket['cancelled']    = cancel_rate_bucket['cancelled'].fillna(0)
cancel_rate_bucket['cancel_rate']  = (
    cancel_rate_bucket['cancelled'] / cancel_rate_bucket['total'] * 100
).round(1)
print(cancel_rate_bucket)

# Chart 3 -- Cancellation rate by rating bucket
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(cancel_rate_bucket['rating_bucket'],
              cancel_rate_bucket['cancel_rate'],
              color=['#f87171', '#facc15', '#4ade80', '#22c55e'],
              edgecolor='white')
for bar, val in zip(bars, cancel_rate_bucket['cancel_rate']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f'{val}%', ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.set_title('Cancellation Rate by Driver Rating Bucket', fontsize=14, fontweight='bold')
ax.set_xlabel('Driver Rating', fontsize=11)
ax.set_ylabel('Cancellation Rate (%)', fontsize=11)
plt.tight_layout()
save("26_cancel_rate_by_driver_rating.png")
plt.close()

# ------------------------------------------------------------
# Q4 -- CANCELLATIONS BY HOUR OF DAY
# ------------------------------------------------------------
print("\nQ4 -- CANCELLATIONS BY HOUR OF DAY")
print("-"*40)

cancels_with_time = cancels.merge(
    trips[['trip_id', 'requested_at']],
    on='trip_id', how='left'
)
cancels_with_time['requested_at'] = pd.to_datetime(cancels_with_time['requested_at'])
cancels_with_time['hour']         = cancels_with_time['requested_at'].dt.hour

cancels_by_hour = (
    cancels_with_time
    .groupby('hour')['cancel_id']
    .count()
    .reset_index()
    .rename(columns={'cancel_id': 'cancellations'})
)
print(cancels_by_hour)

# Chart 4 -- Cancellations by hour
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(cancels_by_hour['hour'], cancels_by_hour['cancellations'],
       color='#f87171', edgecolor='white')
ax.set_title('Cancellations by Hour of Day', fontsize=14, fontweight='bold')
ax.set_xlabel('Hour (0=Midnight, 12=Noon)', fontsize=11)
ax.set_ylabel('Number of Cancellations', fontsize=11)
ax.set_xticks(range(0, 24))
plt.tight_layout()
save("27_cancellations_by_hour.png")
plt.close()

# ------------------------------------------------------------
# Q5 -- REPEAT CANCELLER RIDERS
# ------------------------------------------------------------
print("\nQ5 -- REPEAT CANCELLER RIDERS (3+ cancellations)")
print("-"*40)

cancels_with_rider = cancels.merge(
    trips[['trip_id', 'rider_id']],
    on='trip_id', how='left'
)

repeat_cancellers = (
    cancels_with_rider
    .groupby('rider_id')['cancel_id']
    .count()
    .reset_index()
    .rename(columns={'cancel_id': 'cancel_count'})
    .query('cancel_count >= 3')
    .sort_values('cancel_count', ascending=False)
)

repeat_cancellers = repeat_cancellers.merge(
    users[['user_id', 'name']],
    left_on='rider_id',
    right_on='user_id',
    how='left'
)

print(f"Riders with 3+ cancellations: {len(repeat_cancellers)}")
print(repeat_cancellers[['name', 'cancel_count']].head(10))

print("\nPHASE 6 COMPLETE -- 4 charts saved")






#  -----------------------------------------------------------------------------------------------------------------------------------------------------------------




# PHASE 7 -- PAYMENTS & FINANCIAL OPS
# ============================================================
print("\n" + "="*60)
print("PHASE 7 -- PAYMENTS & FINANCIAL OPS")
print("="*60)

# ------------------------------------------------------------
# Q1 -- PAYMENT METHOD SPLIT
# ------------------------------------------------------------
print("\nQ1 -- PAYMENT METHOD SPLIT")
print("-"*40)

successful_payments = payments[payments['status'] == 'success']

payment_summary = (
    successful_payments
    .groupby('method')
    .agg(count=('amount', 'count'),
         total=('amount', 'sum'))
    .reset_index()
)
payment_summary['total'] = payment_summary['total'].round(2)
print(payment_summary)

# Chart 1 -- Payment split pie chart (by count)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.pie(payment_summary['count'],
        labels=payment_summary['method'],
        autopct='%1.1f%%', startangle=90,
        colors=['#60a5fa', '#4ade80', '#facc15'],
        textprops={'fontsize': 11})
ax1.set_title('Payment Method -- Transaction Count', fontsize=12, fontweight='bold')

ax2.bar(payment_summary['method'], payment_summary['total'],
        color=['#60a5fa', '#4ade80', '#facc15'], edgecolor='white')
ax2.set_title('Payment Method -- Total Amount ($)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Method', fontsize=10)
ax2.set_ylabel('Total Amount ($)', fontsize=10)
for bar, val in zip(ax2.patches, payment_summary['total']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
             f'${val:,.0f}', ha='center', va='bottom', fontsize=9)

plt.suptitle('Payment Method Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
save("28_payment_method_split.png")
plt.close()

# ------------------------------------------------------------
# Q2 -- PAYMENT FAILURE RATE BY METHOD
# ------------------------------------------------------------
print("\nQ2 -- PAYMENT FAILURE RATE BY METHOD")
print("-"*40)

total_by_method = (
    payments
    .groupby('method')['payment_id']
    .count()
    .reset_index()
    .rename(columns={'payment_id': 'total'})
)

failed_by_method = (
    payments[payments['status'] == 'failed']
    .groupby('method')['payment_id']
    .count()
    .reset_index()
    .rename(columns={'payment_id': 'failed'})
)

failure_rate = total_by_method.merge(failed_by_method, on='method', how='left')
failure_rate['failed']       = failure_rate['failed'].fillna(0)
failure_rate['failure_rate'] = (failure_rate['failed'] / failure_rate['total'] * 100).round(1)
failure_rate = failure_rate.sort_values('failure_rate', ascending=False)
print(failure_rate)

# Chart 2 -- Failure rate bar chart
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(failure_rate['method'], failure_rate['failure_rate'],
              color=['#f87171', '#facc15', '#4ade80'], edgecolor='white')
for bar, val in zip(bars, failure_rate['failure_rate']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f'{val}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
ax.set_title('Payment Failure Rate by Method', fontsize=14, fontweight='bold')
ax.set_xlabel('Payment Method', fontsize=11)
ax.set_ylabel('Failure Rate (%)', fontsize=11)
plt.tight_layout()
save("29_payment_failure_rate.png")
plt.close()

# ------------------------------------------------------------
# Q3 -- WALLET VS CASH -- TRIP LOYALTY
# ------------------------------------------------------------
print("\nQ3 -- AVG TRIPS PER RIDER BY PAYMENT METHOD")
print("-"*40)

payments_trips = payments.merge(
    trips[['trip_id', 'rider_id']],
    on='trip_id', how='left'
)
payments_trips = payments_trips.merge(
    riders[['rider_id', 'total_trips']],
    on='rider_id', how='left'
)

avg_trips_method = (
    payments_trips
    .groupby('method')['total_trips']
    .mean()
    .round(1)
    .reset_index()
    .sort_values('total_trips', ascending=False)
)
print(avg_trips_method)

# Chart 3 -- Avg trips by payment method
plt.figure(figsize=(8, 5))
sns.barplot(data=avg_trips_method, x='method', y='total_trips',
            palette='Blues_d')
plt.title('Avg Total Trips per Rider by Payment Method', fontsize=14, fontweight='bold')
plt.xlabel('Payment Method', fontsize=11)
plt.ylabel('Avg Total Trips', fontsize=11)
plt.tight_layout()
save("30_avg_trips_by_payment_method.png")
plt.close()

# ------------------------------------------------------------
# Q4 -- PAYMENT SETTLEMENT TIME
# ------------------------------------------------------------
print("\nQ4 -- PAYMENT SETTLEMENT TIME")
print("-"*40)

payments_completed = payments.merge(
    completed[['trip_id', 'completed_at']],
    on='trip_id', how='inner'
)
payments_completed['paid_at']      = pd.to_datetime(payments_completed['paid_at'])
payments_completed['completed_at'] = pd.to_datetime(payments_completed['completed_at'])

payments_completed['settle_mins'] = (
    (payments_completed['paid_at'] - payments_completed['completed_at'])
    .dt.total_seconds() / 60
)

# Remove negatives (data anomalies)
settle_clean = payments_completed[payments_completed['settle_mins'] >= 0]

avg_settle = round(settle_clean['settle_mins'].mean(), 1)
print(f"Average settlement time : {avg_settle} mins")
print(f"Max settlement time     : {round(settle_clean['settle_mins'].max(), 1)} mins")

# Chart 4 -- Settlement time histogram
plt.figure(figsize=(10, 5))
plt.hist(settle_clean['settle_mins'], bins=40,
         color='steelblue', edgecolor='white', alpha=0.85)
plt.axvline(avg_settle, color='red', linestyle='dashed',
            linewidth=2, label=f'Mean: {avg_settle} mins')
plt.title('Payment Settlement Time Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Minutes from Trip Completion to Payment', fontsize=11)
plt.ylabel('Number of Payments', fontsize=11)
plt.legend(fontsize=11)
plt.tight_layout()
save("31_payment_settlement_time.png")
plt.close()

print("\nPHASE 7 COMPLETE -- 4 charts saved")









#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------  









# PHASE 8 -- REVIEWS & SATISFACTION
# ============================================================
print("\n" + "="*60)
print("PHASE 8 -- REVIEWS & SATISFACTION")
print("="*60)

# ------------------------------------------------------------
# Q1 -- AVG RATING: RIDERS TO DRIVERS vs DRIVERS TO RIDERS
# ------------------------------------------------------------
print("\nQ1 -- AVG RATINGS BOTH DIRECTIONS")
print("-"*40)

reviews_users = reviews.merge(
    users[['user_id', 'is_driver']],
    left_on='reviewer_id',
    right_on='user_id',
    how='left'
)

rider_to_driver = reviews_users[reviews_users['is_driver'] == 0]['rating'].mean().round(2)
driver_to_rider = reviews_users[reviews_users['is_driver'] == 1]['rating'].mean().round(2)

print(f"Riders rating drivers  : {rider_to_driver}")
print(f"Drivers rating riders  : {driver_to_rider}")

# Chart 1 -- Side by side bar comparison
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(['Riders --> Drivers', 'Drivers --> Riders'],
              [rider_to_driver, driver_to_rider],
              color=['#60a5fa', '#f87171'], edgecolor='white', width=0.4)
for bar, val in zip(bars, [rider_to_driver, driver_to_rider]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            str(val), ha='center', va='bottom', fontweight='bold', fontsize=13)
ax.set_title('Average Review Ratings -- Both Directions', fontsize=14, fontweight='bold')
ax.set_ylabel('Average Rating', fontsize=11)
ax.set_ylim(0, 5.5)
ax.axhline(5.0, color='gray', linestyle='dashed', linewidth=1, alpha=0.5)
plt.tight_layout()
save("32_avg_ratings_both_directions.png")
plt.close()

# ------------------------------------------------------------
# Q2 -- BOTTOM 10 DRIVERS BY AVG REVIEW SCORE
# ------------------------------------------------------------
print("\nQ2 -- BOTTOM 10 DRIVERS BY REVIEW SCORE")
print("-"*40)

reviews_drivers = reviews.merge(
    users[['user_id', 'is_driver']],
    left_on='reviewee_id',
    right_on='user_id',
    how='left'
)

# Keep only reviews OF drivers (reviewee is a driver)
driver_reviews = reviews_drivers[reviews_drivers['is_driver'] == 1]

driver_avg_rating = (
    driver_reviews
    .groupby('reviewee_id')
    .agg(avg_rating=('rating', 'mean'),
         review_count=('rating', 'count'))
    .reset_index()
    .query('review_count >= 5')
    .nsmallest(10, 'avg_rating')
    .sort_values('avg_rating', ascending=True)
)

driver_avg_rating = driver_avg_rating.merge(
    users[['user_id', 'name']],
    left_on='reviewee_id',
    right_on='user_id',
    how='left'
)
driver_avg_rating['avg_rating'] = driver_avg_rating['avg_rating'].round(2)
print(driver_avg_rating[['name', 'avg_rating', 'review_count']])

# Chart 2 -- Bottom 10 drivers horizontal bar
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(driver_avg_rating['name'], driver_avg_rating['avg_rating'],
               color='#f87171', edgecolor='white')
for bar, val in zip(bars, driver_avg_rating['avg_rating']):
    ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
            str(val), va='center', fontsize=9, fontweight='bold')
ax.set_title('Bottom 10 Drivers by Avg Review Score (min 5 reviews)',
             fontsize=13, fontweight='bold')
ax.set_xlabel('Average Rating', fontsize=11)
ax.set_ylabel('Driver Name', fontsize=11)
ax.set_xlim(0, 5.5)
ax.axvline(4.0, color='gray', linestyle='dashed', linewidth=1.5, label='4.0 threshold')
ax.legend(fontsize=10)
plt.tight_layout()
save("33_bottom10_drivers_review.png")
plt.close()

# ------------------------------------------------------------
# Q3 -- TRIP FARE VS REVIEW RATING
# ------------------------------------------------------------
print("\nQ3 -- FARE VS REVIEW RATING")
print("-"*40)

reviews_trips = reviews.merge(
    completed[['trip_id', 'total_fare']],
    on='trip_id', how='inner'
)

reviews_trips['fare_bucket'] = pd.cut(
    reviews_trips['total_fare'],
    bins=[0, 10, 25, 50, 100, 99999],
    labels=['Under $10', '$10-$25', '$25-$50', '$50-$100', 'Over $100'],
    include_lowest=True
)

avg_rating_fare = (
    reviews_trips
    .groupby('fare_bucket', observed=True)['rating']
    .mean()
    .round(2)
    .reset_index()
)
print(avg_rating_fare)

# Chart 3 -- Avg rating by fare bucket
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(avg_rating_fare['fare_bucket'], avg_rating_fare['rating'],
              color='steelblue', edgecolor='white')
for bar, val in zip(bars, avg_rating_fare['rating']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            str(val), ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.set_title('Average Review Rating by Fare Bucket', fontsize=14, fontweight='bold')
ax.set_xlabel('Fare Range', fontsize=11)
ax.set_ylabel('Average Rating', fontsize=11)
ax.set_ylim(0, 5.5)
plt.tight_layout()
save("34_rating_by_fare_bucket.png")
plt.close()

# ------------------------------------------------------------
# Q4 -- REVIEW SUBMISSION RATE
# ------------------------------------------------------------
print("\nQ4 -- REVIEW SUBMISSION RATE")
print("-"*40)

overall_rate = round(len(reviews) / len(completed) * 100, 1)
print(f"Overall review submission rate : {overall_rate}%")
print(f"Completed trips                : {len(completed):,}")
print(f"Reviews submitted              : {len(reviews):,}")

# Monthly review submission rate
reviews['reviewed_at'] = pd.to_datetime(reviews['reviewed_at'])
reviews['review_month'] = reviews['reviewed_at'].dt.to_period('M').astype(str)

monthly_reviews = (
    reviews
    .groupby('review_month')['review_id']
    .count()
    .reset_index()
    .rename(columns={'review_id': 'review_count'})
)

monthly_trips = (
    completed
    .groupby('month')['trip_id']
    .count()
    .reset_index()
    .rename(columns={'trip_id': 'trip_count', 'month': 'review_month'})
)

review_rate_monthly = monthly_reviews.merge(monthly_trips, on='review_month', how='inner')
review_rate_monthly['rate'] = (
    review_rate_monthly['review_count'] / review_rate_monthly['trip_count'] * 100
).round(1)

# Chart 4 -- Review submission rate by month
plt.figure(figsize=(14, 5))
plt.plot(review_rate_monthly['review_month'], review_rate_monthly['rate'],
         color='steelblue', linewidth=2.5, marker='o', markersize=5)
plt.axhline(overall_rate, color='red', linestyle='dashed',
            linewidth=1.5, label=f'Overall avg: {overall_rate}%')
plt.title('Review Submission Rate by Month', fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=11)
plt.ylabel('Review Rate (%)', fontsize=11)
plt.xticks(rotation=45)
plt.legend(fontsize=10)
plt.tight_layout()
save("35_review_submission_rate.png")
plt.close()

print("\n" + "="*60)
print("PHASE 8 COMPLETE -- 4 charts saved")

print("="*60)




#--------------------------------------------------------------------------------------------------------------------------------------------------------------------







# ============================================================
# PHASE 9 -- CORRELATION ANALYSIS & KEY FINDINGS
# ============================================================
print("\n" + "="*60)
print("PHASE 9 -- CORRELATION ANALYSIS & KEY FINDINGS")
print("="*60)

# ------------------------------------------------------------
# Q1 -- CORRELATION HEATMAP
# ------------------------------------------------------------
print("\nQ1 -- CORRELATION HEATMAP")
print("-"*40)

# Select only numeric columns
numeric_cols = completed.select_dtypes(include='number')

# Drop columns that are just IDs (not meaningful for correlation)
cols_to_drop = [col for col in numeric_cols.columns
                if 'id' in col.lower()]
numeric_cols = numeric_cols.drop(columns=cols_to_drop, errors='ignore')

corr_matrix = numeric_cols.corr()
print("Columns included in heatmap:")
print(list(numeric_cols.columns))

# Chart 1 -- Correlation heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt='.2f',
    cmap='Blues',
    square=True,
    linewidths=0.5,
    annot_kws={'size': 9}
)
plt.title('Correlation Matrix -- Uber Trip Numeric Features',
          fontsize=14, fontweight='bold', pad=15)
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.yticks(rotation=0, fontsize=9)
plt.tight_layout()
save("36_correlation_heatmap.png")
plt.close()

# ------------------------------------------------------------
# Q2 -- STRONGEST CORRELATIONS WITH total_fare
# ------------------------------------------------------------
print("\nQ2 -- STRONGEST CORRELATIONS WITH total_fare")
print("-"*40)

fare_corr = (
    corr_matrix['total_fare']
    .drop('total_fare')
    .sort_values()
)
print(fare_corr)

# Chart 2 -- Horizontal bar of correlations with fare
colors = ['#f87171' if v < 0 else '#4ade80' for v in fare_corr.values]

plt.figure(figsize=(10, 6))
bars = plt.barh(fare_corr.index, fare_corr.values,
                color=colors, edgecolor='white')
plt.axvline(0, color='black', linewidth=0.8)
plt.title('Correlation of Each Feature with Total Fare',
          fontsize=14, fontweight='bold')
plt.xlabel('Correlation Coefficient', fontsize=11)
plt.ylabel('Feature', fontsize=11)
for bar, val in zip(bars, fare_corr.values):
    x_pos = bar.get_width() + 0.01 if val >= 0 else bar.get_width() - 0.01
    ha     = 'left' if val >= 0 else 'right'
    plt.text(x_pos, bar.get_y() + bar.get_height()/2,
             f'{val:.2f}', va='center', ha=ha, fontsize=9, fontweight='bold')
plt.tight_layout()
save("37_fare_correlation_bar.png")
plt.close()

# ------------------------------------------------------------
# Q3 -- WEEKEND VS WEEKDAY COMPARISON
# ------------------------------------------------------------
print("\nQ3 -- WEEKEND VS WEEKDAY")
print("-"*40)

weekend_compare = (
    completed
    .groupby('is_weekend')
    .agg(
        avg_fare=('total_fare', 'mean'),
        trip_count=('trip_id', 'count'),
        avg_wait=('wait_time_mins', 'mean')
    )
    .reset_index()
)
weekend_compare['is_weekend'] = weekend_compare['is_weekend'].map(
    {True: 'Weekend', False: 'Weekday'}
)
weekend_compare = weekend_compare.round(2)
print(weekend_compare)

# Chart 3 -- 3 side-by-side bar charts
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
colors = ['#60a5fa', '#f97316']

# Avg fare
ax1.bar(weekend_compare['is_weekend'], weekend_compare['avg_fare'],
        color=colors, edgecolor='white', width=0.4)
ax1.set_title('Average Fare', fontsize=12, fontweight='bold')
ax1.set_ylabel('Fare ($)', fontsize=10)
for bar, val in zip(ax1.patches, weekend_compare['avg_fare']):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             f'${val:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Trip volume
ax2.bar(weekend_compare['is_weekend'], weekend_compare['trip_count'],
        color=colors, edgecolor='white', width=0.4)
ax2.set_title('Trip Volume', fontsize=12, fontweight='bold')
ax2.set_ylabel('Number of Trips', fontsize=10)
for bar, val in zip(ax2.patches, weekend_compare['trip_count']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
             f'{val:,}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Avg wait time
ax3.bar(weekend_compare['is_weekend'], weekend_compare['avg_wait'],
        color=colors, edgecolor='white', width=0.4)
ax3.set_title('Average Wait Time', fontsize=12, fontweight='bold')
ax3.set_ylabel('Wait Time (mins)', fontsize=10)
for bar, val in zip(ax3.patches, weekend_compare['avg_wait']):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             f'{val:.1f} min', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.suptitle('Weekend vs Weekday -- Fare, Volume & Wait Time',
             fontsize=14, fontweight='bold')
plt.tight_layout()
save("38_weekend_vs_weekday.png")
plt.close()

# ------------------------------------------------------------
# KEY FINDINGS -- Print to terminal (copy into markdown cell)
# ------------------------------------------------------------
print("\n" + "="*60)
print("KEY FINDINGS -- Copy these into a Markdown cell")
print("="*60)
print("""
## Key Findings

**Finding 1 -- Revenue & Pricing**
Peak revenue hours occur during morning and evening commutes.
Average fare per km shows pricing is consistent across distances,
but surge pricing adds significant uplift during peak windows.

**Finding 2 -- Surge Pricing Impact**
High Surge trips generate significantly higher average fares than
No Surge trips. However, surge may be contributing to cancellations
during late-night hours when both riders and drivers show frustration.

**Finding 3 -- Driver Quality**
The majority of drivers are rated 4.0 and above. Lower-rated drivers
show higher cancellation rates, validating that the rating system
is working as a quality signal. Top 10 drivers account for a
disproportionate share of total platform earnings.

**Finding 4 -- Rider Retention**
High-segment riders (20+ trips) contribute the largest share of
total revenue despite being a small percentage of the rider base.
The first-to-second trip gap is the strongest early retention signal
-- riders who return quickly are significantly more likely to stay.

**Finding 5 -- Location Intelligence**
Airport and commercial zones generate the highest average fares.
Top trip corridors are concentrated between business districts and
transport hubs -- these routes should always have driver supply.

**Finding 6 -- Cancellation Patterns**
Cancellation rate peaks late at night. Rider cancellations are most
commonly caused by long wait times, while driver cancellations are
driven by rider unresponsiveness. Each requires a different fix.

**Finding 7 -- Payment Behaviour**
Wallet users take more trips on average than cash users, confirming
that digital payment adoption is a loyalty indicator. Uber should
incentivise wallet top-ups to shift cash users to digital payments.
""")

print("\nPHASE 9 COMPLETE -- 3 charts saved (36, 37, 38)")

# ============================================================
# PHASE 10 -- MACHINE LEARNING: FARE PREDICTION MODEL
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